#!/usr/bin/env bash
# sync-engine.sh - vendort die Engine aus packages/video-engine/ in jeden video-* Skill.
# Dev-Tool, wird NICHT ausgeliefert. Nach jeder Aenderung an packages/video-engine/ ausfuehren,
# dann Quelle + gevendorte Kopien committen.
#
# Aufruf (vom Repo-Root oder beliebig): bash tools/sync-engine.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/packages/video-engine"
SKILLS="$ROOT/plugins/agency-os-video/skills"

# Basis, die jeder Skill braucht (transcribe importiert ffmpeg_utils; pack haengt am Transkript).
COMMON_HELPERS="ffmpeg_utils.py transcribe.py pack_transcripts.py"

sync_skill() {
  local name="$1" helpers="$2" refs="$3" hyperframes="$4"
  local dst="$SKILLS/$name"
  echo "[sync] $name"
  mkdir -p "$dst"

  # --- helpers (autoritativ: alter Stand wird verworfen) ---
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

  # --- deps (gleicher Satz fuer alle Skills) ---
  cp "$SRC/pyproject.toml" "$dst/pyproject.toml"
  cp "$SRC/uv.lock" "$dst/uv.lock"

  # --- Motion-Graphics-Engine nur wo gebraucht ---
  if [ "$hyperframes" = "yes" ]; then
    mkdir -p "$dst/engines/hyperframes"
    cp "$SRC/engines/hyperframes/package.json" "$dst/engines/hyperframes/package.json"
  else
    rm -rf "$dst/engines"
  fi
}

# ---- Manifest: Skill | zusaetzliche Helfer | References | hyperframes ----
# render.py importiert grade.py lazy mit Fallback -> ohne grade.py laeuft Subtitle-Render trotzdem.

sync_skill video-final \
  "$COMMON_HELPERS render.py grade.py broll.py timeline_view.py" \
  "cut-standards.md hard-rules.md transcription.md motion-style.md" \
  yes

sync_skill video-roughcut \
  "$COMMON_HELPERS export_nle.py timeline_view.py" \
  "cut-standards.md hard-rules.md transcription.md" \
  no

sync_skill video-captions \
  "$COMMON_HELPERS render.py" \
  "transcription.md" \
  no

sync_skill video-footage-mining \
  "$COMMON_HELPERS transcribe_batch.py" \
  "transcription.md" \
  no

echo "[sync] fertig. Nicht vergessen: Quelle + gevendorte Kopien committen."
