#!/usr/bin/env python3
"""Format-agnostic CI reader.

Brand CI lives in ci.md, but the values are not always delivered the same way:
sometimes YAML frontmatter, sometimes a Markdown table. This layer normalizes the
caption-relevant values and hands them to the renderer as parameters, so render.py
stays independent of the document format.

Usage:
    ci_read.py <ci.md>                 # prints all resolved values as JSON
    ci_read.py <ci.md> --get caption-color-ass
    ci_read.py <ci.md> --get caption-font
    ci_read.py <ci.md> --get caption-font-path

Resolves, in order: YAML frontmatter (colors.subtitle / fonts.subtitle[/ _path]) ->
Markdown table rows (a "subtitle"/"untertitel" key with a hex / font value). The
caption colour is always emitted as ASS BGR too (#FED760 -> &H0060D7FE).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HEX_RE = re.compile(r"#?([0-9a-fA-F]{6})\b")


def hex_to_ass(value: str | None) -> str | None:
    """#RRGGBB -> &H00BBGGRR (ASS is AABBGGRR, alpha 00 = opaque). None if no hex."""
    if not value:
        return None
    m = HEX_RE.search(value)
    if not m:
        return None
    rr, gg, bb = m.group(1)[0:2], m.group(1)[2:4], m.group(1)[4:6]
    return f"&H00{bb}{gg}{rr}".upper()


def _unquote(val: str) -> str:
    val = val.strip()
    m = re.match(r'^"([^"]*)"', val) or re.match(r"^'([^']*)'", val)
    if m:
        return m.group(1)
    return val.split("#", 1)[0].strip()  # strip trailing inline comment


def parse_frontmatter(text: str) -> dict:
    """Tiny 2-level YAML reader for the ci.md frontmatter (no pyyaml dependency)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}
    data: dict = {}
    parent: str | None = None
    for ln in lines[1:end]:
        if not ln.strip() or ln.lstrip().startswith("#") or ":" not in ln:
            continue
        indent = len(ln) - len(ln.lstrip())
        key = ln.split(":", 1)[0].strip()
        val = _unquote(ln.split(":", 1)[1])
        if indent == 0:
            if val == "":
                data[key] = {}
                parent = key
            else:
                data[key] = val
                parent = None
        elif parent and isinstance(data.get(parent), dict):
            data[parent][key] = val
    return data


def parse_table(text: str) -> dict:
    """Flat key->value map from any Markdown table rows (lowercased keys)."""
    flat: dict = {}
    for ln in text.splitlines():
        s = ln.strip()
        if not s.startswith("|") or s.count("|") < 2:
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 2:
            continue
        key = cells[0].lower()
        if not key or set(key) <= set("-: "):  # separator / header rule row
            continue
        flat[key] = cells[1]
    return flat


def _from_table(flat: dict, needles: tuple[str, ...], want_hex: bool) -> str | None:
    for k, v in flat.items():
        if any(n in k for n in needles):
            if want_hex and not HEX_RE.search(v):
                continue
            if not want_hex and HEX_RE.fullmatch(v.strip()):
                continue  # a hex is not a font name
            return v
    return None


def resolve(text: str) -> dict:
    fm = parse_frontmatter(text)
    tbl = parse_table(text)
    colors = fm.get("colors") if isinstance(fm.get("colors"), dict) else {}
    fonts = fm.get("fonts") if isinstance(fm.get("fonts"), dict) else {}

    caption_hex = colors.get("subtitle") or _from_table(tbl, ("subtitle", "untertitel"), want_hex=True)
    caption_font = fonts.get("subtitle") or _from_table(tbl, ("subtitle-font", "untertitel-font", "untertitel"), want_hex=False)
    caption_font_path = fonts.get("subtitle_path")

    out = {
        "caption_color_hex": (HEX_RE.search(caption_hex).group(0) if caption_hex and HEX_RE.search(caption_hex) else None),
        "caption_color_ass": hex_to_ass(caption_hex),
        "caption_font": (caption_font or None),
        "caption_font_path": (caption_font_path or None),
        "name": fm.get("name"),
        "handle": fm.get("handle"),
    }
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Read brand CI (frontmatter or table) -> normalized values")
    ap.add_argument("ci", type=Path, help="Path to ci.md")
    ap.add_argument("--get", help="Print a single value: caption-color-ass | caption-color-hex | caption-font | caption-font-path | name | handle")
    args = ap.parse_args()

    if not args.ci.exists():
        sys.exit(f"ci not found: {args.ci}")
    values = resolve(args.ci.read_text())

    if args.get:
        key = args.get.replace("-", "_")
        v = values.get(key)
        if v:
            print(v)
        # empty output + exit 0 when missing: caller applies its own default/fallback
        return
    print(json.dumps(values, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
