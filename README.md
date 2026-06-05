# agency-os-skills

Plugin-Marketplace für das **Agency OS** von Markus Vieghofer. Hier liegen alle Kunden-Skills als versionierte Plugins — Workflows für Marketing-Agenturen im DACH-Raum.

## Installation (für Kunden)

Einmalig in Claude Code oder Cowork:

```
/plugin marketplace add markusvieghofer/agency-os-skills
```

Dann das gewünschte Plugin installieren:

```
/plugin install agency-os-core@agency-os
```

Updates holen:

```
/plugin marketplace update agency-os
```

Hinweis: Wer das [Agency-OS-Template](https://github.com/markusvieghofer/agency-os-brain) nutzt, bekommt den Marketplace beim Öffnen des Repos automatisch vorgeschlagen — die Schritte oben sind dann nicht nötig.

## Verfügbare Plugins

| Plugin | Version | Inhalt |
|---|---|---|
| `agency-os-core` | 1.0.0 | Tages-Workflows: Session-Start, Capture, Projektplanung, Weekly Review, Session-Shutdown |
| `brand-voice` | 1.0.0 | Voice-Profile-System: einmaliges Stimm-Setup, danach klingen alle Texte nach dir |
| `github-cowork` | 1.0.0 | GitHub in normaler Sprache: Commit, Push, Pull, Verlauf — ohne Git-Kenntnisse |
| `icp` | 1.0.0 | ICP-System: Profil per Setup-Interview, dann Bewerten / Persona / Qualifizieren |
| `weekly-goldmine` | 1.0.0 | Content-Mining: 8-Bucket-Wochen-Interview → Goldmine Dump mit Top Plays |
| `carousel` | 1.0.0 | Carousel-Posts nach der 4-Bausteine-Formel: Idee → 10 Slides + Caption + Preview |
| `video-studio` | 1.0.0 | KI-Video-Editing: Roh-Video → Reel/Short (Transkript, Schnitt, Untertitel, Motion Graphics). Braucht einmalig `setup.sh` + ElevenLabs-Key |

Die Content-Plugins greifen ineinander: `icp` pflegt das Wunschkunden-Profil in `01-context/zielgruppe.md`, `brand-voice` die Stimme in `01-context/brand/voice.md` — `weekly-goldmine` und `carousel` lesen beides.

Die Skills werden über natürliche Sprache ausgelöst ("guten morgen", "notiere…", "review machen", "feierabend") oder direkt per `/agency-os-core:agency-os-start` etc.

## Struktur

```
.claude-plugin/marketplace.json   ← Katalog aller Plugins
plugins/
  agency-os-core/
    .claude-plugin/plugin.json    ← Manifest mit Version
    skills/                       ← die Skills
```

## Entwicklung & Release

- **Versions-Schleuse:** Kunden erhalten Updates erst, wenn die `version` im jeweiligen `plugin.json` hochgezählt wird. Commits ohne Version-Bump erreichen keine Kunden.
- **Zwei Arbeitsmodi:**
  - *Release-Ziel* (z.B. brand-voice, icp): Die Quelle lebt in Markus' Brain, hier liegt nur das Kunden-Destillat. Hier nie inhaltlich editieren.
  - *Entwicklungsort* (z.B. video-studio, agency-os-core): Dieses Repo ist die einzige Quelle, Entwicklung passiert direkt hier.
- **Validierung vor Release:** `claude plugin validate .` im Repo-Root.
