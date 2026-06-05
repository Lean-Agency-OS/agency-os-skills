#!/usr/bin/env bash
# video-studio Setup - idempotent.
# Code bleibt im Skill-Ordner (Plugin-Cache, wird bei Updates ersetzt).
# Alles Veraenderliche (venv, node_modules, Chromium, .env, .ready) liegt im
# persistenten Plugin-Daten-Verzeichnis (CLAUDE_PLUGIN_DATA) und UEBERLEBT Updates.
# Aufruf: bash <skill-ordner>/scripts/setup.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"   # Skill-Ordner (Code)
DATA="${CLAUDE_PLUGIN_DATA:-$HOME/.claude/plugins/data/video-studio}"
mkdir -p "$DATA"
echo "[setup] skill root: $ROOT"
echo "[setup] daten-dir:  $DATA"

# Plugin-Version (fuer Re-Setup-Erkennung nach Updates)
VERSION="$(python3 -c "import json;print(json.load(open('$ROOT/../../.claude-plugin/plugin.json'))['version'])" 2>/dev/null || echo dev)"

# --- 1. Pflicht-Tools (muessen in der Umgebung vorhanden sein) ---
fail=0
for bin in ffmpeg node python3 uv; do
  if command -v "$bin" >/dev/null 2>&1; then echo "[setup] OK   $bin"; else echo "[setup] FEHLT $bin"; fail=1; fi
done
ffmpeg -version 2>/dev/null | grep -q 'enable-libass' || echo "[setup] WARN ffmpeg ohne libass - Untertitel-Burn-in koennte fehlschlagen"
[ "$fail" = 1 ] && { echo "[setup] Abbruch: Pflicht-Tools fehlen."; exit 1; }

# --- 2. .env (Key bringt der Nutzer; liegt im Daten-Verzeichnis, ueberlebt Updates) ---
if [ ! -f "$DATA/.env" ]; then
  cp "$ROOT/.env.example" "$DATA/.env"
  echo "[setup] $DATA/.env angelegt - bitte ELEVENLABS_API_KEY eintragen."
else
  echo "[setup] .env vorhanden (bleibt unangetastet)."
fi

# --- 3. video-use Python-Env (venv im Daten-Verzeichnis, Install non-editable) ---
echo "[setup] installiere video-use Python-Deps (uv) nach $DATA/venv ..."
uv venv --quiet "$DATA/venv" \
  && uv pip install --quiet --python "$DATA/venv/bin/python" "$ROOT/engines/video-use" \
  && echo "[setup] OK   video-use Python-Env bereit." \
  || { echo "[setup] FEHLER video-use Python-Install"; exit 1; }

# --- 4. hyperframes Node-Deps (im Daten-Verzeichnis) ---
echo "[setup] installiere hyperframes Node-Deps (npm) nach $DATA/hyperframes ..."
mkdir -p "$DATA/hyperframes"
cp "$ROOT/engines/hyperframes/package.json" "$DATA/hyperframes/"
( cd "$DATA/hyperframes" && npm install --no-audit --no-fund ) \
  && echo "[setup] OK   Node-Deps bereit." \
  || { echo "[setup] FEHLER npm install"; exit 1; }

# --- 5. Chromium fuer Puppeteer (nur Motion Graphics / Phase 5; Schnitt geht ohne) ---
export PUPPETEER_CACHE_DIR="$DATA/chromium-cache"
echo "[setup] installiere Chromium nach $DATA/chromium-cache ..."
if ( cd "$DATA/hyperframes" && npx --yes @puppeteer/browsers install chrome@stable ) >/tmp/chrome-install.log 2>&1; then
  CHROME_PATH="$(grep -oE '/[^ ]+chrome' /tmp/chrome-install.log | tail -1)"
  echo "$CHROME_PATH" > "$DATA/.chromium-path"
  echo "[setup] OK   Chromium -> $CHROME_PATH"
else
  echo "[setup] WARN Chromium-Install fehlgeschlagen - Schnitt+Untertitel gehen trotzdem."
fi

# --- 6. Fertig-Marker (mit Plugin-Version: nach Update meldet doctor Re-Setup) ---
echo "$VERSION $(date +"%Y-%m-%dT%H:%M:%S")" > "$DATA/.ready"
echo "[setup] FERTIG (Version $VERSION). Falls noch offen: ELEVENLABS_API_KEY in $DATA/.env eintragen."
