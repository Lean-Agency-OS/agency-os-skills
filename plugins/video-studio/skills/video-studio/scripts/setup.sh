#!/usr/bin/env bash
# video-studio Setup - idempotent. Installiert alles IN den Skill-Ordner (nichts global).
# Laeuft in Coworks Linux-Sandbox. Aufruf: bash .claude/skills/video-studio/scripts/setup.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"   # -> .claude/skills/video-studio/
cd "$ROOT"
echo "[setup] skill root: $ROOT"

# --- 1. Pflicht-Tools (muessen in der Sandbox vorhanden sein) ---
fail=0
for bin in ffmpeg node python3 uv; do
  if command -v "$bin" >/dev/null 2>&1; then echo "[setup] OK   $bin"; else echo "[setup] FEHLT $bin"; fail=1; fi
done
ffmpeg -version 2>/dev/null | grep -q 'enable-libass' || echo "[setup] WARN ffmpeg ohne libass - Untertitel-Burn-in koennte fehlschlagen"
[ "$fail" = 1 ] && { echo "[setup] Abbruch: Pflicht-Tools fehlen."; exit 1; }

# --- 2. .env (Key bringt der Kunde) ---
if [ ! -f .env ]; then cp .env.example .env; echo "[setup] .env angelegt - bitte ELEVENLABS_API_KEY eintragen."; else echo "[setup] .env vorhanden."; fi
# Helpers lesen .env aus dem Skill-Root (cwd) - liegt jetzt direkt hier, kein Symlink noetig.

# --- 3. Python-Env (uv, lokal im Skill-Root .venv) ---
echo "[setup] installiere Python-Deps (uv)..."
( uv venv --quiet && uv pip install -e . ) \
  && echo "[setup] OK   Python-Env bereit." \
  || { echo "[setup] FEHLER Python-Install"; exit 1; }

# --- 4. hyperframes Node-Deps (lokal in engines/hyperframes/node_modules) ---
echo "[setup] installiere hyperframes Node-Deps (npm)..."
( cd engines/hyperframes && npm install --no-audit --no-fund ) \
  && echo "[setup] OK   Node-Deps bereit." \
  || { echo "[setup] FEHLER npm install"; exit 1; }

# --- 5. Chromium fuer Puppeteer (nur Motion Graphics / Phase 2; Schnitt geht ohne) ---
export PUPPETEER_CACHE_DIR="$ROOT/engines/hyperframes/.chromium-cache"
echo "[setup] installiere Chromium in engines/hyperframes/.chromium-cache..."
if ( cd engines/hyperframes && npx --yes @puppeteer/browsers install chrome@stable ) >/tmp/chrome-install.log 2>&1; then
  CHROME_PATH="$(grep -oE '/[^ ]+chrome' /tmp/chrome-install.log | tail -1)"
  echo "$CHROME_PATH" > engines/hyperframes/.chromium-path
  echo "[setup] OK   Chromium -> $CHROME_PATH"
else
  echo "[setup] WARN Chromium-Install fehlgeschlagen - Schnitt+Untertitel gehen trotzdem."
fi

# --- 6. Fertig-Marker ---
date +"%Y-%m-%dT%H:%M:%S" > .ready
echo "[setup] FERTIG. Naechster Schritt: ELEVENLABS_API_KEY in .env eintragen, dann ein Video schneiden."
