---
name: agency-os-ingest
version: 1.0.0
description: Rohquelle aus dem Inbox-Ordner ins Brain einarbeiten. Verwende wenn der User "arbeite das ein", "ingeste das", "neues Transkript", "hier ist was Neues", "einarbeiten" oder ähnliches sagt, oder auf eine bestimmte Datei im Inbox-Ordner zeigt. Aktualisiert die betroffenen Brain-Files (Klienten, Projekte, IP, etc.), schreibt einen Log-Eintrag und zieht offene Loops nach. Rohquelle wird nach vollständiger Verarbeitung gelöscht.
---

# Ingest

Arbeitet eine Rohquelle aus dem Inbox-Ordner tief ins Brain ein. Substanz, nicht Volumen.

> **Brain-Pfade:** Keine festen Ordnernamen. Die Platzhalter unten (`{inbox}`, `{clients}`, `{projects}`, `{sales}`, `{marketing}`, `{ip}`, `{strategy}`, `{open-loops}`, `{working-memory}`, `{roles}`, `{logs}`) stehen für die Rollen aus `.agency-os/architecture.md` (`agency-os-start` pflegt die Map); fehlt eine, gilt der Standard-Name bzw. per Muster suchen, sonst Schritt überspringen. Default-Tabelle: `agency-os-start/references/architecture.md`. Root-Navigation: `OS.md` (ersatzweise `README.md` / Root-`_index.md`).

**Abgrenzung zu `file-to-markdown`:** `file-to-markdown` konvertiert externe Files (PDF, DOCX, etc.) in den Inbox-Ordner und stoppt dort. `ingest` nimmt Markdown-Files aus dem Inbox-Ordner und arbeitet sie ins Brain ein. Beide laufen nicht automatisch hintereinander.

---

## Workflow

### 1. Rohquelle komplett lesen

- Die referenzierte Datei im Inbox-Ordner komplett einlesen, nicht nur überfliegen.
- Wenn mehrere zusammengehörende Files: alle.

### 2. Kurze Rückmeldung an den User

Bevor irgendwas geschrieben wird, melde dich:
- **Was ist das?** (Call-Transkript, Spoke-Shutdown-File, eigene Note des Users, externes Dokument)
- **Wer ist beteiligt?** (User + Klient, nur User, eine Rolle, externe Quelle)
- **Drei wichtigste Punkte** (kurze Bullets, keine Wand)

Frag dann: *"Willst du was hervorheben, bevor ich einarbeite?"*

Erst wenn der User geantwortet hat, geht's los.

### 3. Betroffene Brain-Files identifizieren

Routing-Tabelle (Default-Pfade, laut Disclaimer oben auflösen):

| Was | Wohin |
|---|---|
| Klient-Update | `{clients}/{name}.md` updaten oder anlegen |
| Projekt-Update | `{projects}/{name}.md` |
| Sales-Lead, Discovery-Call | `{sales}/{name}.md` (Pre-Sale) oder `{clients}/` (Post-Sale) |
| Marketing-Idee | `{marketing}/content/ideen.md` oder eigene Note |
| Methode/Framework | `{ip}/{name}.md` oder `{ip}/frameworks/` |
| Wiederkehrendes Pattern | `{ip}/patterns/` + Notiz im Kunden-Dossier |
| Strategie-Entscheidung des Users | `{strategy}/` oder Eintrag in `{open-loops}` |
| Rollen-Material aus altem Spoke (falls Rollen-Struktur existiert) | Persona-Arbeitsspeicher in `{roles}/{rolle}/role.md`, Tasks in `_todos.md`, Wetten in `_wetten.md` |
| Unsortierter Gedanken-Fetzen | `{inbox}/capture.md` |

### 4. Updates ausführen

Ein Ingest darf problemlos 5-15 Files berühren. Pro File:
- Substanz hinzufügen, nicht copy-paste der Rohquelle
- Cross-Links setzen (jede neue Note verlinkt mindestens eine andere)
- Atomare-Notes-Prinzip: eine Idee = eine Note, unter ~30 Zeilen

### 5. Log-Eintrag

Sektion ins zentrale Tageslog (`{logs}/YYYY-MM-DD.md`) anhängen:

```markdown
## [YYYY-MM-DD] ingest | {Kurztitel}

Quelle: `{inbox}/{filename}.md`

**Was eingearbeitet:**
- {Brain-File 1}: {was geändert}
- {Brain-File 2}: {was geändert}

**Substanz:**
- 2-3 Zeilen Zusammenfassung der wichtigsten Take-Aways

**Beobachtungen:**
- 1-2 Muster oder Auffälligkeiten (optional)
```

Wenn das Log-File noch nicht existiert: anlegen mit `# YYYY-MM-DD` als erste Zeile, dann Sektion einfügen.

### 6. Index aktualisieren (wenn neue Notes entstanden)

Den passenden Ordner-`_index.md` aktualisieren (z.B. `{ip}/_index.md` für IP-Notes). Die Root-Navigation liegt in `OS.md`.

### 7. Strategie-Arbeitsspeicher frisch halten

Falls das Brain einen Arbeitsspeicher-Hub führt (`{working-memory}`, z.B. `02-strategy/hot.md`), nach jedem Ingest prüfen:
- **Active Threads:** neuer Thread entstanden? Stale Thread weg?
- **Key Numbers:** neue Zahl im Ingest? Alte Zahl überholt?
- **Recent:** 3-5 Stichworte aktualisieren

### 8. Loops nachziehen

Wenn der Ingest neue offene Punkte aufwirft: `{open-loops}` Eintrag mit heutigem Datum und passendem Marker (`[ ]` Task, `[?]` offene Entscheidung). Schließt der Ingest einen bestehenden Loop: `[x]` markieren (wandert beim nächsten Review ins Log).

### 9. Rohquelle löschen

Nach vollständiger Verarbeitung wird die Datei im Inbox-Ordner **gelöscht** (nicht archiviert). "Vollständig verarbeitet" heißt:
- Fakten im Brain
- Loops in `{open-loops}`
- Ingest-Eintrag im Tageslog
- Noch unsortierte Substanz in `{inbox}/capture.md` abgelegt

Die Rohquelle lebt danach in der Git-History des sendenden Systems weiter.

### 10. Rückmeldung an den User

Knapp:
- *"Eingearbeitet. {X} Files updated: {Liste}."*
- *"Fällt mir auf: {1-2 Beobachtungen}."*

Beobachtungen sind der Mehrwert. Das ist der Grund, warum der User den Skill einsetzt und nicht nur die Datei selbst kopiert.

---

## Edge Cases

- **Rohquelle ist ein Spoke-Shutdown-File:** Behandlung wie regulärer Ingest, aber Logs/Tagebuch-Updates der Rolle gehen direkt in `{roles}/{rolle}/`, nicht ins Brain-Wiki.
- **Der User korrigiert im Ingest eine frühere Aussage:** alte Brain-Note explizit korrigieren (nicht nur eine neue daneben). Im Review-Block der Note vermerken, was korrigiert wurde und warum.
- **Ingest enthält eine Korrektur/Präferenz zur Arbeitsweise:** sofort an den passenden Enforcement-Ort schreiben (Feedback-Routing des `agency-os-shutdown`-Skills), nicht erst beim Shutdown sammeln.
- **Ingest ist zu groß für eine Session:** User kurz informieren und vorschlagen, nur den ersten Teil zu machen. Den Rest in `{open-loops}` als offenen Ingest tracken.

---

## Was NICHT passiert

- **Kein Copy-Paste der Rohquelle ins Brain.** Substanz, nicht Volumen.
- **Keine destruktiven Edits ohne Rückfrage.** Wenn ein Ingest eine bestehende Note widerlegt: User fragen.
- **Kein Auslassen des Logs.** Jeder Ingest hinterlässt einen Log-Eintrag, sonst wird die Brain-Aktivität intransparent.
- **Kein Löschen von Inbox-Files, bevor alle anderen Schritte fertig sind.** Erst wenn alles drin ist, dann löschen.
