# AGENTS.md

Zentrale Anweisungsdatei für alle Agents, die in diesem Repo arbeiten. Hier liegt der Marketplace **Agency OS**: vier Plugins (`agency-os-core`, `agency-os-brand`, `agency-os-marketing`, `agency-os-video`) mit Skills für Marketing-Agenturen im DACH-Raum, plus die geteilte Video-Engine.

## Struktur

```
.claude-plugin/marketplace.json   ← Katalog; liefert je Plugin nur ./plugins/<name> aus
plugins/agency-os-*/
  .claude-plugin/plugin.json       ← Manifest mit der Liefer-Version
  skills/<skill>/SKILL.md          ← der Skill (+ ggf. references/, resources/, scripts/)
packages/video-engine/             ← DEV-QUELLE der Video-Engine, NICHT ausgeliefert
tools/sync-engine.sh               ← vendort die Engine in die video-* Skills
.githooks/pre-commit               ← hält die Vendor-Kopien in sync
docs/                              ← Repo-Doku (z.B. secrets-konvention.md)
```

Ausgeliefert wird **nur** `plugins/<plugin>/`. Alles am Repo-Root (`packages/`, `tools/`, `docs/`, README, diese Datei) ist Dev-/Doku-Material und landet nie als Plugin beim Kunden.

## Versionierung

**`plugin.json` `version` ist die Liefer-Schleuse.** Claude Code löst die Version aus `plugin.json` auf; ohne Erhöhung behält der Client den Cache und das Update kommt **nicht** an. Das vergessene Bump ist der Fehler, der wirklich wehtut.

**Pflicht-Regel:** Jede kundenrelevante Änderung an einem Plugin bumpt im **selben Commit** zwei Dinge:
1. die `version` in `plugin.json` (steuert die Auslieferung), **und**
2. die `version:` im Frontmatter **jedes geänderten Skills**.

Ein Plugin-Bump kommt also **nie allein**: mindestens eine Skill-Version wird mitgebumpt (ein Plugin ändert sich nur, weil sich ein Skill ändert). Mehrere Plugins geändert → jedes Plugin **plus** jeweils seine geänderten Skills.

- **SemVer (für Skill und Plugin gleich):**
  - **major** = Breaking: Skill umbenannt/entfernt, Trigger oder Pfade, auf die man sich verlässt, brechen (z.B. `video-studio` → Split in vier Skills = `2.0.0`).
  - **minor** = neues Verhalten/Feature oder neuer Skill (z.B. Text-Hooks, Caption-Delegation).
  - **patch** = Fix, Wording, Querverweis, Doku im Skill.
- **Pro Plugin nur EIN Bump pro Commit** — egal wie viele Skills sich ändern. Die Stufe ist die **höchste** unter den geänderten Skills:
  - Patch + Patch → Plugin **patch**
  - Patch + Minor → Plugin **minor**
  - Patch + Minor + Major → Plugin **major**
  - Jeder Skill behält seine **eigene** Stufe (einer patch, einer minor, …); nur das Plugin spiegelt die höchste wider, um die Gesamt-Changes korrekt abzubilden.
- **Repo-Root-Dateien** (README, `docs/`, `tools/`, `packages/`, AGENTS.md) sind **nicht** versioniert und brauchen keinen Plugin-Bump, weil sie in keinem Plugin ausgeliefert werden. Ausnahme: ändert sich `packages/video-engine` und wird in ein Plugin gevendort, bumpt das **konsumierende** Plugin.

**Vor jedem Release:** `claude plugin validate .` (prüft `marketplace.json`) bzw. `claude plugin validate ./plugins/<plugin>`.

## Skills schreiben

- **Keine hartkodierten Pfade.** Ordner über `.agency-os/architecture.md` (Rolle→Pfad-Map, gepflegt von `agency-os-start`) auflösen, sonst per Muster, sonst Schritt überspringen. `{context}`, `{marketing}`, `{logs}` usw. sind aufgelöste Rollen, keine festen Namen.
- **Kundengeneric.** Skills laufen in fremden Brains. Nichts auf Markus' konkrete Struktur festnageln.
- **Use Cases, keine Funktionen.** Ein Skill = ein abgeschlossener Job, nicht eine technische Funktion.
- **Senior-Rolle + Ziel** als Anker direkt unter der H1 (Marketing-/Video-Skills): *"Du … als **[Senior-Rolle]**: [Haltung]. **Dein Ziel:** [Ergebnis]."*

## Sprache & Code-Kommentare

- **User-facing Output ist Deutsch** (SKILL-Prosa, Chat-Ausgaben, `echo` für den Kunden). Keine em-/en-Dashes (—/–); Doppelpunkt/Punkt/Komma stattdessen, normale Bindestriche für Zahlenbereiche.
- **Source-Code-Kommentare sind IMMER Englisch** (Shell, Python, Configs). Dev-only-Tooling (z.B. `tools/sync-engine.sh`) darf komplett Englisch sein, da kein Kunde es sieht.

## Geteilte Video-Engine (Vendoring)

Ein Skill ist **self-contained**: die Sandbox lädt zur Laufzeit nur den Skill-Ordner, nicht den Plugin-Baum. Darum lebt der Engine-Code **einmal** in `packages/video-engine/` und wird in jeden `video-*` Skill **gevendort**.

- **Nie eine Vendor-Kopie editieren** (`plugins/agency-os-video/skills/*/helpers|references|scripts`). Immer die Quelle in `packages/video-engine/` ändern und `bash tools/sync-engine.sh` laufen lassen.
- Der **Pre-Commit-Hook** (`.githooks/pre-commit`, aktivieren mit `git config core.hooksPath .githooks`) re-vendort und staged die Kopien bei jedem Commit. Quelle **und** Kopien werden committet (die Kopien werden ausgeliefert).
- Pro-Skill-Teilmenge + Marker (`.needs-whisper`, hyperframes) steuert `tools/sync-engine.sh` (Manifest dort).
- Schreibbare Artefakte (venv, node_modules, Chromium, `.ready`) liegen unter dem von `scripts/resolve-datadir.sh` aufgelösten DATA-Verzeichnis (Skill-Root in Claude Code, Cache in Cowork bei read-only Mount), nie im Brain.

## Secrets

Secrets liegen im **Brain** unter `{context}/secrets.env` (committet im privaten Repo, aufgelöst über `.agency-os/architecture.md`), **nie** im Skill-Ordner. Details: [docs/secrets-konvention.md](docs/secrets-konvention.md).

## Permissions / `allowed-tools`

- Schreibende Git-Schritte laufen prompt-frei über `allowed-tools` im Skill-Frontmatter. Syntax (offiziell): space-/komma-getrennt, Pattern mit Space-Wildcard, z.B. `allowed-tools: Bash(git add *) Bash(git commit *) Bash(git push *)`.
- **Konflikt-Auflösung lebt nur in `agency-os-github`** (hat `pull`/`rebase` erlaubt). `agency-os-start` und `agency-os-shutdown` delegieren bei Konflikt/Push-Fehler an `/agency-os-github`, lösen nichts selbst.
- Der Schutz vor ungewolltem Push ist die **Klartext-Rückfrage im Workflow** (bzw. bei shutdown der Trigger selbst), nicht der Permission-Prompt. `mv`/`rm` und destruktive Befehle bleiben bestätigungspflichtig.

## Commits

- Nur committen/pushen, wenn der User es verlangt. Vor dem Commit die Staging-Spalte prüfen (`M ` = gestaged vs ` M` = offen) und gezielt mit Pfad-Argument stagen, nicht fremd-gestagete Dateien mitnehmen.
- Commit-Messages: knapp, Deutsch erlaubt, Typ-Präfix optional (`feat:`/`fix:`/…). Plugin-Bump in denselben Commit.
- Co-Author-Zeile am Ende von Commits: `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.
