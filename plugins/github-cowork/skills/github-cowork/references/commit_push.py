"""
COMMIT + PUSH — Erstellt einen neuen Commit via GitHub API und pusht ihn.

Aufruf:
    python3 references/commit_push.py \
        --repo REPO_DIR --api API_BASE --token TOKEN \
        --name "Vorname Nachname" --email "user@example.com" \
        --message "Commit-Nachricht" \
        --changed "datei1.md,datei2.md" \
        --added "neu.md" \
        --deleted "alt.md"

Ausgabe (JSON):
    {"commit_sha": "abc123...", "url": "https://github.com/..."}
"""
import argparse
import base64
import json
import os
from datetime import datetime, timezone
import requests
from helpers import auth_headers


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo",    required=True)
    p.add_argument("--api",     required=True)
    p.add_argument("--token",   required=True)
    p.add_argument("--name",    required=True)
    p.add_argument("--email",   required=True)
    p.add_argument("--message", required=True)
    p.add_argument("--branch",  default="main")
    p.add_argument("--changed", default="")
    p.add_argument("--added",   default="")
    p.add_argument("--deleted", default="")
    args = p.parse_args()

    headers = auth_headers(args.token)
    changed = [f for f in args.changed.split(",") if f]
    added   = [f for f in args.added.split(",")   if f]
    deleted = [f for f in args.deleted.split(",") if f]

    # Aktuellen Branch-Stand holen
    ref_data    = requests.get(f"{args.api}/git/refs/heads/{args.branch}", headers=headers).json()
    base_sha    = ref_data["object"]["sha"]
    commit_data = requests.get(f"{args.api}/git/commits/{base_sha}", headers=headers).json()
    base_tree   = commit_data["tree"]["sha"]

    # Blobs erstellen
    tree_entries = []
    for filepath in changed + added:
        full = os.path.join(args.repo, filepath)
        with open(full, "rb") as f:
            content = f.read()
        blob = requests.post(f"{args.api}/git/blobs", headers=headers, json={
            "content": base64.b64encode(content).decode(),
            "encoding": "base64"
        }).json()
        tree_entries.append({"path": filepath, "mode": "100644", "type": "blob", "sha": blob["sha"]})

    # Gelöschte Files
    for filepath in deleted:
        tree_entries.append({"path": filepath, "mode": "100644", "type": "blob", "sha": None})

    # Tree erstellen
    new_tree = requests.post(f"{args.api}/git/trees", headers=headers, json={
        "base_tree": base_tree,
        "tree": tree_entries
    }).json()

    # Commit erstellen
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_commit = requests.post(f"{args.api}/git/commits", headers=headers, json={
        "message": args.message,
        "tree": new_tree["sha"],
        "parents": [base_sha],
        "author": {"name": args.name, "email": args.email, "date": timestamp}
    }).json()

    # Branch-Ref updaten
    requests.patch(f"{args.api}/git/refs/heads/{args.branch}", headers=headers, json={
        "sha": new_commit["sha"]
    })

    print(json.dumps({
        "commit_sha": new_commit["sha"],
        "url": new_commit.get("html_url", "")
    }))


if __name__ == "__main__":
    main()
