---
name: agency-os-plan
description: Implementierungsplan für ein Projekt oder eine Kampagne erstellen. Verwende wenn der User "plan", "plane Projekt X", "implementierungsplan", "plan erstellen", "kampagne planen", "wie gehen wir vor" oder ähnliche Planungs-Phrasen nutzt.
---

# Agency OS - Plan

Implementierungsplan für ein Projekt erstellen.

## Schritte

1. Frage: "Welches Projekt? Was ist das Ziel?"
2. Falls Projekt in `04-projects/` existiert: `_index.md` lesen für Kontext
3. Falls neues Projekt: Ordner anlegen mit `_index.md` aus Template `references/templates/project-briefing.md` (liegt in diesem Skill). **Index-Pflege:** Markdown-Link auf das neue Projekt in `04-projects/_index.md` (Sektion `## Aktuell vorhanden`) ergänzen, Format: `- [projekt-name](./{projekt-kebab}/_index.md)`. Erste Zeile `- _(noch leer)_` dabei entfernen.
4. Plan schreiben in `04-projects/{projekt-kebab}/plan-{{DATUM}}.md`. **Index-Pflege:** Im `_index.md` des Projekts (in `04-projects/{projekt-kebab}/_index.md`) unter "Verweise" einen Markdown-Link auf das neue Plan-File ergänzen.

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

5. Bestätigung: "Plan erstellt in `04-projects/{projekt-kebab}/`. [X] Schritte. Soll ich anfangen?"

## Regeln

- Markdown-Links setzen: `[Projekt](_index.md)`, `[Kunde](../../03-clients/{kunde}/_index.md)` falls relevant
- Bei Kunde-bezogenen Projekten: Verweis auf `../../03-clients/{kunde}/_index.md`
- Datum im ISO-Format (`YYYY-MM-DD`)
- Bei sehr kleinen Plänen: nur Ziel + Schritte, Rest weglassen
