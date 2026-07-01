#!/usr/bin/env bash
# Render the active versions from each plugin.json + skill SKILL.md frontmatter into
# .claude-plugin/versions.json - the machine-readable "latest" manifest that the
# agency-os-update skill fetches from its raw URL on main.
# The version fields themselves stay the single source of truth; this only renders them.
# Idempotent by design: no timestamp in the output, so re-running without a version change
# produces an empty diff (safe to wire into a pre-commit/CI drift check).
#   Run: bash tools/versions.sh
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
OUT_JSON="$ROOT/.claude-plugin/versions.json"
MARKET="$ROOT/.claude-plugin/marketplace.json"

# Extract a top-level JSON string value ("key": "value"); first match wins.
json_scalar() { grep -m1 "\"$2\"" "$1" | sed -E "s/.*\"$2\"[[:space:]]*:[[:space:]]*\"([^\"]*)\".*/\1/"; }
# Extract a YAML frontmatter field (key: value) from a SKILL.md.
fm_field() { grep -m1 "^$2:" "$1" | sed -E "s/^$2:[[:space:]]*//"; }

# Plugin dir order follows marketplace.json; fall back to a glob if it is missing.
plugins=()
if [ -f "$MARKET" ]; then
  while IFS= read -r p; do plugins+=("$p"); done \
    < <(grep -oE '"source":[[:space:]]*"\./plugins/[^"]+"' "$MARKET" | sed -E 's#.*/plugins/([^"]+)".*#\1#')
fi
if [ ${#plugins[@]} -eq 0 ]; then
  for d in "$ROOT"/plugins/*/; do plugins+=("$(basename "$d")"); done
fi

json_plugins=""      # comma-joined plugin objects
n_plugins=0
n_skills=0
for p in "${plugins[@]}"; do
  pj="$ROOT/plugins/$p/.claude-plugin/plugin.json"
  [ -f "$pj" ] || continue
  n_plugins=$((n_plugins + 1))
  pname="$(json_scalar "$pj" name)"
  pver="$(json_scalar "$pj" version)"

  json_skills=""
  for s in "$ROOT"/plugins/"$p"/skills/*/SKILL.md; do
    [ -f "$s" ] || continue
    n_skills=$((n_skills + 1))
    [ -n "$json_skills" ] && json_skills+=", "
    json_skills+="\"$(fm_field "$s" name)\": \"$(fm_field "$s" version)\""
  done

  [ -n "$json_plugins" ] && json_plugins+=","
  json_plugins+=$'\n    '"\"$pname\": { \"version\": \"$pver\", \"skills\": { $json_skills } }"
done

{
  echo "{"
  echo "  \"marketplace\": \"agency-os\","
  echo "  \"plugins\": {${json_plugins}"
  echo "  }"
  echo "}"
} > "$OUT_JSON"

echo "geschrieben: $OUT_JSON ($n_plugins Plugins, $n_skills Skills)"
