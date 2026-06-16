# agency-os-skills

Plugin-Marketplace für das **Agency OS** von Markus Vieghofer. Hier liegen alle Kunden-Skills als versionierte Plugins — Workflows für Marketing-Agenturen im DACH-Raum.

## Installation (für Kunden)

Einmalig in Claude Code oder Cowork:

```
/plugin marketplace add Lean-Agency-OS/agency-os-skills
```

Dann die gewünschten Plugins installieren:

```
/plugin install agency-os-core@agency-os
/plugin install agency-os-brand@agency-os
/plugin install agency-os-marketing@agency-os
/plugin install agency-os-video@agency-os
```

Updates holen:

```
/plugin marketplace update agency-os
```

Hinweis: Wer das [Agency-OS-Template](https://github.com/markusvieghofer/agency-os-brain) nutzt, bekommt den Marketplace beim Öffnen des Repos automatisch vorgeschlagen — die Schritte oben sind dann nicht nötig.

## Plugins & Skills

| Plugin | Skills | Inhalt |
|---|---|---|
| `agency-os-core` | `agency-os-start`, `agency-os-capture`, `agency-os-ingest`, `agency-os-plan`, `agency-os-review`, `agency-os-shutdown`, `agency-os-lint`, `agency-os-github` | Tages-Workflows: Session-Start, Capture, Ingest (Rohquelle ins Brain einarbeiten), Projektplanung, Weekly Review, Session-Shutdown, Lint (Brain-Hygiene) und GitHub-Sicherung in einfacher Sprache |
| `agency-os-brand` | `brand-voice`, `icp`, `brand-ci`, `positionierung` | Strategie-Fundament: Stimm-Profil, Wunschkunden-Profil (Bewerten / Persona / Qualifizieren), Brand-CI (Farben/Fonts/Logo als ci.md) und Positionierung (Differenzierung, Messaging, Angebot als positionierung.md) - gemeinsame Quelle für die Marketing-Skills |
| `agency-os-marketing` | `kampagnen-plan`, `content-kalender`, `weekly-content-mining`, `landingpage`, `lead-magnet`, `email-sequenz`, `carousel`, `newsletter-email`, `reel-skript`, `instagram-caption`, `linkedin-caption` | Strategie, Conversion + Content: Kampagnen-Plan (zielgebundener Push, orchestriert Asset-Skills), Content-Kalender (laufender Takt), Content-Mining; Conversion-Layer Landingpage / Lead-Magnet / E-Mail-Sequenz; Asset-Skills nach der 4-Bausteine-Formel (Carousel bis 10 Slides, Newsletter, Reel-Skript, IG-/LinkedIn-Captions) |
| `agency-os-video` | `video-shortform`, `video-roughcut`, `video-captions`, `video-footage-mining` | KI-Video-Editing als vier Use-Case-Skills auf geteilter Engine: postfertiges Reel/Short, Rohschnitt + DaVinci/Premiere-Export, Untertitel einbrennen, Footage-Triage lokal ohne API. Braucht einmalig `setup.sh` + ElevenLabs-Key in `{context}/secrets.env` |

Die Plugins greifen ineinander: `icp` pflegt das Wunschkunden-Profil in `01-context/zielgruppe.md`, `brand-voice` die Stimme in `01-context/brand/voice.md` — `agency-os-marketing` (Carousel, Content-Mining, Newsletter-E-Mail, Reel-Skript, Captions) liest beides.

Die Skills werden über natürliche Sprache ausgelöst ("guten morgen", "notiere…", "review machen", "feierabend") oder direkt per `/agency-os-core:agency-os-start` etc.

## Struktur

```
.claude-plugin/
  marketplace.json            ← Marketplace-Katalog (listet alle 4 Plugins)
plugins/
  agency-os-core/
    .claude-plugin/plugin.json  ← Manifest mit Version
    skills/<skill-name>/SKILL.md
  agency-os-brand/
  agency-os-marketing/
  agency-os-video/
```

## Secrets & Environment-Variablen

Kein Plugin speichert Keys oder Tokens im Plugin-Ordner — der wird bei Updates ersetzt. Plugin-eigene Secrets liegen im persistenten Daten-Verzeichnis (`${CLAUDE_PLUGIN_DATA}`, d.h. `~/.claude/plugins/data/{plugin}/`), OS-globale Variablen in der gitignorten `.env` im OS-Root. Details und Regeln für neue Plugins: [docs/secrets-konvention.md](docs/secrets-konvention.md).

## Entwicklung & Release

- **Versions-Schleuse (WICHTIG):** Kunden erhalten Updates eines Plugins nur, wenn die `version` in dessen `plugins/<plugin>/.claude-plugin/plugin.json` hochgezählt wird. Claude Code löst die Version aus `plugin.json` auf; pusht man Commits ohne Bump, sieht der Client dieselbe Version und behält den Cache — das Update kommt nicht an. **Vor jedem Release also: in jedem geänderten Plugin die `version` erhöhen.**
- **Faustregel:** Hast du Skills nur in einem Plugin geändert, reicht der Bump dort. Mehrere Plugins geändert → jedes einzeln bumpen.
- **Validierung vor Release:** `claude plugin validate .` im Repo-Root (prüft `marketplace.json`), bzw. `claude plugin validate ./plugins/<plugin>` für ein einzelnes Plugin.
