#!/usr/bin/env bash
# sync-engine.sh - vendor the engine from packages/video-engine/ into each video-* skill.
# Dev-only tool, never shipped. Run after every change to packages/video-engine/, then commit
# the source AND the vendored copies (the copies are what gets distributed).
#
# Call (from anywhere): bash tools/sync-engine.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/packages/video-engine"
SKILLS="$ROOT/plugins/agency-os-video/skills"

# Optional first arg: sync only that one skill (default: all).
ONLY="${1:-}"

# Base every skill needs (transcribe imports ffmpeg_utils; pack depends on the transcript).
COMMON_HELPERS="ffmpeg_utils.py transcribe.py pack_transcripts.py"

sync_skill() {
  local name="$1" helpers="$2" refs="$3" hyperframes="$4" whisper="$5"
  if [ -n "$ONLY" ] && [ "$ONLY" != "$name" ]; then return 0; fi
  local dst="$SKILLS/$name"
  echo "[sync] $name"
  mkdir -p "$dst"

  # --- helpers (authoritative: previous state is discarded) ---
  rm -rf "$dst/helpers"; mkdir -p "$dst/helpers"
  cp "$SRC/helpers/LICENSE" "$dst/helpers/"
  for h in $helpers; do
    cp "$SRC/helpers/$h" "$dst/helpers/$h"
  done

  # --- references ---
  rm -rf "$dst/references"; mkdir -p "$dst/references"
  for r in $refs; do
    cp "$SRC/references/$r" "$dst/references/$r"
  done

  # --- shared scripts + deps (same for every skill) ---
  mkdir -p "$dst/scripts"
  cp "$SRC/scripts/setup.sh" "$dst/scripts/setup.sh"
  cp "$SRC/scripts/doctor.sh" "$dst/scripts/doctor.sh"
  chmod +x "$dst/scripts/setup.sh" "$dst/scripts/doctor.sh"
  cp "$SRC/pyproject.toml" "$dst/pyproject.toml"
  cp "$SRC/uv.lock" "$dst/uv.lock"
  cp "$SRC/secrets.env.example" "$dst/secrets.env.example"

  # --- motion-graphics engine only where needed ---
  if [ "$hyperframes" = "yes" ]; then
    mkdir -p "$dst/engines/hyperframes"
    cp "$SRC/engines/hyperframes/package.json" "$dst/engines/hyperframes/package.json"
  else
    rm -rf "$dst/engines"
  fi

  # --- local Whisper marker: only skills that transcribe locally get the heavy extra ---
  if [ "$whisper" = "yes" ]; then
    touch "$dst/.needs-whisper"
  else
    rm -f "$dst/.needs-whisper"
  fi
}

# ---- Manifest: skill | extra helpers | references | hyperframes | local whisper ----
# render.py imports grade.py lazily with a fallback -> subtitle-only render works without grade.py.
# Only footage-mining transcribes locally (text-only pass); the Scribe cut skills stay lean.

sync_skill video-final \
  "$COMMON_HELPERS render.py grade.py broll.py timeline_view.py" \
  "cut-standards.md hard-rules.md transcription.md motion-style.md" \
  yes no

sync_skill video-roughcut \
  "$COMMON_HELPERS export_nle.py timeline_view.py" \
  "cut-standards.md hard-rules.md transcription.md" \
  no no

sync_skill video-captions \
  "$COMMON_HELPERS render.py" \
  "transcription.md" \
  no no

sync_skill video-footage-mining \
  "$COMMON_HELPERS transcribe_batch.py" \
  "transcription.md" \
  no yes

echo "[sync] done. Commit the source AND the vendored copies."
