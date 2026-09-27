---
name: video-longform
version: 1.1.0
description: Schneidet Roh-Video(s) zu sendefertigen Longform-Videos (16:9) - YouTube-Videos, Testimonials, Kurs-Lektionen. Jumpcut-Schnitt (Fueller, Haenger, Versprecher raus), Kapitel-Timestamps, Untertitel wahlweise als SRT-Datei, eingebrannt oder keine, Final-Render. Einzeln oder ein ganzer Ordner (Kurs-Modus). Triggert bei "schneid das YouTube-Video", "mach ein Longform draus", "Testimonial-Video schneiden", "Kurs-Videos schneiden", "Lektionen schneiden", "/video-longform". Brand-aware ueber {context}/brand/. Output landet IMMER im selben Ordner wie das Roh-Video.
---

# Skill: video-longform

Du schneidest als **Senior Longform-Editor**: du denkst in Retention, Kapiteln und rotem Faden, nicht in Rohmaterial. **Dein Ziel:** ein sendefertiges Longform-Video ohne Editor-Zeit, das den Zuschauer bis zum Ende haelt und ohne weiteren Schnittprogramm-Schritt hochgeladen werden kann.

**Zweck:** Aus Roh-Video(s) ein **sendefertiges** Longform-Video bauen (YouTube, Testimonial, Kurs-Lektion). Fuer die Variante "ich finishe selbst im NLE" gibt es `/video-roughcut`, fuer vertikale Shorts `/video-shortform`.

**Brand-Pfade:** die Brand-Daten liegen unter `{context}/brand/` - existiert `.agency-os/architecture.md` im Projekt-Root (Rolle-zu-Pfad-Map vom `agency-os-start`-Skill), den `context`-Pfad daraus nehmen. Voice-Profil (`{context}/brand/voice-profile.md`) und ICP (`{context}/zielgruppe.md`) fliessen in Kapitel-Titel und Kuratierung ein.

**Kern:** Schnitt + Render laufen mit reinem ffmpeg. Kein Text-Hook-Overlay, kein Logo, keine Motion Graphics: Longform lebt von Inhalt und Pacing, nicht von Overlays.

---

## Methodik

### Struktur (self-contained Skill)

- `helpers/` - Schnitt-Engine (Python, ElevenLabs Scribe, ffmpeg). Interpreter: `.venv/bin/python` (Setup baut das venv im Skill-Root).
- `references/cut-standards.md` - **die** Quelle fuer Padding, Silence-Checks, Last-Word-Two-Step, EDL-Format.
- `references/hard-rules.md` - die Hard Rules der Schnitt-Engine (Referenz, kein eigener Trigger).
- `references/transcription.md` - Transkriptions-Policy: Scribe als Pfad, Word-Level-Pflicht. Dieser Skill ist Scribe-only (kein lokaler Whisper-Fallback).

Der Code ist aus der geteilten `video-engine`-Quelle gevendort (siehe `packages/video-engine/` im Repo). **Nicht hier editieren** - Aenderungen in der Quelle machen und `tools/sync-engine.sh` laufen lassen.

Abkuerzung in den Befehlen unten: `SK=.claude/skills/video-longform` (Aufruf vom OS-Root). Den `{context}`-Pfad wie oben beschrieben aufloesen.

---

## Workflow

### Phase 0: Setup-Gate (PFLICHT, still)

1. `DATA=$(bash $SK/scripts/resolve-datadir.sh)` (schreibbares Daten-Verzeichnis: Skill-Root in Claude Code, Cache in Cowork). Fehlt `$DATA/.ready` -> `bash $SK/scripts/setup.sh`, Ausgabe zeigen.
2. `{context}` aufloesen, dann `bash $SK/scripts/doctor.sh "{context}/secrets.env"`. Bei `OFFEN ELEVENLABS_API_KEY` -> Nutzer bitten, den Key in `{context}/secrets.env` einzutragen (Vorlage: `$SK/secrets.env.example`), dann stoppen.
3. Bei `FEHLT ffmpeg/python` -> Hard-Stop (Sandbox ohne Tools).

Nur wenn Doctor sauber -> weiter.

---

### Phase 1: Brief + Modus

**1a. Modus erkennen** (aus Anfrage + Material, im Zweifel fragen):
- **YouTube:** ein Talking-Head-/Screencast-Video wird zum publikationsfertigen YouTube-Video. Jumpcut-Schnitt + Kapitel.
- **Testimonial:** aus einem Interview/Gespraech die staerksten O-Toene zu einem kompakten Cut kuratieren (Ziel-Laenge klaeren, Default 60-120 Sekunden). Reihenfolge darf umgestellt werden, solange kein Sinn verfaelscht wird.
- **Kurs (Batch):** ein Ordner mit Lektions-Clips. Inputs **einmal** klaeren (gelten fuer alle), pro Lektion laufen Phase 2-6 durch. Konsistentes Format ueber alle Lektionen.

**1b. Format:** kein Input. Default **16:9**; leitet sich aus dem Quell-Video ab (Seitenverhaeltnis per ffprobe). Anderes Format nur, wenn das Material es klar vorgibt oder der User es ausdruecklich sagt.

**1c. Inputs, pro Lauf genau diese zwei:**
- **Untertitel:** SRT-Datei beilegen / einbrennen / keine. (Empfehlung nennen: SRT beilegen, YouTube und Kursplattformen rendern eigene Captions.)
- **Kapitel:** ja/nein. Default ja bei YouTube und Kurs, nein bei Testimonial.

Keine weiteren Fragen, kein Plan zum Bestaetigen.

**1d. Skript/Outline pruefen:** Liegt ein Skript, eine Outline oder ein Lektions-Plan beim Footage oder im Marketing-Ordner? Wenn ja, dient er als Struktur-Vorlage fuer Schnitt und Kapitel.

**1e. Ordner + Dateiname:** Output landet IMMER im **selben Ordner wie das Roh-Video** (kein neuer datierter Ordner):
- **Sprechender Name**, nicht `final.mp4`: `{slug}.mp4` aus einem kurzen Thema-Slug (z.B. `funnel-grundlagen.mp4`), im Kurs-Modus pro Lektion (z.B. `lektion-03-zielgruppe.mp4`). Dazu `{slug}_index.md` daneben.
- Schnitt-Cache (Transkript, EDL, takes_packed) in `<ordner>/_work/edit/` (gitignored).

Den Edit-Cache nie neu transkribieren, wenn das Raw-File unveraendert ist.

---

### Phase 2: Transkribieren

```bash
SK=.claude/skills/video-longform
DATA="$(bash "$SK/scripts/resolve-datadir.sh")"   # writable: skill root (Claude Code) or cache (Cowork)
PY="$DATA/.venv/bin/python"
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
- `$SK/references/hard-rules.md` - Hard Rules (nie im Wort schneiden, 30ms Audio-Fades, etc.).

Aus `{EDIT}/takes_packed.md` den Cut planen, Silence-Map + verdaechtige Sub-Slices laut cut-standards.md pruefen. EDL als JSON mit `_padding_params`-Block schreiben. Drill-down nur bei Bedarf via `timeline_view.py`.

**Longform-Pacing (anders als Shorts):**
- Raus: Fueller ("aehm", "sozusagen"-Ketten), Versprecher mit Neuansatz, Haenger, Doppel-Takes (den besten behalten), lange Denk-Pausen.
- Drin bleibt: natuerliche Sprechpausen und Atmung. Longform darf atmen; das hektische Short-Pacing traegt keine 20 Minuten. Pausen straffen, nicht eliminieren.
- **Testimonial-Modus:** erst die staerksten Aussagen markieren (konkrete Ergebnisse, emotionale Momente, Einwand-Entkraeftungen; gegen `{context}/zielgruppe.md` bewerten), dann zum Ziel-Laengen-Cut kuratieren. Interviewer-Fragen raus, ausser sie tragen Kontext.
- **Kurs-Modus:** pro Lektion schneiden, Struktur des Lektions-Plans (1d) abbilden.

**Kapitel (wenn gewaehlt):** Themenwechsel aus dem Transkript identifizieren, pro Kapitel einen kurzen, klaren Titel (Voice-Profil beachten, keine Clickbait-Floskeln). Kapitel-Zeiten beziehen sich auf die **Cut-Timeline** (nach dem Schnitt), nicht auf das Rohmaterial: aus der EDL umrechnen.

---

### Phase 4: Cut rendern

```bash
$PY $SK/helpers/render.py "$EDIT/edl.json" \
  -o "$EDIT/cut.mp4" --no-subtitles
```

- **Kein Text-Hook, kein Logo, keine Overlays.**
- **Grade-Optionen** (EDL-Feld `grade`): Preset (z.B. `warm_cinematic`), `auto`, roher ffmpeg-Filter oder 3D-LUT (`"grade": "lut:/pfad/look.cube"`). Bei Kurs-Batches denselben Grade fuer alle Lektionen.
- **Resumierbar + atomar:** render.py ueberspringt bereits gerenderte Segmente (ffprobe) und schreibt atomar (`.part.mp4` -> rename); abgebrochen -> denselben Befehl erneut aufrufen. Bei langen Videos `--budget-seconds N` nutzen und den Befehl wiederholen, bis der Render durch ist.
- **Hard Rule:** nie auf Schwarz starten/enden (erstes + letztes Frame ist Content).

---

### Phase 5: Untertitel (je nach Input aus Phase 1c)

Untertitel baut dieser Skill **nie selbst**, beide Varianten laufen ueber `/video-captions`. Uebergeben wird immer der **fertige Cut** (`$EDIT/cut.mp4`), nicht das Roh-Video: nur dort sitzen die Wort-Zeiten auf der End-Timeline, ein Hochrechnen aus dem Roh-Transkript driftet.

- **SRT beilegen (Empfehlung):** an `/video-captions` im Modus *SRT-Datei* delegieren. Eingabe: `$EDIT/cut.mp4`, Ziel: `{slug}.srt` neben dem Roh-Video. Danach Stichprobe: 3-4 Cues gegen das Video pruefen (Timing, Zeilenlaenge, kein Cue ueber Szenenwechsel hinweg falsch gruppiert).
- **Einbrennen:** an `/video-captions` im Modus *eingebrannt* delegieren. Eingabe: `$EDIT/cut.mp4`, Ziel: `{slug}.mp4` neben dem Roh-Video. Bei 16:9 gilt die Safe-Zone-Logik von captions fuer Landscape.
- **Keine:** Phase ueberspringen.

Wenn nicht eingebrannt wird: `cut.mp4` als `{slug}.mp4` neben das Roh-Video legen.

---

### Phase 6: Kapitel-Timestamps + Ablage

- **Kapitel-Block** (wenn gewaehlt) als Copy-Paste-Text in die `_index.md`, YouTube-Format (erste Marke muss `00:00` sein):

```
00:00 Intro
02:14 {Kapitel-Titel}
07:48 {Kapitel-Titel}
```

- **Self-Eval (einmal):** fertiges `{slug}.mp4` stichprobenartig gegen die EDL pruefen (Schnitt-im-Wort) per `timeline_view` an den Schnitt-Raendern. Erstes + letztes Frame sind Content (nie Schwarz). Kapitel-Marken treffen die Themenwechsel.
- **Ablage (OS-Convention):** `_index.md` neben das Raw-File schreiben (getrackt), `{slug}.mp4` (+ ggf. `{slug}.srt`) daneben, Media/Cache bleibt in `_work/` (gitignored):

```markdown
# {Titel}
- Modus: {YouTube | Testimonial | Kurs, Lektion N}
- Format: {16:9}
- Laenge: {MM:SS}
- Untertitel: {SRT beigelegt | eingebrannt | keine}
- Status: Sendefertig
- Render: {slug}.mp4

## Kapitel
{Kapitel-Block oder "keine"}
```

- Daily-Log-Notiz in `{logs}/{YYYY-MM-DD}.md` ergaenzen.

---

## Output

Landet IMMER im selben Ordner wie das Roh-Video (kein neuer datierter Ordner):
- `{slug}.mp4` (sendefertiges Longform-Video, sprechender Name) + getracktes `_index.md` direkt neben dem Raw-File, optional `{slug}.srt`.
- Kapitel-Timestamps als Copy-Paste-Block in der `_index.md`.
- Schnitt-Cache (Transkript, EDL, takes_packed) in `_work/edit/` (gitignored).
- Daily-Log-Notiz in `{logs}/{YYYY-MM-DD}.md`.

## Verwandte Skills

### Kontext-Bridge (Pflicht, Projekt-Skills haben Vorrang)

- **brand-voice** fuer Kapitel-Titel und Text-Ton (`{context}/brand/voice-profile.md`, Fallback `voice.md`).
- **icp** fuer Testimonial-Kuratierung und Relevanz-Bewertung (`{context}/zielgruppe.md`).

### Abgrenzung

- Baut das **sendefertige** Longform-Video (16:9, YouTube/Testimonial/Kurs). Vertikale Shorts mit Text-Hook -> `/video-shortform`. Wer im NLE finishen will -> `/video-roughcut` (Rohschnitt + DaVinci/Premiere-Export). Nur Untertitel auf ein fertiges Video -> `/video-captions`. Footage sichten/Highlights finden -> `/video-footage-mining` (dessen Highlight-Index ist im Testimonial-Modus ein guter Startpunkt).
- Voice-Profil -> `/brand-voice`, ICP -> `/icp`.
