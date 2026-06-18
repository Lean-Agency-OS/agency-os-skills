---
name: agency-os-lint
version: 1.0.0
description: Brain-Hygiene-Check. Verwende wenn der User "lint", "räum auf", "check brain", "wie geht's dem Wiki", "wiki-check" oder ähnliches sagt. Findet broken Links, Orphan-Pages, veraltete/widersprüchliche Claims und stale Projekt-Hubs. Liefert nur einen Befund-Report mit Empfehlungen, macht NICHTS autonom destruktives.
---

# Lint (Brain-Hygiene)

**Output:** Ein Befund-Report im Chat (keine eigene Datei). Der User entscheidet pro Punkt, was angepackt wird.

**Kritisch:** keine destruktiven Änderungen autonom. Keine Mass-Renames. Der User genehmigt jeden Fix einzeln.

## Bash-Regeln (Prompt-Vermeidung)

Damit dieser Skill ohne Permission-Rückfragen läuft, beim Bauen von Befehlen:
- **Lesen** (Dateien, Verzeichnis-Listen, Suche) mit den Tools `Read`, `Glob`, `Grep` statt `cat`/`ls`/`grep` in Bash.
- **Keine Command-Substitution** `$(...)` und keine Backticks in Bash. Zähl-/Filter-Ausgaben direkt per Pipe ausgeben (z.B. `… | wc -l` als eigene Zeile), nicht in einen `echo`-String verschachteln.
- **Keine Interpreter** (`python3`/`node`/`perl`/`awk`) für Ad-hoc-Logik; JSON mit `jq` lesen. Die mitgelieferten Lint-Skripte (`resources/*.py`) sind ausgenommen und werden bewusst per `python3` aufgerufen.
- Mutierende Bash-Befehle (`mv`, `rm`) bleiben bestätigungspflichtig — keine autonomen Umbenennungen/Löschungen. Dieser Skill sichert nichts auf Git (das macht `/agency-os-github`).

## Pfade & Fundament

> **Brain-Pfade:** Keine festen Ordnernamen. Die Skripte tragen keine Pfad-Logik mehr — **du** löst die Ordner in Schritt 1 auf (LLM) und reichst sie als Config `.agency-os/lint-config.json` rein. Fehlt die Config, greifen die Standard-Namen. `.git`/`node_modules` werden immer übersprungen. Die Skripte scannen das Arbeitsverzeichnis (Brain-Root) als Wurzel und lesen die Config von dort automatisch.

**Aufruf der Skripte:** vom Brain-Root aus. Abkürzung unten: `LINT="${CLAUDE_PLUGIN_ROOT:-.}/skills/agency-os-lint"`. Die Skripte nehmen das aktuelle Verzeichnis als Brain-Root und `.agency-os/lint-config.json` als Config; beides lässt sich optional via Argument bzw. `--config` überschreiben.

## Workflow

### 1. Architektur auflösen + Lint-Config bauen

Die Skripte sind bewusst „dumm" und kennen keine Ordnernamen. Du löst die Struktur einmal auf und legst sie ab:

- **architecture.md abgleichen.** `.agency-os/architecture.md` gegen die echte Top-Level-Struktur prüfen (normalerweise pflegt der `agency-os-start`-Skill sie). Bei Drift - Ordner umbenannt/neu/entfernt - die betroffenen Zeilen aktualisieren; fehlt die Datei, aus der erkannten Struktur neu schreiben. Ohne Rückfrage (Infrastruktur), im Report eine Zeile vermerken.
- **Lint-Config schreiben.** Aus den aufgelösten Rollen **und der echten Struktur** mit dem `Write`-Tool `.agency-os/lint-config.json` erzeugen:

   ```json
   {
     "skip": ["00-inbox", "11-archive"],
     "content": ["01-context", "02-strategy", "03-marketing", "04-sales", "05-clients", "06-projects", "07-org", "08-wiki", "09-ip"],
     "projects": "06-projects",
     "archive": "11-archive"
   }
   ```

   - `skip` = Ordner, die nie durchsucht werden (inbox + archive).
   - `content` = alle Inhalts-Ordner außer inbox/logs/archive, in denen Orphans zählen. **Wichtig:** Hat der Kunde seinen Context-Layer erweitert und eigene Ordner angelegt (über die Standard-Rollen hinaus), nimm sie hier mit auf — sonst werden Orphans dort übersehen.
   - `projects` / `archive` = die jeweiligen Rollen-Ordner (für den Stale-Check).

   Die Skripte lesen diese Datei selbst aus dem Brain-Root. Fehlt sie, greifen die Standard-Defaults.

### 2. Broken-Links-Check

```bash
python3 "$LINT/resources/lint_broken_links.py"
```

Output: pro Datei eine Sektion mit `L{zeile}: {pfad}` für jeden Treffer, plus Total-Zähler. Excludes: `skip` aus der Lint-Config (inbox + archive) plus `.git/`, `node_modules/` (immer). Inkludiert das Log bewusst (auch dort verrotten Links).

### 3. Orphan-Pages

Notes ohne eingehende Links sind ein Lint-Signal. Atomare Notes leben durch Verknüpfung.

```bash
python3 "$LINT/resources/lint_orphans.py"
```

Scope: die `content`-Ordner aus der Lint-Config (flach + verschachtelt). Das Skript filtert automatisch: `_index.md`, Files jünger als 7 Tage. Outgoing-Links werden über das ganze Brain gesammelt (auch das Log, damit Erwähnungen aus Tageslogs als incoming zählen).

### 4. Stale Projekt-Hubs + veraltete Claims

```bash
python3 "$LINT/resources/lint_stale_projekte.py"
```

Status-Frontmatter-Check für Projekt-Hubs im `{projects}`-Ordner. Drei Klassen:
- **closed-in-projekte:** Hub hat Status `closed`/`done`/`archived` (oder `closed-YYYY-MM-DD`-Pattern) und liegt noch in `{projects}` statt `{archive}/projekte/`. Verschieben.
- **stale-active:** Hub hat lebendigen Status, aber kein Git-Commit in 30+ Tagen. Verdacht: vergessen oder closed-ohne-Update.
- **no-status:** Hub-File hat kein `status:` in der Frontmatter. Konsistenz-Defekt.

Widersprüche und veraltete inhaltliche Claims, die kein Skript abdeckt, beim Lesen der betroffenen Files mitnehmen und im Report unter "Widersprüche / veraltete Claims" aufführen.

### 5. Befund-Report formatieren

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

### 6. Mit dem User durchgehen

Pro Punkt: *"Soll ich das fixen, oder ist das beabsichtigt?"*. Mach **nichts** autonom Destruktives. Auch keine Mass-Renames ohne explizite Zustimmung.

### 7. Log-Eintrag

Sektion `## [YYYY-MM-DD] lint` ins zentrale Tageslog (`{logs}/YYYY-MM-DD.md`), mit 1-2 Zeilen über die Anzahl der Findings (inkl. ggf. korrigierter architecture.md).

---

## Output

- Befund-Report im Chat (keine eigene Datei): Broken Links, Orphans, Widersprüche/veraltete Claims, Empfehlungen nach Priorität.
- Log-Eintrag `## [YYYY-MM-DD] lint` in `{logs}/YYYY-MM-DD.md` (Schritt 6). Fixes nur nach Einzel-Genehmigung durch den User, nichts autonom destruktiv.

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
