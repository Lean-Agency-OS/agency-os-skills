---
name: agency-os-capture
description: Schnelle Erfassung von Gedanken, Aufgaben, Ideen, Open Loops oder Entscheidungen. Verwende wenn der User "capture", "notiere", "merken", "halt fest", "schreib das auf", "festhalten", "muss ich mir merken" oder ähnliche Erfassungs-Signale nutzt.
---

# Agency OS - Capture

Schnelle Erfassung. Kategorisieren und ablegen.

## Schritte

1. Falls kein Inhalt mitgegeben: Frage "Was willst du festhalten?"
2. Kategorisiere automatisch nach `references/capture-routing.md` (TASK / IDEE / LOOP / ENTSCHEIDUNG)
3. Schreibe das Item in die passende Datei (siehe Mapping in der reference). **Falls dabei eine neue Datei oder ein neuer Unterordner in einem Top-Level-Ordner entsteht** (z.B. erstes File in `00-inbox/`, neuer Kunde in `03-clients/`): Markdown-Link in der `## Aktuell vorhanden`-Sektion des entsprechenden `_index.md` ergänzen. Erste Zeile `- _(noch leer)_` dabei entfernen.
4. Bestätigung: "Gespeichert in `dateiname.md` als [Kategorie]. Noch was?"
5. Loop bis User fertig ist

Detail-Logik (Erkennung, Prioritäten, Regeln) → `references/capture-routing.md`
