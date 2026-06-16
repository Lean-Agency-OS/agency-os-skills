<div align="center">

# Agency OS

**Dein Marketing-Team als Claude-Skills.**

Ein Plugin-Marketplace für [Claude Code](https://claude.com/claude-code) und Cowork, gebaut für Marketing-Agenturen im DACH-Raum. Strategie, Content und Video laufen als Skills, die wie Senior-Mitarbeiter denken und aus deinem Brain lesen.

`4 Plugins` · `27 Skills` · von [Markus Vieghofer](https://markusvieghofer.com)

</div>

---

## Die Idee

Klassische Tools sind Formulare. Agency OS ist ein **Team**: Jeder Skill hat eine klare Senior-Rolle, ein messbares Ziel und greift auf dasselbe Fundament zu, dein **Brain** (ein Markdown-Repo mit Positionierung, ICP, Voice und CI). Du sagst, was du brauchst, der passende Skill übernimmt, in deiner Stimme, auf deine Zielgruppe.

Drei Prinzipien ziehen sich durch:

- **Ein Fundament, viele Skills.** Positionierung, ICP, Voice und CI liegen einmal im Brain. Jeder Content-Skill liest sie, statt sie neu zu erfinden.
- **Use Cases, keine Funktionen.** Skills bilden einen Job ab ("postfertiges Reel"), nicht eine technische Funktion ("Untertitel rendern").
- **Senior-Haltung.** Jeder Skill weiß, wofür er geradesteht: konsequent vor vollgepackt, Klarheit vor Kreativität, das eine Ziel vor Menge.

---

## ⚡ Installation

Einmalig den Marketplace hinzufügen (Claude Code oder Cowork):

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

> Wer das [Agency-OS-Template](https://github.com/markusvieghofer/agency-os-brain) nutzt, bekommt den Marketplace beim Öffnen automatisch vorgeschlagen, die Schritte oben sind dann nicht nötig.

Ausgelöst werden Skills per natürlicher Sprache ("guten morgen", "schreib mir einen Post", "mach ein Reel draus") oder direkt per `/<skill-name>`.

---

## 🧩 Die vier Plugins

### 🗓️ `agency-os-core` · der Tages-Rhythmus

Die Workflows, die deinen Arbeitstag im Brain halten: Session-Start, Capture, Ingest, Planung, Review, Shutdown, Hygiene und Backup.

| Skill | Job |
|---|---|
| `agency-os-start` | Session-Start: Kontext laden, Tag aufsetzen |
| `agency-os-capture` | Schnelle Notiz/Idee ins Brain werfen |
| `agency-os-ingest` | Rohquelle (PDF, Transkript, …) ins Brain einarbeiten |
| `agency-os-plan` | Projekt planen und im Brain anlegen |
| `agency-os-review` | Weekly Review |
| `agency-os-shutdown` | Session sauber abschließen |
| `agency-os-lint` | Brain-Hygiene (Struktur, Links, Konsistenz) |
| `agency-os-github` | Brain auf GitHub sichern |

### 🎯 `agency-os-brand` · das Strategie-Fundament

Die eine Quelle der Wahrheit für Marke und Zielgruppe. Alles darüber liest hier.

| Skill | Schreibt | Job |
|---|---|---|
| `positionierung` | `positionierung.md` | Differenzierung, Messaging-Pillars, Angebot |
| `icp` | `icp.md` | Wunschkunden-Profil: bewerten, Personas, qualifizieren |
| `brand-voice` | `voice-profile.md` | Stimm-Profil, auf jeden Text angewendet |
| `brand-ci` | `ci.md` | Farben, Fonts, Logo (geteilt mit Carousel + Video) |

### ✍️ `agency-os-marketing` · das Team aus Senior-Marketern

Elf Skills, jeder mit eigener Senior-Rolle und einem Ziel, das dich nach vorne bringt. Strategie- und Conversion-Layer plus Asset-Produktion nach der 4-Bausteine-Formel (Hook → Build → Payoff → CTA).

| Skill | Rolle | Ziel |
|---|---|---|
| `weekly-content-mining` | Senior Content-Stratege | Volle Ideen-Pipeline aus echten Erlebnissen |
| `content-kalender` | Senior Redaktionsleiter | Ein Takt, der die Marke dauerhaft sichtbar hält |
| `kampagnen-plan` | Senior Campaign-Lead | Das eine Kampagnen-Ziel: Leads, Calls, Verkäufe |
| `landingpage` | Senior Conversion-Copywriter | Höchstmögliche Conversion auf die eine Handlung |
| `lead-magnet` | Senior Demand-Gen-Stratege | Pipeline mit qualifizierten Leads füllen |
| `email-sequenz` | Senior Lifecycle-Marketer | Aus Abonnenten automatisiert Kunden machen |
| `newsletter-email` | Senior E-Mail-Copywriter | Die Liste wach halten und zur Handlung bewegen |
| `carousel` | Senior Content-Designer | Content, der gespeichert und geteilt wird |
| `reel-skript` | Senior Short-Form-Creator | Reichweite über die eigene Bubble hinaus |
| `instagram-caption` | Senior Social-Copywriter | Aus einem Scroller eine Handlung machen |
| `linkedin-caption` | Senior LinkedIn-Copywriter | Reichweite + Autorität, die Inbound auslösen |

### 🎬 `agency-os-video` · KI-Video, vier Use Cases auf einer Engine

Aus Rohmaterial wird fertiger Content. Eine geteilte Schnitt-Engine (Transkript, Schnitt, Untertitel, Grade, Motion, NLE-Export), vier saubere Jobs darüber.

| Skill | Rolle | Job |
|---|---|---|
| `video-shortform` | Senior Short-Form-Editor | Rohvideo → postfertiges Reel/Short |
| `video-roughcut` | Senior Assistant Editor | Rohschnitt + DaVinci/Premiere-Export |
| `video-captions` | Senior Captions-Editor | Markenkonforme Untertitel einbrennen |
| `video-footage-mining` | Senior Footage-Logger | Footage-Triage lokal (ohne API), Highlights finden |

---

## 🧠 Wie alles zusammenspielt

```
                        ┌─────────────────────────┐
                        │   Brain (Markdown-Repo)  │
                        │  positionierung · icp ·  │
                        │  voice-profile · ci      │
                        └────────────┬─────────────┘
                                     │  {context} via .agency-os/architecture.md
        ┌────────────────────┬───────┴────────┬────────────────────┐
        ▼                    ▼                ▼                    ▼
   agency-os-core      agency-os-brand   agency-os-marketing   agency-os-video
   (Tages-Rhythmus)    (Fundament)       (Content-Team)        (Video-Team)
```

Kein Skill hat hartkodierte Pfade. Jeder löst seine Ordner über die Rollen-Map in `.agency-os/architecture.md` auf (gepflegt von `agency-os-start`). So passt dasselbe Plugin auf jedes Brain, egal wie es strukturiert ist.

**Der Fluss in der Praxis:**

1. **Fundament** mit `agency-os-brand` schärfen: Positionierung, ICP, Voice, CI.
2. **Ideen** sammeln (`weekly-content-mining`) und in einen **Takt** bringen (`content-kalender`), oder einen zielgebundenen **Push** planen (`kampagnen-plan`).
3. **Assets** produzieren: Carousel, Reel-Skript, Captions, Newsletter, Landingpage, Lead-Magnet, E-Mail-Sequenz, alles in deiner Voice, auf dein ICP.
4. **Video** aus Rohmaterial finishen (`video-*`).

---

## 🔐 Secrets & Environment

Kein Plugin speichert Keys im Plugin-Ordner (der wird bei Updates ersetzt). Secrets liegen im **Brain** unter `{context}/secrets.env` (committet im privaten Repo, aufgelöst über `.agency-os/architecture.md`), z.B. der `ELEVENLABS_API_KEY` für die `video-*`-Skills. Details und Regeln für neue Plugins: [docs/secrets-konvention.md](docs/secrets-konvention.md).

---

## 🛠️ Entwicklung & Release

- **Versions-Schleuse (WICHTIG):** Kunden bekommen Updates eines Plugins nur, wenn die `version` in `plugins/<plugin>/.claude-plugin/plugin.json` hochgezählt wird. Ohne Bump behält der Client den Cache. Vor jedem Release also in jedem geänderten Plugin die `version` erhöhen.
- **Faustregel:** Skills nur in einem Plugin geändert → Bump dort. Mehrere Plugins → jedes einzeln bumpen.
- **Validierung:** `claude plugin validate .` im Repo-Root (prüft `marketplace.json`), bzw. `claude plugin validate ./plugins/<plugin>` für ein einzelnes Plugin.
- **Geteilte Video-Engine:** Der Code der `video-*`-Skills lebt einmal in `packages/video-engine/` und wird per `tools/sync-engine.sh` in jeden Skill gevendort (die Sandbox lädt zur Laufzeit nur den Skill-Ordner). Ein Pre-Commit-Hook (`.githooks/pre-commit`) hält die Kopien in sync, einmal aktivieren mit `git config core.hooksPath .githooks`.

---

## 📁 Struktur

```
.claude-plugin/
  marketplace.json              ← Marketplace-Katalog (alle 4 Plugins)
plugins/
  agency-os-core/
    .claude-plugin/plugin.json  ← Manifest mit Version
    skills/<skill>/SKILL.md
  agency-os-brand/
  agency-os-marketing/
  agency-os-video/
    skills/video-*/             ← gevendorte Engine-Kopien
packages/
  video-engine/                 ← Dev-Quelle der Video-Engine (nicht ausgeliefert)
tools/
  sync-engine.sh                ← vendort die Engine pro Skill
docs/
  secrets-konvention.md
.githooks/
  pre-commit                    ← hält Vendor-Kopien in sync
```

---

<div align="center">

Gebaut von [Markus Vieghofer](https://markusvieghofer.com) · Lean Agency OS

</div>
