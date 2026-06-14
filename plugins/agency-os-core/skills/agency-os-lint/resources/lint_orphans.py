#!/usr/bin/env python3
"""Orphan-Pages-Check fuer Brain-Lint.

Findet Notes ohne eingehende Links. Atomare Notes leben durch Verknuepfung,
ein Orphan ist ein Lint-Signal.

Scope: Inhalts-Ordner laut .agency-os/architecture.md (alle Rollen ausser inbox/logs/archive), ohne _index.md
Excludes: _index.md, Files juenger als 7 Tage, inbox/, archive/, .git/, node_modules/
Outgoing-Links werden ueber das ganze Brain gesammelt (auch das Log, damit
Erwaehnungen aus Tageslogs als incoming zaehlen).

Aufruf aus Brain-Root: python3 <skill>/resources/lint_orphans.py
Optional: python3 lint_orphans.py /pfad/zum/brain-root
"""
from __future__ import annotations
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _arch import load_arch, skip_dirs, content_dirs

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
ARCH = load_arch(ROOT)
SKIP_DIRS = skip_dirs(ARCH)
CONTENT_DIRS = content_dirs(ARCH)
LINK_RE = re.compile(r"\]\(([^)]+)\)")
NEW_FILE_THRESHOLD_DAYS = 7

def iter_md(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".md"):
                yield Path(dirpath) / fn

def in_scope(md: Path) -> bool:
    """Inhalts-Ordner laut architecture.md (inbox/logs/archive ausgenommen, kein _index.md)."""
    rel = md.relative_to(ROOT)
    if rel.name == "_index.md":
        return False
    return rel.parts[0] in CONTENT_DIRS

def is_recent(md: Path) -> bool:
    age_seconds = time.time() - md.stat().st_mtime
    return age_seconds < NEW_FILE_THRESHOLD_DAYS * 86400

def collect_incoming() -> set[Path]:
    """Resolve alle Outgoing-Links zu absoluten Paths. Was kein Ziel hat
    (broken), zaehlt nicht."""
    incoming: set[Path] = set()
    for f in iter_md(ROOT):
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        for m in LINK_RE.finditer(text):
            path = m.group(1).split('#')[0].strip()
            if not path or path.startswith(("http://", "https://", "mailto:")):
                continue
            target = (f.parent / path).resolve()
            if target.exists() and target.is_file() and target != f:
                incoming.add(target)
    return incoming

def main():
    incoming = collect_incoming()
    orphans: list[Path] = []
    for md in iter_md(ROOT):
        if not in_scope(md):
            continue
        if md.resolve() in incoming:
            continue
        if is_recent(md):
            continue
        orphans.append(md)

    orphans.sort()
    by_dir: dict[str, list[Path]] = {}
    for o in orphans:
        rel = o.relative_to(ROOT)
        by_dir.setdefault(str(rel.parent), []).append(o)

    for d in sorted(by_dir):
        files = by_dir[d]
        print(f"\n{d}/ ({len(files)})")
        for f in files:
            print(f"  {f.relative_to(ROOT)}")

    print(f"\n--- {len(orphans)} orphans (in scope, >{NEW_FILE_THRESHOLD_DAYS}d alt, nicht _index.md)")
    return 0 if not orphans else 1

if __name__ == "__main__":
    sys.exit(main())
