---
name: agency-os-capture
version: 2.0.0
description: Schnelle Ersterfassung von Gedanken, Tasks, Ideen, Open Loops oder Entscheidungen ins Brain. Verwende wenn der User "capture", "notiere", "merken", "halt fest", "schreib das auf", "festhalten", "muss ich mir merken", "neue Idee", "Quick Note" oder ähnliche Erfassungs-Signale nutzt.
---

# Agency OS - Capture

Schnelle Ersterfassung. Nicht tief verarbeiten (das ist Job von `/ingest`). Schnell rein, richtig einsortiert.

## Pfade & Fundament

> **Brain-Pfade:** Die `{...}`-Platzhalter hier (`{inbox}/`, `{strategy}/` …) sind **Rollen** aus `.agency-os/architecture.md`, keine festen Ordnernamen - Brains variieren. Pro Rolle: (1) wenn `.agency-os/architecture.md` die Rolle nennt → diesen Pfad; (2) sonst per Rolle/Muster suchen, Standard-Ordnername zuerst; (3) nichts gefunden → Schritt überspringen. Default-Tabelle: `agency-os-start/references/architecture.md`.

## Workflow

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

**_index.md-Pflege:** Falls ein neues File in `{inbox}/` entsteht oder ein neuer Unterordner in einem Top-Level-Ordner angelegt wird, Markdown-Link in der passenden `_index.md` erganzen. Erste Zeile `_(noch leer)_` dabei entfernen.

### 4. Routing-Hinweis geben

Nach dem Schreiben: kurzer Hinweis an den User wohin das Item beim naechsten Ingest weiterwandert:

```
Gespeichert in `{dateiname}` als [Kategorie].
Naechster Schritt: {wohin das beim Ingest geht - z.B. "{clients}/{kunde}/" oder "{open-loops}"}
Noch was?
```

### 5. Loop bis der User fertig ist

---

## Output

Eintrag in der passenden Zieldatei (Mapping in `references/capture-routing.md`, z.B. `{open-loops}` oder `{inbox}/capture.md`), append-only mit Datum `[YYYY-MM-DD]`. Plus kurzer Routing-Hinweis im Chat, wohin das Item beim nächsten Ingest weiterwandert.

---

## Verwandte Skills

| Capture | Ingest |
|---|---|
| Schnell rein, Rohzustand ok | Tiefe Verarbeitung, Cross-Links, Atomare Notes |
| `{open-loops}` / `{inbox}/capture.md` als Zwischenspeicher | Brain-Files direkt updaten |
| Kein User-Ping vorher | User bestaetigt bevor losgeschrieben wird |
| Sekunden, nicht Minuten | Darf 5-15 Files beruehren |

Capture legt das Item in die Inbox. Ingest arbeitet es ein.

---

Detail-Logik (Erkennungsregeln, Prioritaeten, Zieldatei-Mapping) → `references/capture-routing.md`
