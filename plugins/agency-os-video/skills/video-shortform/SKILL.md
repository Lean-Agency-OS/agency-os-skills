---
name: video-shortform
version: 1.1.0
description: Schneidet Roh-Video(s) zu postfertigen Reels/Shorts - Transkript, scroll-stopping Text-Hook drueber, Schnitt, Untertitel, optional Color-Grade + Motion-Graphics, Final-Render. Einzeln oder ein ganzer Ordner auf einmal. Triggert bei "mach ein Reel draus", "bau ein Short aus diesem Video", "schneid mir das Video fertig", "schneid alle Videos in dem Ordner", "postfertiges Reel", "/video-shortform". Brand-aware ueber {context}/brands/{brand}/, nutzt brand-voice + icp. Output landet IMMER im selben Ordner wie das Roh-Video.
---

# Skill: video-shortform

Du schneidest als **Senior Short-Form-Editor**: du denkst in Hook, Pacing und Daumenstopp, nicht in Rohmaterial. **Dein Ziel:** ein postfertiges Social-Video ohne Editor-Zeit, das Watch-Time hält und auf die eine Handlung zieht.

**Zweck:** Aus einem Roh-Video ein **sendefertiges** Reel/Short bauen, fertig zum Posten (kein weiterer Schnittprogramm-Schritt nötig). Für die Variante "ich finishe selbst im NLE" gibt es `/video-roughcut`.

**Brand:** die im Brain konfigurierte Brand (Ordner unter `{context}/brands/`). Gibt es nur einen, den nehmen; bei mehreren die mit `brand-config.md` `status: active`. Kein fester Default-Name.

**Brand-Pfade & CI:** `{context}/brands/{brand}/` ist ein Default - existiert `.agency-os/architecture.md` im Projekt-Root (Rolle→Pfad-Map vom `agency-os-start`-Skill), den `context`-Pfad daraus nehmen. Die Brand-CI liegt als **`ci.md` mit YAML-Frontmatter** (`colors`, `fonts`, `handle`, `name`, `assets_dir`, `logo`) im Brand-Ordner - dieselbe Datei und dasselbe Schema nutzt `/carousel`. Werte aus dem Frontmatter lesen und an die Helfer (ffmpeg/PIL) durchreichen.

**Kern:** Text-Hook + Schnitt + Untertitel laufen mit reinem ffmpeg. Motion Graphics (optional) via hyperframes braucht Chromium. Funktioniert für **ein einzelnes Video** oder **einen ganzen Ordner auf einmal**.

---

## Methodik

### Struktur (self-contained Skill)

- `helpers/` - Schnitt-Engine (Python, ElevenLabs Scribe, ffmpeg). Interpreter: `.venv/bin/python` (Setup baut das venv im Skill-Root).
- `engines/hyperframes/` - Motion-Graphics-Engine (Node, hyperframes per npm in `node_modules`).
- `references/cut-standards.md` - **die** Quelle fuer Padding, Silence-Checks, Last-Word-Two-Step, EDL-Format.
- `references/motion-style.md` - projekt-eigene Motion-Regeln (Anchor-Word-Sync, Render-Defaults). Foundation: hyperframes house-style.md / visual-styles.md in `node_modules`.
- `references/hard-rules.md` - die Hard Rules der Schnitt-Engine (Referenz, kein eigener Trigger).
- `references/safe-zone.md` - **Pflicht** fuer Text-Hook + Untertitel: wohin Text darf (9:16), feste obere Caption-Kante.
- `references/transcription.md` - Transkriptions-Policy: Scribe als Pfad, Word-Level-Pflicht. Dieser Skill ist Scribe-only (kein lokaler Whisper-Fallback).

Der Code ist aus der geteilten `video-engine`-Quelle gevendort (siehe `packages/video-engine/` im Repo). **Nicht hier editieren** - Änderungen in der Quelle machen und `tools/sync-engine.sh` laufen lassen.

Abkuerzung in den Befehlen unten: `SK=.claude/skills/video-shortform` (Aufruf vom OS-Root). Den `{context}`-Pfad wie oben beschrieben auflösen.

---

## Workflow

### Phase 0: Setup-Gate (PFLICHT, still)

1. `DATA=$(bash $SK/scripts/resolve-datadir.sh)` (schreibbares Daten-Verzeichnis: Skill-Root in Claude Code, Cache in Cowork). Fehlt `$DATA/.ready` -> `bash $SK/scripts/setup.sh`, Ausgabe zeigen.
2. `{context}` auflösen, dann `bash $SK/scripts/doctor.sh "{context}/secrets.env"`. Bei `OFFEN ELEVENLABS_API_KEY` -> Nutzer bitten, den Key in `{context}/secrets.env` einzutragen (Vorlage: `$SK/secrets.env.example`), dann stoppen.
3. Bei `FEHLT ffmpeg/node/python` -> Hard-Stop (Sandbox ohne Tools).

Nur wenn Doctor sauber -> weiter.

---

### Phase 1: Brief + Modus

**1a. Modus erkennen:**
- **Einzel-Video:** ein konkreter Datei-Pfad. Die zwei Inputs (1c) kurz klären, dann los.
- **Batch (ganzer Ordner):** Anweisung wie *"schneid alle Videos in {ordner}"*. Alle Video-Files im Ordner sammeln, die Inputs **einmal** klären (gelten dann für **alle**), **keine** Plan-Bestätigung. Pro Video laufen Phase 2-7 durch; der einzige Stop-Punkt bleibt der Text-Hook (Phase 3).

**1b. Format:** kein Input. Default **9:16** (vertikal); leitet sich aus dem Quell-Video ab (Seitenverhältnis per ffprobe). 16:9 / 1:1 nur, wenn das Material es klar vorgibt oder der User es ausdrücklich sagt.

**1c. Inputs:** nur diese zwei: **Untertitel** ja/nein, **Motion Graphics** ja/nein. Brand = aktive Brand aus `{context}/brands/`. Keine weiteren Fragen, kein Plan zum Bestätigen.

**1d. Skript prüfen:** Liegt ein Skript vor (z.B. ein `/reel-skript`-Output im Marketing-Ordner oder eine Skript-Datei beim Footage)? Wenn ja, dient es als Vorlage für Hook + Schnitt. Bei **mehreren** Videos die Skript-Struktur über die Clips abbilden (jeder Clip füllt seinen Beat).

**1e. Ordner + Dateiname:** Output landet IMMER im **selben Ordner wie das Roh-Video** (kein neuer datierter Ordner):
- **Sprechender Name**, nicht `final.mp4`: `{slug}.mp4` aus einem kurzen Thema-/Hook-Slug (z.B. `funnel-fehler.mp4`). Den Slug pro Clip eindeutig wählen, dann ist es auch batch-sicher (kein Überschreiben, wenn mehrere Videos im selben Ordner liegen). Dazu `{slug}_index.md` daneben.
- Schnitt-Cache (Transkript, EDL, SRT, takes_packed) in `<ordner>/_work/edit/` (gitignored)

So bleiben Raw und fertiger Schnitt zusammen. Den Edit-Cache nie neu transkribieren, wenn das Raw-File unveraendert ist.

---

### Phase 2: Transkribieren

```bash
SK=.claude/skills/video-shortform
DATA="$(bash "$SK/scripts/resolve-datadir.sh")"   # writable: skill root (Claude Code) or cache (Cowork)
PY="$DATA/.venv/bin/python"
RAWDIR="$(dirname "{video}")"        # raw video folder = output folder
EDIT="$RAWDIR/_work/edit"            # edit cache next to the raw file (gitignored)
$PY $SK/helpers/transcribe.py "{video}" --edit-dir "$EDIT"
$PY $SK/helpers/pack_transcripts.py --edit-dir "$EDIT" --silence-threshold 0.4
```

Transkript ist gecached (kein Re-Transkribieren, ausser Source aenderte sich). Dieser Skill nutzt Scribe (Word-Timestamps, Diarisierung); Policy siehe `$SK/references/transcription.md`. Kein lokaler Whisper-Fallback - ist Scribe nicht erreichbar, stoppt der Lauf mit klarer Meldung.

---

### Phase 3: Text-Hook generieren (Stop-Punkt, Pflicht)

Der **Text-Hook** ist der scroll-stopping On-Screen-Text, der übers Video gelegt wird. Er entscheidet in den ersten Sekunden über Weiterwischen oder Bleiben - **kein optionales Extra, sondern Pflicht** bei jedem Short.

1. Aus dem Transkript (worum geht's, was ist der Payoff) + `icp.md` (was stoppt genau diese Zielgruppe) **3 Hook-Varianten** generieren. Liegt ein Skript vor (Phase 1d), den Hook daran ausrichten.
2. Die 3 Varianten zeigen und **bestätigen lassen** (User wählt eine oder gibt eine Richtung vor). Das ist der **einzige** Bestätigungspunkt im Ablauf.
3. **Batch:** für **jedes** Video eigene 3 Hooks generieren und **einzeln** bestätigen lassen.

Der gewählte Hook wird in Phase 5 als Overlay über den Cut gelegt - Platzierung nach `$SK/references/safe-zone.md` (oberer/mittlerer Safe-Zone-Bereich, nie unter die Plattform-UI).

---

### Phase 4: Schnitt planen (LLM-Reasoning)

**Pflicht-Lektuere zuerst:**
- `$SK/references/cut-standards.md` - Padding-Tabelle, Pre-Cut-Checks, Last-Word-Two-Step, EDL-Format.
- `$SK/references/hard-rules.md` - Hard Rules (nie im Wort schneiden, Subtitles zuletzt im Filter, 30ms Audio-Fades, etc.).

Aus `{EDIT}/takes_packed.md` den Cut planen, Silence-Map + verdaechtige Sub-Slices laut cut-standards.md pruefen. EDL als JSON mit `_padding_params`-Block schreiben. Drill-down nur bei Bedarf via `timeline_view.py`. **Liegt ein Skript vor (Phase 1d):** den Schnitt an der Skript-Struktur ausrichten; bei mehreren Videos jeden Clip auf seinen Skript-Beat schneiden.

---

### Phase 5: Cut rendern (ohne Untertitel)

Den geschnittenen Cut bauen - **ohne** Untertitel. Die kommen beatgenau erst in Phase 7 (auf dem fertigen Cut). Text-Hook + Grade werden hier eingebrannt, der Cut landet im Edit-Cache:

```bash
SK=.claude/skills/video-shortform
DATA="$(bash "$SK/scripts/resolve-datadir.sh")"   # writable: skill root (Claude Code) or cache (Cowork)
PY="$DATA/.venv/bin/python"
RAWDIR="$(dirname "{video}")"        # raw video folder = output folder
EDIT="$RAWDIR/_work/edit"
$PY $SK/helpers/render.py "$EDIT/edl.json" \
  -o "$EDIT/cut.mp4" --no-subtitles
```

- **Text-Hook:** den in Phase 3 gewählten Hook als On-Screen-Text in den Cut einbrennen - oberer/mittlerer Safe-Zone-Bereich (`$SK/references/safe-zone.md`), Brand-CI-Farben/Fonts. Als ffmpeg-Text-Overlay, oder bei aktiven Motion Graphics als Motion-Layer (Phase 6). **Kein Logo.**
- **Grade-Optionen** (EDL-Feld `grade`): Preset (z.B. `warm_cinematic`), `auto`, roher ffmpeg-Filter oder 3D-LUT (`"grade": "lut:/pfad/look.cube"`). grade.py standalone: `--lut look.cube`.
- **Resumierbar + atomar:** render.py überspringt bereits gerenderte Segmente (ffprobe) und schreibt atomar (`.part.mp4` -> rename); abgebrochen -> denselben Befehl erneut aufrufen. Optional `--budget-seconds N`.
- **Hard Rule:** nie auf Schwarz starten/enden (erstes + letztes Frame ist Content).

---

### Phase 6: Motion Graphics (optional, hyperframes)

Nur wenn in Phase 1 gewuenscht. Voraussetzung: Chromium (Doctor zeigt OK).

- `DATA=$(bash $SK/scripts/resolve-datadir.sh)` (dort liegen node_modules + Chromium, s. Phase 0).
- Lektuere: `$SK/references/motion-style.md` (Anchor-Word-Sync, Render-Defaults) + hyperframes-Skill in `$DATA/engines/hyperframes/node_modules/hyperframes/dist/skills/hyperframes/SKILL.md`.
- Brand: Farben/Fonts aus dem `ci.md`-Frontmatter (`colors`, `fonts`). **Kein Logo einblenden**, auch wenn die CI ein `logo` definiert. Hooks/CTA via `icp`-Skill.
- Compositions bauen, Puppeteer-Render (Executable-Path aus `$DATA/engines/hyperframes/.chromium-path`), Overlays nach cut-standards/motion-style ueber den Cut legen.

---

### Phase 7: Untertitel (beatgenau, via /video-captions)

Der Cut steht fest - **jetzt** die Untertitel. Wichtig: **nicht** aus dem Roh-Transkript hochrechnen (das driftet durch Padding/Fades gegen die echte Cut-Timeline), sondern den **fertigen Cut neu transkribieren**, damit die Wort-Zeiten exakt auf der Cut-Timeline sitzen.

Genau das ist der Job von `/video-captions`. shortform liefert nur den fertigen Cut und übergibt:
- **Eingabe:** `$EDIT/cut.mp4` (fertig geschnitten, inkl. Hook/Overlays).
- **Ziel:** `{slug}.mp4` neben dem Roh-Video (nicht der captions-Default-Name).

`/video-captions` transkribiert den Cut neu, baut die SRT 1:1 aus diesem Transkript (kein Offset), wendet Safe-Zone + feste Caption-Oberkante (kein Springen) + CI-Farbe/Font an und brennt ein. So lebt die Caption-Logik an **einer** Stelle. (Soll der Short keine Untertitel haben: Phase 7 überspringen, `cut.mp4` direkt als `{slug}.mp4` ablegen.)

---

### Phase 8: Self-Eval + Ablegen

- **Self-Eval (einmal):** fertiges `{slug}.mp4` stichprobenartig gegen die EDL pruefen (Schnitt-im-Wort) per `timeline_view` an den Schnitt-Raendern. Zusätzlich: Text-Hook + Untertitel in der Safe Zone, Caption-Oberkante springt nicht, **erstes + letztes Frame sind Content (nie Schwarz)**. Nicht pro Render.
- **Ablage (OS-Convention):** `_index.md` neben das Raw-File schreiben (getrackt), `{slug}.mp4` daneben, Media/Cache bleibt in `_work/` (gitignored):

```markdown
# {Titel}
- Brand: {brand}  | Format: {9:16}
- Text-Hook: {gewählter Hook}
- Status: Postfertig
- Render: {slug}.mp4
- Datum: {YYYY-MM-DD}
```

- Daily-Log-Notiz in `{logs}/{YYYY-MM-DD}.md` ergaenzen.

---

## Output

Landet IMMER im selben Ordner wie das Roh-Video (kein neuer datierter Ordner):
- `{slug}.mp4` (postfertiges Reel/Short, sprechender Name) + getracktes `_index.md` direkt neben dem Raw-File.
- Schnitt-Cache (Transkript, EDL, SRT, takes_packed) in `_work/edit/` (gitignored).
- Daily-Log-Notiz in `{logs}/{YYYY-MM-DD}.md`.

## Verwandte Skills

### Kontext-Bridge (Pflicht, Projekt-Skills haben Vorrang)

- **brand-voice** fuer Untertitel-/Text-Ton (`{context}/brands/{brand}/voice-profile.md`, Fallback `voice.md`).
- **icp** fuer Hook/CTA-Bewertung (`{context}/brands/{brand}/icp.md`).
- **CI** aus `{context}/brands/{brand}/ci.md` (YAML-Frontmatter: `colors`, `fonts`, `logo`, `handle`, `name`, `assets_dir`). Angelegt/gepflegt von `/brand-ci` (dort Schema + Beispiel); gleiche `ci.md` nutzt auch `/carousel`.

### Abgrenzung

- Baut das **postfertige** Reel/Short. Den Untertitel-Schritt **delegiert** shortform an `/video-captions` (beatgenau auf dem fertigen Cut). Wer im NLE finishen will → `/video-roughcut` (Rohschnitt + DaVinci/Premiere-Export). Nur Untertitel auf ein fertiges Video → `/video-captions` direkt. Footage sichten/Highlights finden → `/video-footage-mining`.
- CI anlegen → `/brand-ci`, Voice-Profil → `/brand-voice`, ICP → `/icp`, statische Karussells → `/carousel`.
