"""
PULL — Holt neue Remote-Änderungen und schreibt sie lokal (ohne git CLI).

Aufruf:
    python3 references/pull.py \
        --repo REPO_DIR --api API_BASE --token TOKEN [--branch main]

Ausgabe (JSON):
    {
      "updated":   ["datei1.md", ...],   ← konfliktfrei überschrieben
      "conflicts": ["datei2.md", ...],   ← lokal geändert, muss manuell aufgelöst werden
      "remote_sha": "abc123..."
    }
"""
import argparse
import base64
import json
import os
import requests
from helpers import auth_headers, local_head, blob_sha, update_refs, get_remote_tree, scan_local_files


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo",   required=True)
    p.add_argument("--api",    required=True)
    p.add_argument("--token",  required=True)
    p.add_argument("--branch", default="main")
    args = p.parse_args()

    headers = auth_headers(args.token)

    # Remote HEAD
    remote_sha = requests.get(
        f"{args.api}/git/refs/heads/{args.branch}",
        headers=headers
    ).json()["object"]["sha"]

    # Lokaler HEAD
    local_sha = local_head(args.repo, args.branch)

    if remote_sha == local_sha:
        print(json.dumps({"updated": [], "conflicts": [], "remote_sha": remote_sha, "already_current": True}))
        return

    # Neue Remote-Commits ermitteln
    commits = requests.get(f"{args.api}/commits?sha={args.branch}&per_page=50", headers=headers).json()
    new_commits = []
    for c in commits:
        if c["sha"] == local_sha:
            break
        new_commits.append(c["sha"])

    # Geänderte Files aus neuen Commits sammeln
    remote_changed = {}
    for sha in new_commits:
        files = requests.get(f"{args.api}/commits/{sha}", headers=headers).json().get("files", [])
        for f in files:
            remote_changed[f["filename"]] = f["status"]

    # Lokale Files für Konflikt-Check
    local_files = scan_local_files(args.repo)

    # Remote-Tree für Konflikt-Vergleich (Stand vor den neuen Commits)
    base_commit = requests.get(f"{args.api}/git/commits/{local_sha}", headers=headers).json()
    base_tree = get_remote_tree(args.api, args.token, base_commit["tree"]["sha"])

    updated, conflicts = [], []

    for filepath, status in remote_changed.items():
        local_path = os.path.join(args.repo, filepath)
        local_blob = local_files.get(filepath)
        original_blob = base_tree.get(filepath)

        # Konflikt wenn lokal geändert (lokaler SHA weicht vom ursprünglichen Remote ab)
        if local_blob and local_blob != original_blob:
            conflicts.append(filepath)
            continue

        # Kein Konflikt → überschreiben
        if status == "removed":
            if os.path.exists(local_path):
                os.remove(local_path)
        else:
            file_data = requests.get(
                f"{args.api}/contents/{filepath}?ref={remote_sha}",
                headers=headers
            ).json()
            content = base64.b64decode(file_data["content"])
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(content)

        updated.append(filepath)

    # Refs updaten wenn keine offenen Konflikte
    if not conflicts:
        update_refs(args.repo, remote_sha, args.branch)

    print(json.dumps({"updated": updated, "conflicts": conflicts, "remote_sha": remote_sha}))


if __name__ == "__main__":
    main()
