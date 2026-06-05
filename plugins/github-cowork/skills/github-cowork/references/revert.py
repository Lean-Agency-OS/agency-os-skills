"""
REVERT — Stellt den Stand eines bestimmten Commits wieder her (als neuer Commit).

Aufruf:
    python3 references/revert.py \
        --repo REPO_DIR --api API_BASE --token TOKEN \
        --name "Vorname Nachname" --email "user@example.com" \
        --target-sha "abc123..."

Ablauf:
  1. Tree des Ziel-Commits holen
  2. Alle Dateien lokal überschreiben
  3. Neuen Commit erstellen ("Zurückgesetzt auf: {message}")

Ausgabe (JSON):
    {"commit_sha": "...", "restored_files": [...]}
"""
import argparse
import base64
import json
import os
from datetime import datetime, timezone
import requests
from helpers import auth_headers, update_refs


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo",       required=True)
    p.add_argument("--api",        required=True)
    p.add_argument("--token",      required=True)
    p.add_argument("--name",       required=True)
    p.add_argument("--email",      required=True)
    p.add_argument("--target-sha", required=True)
    p.add_argument("--branch",     default="main")
    args = p.parse_args()

    headers = auth_headers(args.token)

    # Ziel-Commit holen
    target = requests.get(f"{args.api}/git/commits/{args.target_sha}", headers=headers).json()
    target_tree_sha = target["tree"]["sha"]
    target_msg = target["message"].split("\n")[0]

    # Aktuellen Branch-Stand
    ref_data = requests.get(f"{args.api}/git/refs/heads/{args.branch}", headers=headers).json()
    base_sha = ref_data["object"]["sha"]

    # Tree des Ziel-Commits
    tree_data = requests.get(
        f"{args.api}/git/trees/{target_tree_sha}?recursive=1",
        headers=headers
    ).json()

    # Lokale Files überschreiben
    restored = []
    for item in tree_data.get("tree", []):
        if item["type"] != "blob":
            continue
        filepath = item["path"]
        file_data = requests.get(
            f"{args.api}/contents/{filepath}?ref={args.target_sha}",
            headers=headers
        ).json()
        content = base64.b64decode(file_data["content"])
        local_path = os.path.join(args.repo, filepath)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "wb") as f:
            f.write(content)
        restored.append(filepath)

    # Neuen Commit erstellen (kein force-push)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_commit = requests.post(f"{args.api}/git/commits", headers=headers, json={
        "message": f"Zurückgesetzt auf: {target_msg}",
        "tree": target_tree_sha,
        "parents": [base_sha],
        "author": {"name": args.name, "email": args.email, "date": timestamp}
    }).json()

    requests.patch(f"{args.api}/git/refs/heads/{args.branch}", headers=headers, json={
        "sha": new_commit["sha"]
    })

    update_refs(args.repo, new_commit["sha"], args.branch)

    print(json.dumps({"commit_sha": new_commit["sha"], "restored_files": restored}))


if __name__ == "__main__":
    main()
