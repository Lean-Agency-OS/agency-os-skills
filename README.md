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

Updates holen (zwei Stufen, beide nötig):

```
# 1. Marketplace-Cache auf den neuesten Repo-Stand bringen
claude plugin marketplace update agency-os

# 2. Installierte Plugins anheben — Schritt 1 allein reicht NICHT
claude plugin update agency-os-core@agency-os --scope project
claude plugin update agency-os-brand@agency-os --scope project
claude plugin update agency-os-marketing@agency-os --scope project
claude plugin update agency-os-video@agency-os --scope project
```

Danach **Claude Code neu starten**, damit die neuen Skill-Versionen geladen werden (die Update-Befehle melden selbst "Restart to apply changes").

Schnell prüfen, was installiert ist: `claude plugin list`.

> **Stolperfallen:**
> - Der `@agency-os`-Suffix ist Pflicht. Ohne ihn sucht die CLI nur im user-Scope und meldet `Plugin not found`.
> - `--scope project` passt für Template-/Brain-Installs (Plugins in `.claude/settings.json` des Brains). Bei globaler Installation stattdessen `--scope user`.
> - Ein Update greift nur, wenn die Plugin-`version` im Repo hochgezählt wurde, siehe [Entwicklung & Release](#️-entwicklung--release). Ohne Bump bleibt der Client auf dem Cache-Stand.

> Wer das [Agency-OS-Template](https://github.com/markusvieghofer/agency-os-brain) nutzt, bekommt den Marketplace beim Öffnen automatisch vorgeschlagen, die Schritte oben sind dann nicht nötig.

Ausgelöst werden Skills per natürlicher Sprache ("guten morgen", "schreib mir einen Post", "mach ein Reel draus") oder direkt per `/<skill-name>`.

---

## 🧩 Die vier Plugins

### 🗓️ `agency-os-core` · der Tages-Rhythmus

Die Workflows, die deinen Arbeitstag im Brain halten: Session-Start, Capture, Ingest, Planung, Review, Shutdown, Hygiene und Backup.

| Skill | Job | Wann nutzen |
|---|---|---|
| `agency-os-start` | Session-Start: Kontext laden, Tag aufsetzen | Zu Beginn jeder Session ("guten morgen", "los gehts") |
| `agency-os-capture` | Schnelle Notiz/Idee ins Brain werfen | Gedanke, Task oder Idee kommt zwischendurch und soll nicht verloren gehen |
| `agency-os-ingest` | Rohquelle (PDF, Transkript, …) ins Brain einarbeiten | Neues Transkript oder Dokument soll strukturiert ins Brain |
| `agency-os-plan` | Projekt planen und im Brain anlegen | Vor einem mehrstufigen Vorhaben oder einer Kampagne |
| `agency-os-review` | Weekly Review | Wochenabschluss: Rückblick + nächste Woche aufsetzen |
| `agency-os-shutdown` | Session sauber abschließen | Feierabend: lose Enden sichern, Log schreiben |
| `agency-os-lint` | Brain-Hygiene (Struktur, Links, Konsistenz) | Brain fühlt sich unaufgeräumt an, tote Links/Widersprüche vermutet |
| `agency-os-github` | Brain auf GitHub sichern | Änderungen sichern und verfügbar machen, neuesten Stand holen |

### 🎯 `agency-os-brand` · das Strategie-Fundament

Die eine Quelle der Wahrheit für Marke und Zielgruppe. Alles darüber liest hier.

| Skill | Schreibt | Job | Wann nutzen |
|---|---|---|---|
| `positionierung` | `positionierung.md` | Differenzierung, Messaging-Pillars, Angebot | Ganz am Anfang, oder wenn Angebot/Differenzierung unscharf ist |
| `icp` | `icp.md` | Wunschkunden-Profil: bewerten, Personas, qualifizieren | Bevor Content/Copy/Ads rausgehen, oder um einen Lead einzuschätzen |
| `brand-voice` | `voice-profile.md` | Stimm-Profil, auf jeden Text angewendet | Bei jedem Text, der nach dir klingen soll (Mail, Post, Copy) |
| `brand-ci` | `ci.md` | Farben, Fonts, Logo (geteilt mit Carousel + Video) | Einmal beim Setup, bevor Carousel/Video gebrandet werden |

### ✍️ `agency-os-marketing` · das Team aus Senior-Marketern

Elf Skills, jeder mit eigener Senior-Rolle und einem Ziel, das dich nach vorne bringt. Strategie- und Conversion-Layer plus Asset-Produktion nach der 4-Bausteine-Formel (Hook → Build → Payoff → CTA).

| Skill | Rolle | Ziel | Wann nutzen |
|---|---|---|---|
| `weekly-content-mining` | Senior Content-Stratege | Volle Ideen-Pipeline aus echten Erlebnissen | Wöchentlich, wenn dir Ideen für Posts fehlen |
| `content-kalender` | Senior Redaktionsleiter | Ein Takt, der die Marke dauerhaft sichtbar hält | Wenn Posten planlos ist und einen Rhythmus braucht |
| `kampagnen-plan` | Senior Campaign-Lead | Das eine Kampagnen-Ziel: Leads, Calls, Verkäufe | Vor einem Launch oder einer Aktion mit klarem Ziel |
| `landingpage` | Senior Conversion-Copywriter | Höchstmögliche Conversion auf die eine Handlung | Wenn eine Seite ein Angebot oder Opt-in konvertieren soll |
| `lead-magnet` | Senior Demand-Gen-Stratege | Pipeline mit qualifizierten Leads füllen | Wenn du etwas zum Verschenken brauchst, das Leads bringt |
| `email-sequenz` | Senior Lifecycle-Marketer | Aus Abonnenten automatisiert Kunden machen | Für automatisierte Strecken (Welcome, Nurture, Launch) |
| `newsletter-email` | Senior E-Mail-Copywriter | Die Liste wach halten und zur Handlung bewegen | Für eine einzelne, versandfertige Newsletter-Ausgabe |
| `carousel` | Senior Content-Designer | Content, der gespeichert und geteilt wird | Für einen Instagram/LinkedIn-Carousel aus einer Idee |
| `reel-skript` | Senior Short-Form-Creator | Reichweite über die eigene Bubble hinaus | Bevor du ein Reel/Short drehst — du brauchst das Skript |
| `instagram-caption` | Senior Social-Copywriter | Aus einem Scroller eine Handlung machen | Du hast ein Asset (Foto/Grafik) und brauchst die Caption |
| `linkedin-caption` | Senior LinkedIn-Copywriter | Reichweite + Autorität, die Inbound auslösen | Für den Text zu einem LinkedIn-Post oder -Asset |

### 🎬 `agency-os-video` · KI-Video, vier Use Cases auf einer Engine

Aus Rohmaterial wird fertiger Content. Eine geteilte Schnitt-Engine (Transkript, Schnitt, Untertitel, Grade, Motion, NLE-Export), vier saubere Jobs darüber.

| Skill | Rolle | Job | Wann nutzen |
|---|---|---|---|
| `video-shortform` | Senior Short-Form-Editor | Rohvideo → postfertiges Reel/Short | Rohclip soll fertig geschnittenes, gebrandetes Reel werden |
| `video-roughcut` | Senior Assistant Editor | Rohschnitt + DaVinci/Premiere-Export | Cutter finisht nativ, du lieferst den Vorschnitt |
| `video-captions` | Senior Captions-Editor | Markenkonforme Untertitel einbrennen | Fertig geschnittenes Video braucht nur noch Untertitel |
| `video-footage-mining` | Senior Footage-Logger | Footage-Triage lokal (ohne API), Highlights finden | Ganzer Ordner Rohmaterial, du suchst die brauchbaren O-Töne |

---

## 🧠 Wie alles zusammenspielt

```
                        ┌──────────────────────────┐
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
- **Release-Loop:** `version` bumpen → committen + pushen → im Ziel-Workspace die Update-Befehle aus [Installation](#-installation) laufen lassen → Claude Code neu starten. Erst dann sehen Clients die Änderung.

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
