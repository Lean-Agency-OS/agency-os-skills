"""Lokale Schnell-Transkription fuer Triage / Sortieren - OHNE API.

Zweck: schnell wissen, worum es in einem (oder vielen) Videos geht, um sie zu
sortieren/kategorisieren. KEINE Wortgenauigkeit, keine Diarization, keine
Audio-Events, keine Sub-Sekunden-Pausen. Fuer den praezisen Schnitt bleibt
ElevenLabs Scribe (transcribe.py) zustaendig - dieses Skript NICHT dafuer nutzen.

Engine (Auto-Detect):
  - Apple Silicon + mlx-whisper installiert  -> MLX (schnell, GPU/ANE)
  - sonst                                     -> faster-whisper (CPU, portabel)

Output: pro Video eine .txt mit reinem Fließtext nach <out-dir>/ (Default:
<ordner>/local-transcripts/). Gecached: existierende .txt wird uebersprungen.

Usage:
  python transcribe_local.py <video-oder-ordner>
  python transcribe_local.py <ordner> --model base --lang de
  python transcribe_local.py <video> --out-dir /pfad --engine faster
"""

from __future__ import annotations

import argparse
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi", ".mpg", ".mpeg"}


def pick_engine(requested: str) -> str:
    """auto | mlx | faster -> konkrete Engine. Fallback faster-whisper."""
    if requested == "faster":
        return "faster"
    if requested == "mlx":
        return "mlx"
    # auto
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        try:
            import mlx_whisper  # noqa: F401
            return "mlx"
        except ImportError:
            pass
    return "faster"


def extract_audio(video_path: Path, dest: Path) -> None:
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
        str(dest),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def transcribe_mlx(audio_path: Path, model: str, lang: str | None) -> str:
    import mlx_whisper
    repo = f"mlx-community/whisper-{model}"
    kwargs = {"path_or_hf_repo": repo}
    if lang:
        kwargs["language"] = lang
    result = mlx_whisper.transcribe(str(audio_path), **kwargs)
    return result.get("text", "").strip()


def transcribe_faster(audio_path: Path, model: str, lang: str | None) -> str:
    from faster_whisper import WhisperModel
    wm = WhisperModel(model, device="cpu", compute_type="int8")
    segments, _info = wm.transcribe(str(audio_path), language=lang, vad_filter=True)
    return " ".join(seg.text.strip() for seg in segments).strip()


def transcribe_one(video: Path, out_dir: Path, engine: str, model: str,
                   lang: str | None, verbose: bool = True) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{video.stem}.txt"

    if out_path.exists():
        if verbose:
            print(f"cached: {out_path.name}")
        return out_path

    with tempfile.TemporaryDirectory() as tmp:
        audio = Path(tmp) / f"{video.stem}.wav"
        if verbose:
            print(f"  [{engine}/{model}] {video.name} ...", flush=True)
        extract_audio(video, audio)
        if engine == "mlx":
            text = transcribe_mlx(audio, model, lang)
        else:
            text = transcribe_faster(audio, model, lang)

    out_path.write_text(text + "\n", encoding="utf-8")
    if verbose:
        gist = text[:160].replace("\n", " ")
        print(f"  -> {out_path.name} ({len(text)} Zeichen): {gist}{'...' if len(text) > 160 else ''}")
    return out_path


def collect_videos(target: Path) -> list[Path]:
    if target.is_dir():
        return sorted(p for p in target.iterdir()
                      if p.is_file() and p.suffix.lower() in VIDEO_EXTS)
    if target.is_file():
        return [target]
    return []


def main() -> None:
    ap = argparse.ArgumentParser(description="Lokale Schnell-Transkription (Triage, ohne API)")
    ap.add_argument("target", type=Path, help="Video-Datei oder Ordner mit Videos")
    ap.add_argument("--out-dir", type=Path, default=None,
                    help="Output-Ordner (Default: <ordner>/local-transcripts)")
    ap.add_argument("--model", default="base",
                    help="Modellgroesse: tiny|base|small|medium|large-v3 (Default base)")
    ap.add_argument("--lang", default=None,
                    help="ISO-Sprachcode (z.B. 'de'). Weglassen = Auto-Detect.")
    ap.add_argument("--engine", default="auto", choices=["auto", "mlx", "faster"],
                    help="Engine-Wahl (Default auto: mlx auf Apple Silicon, sonst faster-whisper)")
    args = ap.parse_args()

    target = args.target.resolve()
    videos = collect_videos(target)
    if not videos:
        sys.exit(f"Keine Videos gefunden: {target}")

    base_dir = target if target.is_dir() else target.parent
    out_dir = (args.out_dir or (base_dir / "local-transcripts")).resolve()
    engine = pick_engine(args.engine)

    print(f"Engine: {engine} | Modell: {args.model} | {len(videos)} Video(s) -> {out_dir}")
    for v in videos:
        try:
            transcribe_one(v, out_dir, engine, args.model, args.lang)
        except Exception as e:  # noqa: BLE001 - eine kaputte Datei soll den Batch nicht killen
            print(f"  FEHLER bei {v.name}: {e}", file=sys.stderr)

    print(f"\nFertig. Transkripte in: {out_dir}")


if __name__ == "__main__":
    main()
