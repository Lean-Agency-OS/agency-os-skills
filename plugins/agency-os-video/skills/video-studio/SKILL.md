---
name: video-studio
version: 1.1.0
description: Schneidet Roh-Videos zu fertigen Reels/Shorts/Clips - Transkript, Schnitt, Untertitel, Motion Graphics, Render. Triggert bei "schneid das Video", "mach ein Reel draus", "bau ein Short aus diesem Video", "/video", "/reel", "kuerz das Video", "Untertitel aufs Video", "video-studio". Brand-aware ueber {context}/brands/{brand}/, nutzt brand-voice + icp. Output landet IMMER im selben Ordner wie das Roh-Video.
---

# Skill: video-studio

**Zweck:** Aus einem Roh-Video ein sendefertiges Reel/Short bauen. EIN Einstiegspunkt - die Engines laufen intern dahinter, der Nutzer sieht nur diesen Skill.

**Brand:** die im Brain konfigurierte Brand (Ordner unter `{context}/brands/`). Gibt es nur einen, den nehmen; bei mehreren die mit `brand-config.md` `status: active`. Kein fester Default-Name.

**Brand-Pfade & CI:** `{context}/brands/{brand}/` ist ein Default - existiert `.agency-os/architecture.md` im Projekt-Root (Rolle→Pfad-Map vom `agency-os-start`-Skill), den `context`-Pfad daraus nehmen. Die Brand-CI liegt als **`ci.md` mit YAML-Frontmatter** (`colors`, `fonts`, `handle`, `name`, `assets_dir`, `logo`) im Brand-Ordner - dieselbe Datei und dasselbe Schema nutzt `/carousel`. Werte aus dem Frontmatter lesen und an die Helfer (ffmpeg/PIL) durchreichen.

**Zwei Phasen:** Phase 1 = Schnitt + Untertitel (reines ffmpeg). Phase 2 = Motion Graphics via hyperframes (braucht Chromium).

---

## Methodik

### Struktur (alles in diesem Skill, self-contained)

- `helpers/` - Schnitt-Engine (Python, ElevenLabs Scribe, ffmpeg). Interpreter: `.venv/bin/python` (Setup baut das venv im Skill-Root).
- `engines/hyperframes/` - Motion-Graphics-Engine (Node, hyperframes per npm in `node_modules`).
- `references/cut-standards.md` - **die** Quelle fuer Padding, Silence-Checks, Last-Word-Two-Step, EDL-Format.
- `references/motion-style.md` - projekt-eigene Motion-Regeln (Anchor-Word-Sync, Render-Defaults). Foundation: hyperframes house-style.md / visual-styles.md in `node_modules`.
- `references/hard-rules.md` - die Hard Rules der Schnitt-Engine (Referenz, kein eigener Trigger).
- `references/transcription.md` - Transkriptions-Policy: welche Engine wofuer (Scribe vs. lokales Whisper), Word-Level-Pflicht, Fallback-Kette.
- `.env` - `ELEVENLABS_API_KEY`.

Abkuerzung in den Befehlen unten: `VS=.claude/skills/video-studio` (Aufruf vom OS-Root).

---

## Workflow

### Phase 0: Setup-Gate (PFLICHT, still)

1. Existiert `$VS/.ready`? Nein -> `bash $VS/scripts/setup.sh`, Ausgabe zeigen.
2. `bash $VS/scripts/doctor.sh`. Bei `OFFEN ELEVENLABS_API_KEY` -> Nutzer bitten, Key in `$VS/.env` einzutragen, dann stoppen.
3. Bei `FEHLT ffmpeg/node/python` -> Hard-Stop (Sandbox ohne Tools).

Nur wenn Doctor sauber -> weiter.

---

### Phase 1: Brief + Plan (Stop-Punkt, Deutsch)

**1a. Inputs:** Roh-Video-Pfad; Brand (aktive Brand aus `{context}/brands/`); Format `9:16` (default), `16:9` oder `1:1`; Untertitel ja/nein; Motion Graphics ja/nein.

**1b. Ordner:** Output landet IMMER im **selben Ordner wie das Roh-Video** (kein neuer datierter Ordner). Liegt das Raw-File z. B. in `<ordner-des-rohvideos>/IMG_8762.MOV`, dann:
- `final.mp4` + `_index.md` direkt in `<ordner-des-rohvideos>/`
- Schnitt-Cache (Transkript, EDL, SRT, takes_packed) in `<ordner-des-rohvideos>/_work/edit/` (gitignored)

So bleiben Raw und fertiger Schnitt zusammen. Den Edit-Cache nie neu transkribieren, wenn das Raw-File unveraendert ist.

**1c. Plan auf Deutsch bestaetigen lassen** (Pflicht - kein Schnitt ohne OK). Plain Language:

```
Kurz-Plan:
- Video: {dateiname}  | Brand: {brand} | Format: {9:16} | Untertitel: {ja} | Motion Graphics: {ja/nein}
- Ich transkribiere, schneide Fueller/Pausen/Versprecher raus, setze saubere Schnitt-Raender,
  {brenne Untertitel ein,} {baue Overlays,} und rendere.
Passt das so? Dann lege ich los.
```

Erst nach OK -> Phase 2.

---

### Phase 2: Transkribieren

```bash
VS=.claude/skills/video-studio
PY=$VS/.venv/bin/python
RAWDIR="$(dirname "{video}")"        # Ordner des Roh-Videos = Output-Ordner
EDIT="$RAWDIR/_work/edit"            # Schnitt-Cache neben dem Raw-File (gitignored)
$PY $VS/helpers/transcribe.py "{video}" --edit-dir "$EDIT"
$PY $VS/helpers/pack_transcripts.py --edit-dir "$EDIT" --silence-threshold 0.4
```

Transkript ist gecached (kein Re-Transkribieren, ausser Source aenderte sich).

Engine-Wahl + Fallback: siehe `$VS/references/transcription.md`. Kurz: Default `scribe` (genau, diarisiert, Word-Timestamps); `--engine whisper` fuer den schnellen lokalen Rough-Pass (braucht `uv pip install -e '.[whisper]'`); ist Scribe nicht erreichbar, faellt es automatisch auf lokales Whisper zurueck (Word-Timestamps bleiben, keine Diarisierung), abschaltbar mit `--no-fallback`.

---

### Phase 3: Schnitt planen (LLM-Reasoning)

**Pflicht-Lektuere zuerst:**
- `$VS/references/cut-standards.md` - Padding-Tabelle, Pre-Cut-Checks, Last-Word-Two-Step, EDL-Format.
- `$VS/references/hard-rules.md` - Hard Rules (nie im Wort schneiden, Subtitles zuletzt im Filter, 30ms Audio-Fades, etc.).

Aus `{EDIT}/takes_packed.md` den Cut planen, Silence-Map + verdaechtige Sub-Slices laut cut-standards.md pruefen. EDL als JSON mit `_padding_params`-Block schreiben. Drill-down nur bei Bedarf via `timeline_view.py`.

---

### Phase 4: Render

```bash
VS=.claude/skills/video-studio
PY=$VS/.venv/bin/python
RAWDIR="$(dirname "{video}")"        # Ordner des Roh-Videos = Output-Ordner
$PY $VS/helpers/render.py "{EDIT}/edl.json" \
  -o "$RAWDIR/final.mp4" --build-subtitles   # final.mp4 direkt neben das Raw-File
```

Untertitel-Ton vor dem Burn-in via `brand-voice`-Skill gegen das Brand-Profil pruefen. Subtitle-Farbe/Font aus dem `ci.md`-Frontmatter (`colors.subtitle`, `fonts.subtitle` / `fonts.subtitle_path`).

**Grade-Optionen** (EDL-Feld `grade`): Preset-Name (z.B. `warm_cinematic`), `auto` (datengetriebene Korrektur pro Segment), roher ffmpeg-Filter, oder ein 3D-LUT via `"grade": "lut:/pfad/look.cube"` (wird nach dem HDR->709-Tonemap angewandt). grade.py standalone: `--lut look.cube`.

**NLE-Export (optional):** Schnitt zum Finishen nach DaVinci Resolve / Premiere geben:
```bash
# DaVinci Resolve (FCPXML): vertikale 9:16-Timeline, Captions eingebettet,
# Medienpfad vom Cowork-Sandbox auf den echten Mac-Pfad umbiegen:
$PY $VS/helpers/export_nle.py "{EDIT}/edl.json" -o "$RAWDIR/final.fcpxml" --fps 24 \
  --width 1080 --height 1920 --captions --caption-color FED760 \
  --remap "/sessions/<id>/mnt/<Projekt>=/Users/<user>/Documents/<Projekt>"

# Adobe Premiere (FCP7-XML) oder beide Formate auf einmal:
$PY $VS/helpers/export_nle.py "{EDIT}/edl.json" --format both --width 1080 --height 1920
```
Exportiert nur den Schnitt (Clip-Auswahl + Timing, referenziert die Original-Files).
Grade/Overlays bewusst NICHT - die macht der Editor nativ im NLE. Optionen:
- `--width/--height` setzt das Timeline-Raster (z.B. 1080x1920 vertikal); ohne Angabe = Quell-Dimension. Quell-Assets behalten ihr natives Format, sodass rotierte/Querformat-Quellen sauber konformen.
- `--captions` bettet Untertitel aus `transcripts/<src>.json` (gleiches 2-Wort-Chunking wie der Burn-in) als Subtitle-Spur ein (nur FCPXML). `--caption-color` (Hex) setzt die Fuellfarbe.
- `--format premiere|both` schreibt zusaetzlich FCP7-XML (xmeml) fuer aeltere Premiere-Versionen; dort Captions ueber die SRT importieren.
- `--remap FROM=TO` (wiederholbar) biegt Medienpfade um (Cowork-Sandbox -> Mac), damit die NLE die Footage findet.

---

### Phase 5: Motion Graphics (optional, hyperframes)

Nur wenn in Phase 1 gewuenscht. Voraussetzung: Chromium (Doctor zeigt OK).

- Lektuere: `$VS/references/motion-style.md` (Anchor-Word-Sync, Render-Defaults) + hyperframes-Skill in `$VS/engines/hyperframes/node_modules/hyperframes/dist/skills/hyperframes/SKILL.md`.
- Brand: Farben/Fonts/Logo aus dem `ci.md`-Frontmatter (`colors`, `fonts`, `logo`). Hooks/CTA via `icp`-Skill.
- Compositions bauen, Puppeteer-Render (Executable-Path aus `$VS/engines/hyperframes/.chromium-path`), Overlays nach cut-standards/motion-style ueber den Cut legen.

---

### Phase 6: Self-Eval + Ablegen

- **Self-Eval (einmal):** fertigen Cut gegen die EDL pruefen (Schnitt-im-Wort + Untertitel-Leaks) per `timeline_view`-Stichproben an den Schnitt-Raendern. Nicht pro Render.
- **Ablage (OS-Convention):** `_index.md` neben das Raw-File schreiben (getrackt), `final.mp4` daneben, Media/Cache bleibt in `_work/` (gitignored):

```markdown
# {Titel}
- Brand: {brand}  | Format: {9:16}
- Hook: {1 Satz}
- Status: Rohschnitt fertig
- Render: _work/final.mp4
- Datum: {YYYY-MM-DD}
```

- Daily-Log-Notiz in `{logs}/{YYYY-MM-DD}.md` ergaenzen.

---

## Output

Landet IMMER im selben Ordner wie das Roh-Video (kein neuer datierter Ordner):
- `final.mp4` (fertiges Reel/Short) + getracktes `_index.md` direkt neben dem Raw-File.
- Schnitt-Cache (Transkript, EDL, SRT, takes_packed) in `_work/edit/` (gitignored).
- Optional NLE-Export (`final.fcpxml` / FCP7-XML) zum Finishen in DaVinci Resolve / Premiere.
- Daily-Log-Notiz in `{logs}/{YYYY-MM-DD}.md`.

## Verwandte Skills

### Kontext-Bridge (Pflicht, Projekt-Skills haben Vorrang)

- **brand-voice** fuer Untertitel-/Text-Ton (`{context}/brands/{brand}/voice-profile.md`, Fallback `voice.md`).
- **icp** fuer Hook/CTA-Bewertung (`{context}/brands/{brand}/icp.md`).
- **CI** aus `{context}/brands/{brand}/ci.md` (YAML-Frontmatter: `colors`, `fonts`, `logo`, `handle`, `name`, `assets_dir`). Angelegt/gepflegt von `/brand-ci` (dort Schema + Beispiel); gleiche `ci.md` nutzt auch `/carousel`.

### Abgrenzung

- Schneidet nur Video (Reel/Short/Clip). CI anlegen → `/brand-ci`, Voice-Profil → `/brand-voice`, ICP → `/icp`, statische Karussells → `/carousel`.
