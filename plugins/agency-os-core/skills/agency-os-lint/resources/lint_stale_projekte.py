#!/usr/bin/env python3
"""Stale projects check for brain lint.

Checks project hub files in the projects folder for three classes of problems:

1. CLOSED-IN-PROJEKTE: hub file has a status signaling completion (closed,
   done, archived, or a closed-YYYY-MM-DD pattern) but still sits in the
   projects folder instead of the archive folder (.../projekte/). Should move.

2. STALE-ACTIVE: hub file has status: active (or another live status),
   but no git commit in 30+ days. Suspicion: forgotten or finished
   without a status update.

3. NO-STATUS: hub file without any status frontmatter. Consistency defect.

projects and archive paths come from the config built by the lint skill (LLM)
at `<root>/.agency-os/lint-config.json` (or via --config). If missing, the
standard defaults apply.

Hub file definition: {projects}/{name}.md (flat) OR
{projects}/{slug}/{slug}.md (folder hub pattern). Sub-notes inside
folder projects are ignored.

Run from brain root: python3 <skill>/resources/lint_stale_projekte.py
Optional: python3 lint_stale_projekte.py /path/to/brain-root --config path/config.json
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

DEFAULT_CONFIG = {"projects": "06-projects", "archive": "11-archive"}
STALE_THRESHOLD_DAYS = 30

CLOSED_STATUS_RE = re.compile(r"^(closed|done|archived|abgeschlossen|finished)(-\d{4}-\d{2}-\d{2})?$", re.IGNORECASE)
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
STATUS_RE = re.compile(r"^status:\s*(.+?)\s*$", re.MULTILINE)


def load_config(root: Path, cfg_path: Path | None) -> dict:
    cfg = dict(DEFAULT_CONFIG)
    p = cfg_path or (root / ".agency-os" / "lint-config.json")
    if p.exists():
        try:
            cfg.update(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            pass
    return cfg


def find_hub_files(projekte_dir: Path) -> list[Path]:
    """Collect all project hub files."""
    hubs: list[Path] = []
    if not projekte_dir.is_dir():
        return hubs
    for entry in projekte_dir.iterdir():
        if entry.name.startswith("_"):
            continue
        if entry.is_file() and entry.suffix == ".md":
            hubs.append(entry)
        elif entry.is_dir():
            hub = entry / f"{entry.name}.md"
            if hub.exists():
                hubs.append(hub)
    return sorted(hubs)


def parse_status(md: Path) -> str | None:
    try:
        text = md.read_text(encoding="utf-8")
    except Exception:
        return None
    fm = FRONTMATTER_RE.match(text)
    if not fm:
        return None
    m = STATUS_RE.search(fm.group(1))
    if not m:
        return None
    return m.group(1).strip()


def last_git_commit_date(md: Path, root: Path) -> float | None:
    """Unix timestamp of the last commit, or None if not trackable."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ct", "--", str(md.relative_to(root))],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        out = result.stdout.strip()
        if not out:
            return None
        return float(out)
    except (subprocess.SubprocessError, OSError):
        return None


def is_closed_status(status: str) -> bool:
    return bool(CLOSED_STATUS_RE.match(status))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=None)
    ap.add_argument("--config", default=None)
    args = ap.parse_args()
    root = Path(args.root).resolve() if args.root else Path.cwd()
    cfg = load_config(root, Path(args.config) if args.config else None)
    projekte_dir = root / cfg.get("projects", "06-projects")
    archive_dir = cfg.get("archive", "11-archive")

    hubs = find_hub_files(projekte_dir)
    closed_in_projekte: list[tuple[Path, str]] = []
    stale_active: list[tuple[Path, str, int]] = []
    no_status: list[Path] = []

    now = time.time()

    for hub in hubs:
        status = parse_status(hub)
        if status is None:
            no_status.append(hub)
            continue
        if is_closed_status(status):
            closed_in_projekte.append((hub, status))
            continue
        # Status is not "closed" but live - check git activity
        last_ts = last_git_commit_date(hub, root)
        if last_ts is None:
            continue
        age_days = int((now - last_ts) / 86400)
        if age_days >= STALE_THRESHOLD_DAYS:
            stale_active.append((hub, status, age_days))

    print(f"=== CLOSED-IN-PROJEKTE (sollte nach {archive_dir}/projekte/) ===")
    if closed_in_projekte:
        for hub, status in closed_in_projekte:
            print(f"  {hub.relative_to(root)}  status: {status}")
    else:
        print("  (keine)")

    print("\n=== STALE-ACTIVE (kein Commit in 30+ Tagen) ===")
    if stale_active:
        for hub, status, age in sorted(stale_active, key=lambda x: -x[2]):
            print(f"  {hub.relative_to(root)}  status: {status}  ({age}d ohne Commit)")
    else:
        print("  (keine)")

    print("\n=== NO-STATUS (Frontmatter fehlt oder ohne status:) ===")
    if no_status:
        for hub in no_status:
            print(f"  {hub.relative_to(root)}")
    else:
        print("  (keine)")

    total_issues = len(closed_in_projekte) + len(stale_active) + len(no_status)
    print(f"\n--- {len(hubs)} hub-files geprueft, {total_issues} Auffaelligkeiten "
          f"({len(closed_in_projekte)} closed, {len(stale_active)} stale, {len(no_status)} no-status)")
    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
