# agency-os-skills

Plugin-Marketplace für das **Agency OS** von Markus Vieghofer. Hier liegen alle Kunden-Skills als versionierte Plugins — Workflows für Marketing-Agenturen im DACH-Raum.

## Installation (für Kunden)

Einmalig in Claude Code oder Cowork:

```
/plugin marketplace add Lean-Agency-OS/agency-os-skills
```

Dann das Plugin installieren (alle Skills sind in einem Plugin gebündelt):

```
/plugin install agency-os@agency-os
```

Updates holen:

```
/plugin marketplace update agency-os
```

Hinweis: Wer das [Agency-OS-Template](https://github.com/markusvieghofer/agency-os-brain) nutzt, bekommt den Marketplace beim Öffnen des Repos automatisch vorgeschlagen — die Schritte oben sind dann nicht nötig.

## Enthaltene Skills

Alle Skills sind im Plugin `agency-os` gebündelt:

| Skill | Inhalt |
|---|---|
| `agency-os-start` | Morgen-Briefing / Session-Start |
| `agency-os-capture` | Schnelle Ersterfassung ins Brain |
| `agency-os-plan` | Implementierungsplan für Projekt/Kampagne |
| `agency-os-review` | Wöchentliches Lean-Agency-Review |
| `agency-os-shutdown` | Session-Shutdown + Daily Log |
| `agency-os-github` | GitHub in normaler Sprache: Commit, Pull mit Rebase, Push, Konfliktlösung — ohne Git-Kenntnisse |
| `brand-voice` | Voice-Profile-System: einmaliges Stimm-Setup, danach klingen alle Texte nach dir |
| `icp` | ICP-System: Profil per Setup-Interview, dann Bewerten / Persona / Qualifizieren |
| `weekly-content-mining` | Content-Mining: 8-Bucket-Wochen-Interview → Dump mit Top Plays + Wildcard |
| `carousel` | Carousel-Posts nach der 4-Bausteine-Formel: Idee → 10 Slides + Caption + Preview |
| `video-studio` | KI-Video-Editing: Roh-Video → Reel/Short (Transkript, Schnitt, Untertitel, Motion Graphics) + lokale Schnell-Triage ganzer Video-Ordner ohne API. Braucht einmalig `setup.sh` + ElevenLabs-Key |

Die Content-Plugins greifen ineinander: `icp` pflegt das Wunschkunden-Profil in `01-context/zielgruppe.md`, `brand-voice` die Stimme in `01-context/brand/voice.md` — `weekly-content-mining` und `carousel` lesen beides.

Die Skills werden über natürliche Sprache ausgelöst ("guten morgen", "notiere…", "review machen", "feierabend") oder direkt per `/agency-os-core:agency-os-start` etc.

## Struktur

```
.claude-plugin/
  marketplace.json   ← Marketplace-Katalog (ein Plugin: agency-os)
  plugin.json        ← Plugin-Manifest mit Version, zeigt auf ./skills
skills/
  <skill-name>/
    SKILL.md         ← Skill-Definition
    references/      ← optionale Detail-Docs
```

## Secrets & Environment-Variablen

Kein Plugin speichert Keys oder Tokens im Plugin-Ordner — der wird bei Updates ersetzt. Plugin-eigene Secrets liegen im persistenten Daten-Verzeichnis (`${CLAUDE_PLUGIN_DATA}`, d.h. `~/.claude/plugins/data/{plugin}/`), OS-globale Variablen in der gitignorten `.env` im OS-Root. Details und Regeln für neue Plugins: [docs/secrets-konvention.md](docs/secrets-konvention.md).

## Entwicklung & Release

- **Versions-Schleuse:** Kunden erhalten Updates erst, wenn die `version` in `.claude-plugin/plugin.json` (und passend in `marketplace.json` unter `metadata.version`) hochgezählt wird. Commits ohne Version-Bump erreichen keine Kunden.
- **Validierung vor Release:** `claude plugin validate .` im Repo-Root.
