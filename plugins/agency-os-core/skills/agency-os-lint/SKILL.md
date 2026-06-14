---
name: agency-os-lint
version: 1.0.0
description: Brain-Hygiene-Check. Verwende wenn der User "lint", "räum auf", "check brain", "wie geht's dem Wiki", "wiki-check" oder ähnliches sagt. Findet broken Links, Orphan-Pages, veraltete/widersprüchliche Claims und stale Projekt-Hubs. Liefert nur einen Befund-Report mit Empfehlungen, macht NICHTS autonom destruktives.
---

# Lint (Brain-Hygiene)

**Output:** Ein Befund-Report im Chat (keine eigene Datei). Der User entscheidet pro Punkt, was angepackt wird.

**Kritisch:** keine destruktiven Änderungen autonom. Keine Mass-Renames. Der User genehmigt jeden Fix einzeln.

> **Brain-Pfade:** Keine festen Ordnernamen. Pfade unten (`{projects}`, `{ip}`, `{logs}` …) sind Platzhalter für die Rollen aus `.agency-os/architecture.md`; fehlt eine, gilt der Standard-Name. Die mitgelieferten Skripte lösen die Rollen selbst über die `architecture.md` auf (gemeinsamer Helper `resources/_arch.py`, Fallback auf die Standard-Namen) und scannen das Arbeitsverzeichnis (Brain-Root) als Wurzel.

**Aufruf der Skripte:** vom Brain-Root aus. Abkürzung unten: `LINT="${CLAUDE_PLUGIN_ROOT:-.}/skills/agency-os-lint"`. Die Skripte nehmen das aktuelle Verzeichnis als Brain-Root; optional lässt sich der Root als erstes Argument übergeben.

## Architektur aktuell halten

Vor den Checks die `.agency-os/architecture.md` gegen die echte Top-Level-Struktur abgleichen (normalerweise pflegt der `agency-os-start`-Skill sie). Bei Drift - Ordner umbenannt/neu/entfernt - die betroffenen Zeilen aktualisieren; fehlt die Datei, aus der erkannten Struktur neu schreiben. Das ist Infrastruktur (wie `.agency-os/state.md`): ohne Rückfrage schreiben, im Report eine Zeile vermerken. So scannen die Lint-Skripte danach die richtigen Ordner.

---

## Workflow

### 1. Broken-Links-Check

```bash
python3 "$LINT/resources/lint_broken_links.py"
```

Output: pro Datei eine Sektion mit `L{zeile}: {pfad}` für jeden Treffer, plus Total-Zähler. Excludes: `{inbox}`, `{archive}`, `.git/`, `node_modules/` (Rollen aus der architecture.md). Inkludiert das Log (`{logs}`) bewusst (auch dort verrotten Links).

### 2. Orphan-Pages

Notes ohne eingehende Links sind ein Lint-Signal. Atomare Notes leben durch Verknüpfung.

```bash
python3 "$LINT/resources/lint_orphans.py"
```

Scope: Inhalts-Ordner laut architecture.md (alle Rollen außer inbox/logs/archive, flach + verschachtelt). Das Skript filtert automatisch: `_index.md`, Files jünger als 7 Tage. Outgoing-Links werden über das ganze Brain gesammelt (auch das Log, damit Erwähnungen aus Tageslogs als incoming zählen).

### 3. Stale Projekt-Hubs + veraltete Claims

```bash
python3 "$LINT/resources/lint_stale_projekte.py"
```

Status-Frontmatter-Check für Projekt-Hubs im `{projects}`-Ordner. Drei Klassen:
- **closed-in-projekte:** Hub hat Status `closed`/`done`/`archived` (oder `closed-YYYY-MM-DD`-Pattern) und liegt noch in `{projects}` statt `{archive}/projekte/`. Verschieben.
- **stale-active:** Hub hat lebendigen Status, aber kein Git-Commit in 30+ Tagen. Verdacht: vergessen oder closed-ohne-Update.
- **no-status:** Hub-File hat kein `status:` in der Frontmatter. Konsistenz-Defekt.

Widersprüche und veraltete inhaltliche Claims, die kein Skript abdeckt, beim Lesen der betroffenen Files mitnehmen und im Report unter "Widersprüche / veraltete Claims" aufführen.

### 4. Befund-Report formatieren

```markdown
## Lint-Befund Stand {YYYY-MM-DD}

### Broken Links ({N})
- {file}: {pfad}
- ...

### Orphans ({N})
- {file} (keine eingehenden Links)
- ...

### Widersprüche / veraltete Claims ({N})
- {kurze Beschreibung mit Files}
- ...

### Empfehlungen, sortiert nach Priorität
1. **Kritisch:** {z.B. broken Link in CLAUDE.md}
2. **Hoch:** {z.B. Pricing-Widerspruch zwischen 2 Files}
3. **Mittel:** {z.B. Orphan im `{ip}`-Ordner}
4. **Niedrig:** {z.B. Themen-Kandidat}
```

### 5. Mit dem User durchgehen

Pro Punkt: *"Soll ich das fixen, oder ist das beabsichtigt?"*. Mach **nichts** autonom Destruktives. Auch keine Mass-Renames ohne explizite Zustimmung.

### 6. Log-Eintrag

Sektion `## [YYYY-MM-DD] lint` ins zentrale Tageslog (`{logs}/YYYY-MM-DD.md`), mit 1-2 Zeilen über die Anzahl der Findings (inkl. ggf. korrigierter architecture.md).

---

## Was NICHT passiert

- **Keine autonomen Destructive-Actions.** Der User genehmigt jeden Fix einzeln.
- Keine Massen-Edits ohne explizite Bestätigung.
- Kein Lint des inbox-Ordners (das ist eine Inbox, nicht das Wiki).
- Kein Lint des archive-Ordners (das ist explizit eingefroren).

---

## Edge Cases

- **Sehr viele Findings:** nur Top 20 pro Kategorie zeigen, Rest aggregiert. Die Liste muss handhabbar bleiben.
- **Broken Link, der absichtlich auf eine zukünftige Datei zeigt:** der User kann das markieren, dann beim nächsten Lint überspringen.
- **Migration-Reste (z.B. `STALE_MIGRATED.md` in alten Spokes):** als bekannten Zustand kennzeichnen, nicht als Finding.
