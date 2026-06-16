#!/usr/bin/env bash
# Idempotent setup for a video-* skill. Installs everything INTO the skill folder (nothing global).
# Runs in Cowork's Linux sandbox. The Node/Chromium steps only run when this skill bundles the
# motion-graphics engine (engines/hyperframes present) - the slim skills skip them.
# Call: bash <skill>/scripts/setup.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"   # -> skill root
cd "$ROOT"
echo "[setup] skill root: $ROOT"

# --- 1. required tools ---
fail=0
for bin in ffmpeg python3 uv; do
  if command -v "$bin" >/dev/null 2>&1; then echo "[setup] OK   $bin"; else echo "[setup] FEHLT $bin"; fail=1; fi
done
ffmpeg -version 2>/dev/null | grep -q 'enable-libass' || echo "[setup] WARN ffmpeg ohne libass - Untertitel-Burn-in koennte fehlschlagen"
[ "$fail" = 1 ] && { echo "[setup] Abbruch: Pflicht-Tools fehlen."; exit 1; }

# --- 2. Python env (uv, local .venv in the skill root) ---
echo "[setup] installiere Python-Deps (uv)..."
( uv venv --quiet && uv pip install -e . ) \
  && echo "[setup] OK   Python-Env bereit." \
  || { echo "[setup] FEHLER Python-Install"; exit 1; }

# --- 3. motion-graphics engine (only when this skill bundles hyperframes) ---
if [ -d engines/hyperframes ]; then
  command -v node >/dev/null 2>&1 || { echo "[setup] FEHLT node (fuer Motion Graphics)"; exit 1; }
  echo "[setup] installiere hyperframes Node-Deps (npm)..."
  ( cd engines/hyperframes && npm install --no-audit --no-fund ) \
    && echo "[setup] OK   Node-Deps bereit." \
    || { echo "[setup] FEHLER npm install"; exit 1; }

  # Chromium for Puppeteer (only Motion Graphics needs it; cut + subtitles work without)
  export PUPPETEER_CACHE_DIR="$ROOT/engines/hyperframes/.chromium-cache"
  echo "[setup] installiere Chromium in engines/hyperframes/.chromium-cache..."
  if ( cd engines/hyperframes && npx --yes @puppeteer/browsers install chrome@stable ) >/tmp/chrome-install.log 2>&1; then
    CHROME_PATH="$(grep -oE '/[^ ]+chrome' /tmp/chrome-install.log | tail -1)"
    echo "$CHROME_PATH" > engines/hyperframes/.chromium-path
    echo "[setup] OK   Chromium -> $CHROME_PATH"
  else
    echo "[setup] WARN Chromium-Install fehlgeschlagen - Schnitt+Untertitel gehen trotzdem."
  fi
fi

# --- 4. ready marker ---
date +"%Y-%m-%dT%H:%M:%S" > .ready
echo "[setup] FERTIG. Der API-Key liegt extern in {context}/secrets.env - mit doctor.sh pruefen."
