#!/usr/bin/env bash
# video-studio Doctor - prueft die Umgebung, aendert nichts.
# Aufruf: bash <skill-ordner>/scripts/doctor.sh
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA="${CLAUDE_PLUGIN_DATA:-$HOME/.claude/plugins/data/video-studio}"
VERSION="$(python3 -c "import json;print(json.load(open('$ROOT/../../.claude-plugin/plugin.json'))['version'])" 2>/dev/null || echo dev)"

echo "# video-studio Doctor"
echo
echo "## Pflicht-Tools"
for bin in ffmpeg ffprobe node npm python3 uv; do
  command -v "$bin" >/dev/null 2>&1 && echo "OK    $bin ($($bin --version 2>&1 | head -1))" || echo "FEHLT $bin"
done
ffmpeg -version 2>/dev/null | grep -q 'enable-libass' && echo "OK    ffmpeg+libass (Untertitel)" || echo "WARN  ffmpeg ohne libass"

echo
echo "## Setup-Status (Daten-Verzeichnis: $DATA)"
if [ -f "$DATA/.ready" ]; then
  READY_VERSION="$(cut -d' ' -f1 "$DATA/.ready")"
  if [ "$READY_VERSION" = "$VERSION" ]; then
    echo "OK    .ready ($(cat "$DATA/.ready"))"
  else
    echo "OFFEN Plugin aktualisiert ($READY_VERSION -> $VERSION) -> setup.sh erneut ausfuehren (Key bleibt erhalten)"
  fi
else
  echo "OFFEN .ready fehlt -> setup.sh ausfuehren"
fi
[ -f "$DATA/.env" ] && grep -q '^ELEVENLABS_API_KEY=.\+' "$DATA/.env" && echo "OK    ELEVENLABS_API_KEY gesetzt" || echo "OFFEN ELEVENLABS_API_KEY fehlt in $DATA/.env"
[ -d "$DATA/hyperframes/node_modules/hyperframes" ] && echo "OK    hyperframes installiert" || echo "OFFEN hyperframes node_modules fehlt -> setup.sh"
[ -x "$DATA/venv/bin/python" ] && echo "OK    video-use Python-Env" || echo "OFFEN venv fehlt -> setup.sh"
[ -f "$DATA/.chromium-path" ] && echo "OK    Chromium ($(cat "$DATA/.chromium-path"))" || echo "OFFEN Chromium fehlt (nur fuer Motion Graphics noetig)"

echo
echo "## Netzwerk (000=blockiert)"
for h in https://api.elevenlabs.io https://registry.npmjs.org; do
  echo "$(curl -s -o /dev/null -w '%{http_code}' -m 8 "$h" 2>/dev/null)  $h"
done
