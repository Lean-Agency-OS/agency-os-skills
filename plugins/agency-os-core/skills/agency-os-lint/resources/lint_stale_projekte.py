#!/usr/bin/env python3
"""Stale-Projekte-Check fuer Brain-Lint.

Prueft Projekt-Hub-Files im projects-Ordner (Rolle aus .agency-os/architecture.md,
Default 06-projects/) auf drei Klassen Probleme:

1. CLOSED-IN-PROJEKTE: Hub-File hat Status der Abschluss signalisiert (closed,
   done, archived, oder closed-YYYY-MM-DD-Pattern), liegt aber noch im projects-
   Ordner statt im archive-Ordner (.../projekte/). Soll verschoben werden.

2. STALE-ACTIVE: Hub-File hat status: active (oder andere lebendige Status),
   aber kein git-commit in 30+ Tagen. Verdacht: vergessen oder abgeschlossen
   ohne Status-Update.

3. NO-STATUS: Hub-File ohne status-Frontmatter ueberhaupt. Konsistenz-Defekt.

Hub-File-Definition: {projects}/{name}.md (flat) ODER
{projects}/{slug}/{slug}.md (Folder-Hub-Pattern). Sub-Notes innerhalb
Folder-Projekten werden ignoriert.

Aufruf aus Brain-Root: python3 <skill>/resources/lint_stale_projekte.py
Optional: python3 lint_stale_projekte.py /pfad/zum/brain-root
"""
from __future__ import annotations
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _arch import load_arch, role_dir

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
ARCH = load_arch(ROOT)
PROJEKTE_DIR = ROOT / role_dir(ARCH, "projects")
ARCHIVE_DIR = role_dir(ARCH, "archive")
STALE_THRESHOLD_DAYS = 30

CLOSED_STATUS_RE = re.compile(r"^(closed|done|archived|abgeschlossen|finished)(-\d{4}-\d{2}-\d{2})?$", re.IGNORECASE)
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
STATUS_RE = re.compile(r"^status:\s*(.+?)\s*$", re.MULTILINE)

def find_hub_files() -> list[Path]:
    """Sammle alle Projekt-Hub-Files."""
    hubs: list[Path] = []
    if not PROJEKTE_DIR.is_dir():
        return hubs
    for entry in PROJEKTE_DIR.iterdir():
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

def last_git_commit_date(md: Path) -> float | None:
    """Unix-timestamp des letzten Commits, oder None wenn nicht trackable."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ct", "--", str(md.relative_to(ROOT))],
            cwd=ROOT,
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
    hubs = find_hub_files()
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
        # Status ist nicht "closed", aber lebendig - check git-Activity
        last_ts = last_git_commit_date(hub)
        if last_ts is None:
            continue
        age_days = int((now - last_ts) / 86400)
        if age_days >= STALE_THRESHOLD_DAYS:
            stale_active.append((hub, status, age_days))

    print(f"=== CLOSED-IN-PROJEKTE (sollte nach {ARCHIVE_DIR}/projekte/) ===")
    if closed_in_projekte:
        for hub, status in closed_in_projekte:
            rel = hub.relative_to(ROOT)
            print(f"  {rel}  status: {status}")
    else:
        print("  (keine)")

    print("\n=== STALE-ACTIVE (kein Commit in 30+ Tagen) ===")
    if stale_active:
        for hub, status, age in sorted(stale_active, key=lambda x: -x[2]):
            rel = hub.relative_to(ROOT)
            print(f"  {rel}  status: {status}  ({age}d ohne Commit)")
    else:
        print("  (keine)")

    print("\n=== NO-STATUS (Frontmatter fehlt oder ohne status:) ===")
    if no_status:
        for hub in no_status:
            rel = hub.relative_to(ROOT)
            print(f"  {rel}")
    else:
        print("  (keine)")

    total_issues = len(closed_in_projekte) + len(stale_active) + len(no_status)
    print(f"\n--- {len(hubs)} hub-files geprueft, {total_issues} Auffaelligkeiten "
          f"({len(closed_in_projekte)} closed, {len(stale_active)} stale, {len(no_status)} no-status)")
    return 0 if total_issues == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
