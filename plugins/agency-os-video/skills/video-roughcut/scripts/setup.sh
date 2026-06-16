#!/usr/bin/env bash
# Idempotent setup for a video-* skill. Builds all writable artifacts (venv, node_modules,
# Chromium, .ready) under the resolved DATA dir, NOT the skill root: the plugin mount is
# writable in Claude Code (DATA == skill root, back-compat) but read-only in Cowork (DATA
# falls back to a cache dir). resolve-datadir.sh is the single source of truth.
# Node/Chromium steps only run when this skill bundles hyperframes; the slim skills skip them.
# Call: bash <skill>/scripts/setup.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"   # skill root (may be read-only)
DATA="$(bash "$ROOT/scripts/resolve-datadir.sh")"
mkdir -p "$DATA"
echo "[setup] skill root: $ROOT"
echo "[setup] data dir:   $DATA"

# --- 1. required tools ---
fail=0
for bin in ffmpeg python3 uv; do
  if command -v "$bin" >/dev/null 2>&1; then echo "[setup] OK   $bin"; else echo "[setup] FEHLT $bin"; fail=1; fi
done
ffmpeg -version 2>/dev/null | grep -q 'enable-libass' || echo "[setup] WARN ffmpeg ohne libass - Untertitel-Burn-in koennte fehlschlagen"
[ "$fail" = 1 ] && { echo "[setup] Abbruch: Pflicht-Tools fehlen."; exit 1; }

# --- 2. Python env (uv) under DATA. Deps come from the (read-only) pyproject in ROOT;
#        non-editable install so a read-only source dir is fine. The [whisper] extra is
#        only installed for skills that transcribe locally (marker .needs-whisper). ---
VENV="$DATA/.venv"
PIP_TARGET="$ROOT"
if [ -f "$ROOT/.needs-whisper" ]; then
  echo "[setup] installiere Python-Deps inkl. lokalem Whisper (uv)..."
  PIP_TARGET="$ROOT[whisper]"
else
  echo "[setup] installiere Python-Deps (uv)..."
fi
( uv venv --quiet "$VENV" && uv pip install --python "$VENV/bin/python" "$PIP_TARGET" ) \
  && echo "[setup] OK   Python-Env bereit ($VENV)." \
  || { echo "[setup] FEHLER Python-Install"; exit 1; }

# --- 3. motion-graphics engine (only when this skill bundles hyperframes) ---
if [ -d "$ROOT/engines/hyperframes" ]; then
  command -v node >/dev/null 2>&1 || { echo "[setup] FEHLT node (fuer Motion Graphics)"; exit 1; }
  HF="$DATA/engines/hyperframes"
  mkdir -p "$HF"
  cp "$ROOT/engines/hyperframes/package.json" "$HF/package.json"
  echo "[setup] installiere hyperframes Node-Deps (npm)..."
  ( cd "$HF" && npm install --no-audit --no-fund ) \
    && echo "[setup] OK   Node-Deps bereit." \
    || { echo "[setup] FEHLER npm install"; exit 1; }

  # Chromium for Puppeteer (only Motion Graphics needs it; cut + subtitles work without)
  export PUPPETEER_CACHE_DIR="$HF/.chromium-cache"
  echo "[setup] installiere Chromium in $HF/.chromium-cache..."
  if ( cd "$HF" && npx --yes @puppeteer/browsers install chrome@stable ) >/tmp/chrome-install.log 2>&1; then
    CHROME_PATH="$(grep -oE '/[^ ]+chrome' /tmp/chrome-install.log | tail -1)"
    echo "$CHROME_PATH" > "$HF/.chromium-path"
    echo "[setup] OK   Chromium -> $CHROME_PATH"
  else
    echo "[setup] WARN Chromium-Install fehlgeschlagen - Schnitt+Untertitel gehen trotzdem."
  fi
fi

# --- 4. ready marker (under DATA) ---
date +"%Y-%m-%dT%H:%M:%S" > "$DATA/.ready"
echo "[setup] FERTIG. Der API-Key liegt extern in {context}/secrets.env - mit doctor.sh pruefen."
