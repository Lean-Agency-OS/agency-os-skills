#!/usr/bin/env python3
"""Broken-Links-Check fuer Brain-Lint.

Findet Markdown-Links die auf nicht-existente Files zeigen. Excludes: inbox/ und archive/
(Rollen aus .agency-os/architecture.md), .git/, node_modules/. Inkludiert das Log bewusst,
weil dort auch Links rotten koennen.

Aufruf aus Brain-Root: python3 <skill>/resources/lint_broken_links.py
Optional: python3 lint_broken_links.py /pfad/zum/brain-root
"""
from __future__ import annotations
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _arch import load_arch, skip_dirs

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
SKIP_DIRS = skip_dirs(load_arch(ROOT))
LINK_RE = re.compile(r"\]\(([^)]+)\)")

def iter_md(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".md"):
                yield Path(dirpath) / fn

def main():
    broken = []
    for f in sorted(iter_md(ROOT)):
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for m in LINK_RE.finditer(line):
                path = m.group(1).split('#')[0].strip()
                if not path or path.startswith(("http://", "https://", "mailto:")):
                    continue
                target = (f.parent / path).resolve()
                if not target.exists():
                    rel = f.relative_to(ROOT)
                    broken.append((str(rel), lineno, path))

    by_file: dict[str, list[tuple[int, str]]] = {}
    for rel, lineno, path in broken:
        by_file.setdefault(rel, []).append((lineno, path))

    for rel in sorted(by_file):
        items = by_file[rel]
        print(f"\n{rel} ({len(items)})")
        for lineno, path in items:
            print(f"  L{lineno}: {path}")

    print(f"\n--- {len(broken)} broken links in {len(by_file)} files")
    return 0 if not broken else 1

if __name__ == "__main__":
    sys.exit(main())
