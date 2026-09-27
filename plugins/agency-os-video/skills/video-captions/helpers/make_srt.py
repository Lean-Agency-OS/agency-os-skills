#!/usr/bin/env python3
"""make_srt.py - build a sidecar .srt from a word-level transcript JSON.

Input is the transcript shape written by transcribe.py
(<edit_dir>/transcripts/<stem>.json: {"text": ..., "words": [...]}).
Words are grouped into cues by sentence punctuation, speech gaps,
line length and max cue duration. Designed for longform videos where
hand-building an SRT is impractical; the output is a plain upload-ready
SRT (no styling - platforms render their own).

Usage:
  make_srt.py transcript.json -o out.srt
  make_srt.py transcript.json -o out.srt --max-line-chars 42 --max-lines 2 \
      --max-cue-seconds 5.0 --gap-seconds 0.8
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SENTENCE_END = (".", "!", "?", "…")
SOFT_BREAK = (",", ";", ":")


def fmt_time(seconds: float) -> str:
    """Format seconds as SRT timestamp HH:MM:SS,mmm."""
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1_000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def load_words(transcript_path: Path) -> list[dict]:
    data = json.loads(transcript_path.read_text())
    words = [
        w for w in data.get("words", [])
        if w.get("type", "word") == "word" and str(w.get("text", "")).strip()
    ]
    if not words:
        sys.exit(
            f"No word-level timestamps in {transcript_path} - "
            "re-transcribe with word timestamps (Scribe / whisper word mode)."
        )
    return words


def group_cues(
    words: list[dict],
    max_line_chars: int,
    max_lines: int,
    max_cue_seconds: float,
    gap_seconds: float,
) -> list[dict]:
    """Group words into cues. A cue closes on sentence end, a long speech
    gap, max duration, or when the character budget is exhausted."""
    max_chars = max_line_chars * max_lines
    cues: list[dict] = []
    cur: list[dict] = []

    def close():
        if not cur:
            return
        text = " ".join(w["text"].strip() for w in cur)
        cues.append({
            "start": float(cur[0]["start"]),
            "end": float(cur[-1]["end"]),
            "text": text,
        })
        cur.clear()

    for w in words:
        if cur:
            gap = float(w["start"]) - float(cur[-1]["end"])
            duration = float(w["end"]) - float(cur[0]["start"])
            length = len(" ".join(x["text"].strip() for x in cur)) + 1 + len(w["text"].strip())
            if gap >= gap_seconds or duration > max_cue_seconds or length > max_chars:
                close()
        cur.append(w)
        token = w["text"].strip()
        if token.endswith(SENTENCE_END):
            close()
        # Soft breaks only close a cue once past half the character budget,
        # so short clauses do not fragment into one-liner cues.
        elif token.endswith(SOFT_BREAK):
            text_len = len(" ".join(x["text"].strip() for x in cur))
            if text_len >= max_chars // 2:
                close()
    close()
    return cues


def wrap_lines(text: str, max_line_chars: int, max_lines: int) -> str:
    """Greedy word wrap into at most max_lines lines."""
    lines: list[str] = []
    cur = ""
    for token in text.split():
        cand = f"{cur} {token}".strip()
        if len(cand) <= max_line_chars or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = token
    if cur:
        lines.append(cur)
    # Overflow beyond max_lines folds into the last line (rare: single
    # over-long words); cue grouping already bounds total length.
    if len(lines) > max_lines:
        lines = lines[: max_lines - 1] + [" ".join(lines[max_lines - 1:])]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="Build a sidecar SRT from a word-level transcript JSON")
    ap.add_argument("transcript", type=Path, help="transcript JSON from transcribe.py")
    ap.add_argument("-o", "--output", type=Path, required=True, help="output .srt path")
    ap.add_argument("--max-line-chars", type=int, default=42)
    ap.add_argument("--max-lines", type=int, default=2)
    ap.add_argument("--max-cue-seconds", type=float, default=5.0)
    ap.add_argument("--gap-seconds", type=float, default=0.8)
    args = ap.parse_args()

    words = load_words(args.transcript)
    cues = group_cues(
        words, args.max_line_chars, args.max_lines,
        args.max_cue_seconds, args.gap_seconds,
    )

    blocks = []
    for i, cue in enumerate(cues, start=1):
        body = wrap_lines(cue["text"], args.max_line_chars, args.max_lines)
        blocks.append(f"{i}\n{fmt_time(cue['start'])} --> {fmt_time(cue['end'])}\n{body}\n")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(blocks), encoding="utf-8")
    print(f"srt: {args.output} ({len(cues)} cues, {len(words)} words)")


if __name__ == "__main__":
    main()
