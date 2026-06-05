"""
STATUS — Zeigt lokal geänderte Dateien gegenüber Remote.

Aufruf:
    python3 references/status.py --repo REPO_DIR --api API_BASE --token TOKEN

Ausgabe (JSON):
    {
      "changed": ["datei1.md", ...],
      "added":   ["datei2.md", ...],
      "deleted": ["datei3.md", ...]
    }
"""
import argparse
import json
import requests
from helpers import auth_headers, local_head, get_remote_tree, scan_local_files


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo",  required=True)
    p.add_argument("--api",   required=True)
    p.add_argument("--token", required=True)
    p.add_argument("--branch", default="main")
    args = p.parse_args()

    # Remote HEAD → Tree
    branch_data = requests.get(
        f"{args.api}/branches/{args.branch}",
        headers=auth_headers(args.token)
    ).json()
    remote_sha = branch_data["commit"]["sha"]
    tree_sha   = branch_data["commit"]["commit"]["tree"]["sha"]
    remote     = get_remote_tree(args.api, args.token, tree_sha)

    # Lokale Files
    local = scan_local_files(args.repo)

    changed = [p for p in local if p in remote and local[p] != remote[p]]
    added   = [p for p in local if p not in remote]
    deleted = [p for p in remote if p not in local]

    print(json.dumps({"changed": changed, "added": added, "deleted": deleted, "remote_sha": remote_sha}))


if __name__ == "__main__":
    main()
