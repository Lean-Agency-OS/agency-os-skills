#!/usr/bin/env bash
# Resolve GitHub auth for BOTH agency-os runtimes, without ever touching the repo's
# shared .git/config and without putting the token into argv or logs.
#
#   - Claude Code (macOS / Windows / Linux): an SSH key exists -> use native SSH, do nothing.
#   - Cowork (isolated Linux sandbox): there is no SSH key, and the Brain's .git/config
#     remote is SSH (git@github.com). The repo dir is a LIVE mount shared with the Mac, so
#     rewriting its remote would clobber the Mac setup and leak the token into the repo.
#     Instead we write a PAT-based auth into the SANDBOX-LOCAL global config only:
#       * a fixed, token-free insteadOf rewrite (SSH -> https), and
#       * the token in ~/.git-credentials via the "store" credential helper.
#     literal `git pull/push` then authenticate via the token; the repo remote stays on SSH
#     and the Mac never sees any of this.
#
# A GitHub PAT is PERSONAL and per-clone -> it must live in a gitignored local secrets
# file, never in the committed/shared {context}/secrets.env. This script therefore reads
# GITHUB_TOKEN local-first; the committed/shared file is used only as a last resort and
# only inside Cowork (positively detected), never on a personal machine.
#
# Usage: resolve-git-auth.sh <repo_dir> [committed_secrets_path]
# Prints ONE status word to stdout (never the token):
#   ssh             -> an SSH key is present, native SSH, nothing changed
#   pat             -> no SSH key, PAT auth written to the sandbox-local global config
#   missing-secrets -> no SSH key and no local/committed secrets file found
#   missing-token   -> no SSH key and no GITHUB_TOKEN in any source
set -euo pipefail

REPO="${1:-.}"
COMMITTED="${2:-}"

# Positive Cowork detection: combine several OBSERVED markers, never just one (each alone is
# unreliable; e.g. CLAUDE_CODE_TMPDIR can also be set in normal Claude Code). These names are
# not officially documented, so we only USE this to steer the shared-token fallback and the
# guidance text below -> never as the primary auth decision.
is_cowork() {
  [ "$(hostname 2>/dev/null)" = "claude" ] \
    && [ -d "$HOME/mnt/outputs" ] \
    && [ -d "$HOME/mnt/uploads" ] \
    && [ -n "${CLAUDE_CODE_TMPDIR:-}${CLAUDE_TMPDIR:-}" ]
}

# 1) Capability-based, NOT environment-guessing: the only question is "what can push?".
#    Claude Code may run on macOS, Windows or Linux, and Cowork is a Linux sandbox -> no OS
#    string reliably tells them apart. So: if an SSH key exists, use it (the normal Claude
#    Code case, any OS); otherwise fall back to a PAT (the Cowork case, and any keyless
#    machine where the user chose token auth). No key AND no token -> report both options.
if compgen -G "$HOME/.ssh/id_"* >/dev/null 2>&1; then
  echo "ssh"
  exit 0
fi

# Helper: read GITHUB_TOKEN from a KEY=VALUE file (token never echoed).
read_token() {
  [ -f "$1" ] || return 1
  local t
  t="$(grep -E '^GITHUB_TOKEN=' "$1" | head -n1 | cut -d= -f2- | tr -d '\r"' | xargs || true)"
  [ -n "$t" ] || return 1
  printf '%s' "$t"
}

# 2) No SSH key -> find a PAT (the Cowork sandbox case), LOCAL gitignored file first.
LOCAL_CANDIDATES=(
  "$REPO/.agency-os/secrets.env"
)
TOKEN=""
[ -n "${GITHUB_TOKEN:-}" ] && TOKEN="$GITHUB_TOKEN"
if [ -z "$TOKEN" ]; then
  for f in "${LOCAL_CANDIDATES[@]}"; do
    if TOKEN="$(read_token "$f")"; then break; else TOKEN=""; fi
  done
fi
# Committed file is SHARED across all clones -> only use it as a last resort INSIDE Cowork
# (ephemeral sandbox), never on a personal machine where a shared token must not be silently
# configured. Warn either way.
if [ -z "$TOKEN" ] && [ -n "$COMMITTED" ] && is_cowork; then
  if TOKEN="$(read_token "$COMMITTED")"; then
    echo "Warnung: GITHUB_TOKEN liegt in einer committeten Datei ($COMMITTED). Ein PAT ist persoenlich - besser in .agency-os/secrets.env verschieben (gitignored)." >&2
  else
    TOKEN=""
  fi
fi

# Did we find any USABLE secrets source at all? (the committed file only counts in Cowork)
ANY_SOURCE=""
[ -n "$COMMITTED" ] && [ -f "$COMMITTED" ] && is_cowork && ANY_SOURCE="yes"
for f in "${LOCAL_CANDIDATES[@]}"; do [ -f "$f" ] && ANY_SOURCE="yes"; done
if [ -z "$TOKEN" ]; then
  if [ -z "$ANY_SOURCE" ]; then echo "missing-secrets"; else echo "missing-token"; fi
  exit 0
fi

# 3) Sandbox-local global config only (NOT the repo .git/config).
#    Fixed, token-free insteadOf rewrite -> idempotent, no stale sections on token rotation.
git config --global --replace-all "url.https://github.com/.insteadOf" "git@github.com:"
git config --global --add         "url.https://github.com/.insteadOf" "ssh://git@github.com/"

# Token lives only in ~/.git-credentials (0600), supplied by the store helper.
git config --global credential.helper store
umask 077
printf 'https://x-access-token:%s@github.com\n' "$TOKEN" > "$HOME/.git-credentials"
chmod 600 "$HOME/.git-credentials"

echo "pat"
