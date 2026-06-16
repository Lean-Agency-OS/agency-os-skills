#!/usr/bin/env bash
# Resolve a WRITABLE data dir for this skill's build artifacts (venv, node_modules,
# Chromium, .ready). Single source of truth: setup.sh, doctor.sh and the SKILL.md
# helper calls all read the path from here, so setup and runtime never disagree.
#
# The plugin mount is writable in Claude Code -> use the skill root (back-compat).
# In Cowork it is read-only (fuse bindfs ro) -> fall back to a cache dir. NOT the
# Brain/{context}: that is git-tracked and synced Mac<->Linux, and an ARM-Linux venv
# is useless on the Mac.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"   # skill root
SKILL="$(basename "$ROOT")"

if ( : > "$ROOT/.wtest" ) 2>/dev/null; then
  rm -f "$ROOT/.wtest"
  echo "$ROOT"
else
  echo "${VIDEO_ENGINE_DATA:-${XDG_CACHE_HOME:-$HOME/.cache}/agency-os/video-engine/$SKILL}"
fi
