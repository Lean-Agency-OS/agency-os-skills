---
name: video-roughcut
version: 1.0.1
description: Bereitet aus einem Roh-Video einen Rohschnitt vor und exportiert ihn nach DaVinci Resolve / Premiere - Transkript, Fueller/Pausen raus, sauberes Timing, NLE-Export (FCPXML / FCP7-XML). Kein Grade/Render, der Cutter finisht nativ. Triggert bei "Rohschnitt", "schneid vor", "Schnitt fuer DaVinci/Premiere", "exportier als FCPXML", "rough cut", "/video-roughcut". Brand-aware ueber {context}/brands/{brand}/.
---

# Skill: video-roughcut

Du arbeitest als **Senior Assistant Editor**: du denkst in Selektion und Timing, nicht in Effekten. **Dein Ziel:** dem Cutter die tedious 80% abnehmen (transkribieren, Fueller/Pausen raus, sauberer Rohschnitt), sodass er nur noch nativ im NLE finisht.

**Zweck:** Aus einem Roh-Video einen **Rohschnitt** bauen und als NLE-Projekt übergeben (DaVinci Resolve / Premiere). Grade, Overlays und Final-Render macht der Editor nativ. Wer ein **postfertiges** Video ohne NLE will → `/video-shortform`.

**Brand:** die im Brain konfigurierte Brand (Ordner unter `{context}/brands/`). Gibt es nur einen, den nehmen; bei mehreren die mit `brand-config.md` `status: active`.

**Brand-Pfade:** `{context}/brands/{brand}/` ist ein Default - existiert `.agency-os/architecture.md` im Projekt-Root, den `context`-Pfad daraus nehmen.

---

## Methodik

### Struktur (self-contained Skill)

- `helpers/` - Transkriptions-/Schnitt-Helfer (Python, ElevenLabs Scribe, ffmpeg) + `export_nle.py`. Interpreter: `.venv/bin/python` (Setup baut das venv im Skill-Root).
- `references/cut-standards.md` - **die** Quelle fuer Padding, Silence-Checks, Last-Word-Two-Step, EDL-Format.
- `references/hard-rules.md` - die Hard Rules der Schnitt-Engine.
- `references/transcription.md` - Transkriptions-Policy. Scribe-only (kein lokaler Whisper-Fallback).

Der Code ist aus der geteilten `video-engine`-Quelle gevendort. **Nicht hier editieren** - Änderungen in der Quelle machen und `tools/sync-engine.sh` laufen lassen.

Abkuerzung: `SK=.claude/skills/video-roughcut` (Aufruf vom OS-Root). Den `{context}`-Pfad wie oben auflösen.

---

## Workflow

### Phase 0: Setup-Gate (PFLICHT, still)

1. `DATA=$(bash $SK/scripts/resolve-datadir.sh)` (schreibbares Daten-Verzeichnis: Skill-Root in Claude Code, Cache in Cowork). Fehlt `$DATA/.ready` -> `bash $SK/scripts/setup.sh`, Ausgabe zeigen.
2. `{context}` auflösen, dann `bash $SK/scripts/doctor.sh "{context}/secrets.env"`. Bei `OFFEN ELEVENLABS_API_KEY` -> Nutzer bitten, den Key in `{context}/secrets.env` einzutragen (Vorlage: `$SK/secrets.env.example`), dann stoppen.
3. Bei `FEHLT ffmpeg/python` -> Hard-Stop.

Nur wenn Doctor sauber -> weiter. (Node/Chromium braucht dieser Skill nicht.)

---

### Phase 1: Brief + Plan (Stop-Punkt, Deutsch)

**1a. Inputs:** Roh-Video-Pfad; Ziel-NLE (`DaVinci`/`Premiere`/`beide`); Timeline-Format (z.B. 1080x1920 vertikal, 1920x1080); Captions als Spur mitexportieren ja/nein.

**1b. Ordner:** Output landet IMMER im **selben Ordner wie das Roh-Video**. Schnitt-Cache (Transkript, EDL) in `<ordner>/_work/edit/` (gitignored), das NLE-Projekt direkt daneben.

**1c. Plan bestaetigen lassen** (Pflicht):

```
Kurz-Plan (Rohschnitt -> NLE):
- Video: {dateiname} | Ziel: {DaVinci} | Timeline: {1080x1920} | Captions-Spur: {ja}
- Ich transkribiere, schneide Fueller/Pausen/Versprecher raus, setze saubere Schnitt-Raender
  und exportiere den Schnitt (Clip-Auswahl + Timing) als NLE-Projekt. Grade/Overlays machst du nativ.
Passt das? Dann lege ich los.
```

Erst nach OK -> Phase 2.

---

### Phase 2: Transkribieren

```bash
SK=.claude/skills/video-roughcut
DATA="$(bash "$SK/scripts/resolve-datadir.sh")"   # writable: skill root (Claude Code) or cache (Cowork)
PY="$DATA/.venv/bin/python"
RAWDIR="$(dirname "{video}")"        # raw video folder = output folder
EDIT="$RAWDIR/_work/edit"            # edit cache next to the raw file (gitignored)
$PY $SK/helpers/transcribe.py "{video}" --edit-dir "$EDIT"
$PY $SK/helpers/pack_transcripts.py --edit-dir "$EDIT" --silence-threshold 0.4
```

Transkript ist gecached. Scribe-only - ist Scribe nicht erreichbar, stoppt der Lauf mit klarer Meldung (Policy: `$SK/references/transcription.md`).

---

### Phase 3: Schnitt planen (LLM-Reasoning)

**Pflicht-Lektuere zuerst:**
- `$SK/references/cut-standards.md` - Padding, Pre-Cut-Checks, Last-Word-Two-Step, EDL-Format.
- `$SK/references/hard-rules.md` - Hard Rules (nie im Wort schneiden, Wortgrenzen, Padding).

Aus `{EDIT}/takes_packed.md` den Cut planen, EDL als JSON schreiben. Drill-down via `timeline_view.py` nur bei Bedarf. Der EDL ist hier die Übergabe-Basis: Clip-Auswahl + Timing, **kein** Grade/Overlay (das macht der Editor).

---

### Phase 4: NLE-Export

```bash
SK=.claude/skills/video-roughcut
DATA="$(bash "$SK/scripts/resolve-datadir.sh")"   # writable: skill root (Claude Code) or cache (Cowork)
PY="$DATA/.venv/bin/python"
RAWDIR="$(dirname "{video}")"

# DaVinci Resolve (FCPXML): vertical 9:16 timeline, captions embedded,
# remap the media path from the cowork sandbox to the real Mac path:
$PY $SK/helpers/export_nle.py "{EDIT}/edl.json" -o "$RAWDIR/rohschnitt.fcpxml" --fps 24 \
  --width 1080 --height 1920 --captions --caption-color FED760 \
  --remap "/sessions/<id>/mnt/<Projekt>=/Users/<user>/Documents/<Projekt>"

# Adobe Premiere (FCP7-XML) or both at once:
$PY $SK/helpers/export_nle.py "{EDIT}/edl.json" --format both --width 1080 --height 1920
```

Exportiert nur den Schnitt (Clip-Auswahl + Timing, referenziert die Original-Files). Grade/Overlays bewusst NICHT. Optionen:
- `--width/--height` setzt das Timeline-Raster (z.B. 1080x1920 vertikal); ohne Angabe = Quell-Dimension. Quell-Assets behalten ihr natives Format, sodass rotierte/Querformat-Quellen sauber konformen.
- `--captions` bettet Untertitel aus `transcripts/<src>.json` (2-Wort-Chunking) als Subtitle-Spur ein (nur FCPXML). `--caption-color` (Hex) setzt die Fuellfarbe (aus dem `ci.md`-Frontmatter `colors.subtitle`).
- `--format premiere|both` schreibt zusaetzlich FCP7-XML (xmeml) fuer aeltere Premiere-Versionen; dort Captions ueber die SRT importieren.
- `--remap FROM=TO` (wiederholbar) biegt Medienpfade um (Cowork-Sandbox -> Mac), damit die NLE die Footage findet.

---

### Phase 5: Self-Eval + Ablegen

- **Self-Eval (einmal):** EDL gegen die Wortgrenzen pruefen (kein Schnitt im Wort) per `timeline_view`-Stichproben an den Schnitt-Raendern.
- **Ablage (OS-Convention):** `_index.md` neben das Raw-File (getrackt), NLE-Projekt daneben, Cache bleibt in `_work/` (gitignored):

```markdown
# {Titel}
- Brand: {brand} | Ziel-NLE: {DaVinci}
- Status: Rohschnitt uebergeben
- Export: rohschnitt.fcpxml
- Datum: {YYYY-MM-DD}
```

- Daily-Log-Notiz in `{logs}/{YYYY-MM-DD}.md` ergaenzen.

---

## Output

Im selben Ordner wie das Roh-Video:
- NLE-Projekt (`rohschnitt.fcpxml` und/oder FCP7-XML) + getracktes `_index.md`.
- Schnitt-Cache (Transkript, EDL, SRT) in `_work/edit/` (gitignored).
- Daily-Log-Notiz in `{logs}/{YYYY-MM-DD}.md`.

## Verwandte Skills

### Kontext-Bridge

- **CI** aus `{context}/brands/{brand}/ci.md` nur für die Caption-Farbe (`colors.subtitle`), falls `--captions`.

### Abgrenzung

- Liefert einen **Rohschnitt fürs NLE**, kein fertiges Video. Postfertig ohne NLE → `/video-shortform`. Nur Untertitel auf ein fertiges Video → `/video-captions`. Footage sichten → `/video-footage-mining`.
