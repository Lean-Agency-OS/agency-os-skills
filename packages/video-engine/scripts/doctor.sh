#!/usr/bin/env bash
# Environment check for a video-* skill. Read-only, changes nothing.
# Pass the resolved Brain secrets file so the API key can be verified:
#   bash <skill>/scripts/doctor.sh {context}/secrets.env
# Node/Chromium are only checked when this skill bundles the motion-graphics engine.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
SECRETS="${1:-}"

echo "# video Doctor"
echo
echo "## Pflicht-Tools"
for bin in ffmpeg ffprobe python3 uv; do
  command -v "$bin" >/dev/null 2>&1 && echo "OK    $bin ($($bin --version 2>&1 | head -1))" || echo "FEHLT $bin"
done
ffmpeg -version 2>/dev/null | grep -q 'enable-libass' && echo "OK    ffmpeg+libass (Untertitel)" || echo "WARN  ffmpeg ohne libass"

# node/npm only matter when this skill ships the motion-graphics engine
if [ -d engines/hyperframes ]; then
  for bin in node npm; do
    command -v "$bin" >/dev/null 2>&1 && echo "OK    $bin ($($bin --version 2>&1 | head -1))" || echo "FEHLT $bin"
  done
fi

echo
echo "## Setup-Status"
[ -f .ready ] && echo "OK    .ready ($(cat .ready))" || echo "OFFEN .ready fehlt -> setup.sh ausfuehren"
[ -d .venv ] && echo "OK    Python-Env (.venv)" || echo "OFFEN .venv fehlt -> setup.sh"
if [ -d engines/hyperframes ]; then
  [ -d engines/hyperframes/node_modules/hyperframes ] && echo "OK    hyperframes installiert" || echo "OFFEN hyperframes node_modules fehlt -> setup.sh"
  [ -f engines/hyperframes/.chromium-path ] && echo "OK    Chromium ($(cat engines/hyperframes/.chromium-path))" || echo "OFFEN Chromium fehlt (nur fuer Motion Graphics noetig)"
fi

echo
echo "## API-Key (extern im Brain)"
if [ -n "$SECRETS" ] && [ -f "$SECRETS" ]; then
  # source the Brain secrets file (KEY=VALUE lines)
  set -a; . "$SECRETS"; set +a
  [ -n "${ELEVENLABS_API_KEY:-}" ] && echo "OK    ELEVENLABS_API_KEY gesetzt ($SECRETS)" || echo "OFFEN ELEVENLABS_API_KEY fehlt in $SECRETS"
elif [ -n "${ELEVENLABS_API_KEY:-}" ]; then
  echo "OK    ELEVENLABS_API_KEY aus Umgebung"
else
  echo "OFFEN secrets.env nicht uebergeben -> Aufruf: bash scripts/doctor.sh {context}/secrets.env"
fi

echo
echo "## Netzwerk (000=blockiert)"
for h in https://api.elevenlabs.io https://registry.npmjs.org; do
  echo "$(curl -s -o /dev/null -w '%{http_code}' -m 8 "$h" 2>/dev/null)  $h"
done
