#!/usr/bin/env python3
"""Orphan-Pages-Check fuer Brain-Lint.

Findet Notes ohne eingehende Links. Atomare Notes leben durch Verknuepfung,
ein Orphan ist ein Lint-Signal.

Pfade kommen aus einer vom Lint-Skill (LLM) gebauten Config
`<root>/.agency-os/lint-config.json` (oder via --config):
  skip    - Ordner, die nie durchsucht werden (inbox, archive)
  content - Inhalts-Ordner, in denen Orphans zaehlen (inkl. Custom-Ordner)
Fehlt die Config, greifen die Standard-Defaults. `.git`/`node_modules` immer skip.
Outgoing-Links werden ueber das ganze Brain gesammelt (auch das Log, damit
Erwaehnungen aus Tageslogs als incoming zaehlen).

Aufruf aus Brain-Root: python3 <skill>/resources/lint_orphans.py
Optional: python3 lint_orphans.py /pfad/zum/brain-root --config pfad/config.json
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

DEFAULT_CONFIG = {
    "skip": ["00-inbox", "11-archive"],
    "content": ["01-context", "02-strategy", "03-marketing", "04-sales",
                "05-clients", "06-projects", "07-org", "08-wiki", "09-ip"],
}
ALWAYS_SKIP = {".git", "node_modules"}
LINK_RE = re.compile(r"\]\(([^)]+)\)")
NEW_FILE_THRESHOLD_DAYS = 7


def load_config(root: Path, cfg_path: Path | None) -> dict:
    cfg = dict(DEFAULT_CONFIG)
    p = cfg_path or (root / ".agency-os" / "lint-config.json")
    if p.exists():
        try:
            cfg.update(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            pass
    return cfg


def iter_md(root: Path, skip: set):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip and not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".md"):
                yield Path(dirpath) / fn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=None)
    ap.add_argument("--config", default=None)
    args = ap.parse_args()
    root = Path(args.root).resolve() if args.root else Path.cwd()
    cfg = load_config(root, Path(args.config) if args.config else None)
    skip = ALWAYS_SKIP | set(cfg.get("skip", []))
    content = set(cfg.get("content", []))

    def in_scope(md: Path) -> bool:
        rel = md.relative_to(root)
        if rel.name == "_index.md":
            return False
        return rel.parts[0] in content

    def is_recent(md: Path) -> bool:
        return (time.time() - md.stat().st_mtime) < NEW_FILE_THRESHOLD_DAYS * 86400

    # Outgoing-Links ueber das ganze Brain zu absoluten Paths aufloesen.
    incoming: set[Path] = set()
    for f in iter_md(root, skip):
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

    orphans: list[Path] = []
    for md in iter_md(root, skip):
        if not in_scope(md) or md.resolve() in incoming or is_recent(md):
            continue
        orphans.append(md)

    orphans.sort()
    by_dir: dict[str, list[Path]] = {}
    for o in orphans:
        rel = o.relative_to(root)
        by_dir.setdefault(str(rel.parent), []).append(o)

    for d in sorted(by_dir):
        files = by_dir[d]
        print(f"\n{d}/ ({len(files)})")
        for f in files:
            print(f"  {f.relative_to(root)}")

    print(f"\n--- {len(orphans)} orphans (in scope, >{NEW_FILE_THRESHOLD_DAYS}d alt, nicht _index.md)")
    return 0 if not orphans else 1


if __name__ == "__main__":
    sys.exit(main())
