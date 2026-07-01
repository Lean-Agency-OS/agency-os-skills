---
name: agency-os-start
version: 1.1.0
description: "Morgen-/Start-Briefing für den User. Verwende diesen Skill IMMER wenn der User 'guten morgen', 'morgen', 'start', 'gm', 'los gehts', 'was steht an', 'starten wir', 'lass uns starten', 'good morning' oder ähnliche Begrüßungen/Start-Signale sagt."
allowed-tools: Bash(git rev-parse *)
---

# Start-Briefing

**Trigger:** Der User sagt *"guten morgen"*, *"morgen"*, *"start"*, *"gm"*, *"los gehts"*, *"was steht an"*, *"starten wir"*, *"good morning"* oder ruft `/start` auf.

**Output:** Knappes Briefing im Chat plus eine Sektion `## [YYYY-MM-DD] <name>-session | startup` im zentralen `{logs}/YYYY-MM-DD.md` (`<name>` = Vorname-Slug des Users, z.B. `max`).

Der User will in 30 Sekunden wissen was los ist. Keine Wand.

---

## Bash-Regeln (Prompt-Vermeidung)

Damit dieser Skill ohne Permission-Rückfragen läuft, beim Bauen von Befehlen:
- **Lesen** (Dateien, Verzeichnis-Listen, Suche) mit den Tools `Read`, `Glob`, `Grep` statt `cat`/`ls`/`grep` in Bash.
- **Keine Command-Substitution** `$(...)` und keine Backticks in Bash. Zähl-/Filter-Ausgaben direkt per Pipe ausgeben (z.B. `… | wc -l` als eigene Zeile), nicht in einen `echo`-String verschachteln.
- **Keine Interpreter** (`python3`/`node`/`perl`/`awk`) für Ad-hoc-Logik; JSON mit `jq` lesen. Mitgelieferte Skripte dieses Skills sind ausgenommen.
- Dieser Skill macht **keine** Git-Schreib-/Sync-Operationen selbst (kein `git pull`/`commit`/`push`). Das Holen des neuesten Stands (Schritt 1) wird **immer** an `/agency-os-github` delegiert. Erlaubt sind nur read-only Checks (`git rev-parse` für den Repo-Test, `git status/log/diff`, `jq`). `mv`/`rm` bleiben bestätigungspflichtig.

## Pfade & Fundament

Die `{...}`-Platzhalter unten (`{strategy}/`, `{logs}/`, `{knowledge}/` …) sind **Rollen** aus `.agency-os/architecture.md`, keine festen Ordnernamen - Brains variieren (z.B. `08-knowledge/` statt `08-wiki/` als `{knowledge}`, oder ein Ordner fehlt). Auflösung pro Rolle: (1) wenn `.agency-os/architecture.md` die Rolle nennt → diesen Pfad; (2) sonst per Rolle/Muster suchen, Standard-Ordnername zuerst; (3) nichts gefunden → Schritt überspringen. Details + Default-Tabelle: [`references/architecture.md`](references/architecture.md).

**Map automatisch pflegen (einmal pro Start, vor den Schritten):** Top-Level-Struktur des Brains scannen und gegen `.agency-os/architecture.md` abgleichen:
- Map fehlt → aus der erkannten Struktur neu schreiben.
- Map zeigt auf Ordner, die es nicht mehr gibt, oder ein neuer rollen-relevanter Ordner ist dazugekommen (Drift) → betroffene Zeilen aktualisieren.
- Map stimmt → nichts tun.

Das Schreiben ist Infrastruktur (wie `.agency-os/state.md` beim github-Skill), kein Brain-Content: ohne Rückfrage schreiben, nur in einer Zeile melden was sich geändert hat (oder still lassen, wenn nichts).

---

## Workflow

### 1. Neuesten Stand holen (delegiert, nur wenn Git-Repo)

Hole die neuesten Änderungen (eine Automatisierung, z.B. n8n, könnte über Nacht Brain-Ingest-Files committed haben).

- **Erst prüfen, ob der Arbeitsordner ein Git-Repo ist** (read-only, z.B. `git rev-parse --is-inside-work-tree`). Ist es **kein** Repo (oder kein Remote), überspringe diesen Schritt komplett.
- Ist es ein Repo: den Pull **nicht selbst** ausführen. **Immer** an `/agency-os-github` delegieren - der holt den neuesten Stand (Pull mit Rebase) und löst Konflikte / divergente Remote. Dieser Skill führt selbst kein `git pull` aus.

### 1b. Plugin-Updates prüfen (still, einmal pro Start)

Führe kurz den Update-Check durch (Skill `/agency-os-update`): installierte Plugin-Versionen vs. neuester Marketplace-Stand. Nur das Ergebnis merken, **nicht** die vollen Details/Update-Befehle hier ausgeben.

- **Alles aktuell** → still, keine Zeile im Briefing.
- **Rückstand** → im Briefing genau eine `**Updates:**`-Zeile (welche Plugins, ein Hinweis „Details/Schritte: `/agency-os-update`"). Nicht selbst aktualisieren.

Netz/CLI nicht verfügbar oder Check schlägt fehl → still überspringen, Briefing nicht blockieren.

### 2. Neue Files in der Inbox prüfen

Checke `{inbox}/` auf neue Brain-Ingest-Files oder Spoke-Einträge. Wenn ja: kurz melden was da ist (nicht ingesten, nur melden, das ist Job des `/ingest`-Skills).

### 3. Arbeitsspeicher (hot.md) lesen

Lies `{working-memory}`, das ist der Arbeitsspeicher. Fasse Current Focus und Active Threads in 2-3 Sätzen zusammen. Wenn die Datei (noch) nicht existiert, überspringe den Punkt.

### 4. Open Loops prüfen

Lies `{open-loops}`. Wenn die Datei (noch) nicht existiert, überspringe den Punkt. Sonst melde:
- **Loops älter als 2 Wochen** (Aging-Check, sichtbar machen)
- **Neue offene Entscheidungen** mit Marker `[?]`
- **Erledigte** mit `[x]` die noch nicht ins Log verschoben wurden

### 5. Daily Log heute prüfen

Prüfe `{logs}/` auf eine Datei mit dem heutigen Datum (`YYYY-MM-DD.md`). Wenn keine existiert, lege sie an mit dem Header `# YYYY-MM-DD` und ergänze später beim Briefing-Ende eine Sektion `## [YYYY-MM-DD] <name>-session | startup`.

### 6. Tasks checken

Ermittle die Task-Quelle des Users in dieser Reihenfolge und nutze die erste, die greift:

1. **Konfiguration:** Falls in `{context}/` ein Setup-File das Task-Tool und/oder einen Board-Link festlegt, nutze diese Angabe.
2. **Gecachter Export:** Prüfe `{context}/` auf einen Tasks-Export, z.B. `notion-tasks.json`, `clickup-tasks.json`, `asana-tasks.json` (von n8n o.ä. geschrieben). Nimm den, falls vorhanden.
3. **Verbundenes MCP:** Sonst frage das verbundene Task-Management-MCP direkt ab, je nachdem was der User hat (ClickUp, Notion, Asana, Airtable, ...). Wenn mehrere verbunden sind, bevorzuge das in der Konfiguration genannte, sonst das offensichtlich aktiv genutzte.

**Tasks anzeigen (egal aus welcher Quelle):**
- Zuerst High-Prio Tasks
- Dann fällige/überfällige Tasks (Datum kleiner-gleich heute)
- Gruppiert nach Status: In Arbeit, Nächste, Wartet
- Maximal 10 Tasks zeigen
- Bei einem Export: zeige wie alt er ist (`updated_at`)

**Wenn keine Task-Quelle verfügbar (Fallback):**
- Melde: *"Kein Task-Tool eingerichtet oder verbunden."*
- Falls in der Konfiguration ein Board-Link hinterlegt ist, gib ihn aus.
- Hinweis, wie man es einrichtet: Task-MCP verbinden (ClickUp, Notion, ...) oder einen Tasks-Export nach `{context}/` schreiben lassen.

### 7. Kalender checken

Ermittle die Kalender-Quelle in dieser Reihenfolge:

1. **Gecachter Export:** Prüfe `{context}/calendar-today.json` (z.B. n8n-Export heutiger + morgiger Termine). Nimm den, falls vorhanden.
2. **Verbundenes MCP:** Sonst frage das verbundene Kalender-MCP für heute + morgen ab (z.B. Google Calendar `list_events`).
3. **Sonst:** überspringe den Kalender-Teil.

**Anzeige:**
- Heutige Termine chronologisch mit Uhrzeit und Typ
- Wiederkehrend wichtige Termin-Typen markieren (z.B. Calls/Meetings, die danach ausgewertet werden)
- Morgen als kurzen Ausblick (1-2 Zeilen)
- Optional eine Wochen-Summary als Zähler nach Termin-Typ (z.B. *"Diese Woche: 4 Calls, 1 Workshop, 1 Sales"*)
- Bei einem Export: zeige wie alt er ist

### 8. Rollen-/Persona-Status (optional)

**Nur relevant, wenn der User mit Rollen/Personas arbeitet** (eine Org-Struktur im Brain, z.B. ein `{roles}/`-Ordner mit einem Unterordner pro Rolle). Existiert keine solche Struktur, **überspringe diesen Schritt komplett** und gib keine Rollen-Zeile im Briefing aus.

Wenn eine Rollen-Struktur existiert, ermittle die Rollen **dynamisch** (Unterordner der Org-Struktur, nicht hardcoden) und prüfe, ob seit der letzten Session eine aktiv war. Zwei Signale:

1. **Persona-Session-Header in den letzten `{logs}/`-Files**: grep in den letzten 3-5 Tages-Logs nach fremden Session-Headern (Muster `<rolle>-session`), die nicht die eigene Session sind.
2. **mtime-Check der Rollen-Files**: den Org-Ordner jeder Rolle auf neue/geänderte Files (z.B. `role.md`, `_todos.md`) seit der letzten Session prüfen.

Nur prüfen ob sich was geändert hat, nicht alles lesen. Wenn aktiv: in 1 Zeile pro Rolle zusammenfassen.

### 9. Briefing ausgeben

Ermittle zuerst die Anrede:
- **Name:** aus dem Claude-Account des Users. Nicht hardcoden. Nutze den Vornamen.
- **Begrüßung:** passend zur lokalen Tageszeit, nicht immer "Guten Morgen": vor ~11 Uhr *"Guten Morgen"*, tagsüber *"Guten Tag"* / *"Hallo"*, abends *"Guten Abend"*.

Fasse dann alles in einem knappen Briefing zusammen:

```
{Begrüßung je nach Tageszeit}, {Vorname}.

**Fokus:** {aus {working-memory}}
**Heute:** {Termine + fällige Tasks}
**Tasks:** {High-Prio + fällige aus dem Task-Tool}
**Offen:** {wichtigste Loops, besonders aging}
**Inbox:** {X neue Files in {inbox}/}
**Updates:** {nur falls Plugins veraltet: welche + "Schritte: /agency-os-update", sonst Zeile weglassen}
**Rollen:** {nur falls eine Rollen-Struktur existiert: welche Rolle war aktiv, was hat sie getan, sonst Zeile weglassen}
```

Kurz halten. Kein Essay. Der User will in 30 Sekunden wissen, was los ist.

### 10. Log-Sektion für Startup

Ergänze die Datei `{logs}/YYYY-MM-DD.md` mit einer Sektion:

```markdown
## [YYYY-MM-DD] <name>-session | startup

Briefing ausgegeben. Loops aging: {N}. Neue Inbox-Items: {N}. Aktive Rollen seit letzter Session: {Liste, "keine" oder "n/a" falls keine Rollen-Struktur}.
```

---

## Output

- Knappes Briefing im Chat (Schritt 9).
- Eine Sektion `## [YYYY-MM-DD] <name>-session | startup` in `{logs}/YYYY-MM-DD.md` (Schritt 10; `<name>` = Vorname-Slug des Users).

---

## Edge Cases

- **Daily Log existiert schon (z.B. weil eine Automatisierung früher etwas reingeschrieben hat):** ergänze die Sektion am Ende, nicht überschreiben.
- **User hat heute schon einen Startup gemacht:** kurz darauf hinweisen (*"heute schon gestartet, hier nur Diff"*) statt das volle Briefing nochmal.
- **Mehrere Rollen waren aktiv:** Kurzfassung pro Rolle, nicht alle Tagebuch-Inhalte zitieren.
- **Task- oder Kalender-Quelle fehlt:** Briefing nicht blockieren, Fallback nutzen (verbundenes MCP) oder Sektion auslassen.
