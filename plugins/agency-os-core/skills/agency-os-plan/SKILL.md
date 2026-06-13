---
name: agency-os-plan
version: 1.0.1
description: Implementierungsplan für ein Projekt oder eine Kampagne erstellen. Verwende wenn der User "plan", "plane Projekt X", "implementierungsplan", "plan erstellen", "kampagne planen", "wie gehen wir vor" oder ähnliche Planungs-Phrasen nutzt.
---

# Agency OS - Plan

Implementierungsplan für ein Projekt erstellen.

## Schritte

1. Frage: "Welches Projekt? Was ist das Ziel?"
2. Falls Projekt in `06-projects/` existiert (als File `{projekt}.md` oder Ordner `{projekt}/`): die entsprechende Datei / `_index.md` lesen für Kontext
3. Falls neues Projekt ohne bestehende Infrastruktur: Ordner anlegen mit `_index.md` aus Template `references/templates/project-briefing.md` (liegt in diesem Skill). **Index-Pflege:** Markdown-Link auf das neue Projekt in `06-projects/_index.md` ergänzen (je nach Typ in Sektion `## Aktive Kunden-Projekte` oder `## Aktive Interne Projekte`). Hinweis: Projekt-Infrastruktur (eigenes Git-Repo, CLAUDE.md, settings.json) wird via `/spoke-new` angelegt — dieser Skill macht nur das Planungs-Dokument, kein Duplikat.
4. Plan schreiben in `06-projects/{projekt-kebab}/plan-{{DATUM}}.md`. Falls das Projekt noch ein Single-File ist (`06-projects/{projekt}.md`): Plan als eigenständige Datei daneben ablegen (`06-projects/{projekt}-plan-{{DATUM}}.md`) und im Projekt-File unter einem `## Verweise`-Abschnitt verlinken. **Index-Pflege:** Im `_index.md` des Projekts (falls Ordner vorhanden) unter "Verweise" einen Markdown-Link auf das neue Plan-File ergänzen.

```markdown
# Plan: [Titel]

> Erstellt: {{DATUM}}
> Projekt: [{{PROJEKT}}](_index.md)
> Status: Offen

## Ziel
[Was soll erreicht werden]

## Kontext
[Aktuelle Situation, relevante Infos, Verweise auf externe Tools]

## Schritte
1. [Schritt 1]
2. [Schritt 2]
3. [...]

## Risiken
- [Was könnte schiefgehen]

## Erfolgskriterien
- [ ] [Woran erkennt man dass es fertig ist]
```

5. Bestätigung: "Plan erstellt in `06-projects/{projekt-kebab}/`. [X] Schritte. Soll ich anfangen?"

## Regeln

- Markdown-Links setzen: `[Projekt](_index.md)`, `[Kunde](05-clients/{kunde}/_index.md)` falls relevant
- Bei Kunden-bezogenen Projekten: Verweis auf `../../05-clients/{kunde}/_index.md`
- Datum im ISO-Format (`YYYY-MM-DD`)
- Bei sehr kleinen Plänen: nur Ziel + Schritte, Rest weglassen
