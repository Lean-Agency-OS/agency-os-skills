---
name: agency-os-review
version: 2.0.0
description: Wöchentliches Review für die schlanke Agentur des Users. Triggert wenn der User "review", "wochenrückblick", "weekly review", "sonntags-review", "review machen", "wochen-check", "lass uns reviewen" oder ähnliche Review-Phrasen nutzt. Kombiniert strukturiertes 6-Schritt-Protokoll mit ehrlicher Muster-Spiegelung und Anti-Pattern-Disziplin.
---

# Agency OS — Review

Wöchentliches Review. Am besten Sonntag abend oder Montag morgen.

## Bash-Regeln (Prompt-Vermeidung)

Damit dieser Skill ohne Permission-Rückfragen läuft, beim Bauen von Befehlen:
- **Lesen** (Dateien, Verzeichnis-Listen, Suche) mit den Tools `Read`, `Glob`, `Grep` statt `cat`/`ls`/`grep` in Bash.
- **Keine Command-Substitution** `$(...)` und keine Backticks in Bash. Zähl-/Filter-Ausgaben direkt per Pipe ausgeben (z.B. `… | wc -l` als eigene Zeile), nicht in einen `echo`-String verschachteln.
- **Keine Interpreter** (`python3`/`node`/`perl`/`awk`) für Ad-hoc-Logik; JSON mit `jq` lesen. Mitgelieferte Skripte dieses Skills sind ausgenommen.
- Mutierende Bash-Befehle (`mv`, `rm`) bleiben bestätigungspflichtig. Dieser Skill sichert nichts auf Git (das macht `/agency-os-github`).

## Methodik

Lies `references/review-protocol.md` für den vollständigen Ablauf. Dieser Skill ist der Trigger — das Protokoll ist die kanonische Quelle.

## Pfade & Fundament

> **Brain-Pfade:** Die `{...}`-Platzhalter im Protokoll (`{strategy}/`, `{projects}/`, `{logs}/` …) sind **Rollen** aus `.agency-os/architecture.md`, keine festen Ordnernamen - Brains variieren. Pro Rolle: (1) wenn `.agency-os/architecture.md` die Rolle nennt → diesen Pfad; (2) sonst per Rolle/Muster suchen, Standard-Ordnername zuerst; (3) nichts gefunden → Schritt überspringen. Default-Tabelle: `agency-os-start/references/architecture.md`.

## Workflow

1. Brain lesen (bevor du irgendwas sagst)
2. Inbox leeren (`{inbox}/`)
3. Loops prüfen + altern (`{open-loops}`)
4. Projekte updaten (`{projects}/`)
5. Muster spiegeln — ehrlich, kein Schmeicheln
6. Nächste Woche planen + Log schreiben (`{logs}/`)

Jeden Schritt einzeln durchgehen. Kein Hetzen, kein Überspringen.

**Reflexions-Modus:** Das Review endet nicht mit einer Tabelle. Es endet mit einer Spiegelung und einer Frage, die sitzt.

## Output

Aktualisierte Brain-Files (`{inbox}/` geleert, `{open-loops}`, `{projects}/`) plus ein Log-Eintrag in `{logs}/` (Schritt 6). Im Chat: Muster-Spiegelung und eine Frage, die sitzt.
