---
name: agency-os-shutdown
description: Session beenden - Daily Log schreiben, Status sichern, offene Loops erfassen. Verwende wenn der User "shutdown", "feierabend", "fertig für heute", "gute nacht", "session beenden", "bis morgen", "schluss für heute", "eod" oder ähnliche Abschluss-Signale nutzt.
---

# Agency OS - Shutdown

Session beenden. Status sichern.

## Schritte

1. Frage: "Was hat sich heute bewegt? Neue Aufgaben oder Blocker?"
2. `02-strategy/current-priorities.md` aktualisieren (Status, neue Items)
3. Frage: "Offene Gedanken oder Loops?"
4. `02-strategy/open-loops.md` aktualisieren falls nötig
5. Daily Log schreiben/ergänzen in `07-logs/{{DATUM}}.md`:

```markdown
# {{DATUM}}

## Notizen
- [Was passiert ist - Stichpunkte]
- [Entscheidungen]
- [Was erstellt/geändert wurde]

## Entscheidungen
- [Wichtige Entscheidungen mit Begründung]
```

Falls Daily Log schon existiert: nur neuen Abschnitt anhängen (append-only).

6. Lernprotokoll prüfen: siehe `references/teaching-loop.md` für Erkennungs-Logik (Korrektur-Signale) und Lern-Kategorien. Bei Treffer: Eintrag in `OS.md` unter `## Wichtige Entscheidungen`.
7. Zeige: "Session gesichert. Bis zum nächsten Mal!"

## Regeln

- Append-only beim Daily Log: nichts überschreiben
- Open Loops gehören NICHT in den Daily Log (separates File `02-strategy/open-loops.md`)
- Lernprotokoll-Updates kompakt halten - OS.md soll schlank bleiben
- Bei kurzen Sessions (z.B. nur 5 min): nur 1-2 Zeilen Notizen reichen
