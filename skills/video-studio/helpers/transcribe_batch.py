"""Batch-transcribe every video in a directory with 4 parallel workers.

Walks <videos_dir> for common video extensions, runs ElevenLabs Scribe on
each, writes transcripts to <videos_dir>/edit/transcripts/<name>.json.

Cached per-file: any source that already has a transcript is skipped.

Usage:
    python helpers/transcribe_batch.py <videos_dir>
    python helpers/transcribe_batch.py <videos_dir> --workers 4
    python helpers/transcribe_batch.py <videos_dir> --num-speakers 2
    python helpers/transcribe_batch.py <videos_dir> --edit-dir /custom/edit
"""

from __future__ import annotations

import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from transcribe import load_api_key, transcribe_one


VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".m4v", ".webm", ".mts", ".m2ts"}


def find_videos(videos_dir: Path) -> list[Path]:
    # Compare on the lowercased suffix so .MP4 / .Mov / .MTS are all matched.
    videos = sorted(
        p for p in videos_dir.iterdir()
        if p.is_file() and p.suffix.lower() in VIDEO_EXTS
    )
    return videos


def write_gist(edit_dir: Path, videos: list[Path]) -> None:
    """Combine the per-file <stem>.txt gists into one overview at <edit>/gist.md."""
    tdir = edit_dir / "transcripts"
    lines = ["# Spoken-text gist (local whisper pass)", ""]
    for v in videos:
        txt = tdir / f"{v.stem}.txt"
        if txt.exists():
            content = txt.read_text(encoding="utf-8").strip()
            lines.append(f"## {v.name}")
            lines.append("")
            lines.append(content if content else "_(no speech detected)_")
            lines.append("")
    out = edit_dir / "gist.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"gist overview -> {out}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Parallel batch transcription of a videos directory")
    ap.add_argument("videos_dir", type=Path, help="Directory containing source videos")
    ap.add_argument(
        "--edit-dir",
        type=Path,
        default=None,
        help="Edit output directory (default: <videos_dir>/edit)",
    )
    ap.add_argument("--workers", type=int, default=4, help="Parallel workers (default: 4; forced to 1 for whisper)")
    ap.add_argument(
        "--engine",
        choices=["scribe", "whisper"],
        default="scribe",
        help="scribe (default, API) or whisper (fast local gist).",
    )
    ap.add_argument(
        "--whisper-model",
        type=str,
        default="base",
        help="faster-whisper model size for --engine whisper. Default base.",
    )
    ap.add_argument(
        "--language",
        type=str,
        default=None,
        help="Optional ISO language code. Omit to auto-detect per file.",
    )
    ap.add_argument(
        "--num-speakers",
        type=int,
        default=None,
        help="Optional number of speakers. Improves diarization when known (scribe only).",
    )
    ap.add_argument(
        "--text-only",
        action="store_true",
        help="Fast local gist for many files: text only, no timestamps. Implies whisper. "
             "Writes <stem>.txt per file plus a combined <edit>/gist.md overview.",
    )
    ap.add_argument(
        "--no-fallback",
        action="store_true",
        help="Disable local-whisper fallback when scribe is unreachable.",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Re-transcribe sources that already have a transcript.",
    )
    args = ap.parse_args()

    videos_dir = args.videos_dir.resolve()
    if not videos_dir.is_dir():
        sys.exit(f"not a directory: {videos_dir}")

    edit_dir = (args.edit_dir or (videos_dir / "edit")).resolve()
    (edit_dir / "transcripts").mkdir(parents=True, exist_ok=True)

    videos = find_videos(videos_dir)
    if not videos:
        sys.exit(f"no videos found in {videos_dir}")

    # Text-only gist is inherently local: imply the whisper engine.
    engine = "whisper" if args.text_only else args.engine
    ext = "txt" if args.text_only else "json"

    if args.force:
        already_cached, pending = [], list(videos)
    else:
        already_cached = [v for v in videos if (edit_dir / "transcripts" / f"{v.stem}.{ext}").exists()]
        pending = [v for v in videos if v not in already_cached]

    print(f"found {len(videos)} videos ({len(already_cached)} cached, {len(pending)} to transcribe)")
    if not pending:
        if args.text_only:
            write_gist(edit_dir, videos)
        print("nothing to do")
        return

    api_key = load_api_key() if engine == "scribe" else None

    # Local whisper is a CPU-bound model: running several in parallel thrashes
    # and loads N copies of the model. Force a single worker for whisper.
    workers = 1 if engine == "whisper" else args.workers

    print(f"transcribing {len(pending)} files (engine={engine}, {workers} worker(s))")
    t0 = time.time()

    errors: list[tuple[Path, str]] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(
                transcribe_one,
                video=v,
                edit_dir=edit_dir,
                api_key=api_key,
                language=args.language,
                num_speakers=args.num_speakers,
                engine=engine,
                whisper_model=args.whisper_model,
                text_only=args.text_only,
                fallback_whisper=not args.no_fallback,
                force=args.force,
                verbose=False,
            ): v
            for v in pending
        }
        for fut in as_completed(futures):
            v = futures[fut]
            try:
                out = fut.result()
                print(f"  + {v.stem}  →  {out.name}")
            except Exception as e:
                errors.append((v, str(e)))
                print(f"  x {v.stem}  FAILED: {e}")

    dt = time.time() - t0
    print(f"\ndone in {dt:.1f}s")
    if args.text_only:
        write_gist(edit_dir, videos)
    if errors:
        print(f"{len(errors)} failures:")
        for v, msg in errors:
            print(f"  {v.name}: {msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()
