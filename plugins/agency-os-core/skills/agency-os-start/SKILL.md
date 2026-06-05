---
name: agency-os-start
description: Session starten - Kontext laden und Status zeigen. Verwende wenn der User "start", "starte session", "guten morgen", "los gehts", "was steht an", "morning", "gm" oder ähnliche Begrüßungs-/Start-Phrasen nutzt.
---

# Agency OS - Start

Session starten. Kontext laden, Status zeigen.

## Pre-flight Check

1. Prüfe ob `OS.md` das vollständige Template enthält (nicht Stub)
2. Falls Stub: "Agency OS ist noch nicht eingerichtet. Sag 'setup' oder 'einrichten' um zu starten."
3. Falls vollständig: Weiter

## Schritte

1. Lies `OS.md` (ist meist schon im Kontext)
2. Lies `01-context/positionierung.md` und `01-context/services.md` (falls vorhanden)
3. Lies `02-strategy/current-priorities.md` (falls vorhanden)
4. Lies `02-strategy/open-loops.md` (falls vorhanden)
5. Schaue in `00-inbox/` - wieviele Items?
6. Lies die letzten 2 Daily Logs aus dem Logs-Ordner (der `*-logs/`-Ordner im OS-Root — je nach OS-Layout `07-logs/` oder `08-logs/`; nach Dateiname sortiert, neueste zuerst)
7. Zeige kompaktes Dashboard (max 20 Zeilen):

```
## Agency OS - [Wochentag], [Datum]

**Top 3 heute:**
1. [höchste Priorität aus current-priorities]
2. [...]
3. [...]

**Open Loops:** [X] aktiv, davon [Y] älter als 2 Wochen
**Inbox:** [X] Items

Bereit. Was steht an?
```

## Regeln

- NIE zusammenfassen wer der User ist - das weiß er selbst
- Nur Status und Handlungsempfehlungen zeigen
- Falls Loops älter als 2 Wochen: explizit warnen
- Falls Inbox voll (>10 Items): erwähnen
- Bei fehlenden Files: kurz hinweisen, aber nicht abbrechen
