---
name: agency-os-shutdown
version: 1.0.0
description: "Session-Shutdown und Daily Log. Verwende diesen Skill IMMER wenn der User 'gute nacht', 'shutdown', 'fertig für heute', 'session ende', 'bis morgen', 'schluss für heute', 'feierabend', 'mach zu', 'good night', 'eod' oder ähnliche Abschluss-Signale sagt."
---

# Shutdown

**Trigger:** Der User sagt *"gute nacht"*, *"shutdown"*, *"fertig für heute"*, *"session ende"*, *"bis morgen"*, *"schluss für heute"*, *"feierabend"*, *"mach zu"*, *"good night"*, *"eod"* oder ruft `/shutdown` auf.

**Output:** Brain-Updates (`{open-loops}`, `{working-memory}`, Daily Log) + Commit + Push + knappe Abschluss-Meldung im Chat.

---

## Pfade & Fundament

Die `{...}`-Platzhalter unten (`{strategy}/`, `{logs}/` …) sind **Rollen** aus `.agency-os/architecture.md`, keine festen Ordnernamen - Brains variieren (z.B. `08-knowledge/` statt `08-wiki/` als `{knowledge}`, oder ein Ordner fehlt). Auflösung pro Rolle: (1) wenn `.agency-os/architecture.md` die Rolle nennt → diesen Pfad; (2) sonst per Rolle/Muster suchen, Standard-Ordnername zuerst; (3) nichts gefunden → Schritt überspringen. Default-Tabelle: `agency-os-start/references/architecture.md`.

---

## Workflow

### 1. Faktenlage ziehen

```bash
git log --since=midnight --oneline
git status --short
```

Erste Liste = heutige Commits (was bereits versioniert ist). Zweite = uncommitted (was im Shutdown-Commit landet). Damit hat der Shutdown die volle Tagesbilanz ohne Raten oder Nachfrage-Ping-Pong.

Optional Reflexions-Frage an den User: *"Was war heute schwer, was ein Quick-Win?"* - qualitativ, nicht faktisch.

### 2. Open Loops updaten

`{open-loops}`:
- **Neue Einträge** mit heutigem Datum `[YYYY-MM-DD]` und Marker (`[ ]` Task, `[?]` Entscheidung)
- **Erledigte** ins Log überführt und aus `{open-loops}` löschen.

### 3. Arbeitsspeicher (hot.md) aktualisieren

`{working-memory}`, wenn sich der aktive Kontext verschoben hat:
- **Current Focus** updaten
- **Active Threads** aktualisieren (Threads, die heute neu entstanden oder weitergegangen sind)
- **Key Numbers** wenn neue Zahlen aufgetaucht sind
- **Recent** mit der heutigen Session ergänzen (3-5 Stichworte zur Tagesleistung)

In `{working-memory}` dürfen die Einträge maximal 7 Tage alt sein. Alles was älter ist, muss gelöscht werden.

**WICHTIG:** Keine Open Loops in `{working-memory}`, die gehören in `{open-loops}`. `{working-memory}` ist Arbeitsspeicher, nicht Persistenz.

### 4. Korrekturen-Check

Sicherheitsnetz: Falls heute eine Korrektur/Präferenz kam, die noch nicht an ihrem Enforcement-Ort steht (Reflex aus OS.md/CLAUDE.md sollte das schon erledigt haben) — jetzt dorthin schreiben. Routing-Tabelle: `feedback.md`. **Nicht** in `feedback.md` selbst eintragen (das ist nur noch die Anleitung, kein Log).

### 5. Daily Log vervollständigen

`{logs}/YYYY-MM-DD.md` wird **permanent über den Tag** beschrieben (Morning-Startup, Persona-Sessions, Ingests, Reviews schreiben jeweils ihre eigenen Sektionen). Beim Shutdown:

**Default (Log existiert bereits):** Sektionen durchgehen, Lücken ergänzen, dann eine abschließende Bilanz-Sektion anhängen mit dem was die Tages-Sektionen nicht abdecken:

```markdown
## [YYYY-MM-DD] <name>-session | shutdown

**Bilanz:**
- 1-2 Zeilen Take-Aways des Tages

**Loops:** Neu: {N}, Erledigt: {N}

**Beobachtungen:**
- 1-2 Muster oder Auffälligkeiten (optional, nur wenn substanziell)
```

**Edge (Log existiert nicht):** Anlegen mit `# YYYY-MM-DD` als erste Zeile, dann die Shutdown-Sektion einfügen.

### 6. Tasks updaten

Falls in der Session Tasks erledigt oder neue angelegt wurden, im Task-Tool des Users nachziehen (gleiche Quelle wie im Start-Skill: Konfig → verbundenes Task-MCP, je nachdem was der User hat: ClickUp, Notion, Asana, ...):
- **Erledigte** auf "Abgeschlossen" setzen
- **Neue Tasks** anlegen wenn nötig
- Wenn kein Task-MCP verfügbar: dem User den Board-Link (falls konfiguriert) geben und ihn manuell setzen lassen

### 7. Commit + Push

Der Shutdown-Trigger IST die Anweisung zu committen und zu pushen. Keine "soll ich?"-Frage.

```bash
git add -A
git status --short
```

Commit-Message-Stil (lowercase, knapp, ":"-getrennt):

```
shutdown YYYY-MM-DD: {1-3 stichworte was substanziell war}

{1-3 Zeilen was passiert ist}

Co-Authored-By: Claude {model} <noreply@anthropic.com>
```

Dann push:

```bash
git push
```

Bei Pre-commit-Hook-Fehler: investigieren, fixen, neu committen. Niemals `--no-verify` ohne explizite Anweisung des Users.

### 8. Abschluss-Meldung

Knappe Schlussmeldung im Chat:

```
Session gesichert.
{X} Loops updated, {Y} neue Einträge.
{nur falls eine Rollen-Struktur existiert: Aktive Rollen heute: Liste, sonst Zeile weglassen}
Commit {hash} gepusht.
Bis zum nächsten Mal.
```

---

## Output

- Brain-Updates: `{open-loops}`, `{working-memory}`, Daily Log `{logs}/YYYY-MM-DD.md` (Sektion `## [YYYY-MM-DD] <name>-session | shutdown`).
- Commit + Push (Schritt 7) plus knappe Abschluss-Meldung im Chat (Schritt 8).

---

## Edge Cases

- **User shutdownt mehrmals am Tag:** Erste Shutdown-Sektion bleibt, nächste wird als zusätzlicher `<name>-session | shutdown` Eintrag angehängt. Pro Shutdown ein Commit.
- **Während der Session keine Brain-Änderungen, nur Sparring:** Trotzdem Bilanz-Eintrag mit Sparring-Thema und Beobachtung. Wenn `git status` clean ist und kein neuer Log-Eintrag nötig: Shutdown ohne Commit, nur Abschluss-Meldung.
- **Pre-commit-Hook schlägt fehl:** Investigieren, nicht überspringen. Fixen, neu committen.
- **Aging-Loops älter als 4 Wochen:** beim Shutdown explizit ansprechen (*"Loop X hängt seit {N} Wochen, noch aktuell?"*).
- **Push schlägt fehl (z.B. divergente Remote):** Pull mit Rebase, neu pushen. Bei Konflikt: den User fragen, nicht autonom mergen.

---

## Was NICHT passiert

- **Kein Force-Push auf main.**
- **Kein --no-verify** ohne explizite Zustimmung des Users.
- **Keine destruktiven Operationen** (Files löschen etc.) ohne explizite Bestätigung des Users.
- **Kein Beschönigen.** Wenn der Tag dünn war, das auch so im Log benennen.
- **Kein Überspringen** des Daily Logs, auch wenn die Session kurz war.
