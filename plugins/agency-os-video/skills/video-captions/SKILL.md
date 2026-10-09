---
name: video-captions
version: 2.1.1
description: Legt markenkonforme Untertitel zu einem bereits fertig geschnittenen Video an - transkribiert, baut Caption-Chunks, wahlweise eingebrannt (gestyltes ASS mit CI-Farbe, Schrift, Position und Schatten) oder als SRT-Datei daneben. Kein Schnitt. Untertitel entstehen immer hier; /video-shortform und /video-longform rufen diesen Skill auf, statt selbst welche zu bauen. Triggert bei "Untertitel aufs Video", "Captions einbrennen", "Subtitles fuer das Video", "burn captions", "/video-captions". Brand-aware ueber {context}/brand/, nutzt brand-voice + CI.
---

# Skill: video-captions

Du arbeitest als **Senior Captions-Editor**: du denkst in Lesbarkeit und Timing, nicht in Schnitt. **Dein Ziel:** markenkonforme, gut getimte Untertitel, die die Watch-Time halten - sauber lesbar, nie im Bild verrutscht.

**Zweck:** Auf ein **schon fertig geschnittenes** Video markenkonforme Untertitel einbrennen. Kein Schnitt, kein Grade. Wer aus Rohmaterial schneiden will → `/video-shortform` (postfertig) oder `/video-roughcut` (NLE).

**Brand-Pfade & CI:** die Brand-CI liegt in `{context}/brand/ci.md`. Existiert `.agency-os/architecture.md` im Projekt-Root, den `context`-Pfad daraus nehmen. Subtitle-Farbe/Font aus dem `ci.md`-Frontmatter (`colors.subtitle`, `fonts.subtitle` / `fonts.subtitle_path`).

---

## Methodik

### Struktur (self-contained Skill)

- `helpers/` - Transkriptions-/Render-Helfer (Python, ElevenLabs Scribe, ffmpeg). Interpreter: `.venv/bin/python` (Setup baut das venv im Skill-Root).
- `references/safe-zone.md` - **Pflicht:** wohin Untertitel dürfen (9:16), feste obere Caption-Kante, kein Springen.
- `references/transcription.md` - Transkriptions-Policy. Scribe-only (kein lokaler Whisper-Fallback).

Der Code ist aus der geteilten `video-engine`-Quelle gevendort. **Nicht hier editieren** - Änderungen in der Quelle machen und `tools/sync-engine.sh` laufen lassen.

Abkuerzung: `SK=.claude/skills/video-captions` (Aufruf vom OS-Root). Den `{context}`-Pfad wie oben auflösen.

---

## Workflow

### Phase 0: Setup-Gate (PFLICHT, still)

1. `DATA=$(bash $SK/scripts/resolve-datadir.sh)` (schreibbares Daten-Verzeichnis: Skill-Root in Claude Code, Cache in Cowork). Fehlt `$DATA/.ready` -> `bash $SK/scripts/setup.sh`, Ausgabe zeigen.
2. `{context}` auflösen, dann `bash $SK/scripts/doctor.sh "{context}/secrets.env"`. Bei `OFFEN ELEVENLABS_API_KEY` -> Nutzer bitten, den Key in `{context}/secrets.env` einzutragen (Vorlage: `$SK/secrets.env.example`), dann stoppen.
3. Bei `FEHLT ffmpeg/python` -> Hard-Stop. (Node/Chromium braucht dieser Skill nicht.)

Nur wenn Doctor sauber -> weiter.

---

### Phase 1: Brief (Stop-Punkt, Deutsch)

**1a. Inputs:** Pfad zum **fertig geschnittenen** Video; **Modus** (eingebrannt = Default, oder SRT-Datei daneben); Sprache, falls nicht offensichtlich. Stil, Farbe und Schrift kommen aus `{context}/brand/ci.md`.

Ruft ein anderer Skill (`/video-shortform`, `/video-longform`) hier herein, gibt er Video, Modus und Ziel-Dateinamen mit. Untertitel entstehen **immer** hier, nie im aufrufenden Skill.

**1b. Ordner:** Output landet IMMER im **selben Ordner wie das Video**. Transkript/Cache in `<ordner>/_work/edit/` (gitignored), `{quell-stem}-captioned.mp4` direkt daneben.

**1c. Bestaetigen** (Pflicht): *"Ich transkribiere das Video und lege die Untertitel in der Brand-CI an (eingebrannt / als SRT). Kein Schnitt. Passt das?"* Erst nach OK -> Phase 2. Kommt der Aufruf aus einem anderen Video-Skill, der schon bestaetigt hat: nicht erneut fragen.

---

### Phase 2: Transkribieren

```bash
SK=.claude/skills/video-captions
DATA="$(bash "$SK/scripts/resolve-datadir.sh")"   # writable: skill root (Claude Code) or cache (Cowork)
PY="$DATA/.venv/bin/python"
RAWDIR="$(dirname "{video}")"        # video folder = output folder
EDIT="$RAWDIR/_work/edit"            # cache next to the file (gitignored)
$PY $SK/helpers/transcribe.py "{video}" --edit-dir "$EDIT"
```

Transkript ist gecached (Word-Timestamps). Scribe-only - ist Scribe nicht erreichbar, stoppt der Lauf mit klarer Meldung (Policy: `$SK/references/transcription.md`).

**Beatgenau:** Weil hier das **fertig geschnittene** Video transkribiert wird, sitzen die Wort-Zeiten direkt auf der finalen Timeline - kein Hochrechnen aus Schnitt-Offsets, kein Drift. Genau deshalb ruft `/video-shortform` für seine Untertitel diesen Skill auf dem fertigen Cut auf.

---

### Phase 3: Untertitel anlegen

**Modus SRT-Datei:** nur die Sidecar-Datei bauen, nichts rendern, fertig nach diesem Schritt:

```bash
$PY $SK/helpers/make_srt.py "$EDIT/transcripts/{quell-stem}.json" -o "$RAWDIR/{ziel-stem}.srt"
```

**Modus eingebrannt (Default):** Da nicht geschnitten wird, ist die EDL ein **einziges Segment über die volle Laenge**. Dauer per ffprobe holen, eine minimale EDL schreiben (`grade: null`, ein Segment `start: 0` bis `dauer`), dann die gestylten Untertitel bauen und brennen:

```bash
SK=.claude/skills/video-captions
DATA="$(bash "$SK/scripts/resolve-datadir.sh")"   # writable: skill root (Claude Code) or cache (Cowork)
PY="$DATA/.venv/bin/python"
RAWDIR="$(dirname "{video}")"
EDIT="$RAWDIR/_work/edit"
CI="{context}/brand/ci.md"
# 1. Zielaufloesung holen - Schriftgroesse und Position skalieren proportional mit
# nk=1:nw=1, NICHT csv=p=0: ffprobe 8 haengt dort ein Komma an ("1080,")
W="$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of default=nk=1:nw=1 "{video}")"
H="$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of default=nk=1:nw=1 "{video}")"
# 2. Gestylte Untertitel bauen: Farbe, Schrift, Groesse, Position, Schatten und
#    Schreibweisen kommen alle aus der ci.md; ohne ci.md gelten die Referenzwerte.
$PY $SK/helpers/make_ass.py "$EDIT/transcripts/{quell-stem}.json" "$EDIT/captions.ass" \
  --width "$W" --height "$H" --ci "$CI"
# 3. Brennen: EDL mit EINEM Segment ueber die volle Laenge und "subtitles": "captions.ass".
#    Kein --build-subtitles (das waere der alte SRT-Weg), kein force_style auf ASS.
FONTDIR="$(dirname "$($PY $SK/helpers/ci_read.py "$CI" --get caption-font-path 2>/dev/null)")"
$PY $SK/helpers/render.py "$EDIT/edl.json" \
  -o "$RAWDIR/{quell-stem}-captioned.mp4" ${FONTDIR:+--fonts-dir "$FONTDIR"}
```

- **Ton-Check:** Untertitel-Text vor dem Burn-in via `brand-voice`-Skill gegen das Brand-Profil pruefen (Schreibweisen, Begriffe).
- **CI:** `make_ass.py` liest Farbe und Schrift aus der `ci.md` (Frontmatter oder Tabelle) und das Caption-Styling aus dem optionalen Frontmatter-Block `captions:` (`size`, `baseline`, `max_width`, `shadow_dy`, `shadow_blur`, `shadow_alpha`, `shadow_border`, `max_words`, `max_dur`, `filler`, `replacements`). Alle Werte sind Referenz-Pixel bei 1080 Breite und skalieren auf jede Zielaufloesung. Fehlt ein Wert: getestete Referenz. Fehlt die CI ganz: weiss auf Referenz-Geometrie.
- **Schreibweisen:** `captions.replacements` in der `ci.md`, Form `Quelle => Cue | Cue; naechste Quelle => Cue`. Trifft auch dann, wenn das Transkript den Begriff in mehrere Woerter zerlegt; die Zeit des Originals wird auf die Cues aufgeteilt. Ohne Eintrag passiert nichts.
- **Schrift:** libass findet eine Marken-Schrift nur, wenn sie systemweit installiert ist oder `--fonts-dir` auf den Ordner der Datei zeigt (kommt aus `fonts.subtitle_path` in der CI). Fehlt die Datei, bricht `make_ass.py` mit klarer Meldung ab statt still eine Systemschrift zu nehmen.
- **Timing:** Standard sind die Transkript-Stempel. Mit `--audio "{video}"` misst `make_ass.py` stattdessen den hoerbaren Wortanfang im Ton und zieht den Wechsel dorthin (plus 50 ms). Genauer, kostet einen zusaetzlichen Durchlauf ueber die Tonspur, kein Re-Encode.
- **Safe Zone (Pflicht, `$SK/references/safe-zone.md`):** bei 9:16 die Untertitel in den unteren Safe-Zone-Bereich, **über** dem unteren 19-%-Band, nie unter die Plattform-UI.
- **Kein Springen:** feste **obere Kante** (Anchor), Captions wachsen nach unten. Die obere Kante bleibt über alle Captions hinweg auf derselben Linie, egal ob ein- oder mehrzeilig.
- **Hard Rule:** Untertitel werden zuletzt in der Filter-Chain angewandt (kein Overlay verdeckt sie).
- **Resumierbar + atomar:** render.py überspringt fertige Segmente und schreibt atomar (`.part.mp4` -> rename). Bricht ein Lauf ab, denselben Befehl erneut aufrufen; optional `--budget-seconds N`.

---

### Phase 4: Self-Eval + Ablegen

- **Self-Eval (einmal):** Stichproben pruefen, dass keine Caption im Wort bricht / über den Rand laeuft / verrutscht ist.
- **Ablage (OS-Convention):** `_index.md` neben das Video (getrackt), `{quell-stem}-captioned.mp4` daneben, Cache in `_work/` (gitignored):

```markdown
# {Titel} (Untertitel)
- Status: Untertitel eingebrannt
- Render: {quell-stem}-captioned.mp4
- Datum: {YYYY-MM-DD}
```

- Daily-Log-Notiz in `{logs}/{YYYY-MM-DD}.md` ergaenzen.

---

## Output

Im selben Ordner wie das Video, je nach Modus:
- `{quell-stem}-captioned.mp4` (Video + eingebrannte Untertitel) + getracktes `_index.md`, **oder**
- `{ziel-stem}.srt` (Sidecar-Datei, Video unveraendert).
- Transkript/Cache in `_work/edit/` (gitignored).
- Daily-Log-Notiz in `{logs}/{YYYY-MM-DD}.md`.

## Verwandte Skills

### Kontext-Bridge (Pflicht, Projekt-Skills haben Vorrang)

- **brand-voice** fuer den Untertitel-Ton (`{context}/brand/voice-profile.md`, Fallback `voice.md`).
- **CI** aus `{context}/brand/ci.md` (`colors.subtitle`, `fonts.subtitle`). Angelegt/gepflegt von `/brand-ci`.

### Abgrenzung

- Brennt nur Untertitel auf ein **fertiges** Video, schneidet nicht. Aus Rohmaterial postfertig → `/video-shortform`. Rohschnitt fürs NLE → `/video-roughcut`. Footage sichten → `/video-footage-mining`.
