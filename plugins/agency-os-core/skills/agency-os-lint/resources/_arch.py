#!/usr/bin/env python3
"""Rollen->Pfad-Aufloesung fuer die Lint-Skripte.

Liest die Map aus `<root>/.agency-os/architecture.md` (Markdown-Liste `- rolle: pfad`,
gepflegt vom agency-os-start-Skill). Faellt auf die Standard-Ordnernamen zurueck, wenn die
Datei fehlt oder eine Rolle nicht genannt ist. So sind in den Skripten keine Ordnernamen
mehr hartkodiert.
"""
from __future__ import annotations
import re
from pathlib import Path

DEFAULTS = {
    "inbox": "00-inbox", "context": "01-context", "strategy": "02-strategy",
    "marketing": "03-marketing", "sales": "04-sales", "clients": "05-clients",
    "projects": "06-projects", "roles": "07-org", "knowledge": "08-wiki",
    "ip": "09-ip", "logs": "10-logs", "archive": "11-archive",
}
# Rollen, die keine durchsuchbaren Inhalts-Ordner sind:
NON_CONTENT = {"inbox", "logs", "archive"}
_LINE = re.compile(r"^\s*-\s*([a-z0-9_-]+)\s*:\s*(.+?)\s*$", re.IGNORECASE)


def load_arch(root: Path) -> dict:
    """Rolle->Pfad-Dict, Defaults gemerged mit der architecture.md (falls vorhanden)."""
    roles = dict(DEFAULTS)
    f = root / ".agency-os" / "architecture.md"
    if f.exists():
        try:
            for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
                m = _LINE.match(line)
                if m and m.group(1).lower() in DEFAULTS:
                    roles[m.group(1).lower()] = m.group(2).strip().strip("/")
        except Exception:
            pass
    return roles


def role_dir(roles: dict, name: str) -> str:
    """Top-Level-Ordnername einer Rolle (erstes Pfad-Segment)."""
    return roles.get(name, DEFAULTS.get(name, name)).split("/")[0]


def skip_dirs(roles: dict) -> set:
    """Ordner, die der Lint nie durchsucht."""
    return {".git", "node_modules", role_dir(roles, "inbox"), role_dir(roles, "archive")}


def content_dirs(roles: dict) -> set:
    """Durchsuchbare Inhalts-Ordner (alle Rollen ausser inbox/logs/archive)."""
    return {role_dir(roles, r) for r in roles if r not in NON_CONTENT}
