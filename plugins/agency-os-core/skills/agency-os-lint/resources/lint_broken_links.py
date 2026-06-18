#!/usr/bin/env python3
"""Broken-Links-Check fuer Brain-Lint.

Findet Markdown-Links die auf nicht-existente Files zeigen.

Pfade kommen aus einer vom Lint-Skill (LLM) gebauten Config
`<root>/.agency-os/lint-config.json` (oder via --config). Fehlt sie, greifen
die Standard-Defaults. `.git` und `node_modules` werden immer uebersprungen,
das Log bewusst NICHT (auch dort rotten Links).

Aufruf aus Brain-Root: python3 <skill>/resources/lint_broken_links.py
Optional: python3 lint_broken_links.py /pfad/zum/brain-root --config pfad/config.json
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
from pathlib import Path

DEFAULT_CONFIG = {"skip": ["00-inbox", "11-archive"]}
ALWAYS_SKIP = {".git", "node_modules"}
LINK_RE = re.compile(r"\]\(([^)]+)\)")


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

    broken = []
    for f in sorted(iter_md(root, skip)):
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
                    rel = f.relative_to(root)
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
