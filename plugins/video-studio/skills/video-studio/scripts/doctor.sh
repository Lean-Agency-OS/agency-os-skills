#!/usr/bin/env bash
# video-studio Doctor - prueft die Umgebung, aendert nichts.
# Aufruf: bash .claude/skills/video-studio/scripts/doctor.sh
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "# video-studio Doctor"
echo
echo "## Pflicht-Tools"
for bin in ffmpeg ffprobe node npm python3 uv; do
  command -v "$bin" >/dev/null 2>&1 && echo "OK    $bin ($($bin --version 2>&1 | head -1))" || echo "FEHLT $bin"
done
ffmpeg -version 2>/dev/null | grep -q 'enable-libass' && echo "OK    ffmpeg+libass (Untertitel)" || echo "WARN  ffmpeg ohne libass"

echo
echo "## Setup-Status"
[ -f .ready ] && echo "OK    .ready ($(cat .ready))" || echo "OFFEN .ready fehlt -> setup.sh ausfuehren"
[ -f .env ] && grep -q '^ELEVENLABS_API_KEY=.\+' .env && echo "OK    ELEVENLABS_API_KEY gesetzt" || echo "OFFEN ELEVENLABS_API_KEY fehlt in .env"
[ -d engines/hyperframes/node_modules/hyperframes ] && echo "OK    hyperframes installiert" || echo "OFFEN hyperframes node_modules fehlt -> setup.sh"
[ -d engines/video-use/.venv ] && echo "OK    video-use Python-Env" || echo "OFFEN video-use/.venv fehlt -> setup.sh"
[ -f engines/hyperframes/.chromium-path ] && echo "OK    Chromium ($(cat engines/hyperframes/.chromium-path))" || echo "OFFEN Chromium fehlt (nur fuer Motion Graphics noetig)"

echo
echo "## Netzwerk (000=blockiert)"
for h in https://api.elevenlabs.io https://registry.npmjs.org; do
  echo "$(curl -s -o /dev/null -w '%{http_code}' -m 8 "$h" 2>/dev/null)  $h"
done
