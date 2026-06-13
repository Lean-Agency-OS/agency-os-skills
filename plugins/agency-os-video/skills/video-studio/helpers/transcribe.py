"""Transcribe a video. Two engines, chosen from outside via --engine.

  scribe  (default) ElevenLabs Scribe: verbatim + diarize + audio events +
          word-level timestamps. The accurate, timestamped transcript the
          cut pipeline relies on. Needs ELEVENLABS_API_KEY and network.
  whisper local faster-whisper: a fast offline pass to quickly capture what
          is in a clip. Word timestamps, no diarization. No API key, no
          network. Optional dependency (install extra: `pip install -e .[whisper]`).

Both engines write the SAME shape to <edit_dir>/transcripts/<video_stem>.json
so pack_transcripts / render / timeline_view work regardless of engine.

Cached: if the output file already exists, transcription is skipped (use
--force to overwrite, e.g. to replace a quick whisper pass with scribe).

Usage:
    python helpers/transcribe.py <video_path>
    python helpers/transcribe.py <video_path> --engine whisper
    python helpers/transcribe.py <video_path> --engine whisper --whisper-model small
    python helpers/transcribe.py <video_path> --edit-dir /custom/edit --force
    python helpers/transcribe.py <video_path> --language en --num-speakers 2
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import requests

from ffmpeg_utils import run as ffrun


SCRIBE_URL = "https://api.elevenlabs.io/v1/speech-to-text"


def load_api_key() -> str:
    for candidate in [Path(__file__).resolve().parent.parent / ".env", Path(".env")]:
        if candidate.exists():
            for line in candidate.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == "ELEVENLABS_API_KEY":
                    return v.strip().strip('"').strip("'")
    v = os.environ.get("ELEVENLABS_API_KEY", "")
    if not v:
        sys.exit("ELEVENLABS_API_KEY not found in .env or environment")
    return v


def extract_audio(video_path: Path, dest: Path) -> None:
    ffrun([
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
        str(dest),
    ])


# -------- Engine: ElevenLabs Scribe -----------------------------------------


def call_scribe(
    audio_path: Path,
    api_key: str,
    language: str | None = None,
    num_speakers: int | None = None,
    max_retries: int = 4,
) -> dict:
    data: dict[str, str] = {
        "model_id": "scribe_v1",
        "diarize": "true",
        "tag_audio_events": "true",
        "timestamps_granularity": "word",
    }
    if language:
        data["language_code"] = language
    if num_speakers:
        data["num_speakers"] = str(num_speakers)

    # Retry transient failures (429 rate limit, 5xx, network errors) with
    # exponential backoff. A single blip should not kill a paid transcription.
    last_err = ""
    for attempt in range(max_retries):
        try:
            with open(audio_path, "rb") as f:
                resp = requests.post(
                    SCRIBE_URL,
                    headers={"xi-api-key": api_key},
                    files={"file": (audio_path.name, f, "audio/wav")},
                    data=data,
                    timeout=1800,
                )
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code == 429 or resp.status_code >= 500:
                last_err = f"{resp.status_code}: {resp.text[:200]}"
            else:
                # Non-retryable (4xx other than 429): fail fast.
                raise RuntimeError(f"Scribe returned {resp.status_code}: {resp.text[:500]}")
        except requests.RequestException as e:
            last_err = str(e)

        if attempt < max_retries - 1:
            wait = 2 ** attempt  # 1s, 2s, 4s, ...
            print(f"  scribe attempt {attempt + 1} failed ({last_err}); retry in {wait}s", flush=True)
            time.sleep(wait)

    raise RuntimeError(f"Scribe failed after {max_retries} attempts: {last_err}")


# -------- Engine: local faster-whisper (fast offline gist) ------------------


def call_whisper(
    audio_path: Path,
    model_size: str = "base",
    language: str | None = None,
    word_timestamps: bool = True,
) -> dict:
    """Transcribe locally with faster-whisper. Returns a Scribe-shaped dict.

    No diarization (speaker_id is None on every word). Optimized for a fast
    CPU pass (int8); raise the model size for better accuracy.

    word_timestamps=False is the fast text-only "gist" mode: it skips the
    word-alignment pass (faster) and returns text with an empty words list.
    Use it only for "what is spoken in these files"; never for cutting.
    """
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit(
            "faster-whisper is not installed. Install the optional extra:\n"
            "  uv pip install -e '.[whisper]'   (or: pip install faster-whisper)"
        )

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        str(audio_path), word_timestamps=word_timestamps, language=language,
    )

    words: list[dict] = []
    full_parts: list[str] = []
    for seg in segments:
        full_parts.append(seg.text.strip())
        if word_timestamps:
            for wd in (seg.words or []):
                words.append({
                    "type": "word",
                    "text": wd.word.strip(),
                    "start": round(float(wd.start), 3),
                    "end": round(float(wd.end), 3),
                    "speaker_id": None,
                })

    return {
        "engine": "whisper",
        "whisper_model": model_size,
        "timestamps": bool(word_timestamps),
        "language_code": getattr(info, "language", None),
        "text": " ".join(p for p in full_parts if p).strip(),
        "words": words,
    }


# -------- Orchestration ------------------------------------------------------


def transcribe_one(
    video: Path,
    edit_dir: Path,
    api_key: str | None = None,
    language: str | None = None,
    num_speakers: int | None = None,
    engine: str = "scribe",
    whisper_model: str = "base",
    text_only: bool = False,
    fallback_whisper: bool = True,
    force: bool = False,
    verbose: bool = True,
) -> Path:
    """Transcribe a single video. Returns path to transcript JSON.

    Cached: returns existing path immediately unless `force` is set.
    """
    transcripts_dir = edit_dir / "transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    # Text-only gist (whisper, no timestamps) writes <stem>.txt and is NOT a
    # cut artifact. Everything else writes the cut JSON <stem>.json.
    gist = engine == "whisper" and text_only
    out_path = transcripts_dir / (f"{video.stem}.txt" if gist else f"{video.stem}.json")

    if out_path.exists() and not force:
        if verbose:
            print(f"cached: {out_path.name}")
        return out_path

    if verbose:
        print(f"  extracting audio from {video.name} (engine={engine})", flush=True)

    t0 = time.time()
    with tempfile.TemporaryDirectory() as tmp:
        audio = Path(tmp) / f"{video.stem}.wav"
        extract_audio(video, audio)
        size_mb = audio.stat().st_size / (1024 * 1024)
        if verbose:
            print(f"  processing {video.stem}.wav ({size_mb:.1f} MB)", flush=True)
        if engine == "whisper":
            payload = call_whisper(audio, model_size=whisper_model, language=language, word_timestamps=not text_only)
        else:
            if not api_key:
                api_key = load_api_key()
            try:
                payload = call_scribe(audio, api_key, language, num_speakers)
            except Exception as e:
                if not fallback_whisper:
                    raise
                # Scribe unreachable: fall back to local whisper. We keep WORD
                # timestamps (not just plain text), so the cut pipeline still
                # works - only diarization is lost. Marked in the JSON.
                print(f"  scribe unavailable ({e});", flush=True)
                print("  -> falling back to local whisper (word timestamps kept, no diarization)", flush=True)
                payload = call_whisper(audio, model_size=whisper_model, language=language)
                payload["fallback_from"] = "scribe"
                payload["fallback_reason"] = str(e)[:300]

    if gist:
        out_path.write_text((payload.get("text") or "") + "\n", encoding="utf-8")
    else:
        out_path.write_text(json.dumps(payload, indent=2))
    dt = time.time() - t0

    if verbose:
        kb = out_path.stat().st_size / 1024
        print(f"  saved: {out_path.name} ({kb:.1f} KB) in {dt:.1f}s")
        if not gist and isinstance(payload, dict) and "words" in payload:
            print(f"    words: {len(payload['words'])}")

    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description="Transcribe a video (ElevenLabs Scribe or local Whisper)")
    ap.add_argument("video", type=Path, help="Path to video file")
    ap.add_argument(
        "--engine",
        choices=["scribe", "whisper"],
        default="scribe",
        help="scribe (default, accurate + diarized + needs API key) or whisper (fast local gist).",
    )
    ap.add_argument(
        "--whisper-model",
        type=str,
        default="base",
        help="faster-whisper model size for --engine whisper (tiny/base/small/medium/large-v3). Default base.",
    )
    ap.add_argument(
        "--edit-dir",
        type=Path,
        default=None,
        help="Edit output directory (default: <video_parent>/edit)",
    )
    ap.add_argument(
        "--language",
        type=str,
        default=None,
        help="Optional ISO language code (e.g., 'en'). Omit to auto-detect.",
    )
    ap.add_argument(
        "--num-speakers",
        type=int,
        default=None,
        help="Optional number of speakers when known (scribe only). Improves diarization.",
    )
    ap.add_argument(
        "--text-only",
        action="store_true",
        help="Fast local gist: text only, no timestamps. Implies --engine whisper. "
             "Writes <stem>.txt (not a cut artifact). For 'what is spoken in these files'.",
    )
    ap.add_argument(
        "--no-fallback",
        action="store_true",
        help="Disable automatic local-whisper fallback when scribe is unreachable (fail hard instead).",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing cached transcript (e.g. replace a whisper pass with scribe).",
    )
    args = ap.parse_args()

    video = args.video.resolve()
    if not video.exists():
        sys.exit(f"video not found: {video}")

    edit_dir = (args.edit_dir or (video.parent / "edit")).resolve()
    # Text-only gist is inherently local: imply the whisper engine.
    engine = "whisper" if args.text_only else args.engine
    api_key = load_api_key() if engine == "scribe" else None

    transcribe_one(
        video=video,
        edit_dir=edit_dir,
        api_key=api_key,
        language=args.language,
        num_speakers=args.num_speakers,
        engine=engine,
        whisper_model=args.whisper_model,
        text_only=args.text_only,
        fallback_whisper=not args.no_fallback,
        force=args.force,
    )


if __name__ == "__main__":
    main()
