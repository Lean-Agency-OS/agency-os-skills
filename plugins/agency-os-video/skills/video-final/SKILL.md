---
name: video-final
version: 1.0.0
description: Schneidet ein Roh-Video zum postfertigen Reel/Short - Transkript, Schnitt, Untertitel, optional Color-Grade + Motion-Graphics, Final-Render. Triggert bei "mach ein Reel draus", "bau ein Short aus diesem Video", "schneid mir das Video fertig", "postfertiges Reel", "/video-final". Brand-aware ueber {context}/brands/{brand}/, nutzt brand-voice + icp. Output landet IMMER im selben Ordner wie das Roh-Video.
---

# Skill: video-final

Du schneidest als **Senior Short-Form-Editor**: du denkst in Hook, Pacing und Daumenstopp, nicht in Rohmaterial. **Dein Ziel:** ein postfertiges Social-Video ohne Editor-Zeit, das Watch-Time hält und auf die eine Handlung zieht.

**Zweck:** Aus einem Roh-Video ein **sendefertiges** Reel/Short bauen, fertig zum Posten (kein weiterer Schnittprogramm-Schritt nötig). Für die Variante "ich finishe selbst im NLE" gibt es `/video-roughcut`.

**Brand:** die im Brain konfigurierte Brand (Ordner unter `{context}/brands/`). Gibt es nur einen, den nehmen; bei mehreren die mit `brand-config.md` `status: active`. Kein fester Default-Name.

**Brand-Pfade & CI:** `{context}/brands/{brand}/` ist ein Default - existiert `.agency-os/architecture.md` im Projekt-Root (Rolle→Pfad-Map vom `agency-os-start`-Skill), den `context`-Pfad daraus nehmen. Die Brand-CI liegt als **`ci.md` mit YAML-Frontmatter** (`colors`, `fonts`, `handle`, `name`, `assets_dir`, `logo`) im Brand-Ordner - dieselbe Datei und dasselbe Schema nutzt `/carousel`. Werte aus dem Frontmatter lesen und an die Helfer (ffmpeg/PIL) durchreichen.

**Zwei Phasen:** Phase 1 = Schnitt + Untertitel (reines ffmpeg). Phase 5 = Motion Graphics via hyperframes (braucht Chromium).

---

## Methodik

### Struktur (self-contained Skill)

- `helpers/` - Schnitt-Engine (Python, ElevenLabs Scribe, ffmpeg). Interpreter: `.venv/bin/python` (Setup baut das venv im Skill-Root).
- `engines/hyperframes/` - Motion-Graphics-Engine (Node, hyperframes per npm in `node_modules`).
- `references/cut-standards.md` - **die** Quelle fuer Padding, Silence-Checks, Last-Word-Two-Step, EDL-Format.
- `references/motion-style.md` - projekt-eigene Motion-Regeln (Anchor-Word-Sync, Render-Defaults). Foundation: hyperframes house-style.md / visual-styles.md in `node_modules`.
- `references/hard-rules.md` - die Hard Rules der Schnitt-Engine (Referenz, kein eigener Trigger).
- `references/transcription.md` - Transkriptions-Policy: Scribe als Pfad, Word-Level-Pflicht. Dieser Skill ist Scribe-only (kein lokaler Whisper-Fallback).

Der Code ist aus der geteilten `video-engine`-Quelle gevendort (siehe `packages/video-engine/` im Repo). **Nicht hier editieren** - Änderungen in der Quelle machen und `tools/sync-engine.sh` laufen lassen.

Abkuerzung in den Befehlen unten: `SK=.claude/skills/video-final` (Aufruf vom OS-Root). Den `{context}`-Pfad wie oben beschrieben auflösen.

---

## Workflow

### Phase 0: Setup-Gate (PFLICHT, still)

1. Existiert `$SK/.ready`? Nein -> `bash $SK/scripts/setup.sh`, Ausgabe zeigen.
2. `{context}` auflösen, dann `bash $SK/scripts/doctor.sh "{context}/secrets.env"`. Bei `OFFEN ELEVENLABS_API_KEY` -> Nutzer bitten, den Key in `{context}/secrets.env` einzutragen (Vorlage: `$SK/secrets.env.example`), dann stoppen.
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
SK=.claude/skills/video-final
PY=$SK/.venv/bin/python
RAWDIR="$(dirname "{video}")"        # raw video folder = output folder
EDIT="$RAWDIR/_work/edit"            # edit cache next to the raw file (gitignored)
$PY $SK/helpers/transcribe.py "{video}" --edit-dir "$EDIT"
$PY $SK/helpers/pack_transcripts.py --edit-dir "$EDIT" --silence-threshold 0.4
```

Transkript ist gecached (kein Re-Transkribieren, ausser Source aenderte sich). Dieser Skill nutzt Scribe (Word-Timestamps, Diarisierung); Policy siehe `$SK/references/transcription.md`. Kein lokaler Whisper-Fallback - ist Scribe nicht erreichbar, stoppt der Lauf mit klarer Meldung.

---

### Phase 3: Schnitt planen (LLM-Reasoning)

**Pflicht-Lektuere zuerst:**
- `$SK/references/cut-standards.md` - Padding-Tabelle, Pre-Cut-Checks, Last-Word-Two-Step, EDL-Format.
- `$SK/references/hard-rules.md` - Hard Rules (nie im Wort schneiden, Subtitles zuletzt im Filter, 30ms Audio-Fades, etc.).

Aus `{EDIT}/takes_packed.md` den Cut planen, Silence-Map + verdaechtige Sub-Slices laut cut-standards.md pruefen. EDL als JSON mit `_padding_params`-Block schreiben. Drill-down nur bei Bedarf via `timeline_view.py`.

---

### Phase 4: Render

```bash
SK=.claude/skills/video-final
PY=$SK/.venv/bin/python
RAWDIR="$(dirname "{video}")"        # raw video folder = output folder
$PY $SK/helpers/render.py "{EDIT}/edl.json" \
  -o "$RAWDIR/final.mp4" --build-subtitles   # final.mp4 right next to the raw file
```

Untertitel-Ton vor dem Burn-in via `brand-voice`-Skill gegen das Brand-Profil pruefen. Subtitle-Farbe/Font aus dem `ci.md`-Frontmatter (`colors.subtitle`, `fonts.subtitle` / `fonts.subtitle_path`).

**Grade-Optionen** (EDL-Feld `grade`): Preset-Name (z.B. `warm_cinematic`), `auto` (datengetriebene Korrektur pro Segment), roher ffmpeg-Filter, oder ein 3D-LUT via `"grade": "lut:/pfad/look.cube"` (wird nach dem HDR->709-Tonemap angewandt). grade.py standalone: `--lut look.cube`.

---

### Phase 5: Motion Graphics (optional, hyperframes)

Nur wenn in Phase 1 gewuenscht. Voraussetzung: Chromium (Doctor zeigt OK).

- Lektuere: `$SK/references/motion-style.md` (Anchor-Word-Sync, Render-Defaults) + hyperframes-Skill in `$SK/engines/hyperframes/node_modules/hyperframes/dist/skills/hyperframes/SKILL.md`.
- Brand: Farben/Fonts/Logo aus dem `ci.md`-Frontmatter (`colors`, `fonts`, `logo`). Hooks/CTA via `icp`-Skill.
- Compositions bauen, Puppeteer-Render (Executable-Path aus `$SK/engines/hyperframes/.chromium-path`), Overlays nach cut-standards/motion-style ueber den Cut legen.

---

### Phase 6: Self-Eval + Ablegen

- **Self-Eval (einmal):** fertigen Cut gegen die EDL pruefen (Schnitt-im-Wort + Untertitel-Leaks) per `timeline_view`-Stichproben an den Schnitt-Raendern. Nicht pro Render.
- **Ablage (OS-Convention):** `_index.md` neben das Raw-File schreiben (getrackt), `final.mp4` daneben, Media/Cache bleibt in `_work/` (gitignored):

```markdown
# {Titel}
- Brand: {brand}  | Format: {9:16}
- Hook: {1 Satz}
- Status: Postfertig
- Render: final.mp4
- Datum: {YYYY-MM-DD}
```

- Daily-Log-Notiz in `{logs}/{YYYY-MM-DD}.md` ergaenzen.

---

## Output

Landet IMMER im selben Ordner wie das Roh-Video (kein neuer datierter Ordner):
- `final.mp4` (postfertiges Reel/Short) + getracktes `_index.md` direkt neben dem Raw-File.
- Schnitt-Cache (Transkript, EDL, SRT, takes_packed) in `_work/edit/` (gitignored).
- Daily-Log-Notiz in `{logs}/{YYYY-MM-DD}.md`.

## Verwandte Skills

### Kontext-Bridge (Pflicht, Projekt-Skills haben Vorrang)

- **brand-voice** fuer Untertitel-/Text-Ton (`{context}/brands/{brand}/voice-profile.md`, Fallback `voice.md`).
- **icp** fuer Hook/CTA-Bewertung (`{context}/brands/{brand}/icp.md`).
- **CI** aus `{context}/brands/{brand}/ci.md` (YAML-Frontmatter: `colors`, `fonts`, `logo`, `handle`, `name`, `assets_dir`). Angelegt/gepflegt von `/brand-ci` (dort Schema + Beispiel); gleiche `ci.md` nutzt auch `/carousel`.

### Abgrenzung

- Baut das **postfertige** Reel/Short. Wer im NLE finishen will → `/video-roughcut` (Rohschnitt + DaVinci/Premiere-Export). Nur Untertitel auf ein fertiges Video → `/video-captions`. Footage sichten/Highlights finden → `/video-footage-mining`.
- CI anlegen → `/brand-ci`, Voice-Profil → `/brand-voice`, ICP → `/icp`, statische Karussells → `/carousel`.
