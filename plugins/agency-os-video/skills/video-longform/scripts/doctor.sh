#!/usr/bin/env bash
# Environment check for a video-* skill. Read-only, changes nothing.
# Resolves the writable DATA dir (same logic as setup.sh) and checks the artifacts there.
# Pass the resolved Brain secrets file to verify the API key:
#   bash <skill>/scripts/doctor.sh {context}/secrets.env
# Node/Chromium are only checked when this skill bundles the motion-graphics engine.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA="$(bash "$ROOT/scripts/resolve-datadir.sh")"
SECRETS="${1:-}"

echo "# video Doctor"
echo "(data dir: $DATA)"
echo
echo "## Pflicht-Tools"
for bin in ffmpeg ffprobe python3 uv; do
  command -v "$bin" >/dev/null 2>&1 && echo "OK    $bin ($($bin --version 2>&1 | head -1))" || echo "FEHLT $bin"
done
ffmpeg -version 2>/dev/null | grep -q 'enable-libass' && echo "OK    ffmpeg+libass (Untertitel)" || echo "WARN  ffmpeg ohne libass"

# node/npm only matter when this skill ships the motion-graphics engine
if [ -d "$ROOT/engines/hyperframes" ]; then
  for bin in node npm; do
    command -v "$bin" >/dev/null 2>&1 && echo "OK    $bin ($($bin --version 2>&1 | head -1))" || echo "FEHLT $bin"
  done
fi

echo
echo "## Setup-Status"
[ -f "$DATA/.ready" ] && echo "OK    .ready ($(cat "$DATA/.ready"))" || echo "OFFEN .ready fehlt -> setup.sh ausfuehren"
[ -d "$DATA/.venv" ] && echo "OK    Python-Env (.venv)" || echo "OFFEN .venv fehlt -> setup.sh"
# local Whisper is only expected for skills that bundle it (marker .needs-whisper)
if [ -f "$ROOT/.needs-whisper" ] && [ -x "$DATA/.venv/bin/python" ]; then
  "$DATA/.venv/bin/python" -c "import faster_whisper" 2>/dev/null \
    && echo "OK    faster-whisper (lokale Transkription)" \
    || echo "OFFEN faster-whisper fehlt -> setup.sh"
fi
if [ -d "$ROOT/engines/hyperframes" ]; then
  [ -d "$DATA/engines/hyperframes/node_modules/hyperframes" ] && echo "OK    hyperframes installiert" || echo "OFFEN hyperframes node_modules fehlt -> setup.sh"
  [ -f "$DATA/engines/hyperframes/.chromium-path" ] && echo "OK    Chromium ($(cat "$DATA/engines/hyperframes/.chromium-path"))" || echo "OFFEN Chromium fehlt (nur fuer Motion Graphics noetig)"
fi

echo
echo "## API-Key (extern im Brain)"
key_src=""
if [ -n "$SECRETS" ] && [ -f "$SECRETS" ]; then
  # source the Brain secrets file (KEY=VALUE lines)
  set -a; . "$SECRETS"; set +a
  key_src="$SECRETS"
elif [ -n "${ELEVENLABS_API_KEY:-}" ]; then
  key_src="Umgebung"
fi
if [ -n "${ELEVENLABS_API_KEY:-}" ]; then
  echo "OK    ELEVENLABS_API_KEY gesetzt ($key_src)"
  # The 'speech_to_text' scope can NOT be checked without a real (credit-spending) call:
  # the Scribe endpoint validates the request body BEFORE auth, so a probe without audio
  # returns 422 for any key. This stays read-only and just sets the right expectation.
  echo "      Scope-Hinweis: wirft die Transkription HTTP 403, fehlt dem Key der"
  echo "      'speech_to_text'-Scope -> im ElevenLabs-Dashboard 'Sprache zu Text' auf"
  echo "      Zugriff stellen (Key ggf. neu erzeugen)."
elif [ -z "$SECRETS" ]; then
  echo "OFFEN secrets.env nicht uebergeben -> Aufruf: bash scripts/doctor.sh {context}/secrets.env"
else
  echo "OFFEN ELEVENLABS_API_KEY fehlt in $SECRETS"
fi

echo
echo "## Netzwerk"
for h in https://api.elevenlabs.io https://registry.npmjs.org; do
  code="$(curl -s -o /dev/null -w '%{http_code}' -m 8 "$h" 2>/dev/null)"
  if [ "$code" = "000" ]; then
    echo "BLOCKIERT  $h (HTTP 000 - kein Netz / Sandbox dicht)"
  else
    echo "erreichbar $h (HTTP $code - jede Antwort != 000 heisst: Netz offen)"
  fi
done
