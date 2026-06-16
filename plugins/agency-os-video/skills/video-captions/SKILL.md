---
name: video-captions
version: 1.0.0
description: Brennt markenkonforme Untertitel auf ein bereits fertig geschnittenes Video - transkribiert, baut Caption-Chunks, Burn-in mit CI-Farbe/Font. Kein Schnitt. Triggert bei "Untertitel aufs Video", "Captions einbrennen", "Subtitles fuer das Video", "burn captions", "/video-captions". Brand-aware ueber {context}/brands/{brand}/, nutzt brand-voice + CI.
---

# Skill: video-captions

Du arbeitest als **Senior Captions-Editor**: du denkst in Lesbarkeit und Timing, nicht in Schnitt. **Dein Ziel:** markenkonforme, gut getimte Untertitel, die die Watch-Time halten - sauber lesbar, nie im Bild verrutscht.

**Zweck:** Auf ein **schon fertig geschnittenes** Video markenkonforme Untertitel einbrennen. Kein Schnitt, kein Grade. Wer aus Rohmaterial schneiden will → `/video-shortform` (postfertig) oder `/video-roughcut` (NLE).

**Brand:** die im Brain konfigurierte Brand (Ordner unter `{context}/brands/`). Gibt es nur einen, den nehmen; bei mehreren die mit `brand-config.md` `status: active`.

**Brand-Pfade & CI:** `{context}/brands/{brand}/` ist ein Default - existiert `.agency-os/architecture.md` im Projekt-Root, den `context`-Pfad daraus nehmen. Subtitle-Farbe/Font aus dem `ci.md`-Frontmatter (`colors.subtitle`, `fonts.subtitle` / `fonts.subtitle_path`).

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

1. Existiert `$SK/.ready`? Nein -> `bash $SK/scripts/setup.sh`, Ausgabe zeigen.
2. `{context}` auflösen, dann `bash $SK/scripts/doctor.sh "{context}/secrets.env"`. Bei `OFFEN ELEVENLABS_API_KEY` -> Nutzer bitten, den Key in `{context}/secrets.env` einzutragen (Vorlage: `$SK/secrets.env.example`), dann stoppen.
3. Bei `FEHLT ffmpeg/python` -> Hard-Stop. (Node/Chromium braucht dieser Skill nicht.)

Nur wenn Doctor sauber -> weiter.

---

### Phase 1: Brief (Stop-Punkt, Deutsch)

**1a. Inputs:** Pfad zum **fertig geschnittenen** Video; Brand (für CI-Farbe/Font); Sprache, falls nicht offensichtlich.

**1b. Ordner:** Output landet IMMER im **selben Ordner wie das Video**. Transkript/Cache in `<ordner>/_work/edit/` (gitignored), `{quell-stem}-captioned.mp4` direkt daneben.

**1c. Bestaetigen** (Pflicht): *"Ich transkribiere das Video und brenne die Untertitel in {brand}-CI ein. Kein Schnitt. Passt das?"* Erst nach OK -> Phase 2.

---

### Phase 2: Transkribieren

```bash
SK=.claude/skills/video-captions
PY=$SK/.venv/bin/python
RAWDIR="$(dirname "{video}")"        # video folder = output folder
EDIT="$RAWDIR/_work/edit"            # cache next to the file (gitignored)
$PY $SK/helpers/transcribe.py "{video}" --edit-dir "$EDIT"
```

Transkript ist gecached (Word-Timestamps). Scribe-only - ist Scribe nicht erreichbar, stoppt der Lauf mit klarer Meldung (Policy: `$SK/references/transcription.md`).

---

### Phase 3: Untertitel einbrennen

Da nicht geschnitten wird, ist die EDL ein **einziges Segment über die volle Laenge**. Dauer per ffprobe holen, eine minimale EDL schreiben (`grade: null`, ein Segment `start: 0` bis `dauer`), dann mit `--build-subtitles` rendern:

```bash
SK=.claude/skills/video-captions
PY=$SK/.venv/bin/python
RAWDIR="$(dirname "{video}")"
EDIT="$RAWDIR/_work/edit"
# write {EDIT}/edl.json: one full-length segment, no grade, then:
$PY $SK/helpers/render.py "{EDIT}/edl.json" \
  -o "$RAWDIR/{quell-stem}-captioned.mp4" --build-subtitles
```

- **Ton-Check:** Untertitel-Text vor dem Burn-in via `brand-voice`-Skill gegen das Brand-Profil pruefen (Schreibweisen, Begriffe).
- **CI:** Subtitle-Farbe/Font aus dem `ci.md`-Frontmatter (`colors.subtitle`, `fonts.subtitle` / `fonts.subtitle_path`).
- **Safe Zone (Pflicht, `$SK/references/safe-zone.md`):** bei 9:16 die Untertitel in den unteren Safe-Zone-Bereich, **über** dem unteren 19-%-Band, nie unter die Plattform-UI.
- **Kein Springen:** feste **obere Kante** (Anchor), Captions wachsen nach unten. Die obere Kante bleibt über alle Captions hinweg auf derselben Linie, egal ob ein- oder mehrzeilig.
- **Hard Rule:** Untertitel werden zuletzt in der Filter-Chain angewandt (kein Overlay verdeckt sie).

---

### Phase 4: Self-Eval + Ablegen

- **Self-Eval (einmal):** Stichproben pruefen, dass keine Caption im Wort bricht / über den Rand laeuft / verrutscht ist.
- **Ablage (OS-Convention):** `_index.md` neben das Video (getrackt), `{quell-stem}-captioned.mp4` daneben, Cache in `_work/` (gitignored):

```markdown
# {Titel} (Untertitel)
- Brand: {brand}
- Status: Untertitel eingebrannt
- Render: {quell-stem}-captioned.mp4
- Datum: {YYYY-MM-DD}
```

- Daily-Log-Notiz in `{logs}/{YYYY-MM-DD}.md` ergaenzen.

---

## Output

Im selben Ordner wie das Video:
- `{quell-stem}-captioned.mp4` (Video + eingebrannte Untertitel) + getracktes `_index.md`.
- Transkript/Cache in `_work/edit/` (gitignored).
- Daily-Log-Notiz in `{logs}/{YYYY-MM-DD}.md`.

## Verwandte Skills

### Kontext-Bridge (Pflicht, Projekt-Skills haben Vorrang)

- **brand-voice** fuer den Untertitel-Ton (`{context}/brands/{brand}/voice-profile.md`, Fallback `voice.md`).
- **CI** aus `{context}/brands/{brand}/ci.md` (`colors.subtitle`, `fonts.subtitle`). Angelegt/gepflegt von `/brand-ci`.

### Abgrenzung

- Brennt nur Untertitel auf ein **fertiges** Video, schneidet nicht. Aus Rohmaterial postfertig → `/video-shortform`. Rohschnitt fürs NLE → `/video-roughcut`. Footage sichten → `/video-footage-mining`.
