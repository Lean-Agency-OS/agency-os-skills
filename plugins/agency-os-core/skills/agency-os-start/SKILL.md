---
name: agency-os-start
description: "Morgen-Briefing für Markus. Verwende diesen Skill IMMER wenn der User 'guten morgen', 'morgen', 'start', 'gm', 'los gehts', 'was steht an', 'starten wir', 'lass uns starten', 'good morning' oder ähnliche Begrüßungen/Start-Signale sagt."
---

# Morgen-Briefing

**Trigger:** Markus sagt *"guten morgen"*, *"morgen"*, *"start"*, *"gm"*, *"los gehts"*, *"was steht an"*, *"starten wir"*, *"good morning"* oder ruft `/start` auf.

**Output:** Knappes Morgen-Briefing im Chat plus eine Sektion `## [YYYY-MM-DD] markus-session | startup` im zentralen `10-logs/YYYY-MM-DD.md`.

Markus will in 30 Sekunden wissen was los ist. Keine Wand.

---

## Workflow

### 1. Git Pull

Hole die neuesten Änderungen, n8n könnte über Nacht Brain-Ingest-Files committed haben.

```bash
cd "/Users/markus.vieghofer/Documents/Claude Workspace/Marcus" && git pull
```

### 2. Neue Files in 00-inbox/ prüfen

Checke `00-inbox/` auf neue Brain-Ingest-Files oder Spoke-Einträge. Wenn ja: kurz melden was da ist (nicht ingesten, nur melden, das ist Job des `/ingest`-Skills).

### 3. 02-strategy/hot.md lesen

Lies `02-strategy/hot.md`, das ist der Arbeitsspeicher. Fasse Current Focus und Active Threads in 2-3 Sätzen zusammen.

### 4. 02-strategy/open-loops.md prüfen

Lies `02-strategy/open-loops.md`. Melde:
- **Loops älter als 2 Wochen** (Aging-Check, sichtbar machen)
- **Neue offene Entscheidungen** mit Marker `[?]`
- **Erledigte** mit `[x]` die noch nicht ins Log verschoben wurden

### 5. Daily Log heute prüfen

Prüfe `10-logs/` auf eine Datei mit dem heutigen Datum (`YYYY-MM-DD.md`). Wenn keine existiert, lege sie an mit dem Header `# YYYY-MM-DD` und ergänze später beim Briefing-Ende eine Sektion `## [YYYY-MM-DD] markus-session | startup`.

### 6. Notion Tasks checken

Lies `01-context/notion-tasks.json`, das ist der n8n-Export der aktiven Notion Tasks.

**Wenn die Datei existiert:**
- Zuerst High-Prio Tasks
- Dann fällige/überfällige Tasks (Datum kleiner-gleich heute)
- Gruppiert nach Status: In Arbeit, Nächste, Wartet
- Maximal 10 Tasks zeigen
- Zeige wie alt der Export ist (`updated_at`)

**Wenn die Datei NICHT existiert (Fallback):**
- Melde: *"Notion-Tasks-Export noch nicht eingerichtet. Hier ist dein Board:"*
- Gib den Link aus: https://www.notion.so/markusvieghofer/2e5b779bc24980db94ccced1341e3f42?v=2e5b779bc24981ba9386000c761cd4b7

### 7. Kalender checken

Lies `01-context/calendar-today.json`, das ist der n8n-Export der heutigen + morgigen Termine.

**Wenn die Datei existiert:**
- Heutige Termine chronologisch mit Uhrzeit und Typ
- Coaching-Calls markieren (Fathom extrahiert danach automatisch)
- Morgen als kurzen Ausblick (1-2 Zeilen)
- Wochensummary als Zähler (z.B. *"Diese Woche: 4 Coaching, 1 Workshop, 1 Sales"*)
- Zeige wie alt der Export ist

**Wenn die Datei NICHT existiert (Fallback):**
- Melde: *"Kalender-Export noch nicht eingerichtet."*
- Versuche Google Calendar MCP (`gcal_list_events`) für heute abzufragen
- Wenn auch das nicht geht: überspringe den Kalender-Teil

### 8. Rollen-Status (Brain-organisation)

Checke ob seit der letzten Markus-Session eine Rolle aktiv war. Zwei Signale:

1. **Persona-Session-Header in den letzten `10-logs/`-Files**: grep nach `kai-session`, `mara-session`, `viktor-session`, `linus-session`, `nora-session`, `ip-architect-session` in den letzten 3-5 Tages-Logs.
2. **mtime-Check der Rollen-Files**: `07-org/{rolle}/` auf neue/geänderte `role.md`, `_todos.md`, `_wetten.md` seit letzter Session.

Rollen: Kai/CEO · Mara/CMO · Viktor/CSO · Linus/CTO · Nora/Head of Coaching · IP-Architect.

Nur prüfen ob sich was geändert hat, nicht alles lesen. Wenn aktiv: in 1 Zeile zusammenfassen pro Rolle.

### 9. Briefing ausgeben

Fasse alles in einem knappen Morgen-Briefing zusammen:

```
Guten Morgen, Markus.

**Fokus:** {aus 02-strategy/hot.md}
**Heute:** {Termine + fällige Tasks}
**Tasks:** {High-Prio + fällige aus notion-tasks.json}
**Offen:** {wichtigste Loops, besonders aging}
**Inbox:** {X neue Files in 00-inbox/}
**Rollen:** {welche Rolle war aktiv, was hat sie getan}
```

Kurz halten. Kein Essay. Markus will in 30 Sekunden wissen, was los ist.

### 10. Log-Sektion für Startup

Ergänze die Datei `10-logs/YYYY-MM-DD.md` mit einer Sektion:

```markdown
## [YYYY-MM-DD] markus-session | startup

Briefing ausgegeben. Loops aging: {N}. Neue Inbox-Items: {N}. Aktive Rollen seit letzter Session: {Liste oder "keine"}.
```

---

## Edge Cases

- **Daily Log existiert schon (z.B. weil n8n früher etwas reingeschrieben hat):** ergänze die Sektion am Ende, nicht überschreiben.
- **Markus hat heute schon einen Startup gemacht:** kurz darauf hinweisen (*"heute schon gestartet, hier nur Diff"*) statt das volle Briefing nochmal.
- **Mehrere Rollen waren aktiv:** Kurzfassung pro Rolle, nicht alle Tagebuch-Inhalte zitieren.
- **Notion- oder Calendar-Export fehlt:** Briefing nicht blockieren, Fallback nutzen oder Sektion auslassen.
