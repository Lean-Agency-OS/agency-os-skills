---
name: agency-os-capture
version: 2.0.0
description: Schnelle Ersterfassung von Gedanken, Tasks, Ideen, Open Loops oder Entscheidungen ins Brain. Verwende wenn der User "capture", "notiere", "merken", "halt fest", "schreib das auf", "festhalten", "muss ich mir merken", "neue Idee", "Quick Note" oder ähnliche Erfassungs-Signale nutzt.
---

# Agency OS - Capture

Schnelle Ersterfassung. Nicht tief verarbeiten (das ist Job von `/ingest`). Schnell rein, richtig einsortiert.

## Schritte

### 1. Inhalt prüfen

Falls kein Inhalt mitgegeben: frage "Was willst du festhalten?"

### 2. Kategorisieren

Kategorisiere automatisch nach `references/capture-routing.md`:

- **TASK** - konkrete Aktion mit klarem Ergebnis
- **IDEE** - vage, braucht Reifung, kein direkter Schritt
- **LOOP** - wartet auf jemanden oder etwas externes
- **ENTSCHEIDUNG** - Optionen vorhanden, muss geklaert werden
- **QUICK NOTE** - Fakt, Zahl, Beobachtung, Kontext-Snippet

### 3. Eintrag schreiben

Schreibe in die passende Zieldatei (Mapping in `references/capture-routing.md`). Regeln:

- Append-only, niemals ueberschreiben
- Datum immer mitschiessen: `[YYYY-MM-DD]`
- Cross-Links setzen wenn ein Klient, Projekt oder eine Rolle klar ist
- Relative Zeitangaben in absolute umwandeln ("Donnerstag" → konkretes Datum)

**_index.md-Pflege:** Falls ein neues File in `00-inbox/` entsteht oder ein neuer Unterordner in einem Top-Level-Ordner angelegt wird, Markdown-Link in der passenden `_index.md` erganzen. Erste Zeile `_(noch leer)_` dabei entfernen.

### 4. Routing-Hinweis geben

Nach dem Schreiben: kurzer Hinweis an Markus wohin das Item beim naechsten Ingest weiterwandert:

```
Gespeichert in `{dateiname}` als [Kategorie].
Naechster Schritt: {wohin das beim Ingest geht - z.B. "05-clients/Klaus/" oder "02-strategy/open-loops.md"}
Noch was?
```

### 5. Loop bis Markus fertig ist

---

## Abgrenzung

| Capture | Ingest |
|---|---|
| Schnell rein, Rohzustand ok | Tiefe Verarbeitung, Cross-Links, Atomare Notes |
| `02-strategy/open-loops.md` / `00-inbox/capture.md` als Zwischenspeicher | Brain-Files direkt updaten |
| Kein Markus-Ping vorher | Markus bestaetigt bevor losgeschrieben wird |
| Sekunden, nicht Minuten | Darf 5-15 Files beruehren |

Capture legt das Item in die Inbox. Ingest arbeitet es ein.

---

Detail-Logik (Erkennungsregeln, Prioritaeten, Zieldatei-Mapping) → `references/capture-routing.md`
