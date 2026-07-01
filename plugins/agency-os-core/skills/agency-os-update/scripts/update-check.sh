#!/usr/bin/env bash
# Gather the facts the update check needs and print them as plain text blocks.
# It does NOT compare or decide - the skill (Claude) reads the blocks and reports.
# Letting Claude compare two texts is more robust than a brittle parser here.
#
#   ENV:         which runtime -> decides which update instructions the skill shows.
#                Probed by capability (is the `claude` CLI usable?), not by OS guessing.
#   INSTALLIERT: what is running now (claude plugin list, else readable plugin.json files).
#   LATEST:      the marketplace's current versions.json on main (public raw URL, no auth).
#
# Usage: bash scripts/update-check.sh
set -uo pipefail   # no -e: a missing tool must not abort the whole report

RAW_URL="https://raw.githubusercontent.com/Lean-Agency-OS/agency-os-skills/main/.claude-plugin/versions.json"

# Resolve this skill's own location so we can find sibling plugin.json files if they are
# mounted (Claude Code cache has the full tree; Cowork may expose only this skill folder).
SELF="$(cd "$(dirname "$0")/.." 2>/dev/null && pwd || echo "")"      # .../skills/agency-os-update
PLUGINS_DIR="$(cd "$SELF/../../.." 2>/dev/null && pwd || echo "")"    # .../plugins

# --- ENV: capability probe -------------------------------------------------
if command -v claude >/dev/null 2>&1 && claude plugin list >/dev/null 2>&1; then
  ENV="code"
else
  ENV="cowork"
fi
echo "== ENV =="
echo "$ENV   (code = Claude Code / CLI vorhanden; cowork = keine CLI, Update ueber den Repo-Button)"

# --- INSTALLIERT -----------------------------------------------------------
echo
echo "== INSTALLIERT =="
if [ "$ENV" = "code" ]; then
  claude plugin list 2>&1
else
  found=0
  if [ -n "$PLUGINS_DIR" ] && [ -d "$PLUGINS_DIR" ]; then
    for pj in "$PLUGINS_DIR"/*/.claude-plugin/plugin.json; do
      [ -f "$pj" ] || continue
      found=1
      name="$(grep -m1 '"name"'    "$pj" | sed -E 's/.*"name":[[:space:]]*"([^"]*)".*/\1/')"
      ver="$( grep -m1 '"version"' "$pj" | sed -E 's/.*"version":[[:space:]]*"([^"]*)".*/\1/')"
      echo "$name: $ver"
    done
  fi
  if [ "$found" = 0 ]; then
    echo "(installierte Versionen in dieser Sandbox nicht lesbar - nur der eigene Skill-Ordner ist gemountet."
    echo " Dann NICHT als exakten Diff behandeln: die LATEST-Liste zeigen und zum Aktualisieren den Cowork-Button-Weg nennen.)"
  fi
fi

# --- LATEST ----------------------------------------------------------------
echo
echo "== LATEST (marketplace main: versions.json) =="
if command -v curl >/dev/null 2>&1; then
  # Capture body + HTTP status so we can tell 404 (not pushed yet) from 000 (no network).
  resp="$(curl -sS -w $'\n%{http_code}' "$RAW_URL" 2>/dev/null)"
  code="${resp##*$'\n'}"
  body="${resp%$'\n'*}"
  if [ "$code" = "200" ]; then
    echo "$body"
  elif [ "$code" = "000" ]; then
    echo "(kein Netz erreichbar - LATEST nicht abrufbar)"
  else
    echo "(versions.json nicht ladbar: HTTP $code - evtl. noch nicht auf main gepusht)"
  fi
elif command -v wget >/dev/null 2>&1; then
  wget -qO- "$RAW_URL" 2>/dev/null || echo "(konnte versions.json nicht laden)"
else
  echo "(weder curl noch wget verfuegbar)"
fi
