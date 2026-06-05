"""
HISTORY — Zeigt die letzten Commits des Repos.

Aufruf:
    python3 references/history.py \
        --api API_BASE --token TOKEN [--branch main] [--author "Name"] [--limit 20]

Ausgabe (JSON):
    [
      {"sha": "abc123", "author": "{Name}", "date": "TT.MM.JJJJ HH:MM", "message": "..."},
      ...
    ]
"""
import argparse
import json
from datetime import datetime
import requests
from helpers import auth_headers


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--api",    required=True)
    p.add_argument("--token",  required=True)
    p.add_argument("--branch", default="main")
    p.add_argument("--author", default="")
    p.add_argument("--limit",  type=int, default=20)
    args = p.parse_args()

    headers = auth_headers(args.token)
    params = {"sha": args.branch, "per_page": args.limit}
    if args.author:
        params["author"] = args.author

    commits = requests.get(f"{args.api}/commits", headers=headers, params=params).json()

    result = []
    for c in commits:
        raw_date = c["commit"]["author"]["date"]  # ISO 8601
        dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
        result.append({
            "sha":     c["sha"][:7],
            "author":  c["commit"]["author"]["name"],
            "date":    dt.strftime("%d.%m.%Y %H:%M"),
            "message": c["commit"]["message"].split("\n")[0]
        })

    print(json.dumps(result))


if __name__ == "__main__":
    main()
