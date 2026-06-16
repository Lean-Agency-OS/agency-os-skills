---
name: video-footage-mining
version: 1.0.0
description: Sichtet ganze Roh-Footage-Ordner lokal und schnell (ohne API) - transkribiert alle Clips per lokalem Whisper, findet die postwuerdigen O-Toene/Highlights mit Timecodes und schreibt einen Highlight-Index. Triggert bei "Footage sichten", "was steckt in dem Material", "Highlights finden", "O-Toene raussuchen", "Video-Triage", "/video-footage-mining". Liest ICP/Positionierung fuers Highlight-Gespuer.
---

# Skill: video-footage-mining

Du arbeitest als **Senior Footage-Logger**: du denkst in Gold-Momenten, nicht in Vollstaendigkeit. **Dein Ziel:** aus Stunden Rohmaterial schnell die wenigen postwuerdigen O-Toene/Highlights finden, mit Timecode und Begruendung, sodass daraus direkt geschnitten werden kann.

**Zweck:** Einen ganzen Footage-Ordner **lokal und ohne API** durchsuchbar machen und die Highlights herausziehen. Produziert **kein Video** - liefert einen Highlight-Index. Schneiden danach → `/video-shortform`.

**Lokal, kein Key noetig:** Die Sichtung laeuft per lokalem Whisper (Text-only Gist), braucht **keinen** ElevenLabs-Key und kein Netz. Erst wenn ein gewaehlter Highlight final geschnitten wird (in `/video-shortform`), kommt der Scribe-Key ins Spiel.

**Brand:** existiert `.agency-os/architecture.md`, den `context`-Pfad daraus nehmen; ICP/Positionierung aus `{context}/brands/{brand}/` schaerfen das Highlight-Gespuer (was trifft die Zielgruppe).

---

## Methodik

### Struktur (self-contained Skill)

- `helpers/` - `transcribe_batch.py` (lokaler Whisper-Gist über viele Files) + Transkriptions-Helfer. Interpreter: `.venv/bin/python` (Setup baut das venv im Skill-Root, **mit** lokalem Whisper via `.needs-whisper`).
- `references/transcription.md` - Transkriptions-Policy: hier zaehlt der `--text-only`-Modus (Gist, `.txt` + `gist.md`, keine Timestamps, kein Cut-Artefakt).

Der Code ist aus der geteilten `video-engine`-Quelle gevendort. **Nicht hier editieren** - Änderungen in der Quelle machen und `tools/sync-engine.sh` laufen lassen.

Abkuerzung: `SK=.claude/skills/video-footage-mining` (Aufruf vom OS-Root).

---

## Workflow

### Phase 0: Setup-Gate (PFLICHT, still)

1. `DATA=$(bash $SK/scripts/resolve-datadir.sh)` (schreibbares Daten-Verzeichnis: Skill-Root in Claude Code, Cache in Cowork). Fehlt `$DATA/.ready` -> `bash $SK/scripts/setup.sh`, Ausgabe zeigen (installiert lokalen Whisper).
2. `bash $SK/scripts/doctor.sh`. Bei `OFFEN faster-whisper` -> Setup nochmal laufen lassen. **`OFFEN ELEVENLABS_API_KEY` ist hier OK** (die Sichtung braucht keinen Key) - nur als Hinweis behandeln, nicht stoppen.
3. Bei `FEHLT ffmpeg/python` -> Hard-Stop.

Nur wenn ffmpeg + Python + faster-whisper da sind -> weiter.

---

### Phase 1: Brief (Stop-Punkt, Deutsch)

**1a. Inputs:** Pfad zum Footage-Ordner; grobes Ziel (welche Art Highlights gesucht: Hooks, Aussagen zu Thema X, Emotion, …).

**1b. Ordner:** Gist + Index landen IM Footage-Ordner: `gist.md` + `*.txt` neben den Clips, der Highlight-Index als `highlights.md` daneben.

**1c. Bestaetigen** (Pflicht): *"Ich transkribiere alle Clips lokal (ohne API) und ziehe die Highlights mit Timecodes. Passt das?"* Erst nach OK -> Phase 2.

---

### Phase 2: Batch-Transkription (lokal, Text-only)

```bash
SK=.claude/skills/video-footage-mining
DATA="$(bash "$SK/scripts/resolve-datadir.sh")"   # writable: skill root (Claude Code) or cache (Cowork)
PY="$DATA/.venv/bin/python"
RAWDIR="{footage_ordner}"
$PY $SK/helpers/transcribe_batch.py "$RAWDIR" --text-only   # -> *.txt + gist.md (lokaler Whisper)
```

Schreibt pro Clip ein `.txt` und einen Sammel-`gist.md`. **Keine** Timestamps, **kein** Cut-Artefakt (rührt etwaige spätere Cut-Daten nicht an). Policy: `$SK/references/transcription.md`.

---

### Phase 3: Highlights ziehen (LLM-Reasoning)

`gist.md` + die `.txt` lesen. Pro Clip die postwuerdigen Stellen markieren: was gesagt wird, warum es ein Hook/O-Ton ist, grober Timecode/Fundstelle. ICP/Positionierung als Filter: was trifft die Zielgruppe.

Einen **Highlight-Index** schreiben (`{RAWDIR}/highlights.md`):

```markdown
# Footage-Highlights: {Ordner}
| Clip | ~Stelle | O-Ton / Hook | Warum stark | Naechster Schritt |
|---|---|---|---|---|
| IMG_8762.MOV | ~0:42 | "{Kernsatz}" | klarer Hook, ICP-Schmerz | -> /video-shortform |
```

---

### Phase 4: Uebergabe

Pro starkem Highlight der Vorschlag, ihn mit `/video-shortform` zu einem postfertigen Reel/Short zu schneiden (Clip-Pfad + Timecode mitgeben). `video-footage-mining` selbst schneidet/rendert nicht.

---

## Output

Im Footage-Ordner:
- `gist.md` + pro Clip ein `.txt` (lokaler Whisper-Gist).
- `highlights.md` (der Highlight-Index mit Timecodes + Begruendung).
- Daily-Log-Notiz in `{logs}/{YYYY-MM-DD}.md`.

## Verwandte Skills

### Kontext-Bridge

- **icp** / **positionierung** aus `{context}/brands/{brand}/` schaerfen, welche Stellen die Zielgruppe wirklich treffen.

### Abgrenzung

- Sichtet + findet, **produziert kein Video**. Aus einem Highlight ein postfertiges Reel → `/video-shortform`. Rohschnitt fürs NLE → `/video-roughcut`. Untertitel auf ein fertiges Video → `/video-captions`.
