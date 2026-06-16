---
name: hard-rules
description: Hard Rules der Schnitt-Engine der video-* Skills (Referenz-Doku, kein eigener Skill-Trigger). Production-correctness rules are hard; everything else is artistic freedom.
---

# Schnitt-Engine: Hard Rules

## Prinzip

1. **Das LLM denkt aus dem Roh-Transkript + visuellen Einblicken on demand.** Das einzige abgeleitete Artefakt, das sich lohnt, ist ein gepacktes Transkript auf Phrasen-Ebene (`takes_packed.md`). Alles andere (Filler-Tagging, Retake-Erkennung, Shot-Klassifizierung, Emphasis-Scoring) leitest du im Moment der Entscheidung ab.
2. **Audio ist primär, Bild folgt.** Schnitt-Kandidaten kommen aus Sprech-Grenzen und Stille-Lücken. Geh nur an Entscheidungspunkten ins Bild-Detail.
3. **Fragen → Bestätigen → Ausführen → Iterieren → Persistieren.** Fass den Schnitt nie an, bevor der Nutzer die Strategie in Klartext bestätigt hat.
4. **Generalisiere.** Nimm nicht an, was für ein Video das ist. Schau dir das Material an, frag den Nutzer, dann schneide.
5. **Künstlerische Freiheit ist der Default.** Jeder konkrete Wert, jedes Preset, jede Schrift, Farbe, Dauer, Pitch-Struktur und Technik in diesem Dokument ist ein *durchgespieltes Beispiel* aus einem bewährten Video, kein Gebot. Lies sie, um zu verstehen, was möglich ist und warum es funktioniert hat. Dann triff deine eigenen Geschmacks-Entscheidungen, basierend darauf, was das Material wirklich ist und was der Nutzer wirklich will. **Das Einzige, was du tun MUSST, steht im Abschnitt Hard Rules unten.** Alles andere gehört dir.
6. **Erfinde frei.** Wenn das Material eine Technik verlangt, die hier nicht beschrieben ist (Split-Screen, Picture-in-Picture, Lower-Third-Identity-Cards, Reaction-Cuts, Speed-Ramps, Freeze-Frames, Crossfades, Match-Cuts, L-Cuts, J-Cuts, Speed-Ramps über den Atem, was auch immer), bau es. Die Helfer sind ffmpeg und PIL. Sie können alles, was das Format hergibt. Warte nicht auf Erlaubnis.
7. **Prüfe deinen eigenen Output, bevor du ihn dem Nutzer zeigst.** Wenn du es nicht ausliefern würdest, präsentiere es nicht.

## Hard Rules (Produktions-Korrektheit, nicht verhandelbar)

Das sind die Dinge, bei denen Abweichung zu stillen Fehlern oder kaputtem Output führt. Das ist kein Geschmack, das ist Korrektheit. Lern sie auswendig.

1. **Untertitel werden ZULETZT in der Filter-Chain angewandt**, nach jedem Overlay. Sonst verdecken Overlays die Captions. Stiller Fehler.
2. **Pro-Segment-Extract, dann verlustfreies `-c copy`-Concat**, kein Single-Pass-Filtergraph. Sonst encodierst du jedes Segment doppelt, sobald Overlays dazukommen.
3. **30ms Audio-Fades an jeder Segment-Grenze** (`afade=t=in:st=0:d=0.03,afade=t=out:st={dur-0.03}:d=0.03`). Sonst hörbare Pops an jedem Schnitt.
4. **Overlays nutzen `setpts=PTS-STARTPTS+T/TB`**, um Frame 0 des Overlays auf seinen Fenster-Start zu schieben. Sonst siehst du die Mitte der Animation während des Overlay-Fensters.
5. **Master-SRT nutzt Output-Timeline-Offsets**: `output_time = word.start - segment_start + segment_offset`. Sonst verrutschen die Captions nach dem Segment-Concat.
6. **Nie innerhalb eines Wortes schneiden.** Snap jede Schnittkante an eine Wortgrenze aus dem Scribe-Transkript.
7. **Jede Schnittkante padden.** Arbeitsfenster: 30-200ms. Scribe-Timestamps driften 50-100ms, das Padding fängt den Drift ab. Enger für schnelles Tempo, weiter für cineastisch.
8. **Nur Wort-genaues, wörtliches ASR.** Nie SRT-/Phrasen-Modus (verliert Sub-Sekunden-Lückendaten). Nie normalisierte Filler (verliert redaktionelles Signal).
9. **Transkripte pro Source cachen.** Nie neu transkribieren, außer die Source-Datei selbst hat sich geändert.
10. **Parallele Sub-Agents für mehrere Animationen.** Nie sequentiell. Spawne N gleichzeitig über das `Agent`-Tool; Gesamt-Wandzeit ≈ langsamster.
11. **Strategie-Bestätigung vor Ausführung.** Fass den Schnitt nie an, bevor der Nutzer den Klartext-Plan freigegeben hat.
12. **Alle Session-Outputs in `<videos_dir>/edit/`.** Schreibe nie in das Skill-Verzeichnis.

Alles andere in diesem Dokument ist ein durchgespieltes Beispiel. Weiche ab, wann immer das Material es verlangt.

## Verzeichnis-Layout

Die Schnitt-Engine lebt im jeweiligen video-*-Skill. Nutzer-Footage liegt, wo der Nutzer es hinlegt. Alle Session-Outputs gehen nach `<videos_dir>/edit/`.

```
<videos_dir>/
├── <source files, untouched>
└── edit/
    ├── project.md               ← memory; appended every session
    ├── takes_packed.md          ← phrase-level transcripts, the LLM's primary reading view
    ├── edl.json                 ← cut decisions
    ├── transcripts/<name>.json  ← cached raw Scribe JSON
    ├── animations/slot_<id>/    ← per-animation source + render + reasoning
    ├── clips_graded/            ← per-segment extracts with grade + fades
    ├── master.srt               ← output-timeline subtitles
    ├── downloads/               ← yt-dlp outputs
    ├── verify/                  ← debug frames / timeline PNGs
    ├── preview.mp4
    └── final.mp4
```

## Setup

Setup + Umgebungs-Check laufen über `scripts/setup.sh` und `scripts/doctor.sh` des Skills (nicht jede Session neu). Bei Kaltstart nur prüfen:

- `ELEVENLABS_API_KEY` auflösbar: er liegt extern im Brain unter `{context}/secrets.env` (committet, nie im Skill-Verzeichnis, nie im `<videos_dir>` des Nutzers). Fehlt er, bitte den Nutzer, ihn dort einzutragen (Vorlage: `secrets.env.example`).
- `ffmpeg` + `ffprobe` im PATH.
- Python-Deps installiert (`scripts/setup.sh` baut das venv im Skill-Root).
- Node.js + npm + Chromium nur für Motion-Graphics nötig, und nur im `video-shortform`-Skill gebündelt.

Die Helfer (`helpers/transcribe.py`, `helpers/render.py`, etc.) liegen im Skill-Root, eine Ebene über dieser `references/`-Datei.

## Helfer

- **`transcribe.py <video>`** : Single-File-Scribe-Aufruf. `--num-speakers N` optional. Gecached.
- **`transcribe_batch.py <videos_dir>`** : 4-Worker-Parallel-Transkription. Für Multi-Take.
- **`pack_transcripts.py --edit-dir <dir>`** : `transcripts/*.json` → `takes_packed.md` (Phrasen-Ebene, Umbruch bei Stille ≥ 0.5s).
- **`timeline_view.py <video> <start> <end>`** : Filmstreifen + Waveform-PNG. Visueller Drill-Down on demand. **Kein Scan-Tool**: an Entscheidungspunkten nutzen, nicht permanent.
- **`render.py <edl.json> -o <out>`** : Pro-Segment-Extract → Concat → Overlays (PTS-verschoben) → Untertitel ZULETZT. `--preview` für schnelles 720p. `--build-subtitles`, um master.srt inline zu erzeugen.
- **`grade.py <in> -o <out>`** : ffmpeg-Filter-Chain-Grade. Presets + `--filter '<raw>'` für Custom.

Für Animationen `<edit>/animations/slot_<id>/` mit `Bash` anlegen und einen Sub-Agent über das `Agent`-Tool spawnen.

## Der Prozess

1. **Inventory.** `ffprobe` auf jede Source. `transcribe_batch.py` auf das Verzeichnis. `pack_transcripts.py`, um `takes_packed.md` zu erzeugen. Ein oder zwei `timeline_view`s als visuellen ersten Eindruck ziehen.
2. **Pre-Scan auf Probleme.** Ein Durchgang über `takes_packed.md`, um Versprecher, offensichtliche Patzer oder zu vermeidende Formulierungen zu notieren. Schlichte Liste, fließt ins Editor-Brief.
3. **Sprich mit dem Nutzer.** Beschreibe in Klartext, was du siehst. Stell Fragen, *die das Material vorgibt*. Sammle: Content-Typ, Ziel-Länge/-Format, Ästhetik/Brand-Richtung, Tempo-Gefühl, Must-Preserve-Momente, Must-Cut-Momente, Animations- und Grade-Präferenzen, Untertitel-Bedarf. Keine feste Checkliste: die richtigen Fragen sind jedes Mal andere.
4. **Strategie vorschlagen.** 4-8 Sätze: Form, Take-Wahl, Schnitt-Richtung, Animations-Plan, Grade-Richtung, Untertitel-Stil, Längen-Schätzung. **Auf Bestätigung warten.**
5. **Ausführen.** `edl.json` über das Editor-Sub-Agent-Brief erzeugen. An mehrdeutigen Stellen in `timeline_view` reinzoomen. Animationen in parallelen Sub-Agents bauen. Grade pro Segment anwenden. Über `render.py` komponieren.
6. **Preview.** `render.py --preview`.
7. **Self-Eval (bevor du es dem Nutzer zeigst).** `timeline_view` auf dem **gerenderten Output** (nicht den Sources) an jeder Schnittgrenze laufen lassen (±1.5s-Fenster). Jedes Bild prüfen auf:
   - Visuelle Diskontinuität / Flash / Sprung am Schnitt
   - Waveform-Spike an der Grenze (Audio-Pop, der am 30ms-Fade vorbeigerutscht ist)
   - Untertitel hinter einem Overlay versteckt (Verstoß gegen Regel 1)
   - Overlay verrutscht oder zeigt falsche Frames (Verstoß gegen Regel 4)

   Außerdem als Stichprobe: erste 2s, letzte 2s und 2-3 Mittelpunkte: Grade-Konsistenz, Untertitel-Lesbarkeit, Gesamt-Kohärenz prüfen. `ffprobe` auf den Output, um zu verifizieren, dass die Dauer der EDL-Erwartung entspricht.

   Wenn etwas durchfällt: fixen → neu rendern → neu evaluieren. **Maximal 3 Self-Eval-Durchgänge**: bleiben nach 3 noch Probleme, melde sie dem Nutzer, statt endlos zu loopen. Zeig die Preview erst, wenn die Self-Eval besteht.
8. **Iterieren + persistieren.** Natürlich-sprachliches Feedback, neu planen, neu rendern. Nie neu transkribieren. Final-Render bei Bestätigung. An `project.md` anhängen.

## Schnitt-Handwerk (Techniken)

- **Audio-first.** Kandidaten-Schnitte aus Wortgrenzen und Stille-Lücken.
- **Peaks bewahren.** Lacher, Pointen, Betonungs-Beats. Über die Pointe hinaus verlängern, um Reaktionen einzuschließen: der Lacher IST der Beat.
- **Sprecher-Übergaben** profitieren von Luft zwischen den Äußerungen. Übliche Werte: 400-600ms. Weniger für schnelles Tempo, mehr für cineastisch. Geschmacks-Entscheidung.
- **Audio-Events als Signale.** `(laughs)`, `(sighs)`, `(applause)` markieren Beats. Über sie hinaus verlängern.
- **Stille-Lücken sind Schnitt-Kandidaten.** Stillen ≥400ms sind meist die saubersten. 150-400ms-Phrasengrenzen sind mit Sicht-Check nutzbar. <150ms ist unsicher (mitten in der Phrase).
- **Beispiel-Schnitt-Padding** (mit dem das Launch-Video ausgeliefert wurde): 50ms vor dem ersten behaltenen Wort, 80ms nach dem letzten. Enger für Montage-Energie, weiter für Doku. Bleib im 30-200ms-Arbeitsfenster (Hard Rule 7).
- **Audio und Video nie unabhängig denken.** Jeder Schnitt muss auf beiden Spuren funktionieren.

## Das gepackte Transkript (primäre Lese-Ansicht)

`pack_transcripts.py` liest alle `transcripts/*.json` und erzeugt eine Markdown-Datei, in der jeder Take eine Liste von Zeilen auf Phrasen-Ebene ist, jede mit ihrem `[start-end]`-Zeitbereich als Präfix. Phrasen brechen bei jeder Stille ≥ 0.5s ODER Sprecher-Wechsel. Das ist das Artefakt, das der Editor-Sub-Agent liest, um Schnitte zu wählen: es gibt Wortgrenzen-Präzision allein aus Text, bei 1/10 der Tokens des Roh-JSON.

Beispiel-Zeile:
```
## C0103  (duration: 43.0s, 8 phrases)
  [002.52-005.36] S0 Ninety percent of what a web agent does is completely wasted.
  [006.08-006.74] S0 We fixed this.
```

## Editor-Sub-Agent-Brief (für Multi-Take-Auswahl)

Wenn die Aufgabe lautet "wähle den besten Take jedes Beats über viele Clips", spawne einen dedizierten Sub-Agent mit einem Brief in dieser Form. Die Struktur ist tragend; das Pitch-Shape-Beispiel nicht.

```
You are editing a <type> video. Pick the best take of each beat and 
assemble them chronologically by beat, not by source clip order.

INPUTS:
  - takes_packed.md (time-annotated phrase-level transcripts of all takes)
  - Product/narrative context: <2 sentences from the user>
  - Speaker(s): <name, role, delivery style note>
  - Expected structure: <pick an archetype or invent one>
  - Verbal slips to avoid: <list from the pre-scan pass>
  - Target runtime: <seconds>

Common structural archetypes (pick, adapt, or invent):
  - Tech launch / demo:   HOOK → PROBLEM → SOLUTION → BENEFIT → EXAMPLE → CTA
  - Tutorial:             INTRO → SETUP → STEPS → GOTCHAS → RECAP
  - Interview:            (QUESTION → ANSWER → FOLLOWUP) repeat
  - Travel / event:       ARRIVAL → HIGHLIGHTS → QUIET MOMENTS → DEPARTURE
  - Documentary:          THESIS → EVIDENCE → COUNTERPOINT → CONCLUSION
  - Music / performance:  INTRO → VERSE → CHORUS → BRIDGE → OUTRO
  - Or invent your own.

RULES:
  - Start/end times must fall on word boundaries from the transcript.
  - Pad cut boundaries (working window 30-200ms).
  - Prefer silences ≥ 400ms as cut targets.
  - Unavoidable slips are kept if no better take exists. Note them in "reason".
  - If over budget, revise: drop a beat or trim tails. Report total and self-correct.

OUTPUT (JSON array, no prose):
  [{"source": "C0103", "start": 2.42, "end": 6.85, "beat": "HOOK",
    "quote": "...", "reason": "..."}, ...]

Return the final EDL and a one-line total runtime check.
```

## Color-Grade (auf Wunsch)

Deine Aufgabe ist es, **über das Bild nachzudenken**, nicht ein Preset anzuwenden. Schau dir einen Frame an (via `timeline_view`), entscheide, was falsch ist, ändere eine Sache, schau wieder.

Mentales Modell ist ASC CDL. Pro Kanal: `out = (in * slope + offset) ** power`, dann globale Sättigung. `slope` → Highlights, `offset` → Schatten, `power` → Mitten.

**Beispiel-Filter-Chains** (`grade.py` hat `--list-presets`; nutz sie als Startpunkt oder misch deine eigenen):

- **`warm_cinematic`** : retro/technisch, dezenter Teal/Orange-Split, entsättigt. In einem echten Launch-Video ausgeliefert. Sicher für Talking Heads.
- **`neutral_punch`** : minimal korrektiv: Kontrast-Bump + sanfte S-Kurve. Keine Hue-Shifts.
- **`none`** : reiner Copy. Default, wenn der Nutzer nichts verlangt hat.

Für alles andere (Portrait, Natur, Produkt, Musikvideo, Doku) erfinde deine eigene Chain. `grade.py --filter '<raw ffmpeg>'` akzeptiert jeden Filter-String.

Hard Rules: **pro Segment während der Extraktion** anwenden (nicht nach dem Concat, das encodiert zweimal). Nie aggressiv werden, ohne Hauttöne zu testen.

## Untertitel (auf Wunsch)

Untertitel haben drei Dimensionen, über die es sich nachzudenken lohnt: **Chunking** (1/2/3/Satz pro Zeile), **Schreibung** (UPPER/Title/Natural) und **Platzierung** (Abstand vom unteren Rand). Die richtige Kombi hängt vom Content ab.

**Durchgespielte Stile** : wählen, anpassen oder erfinden:

**`bold-overlay`** : Short-Form-Tech-Launch, schnelles Social. 2-Wort-Chunks, GROSSBUCHSTABEN, Umbruch bei Satzzeichen, Helvetica 18 Bold, Weiß-auf-Outline, `MarginV=35`. `render.py` liefert das als `SUB_FORCE_STYLE` mit.

```
FontName=Helvetica,FontSize=18,Bold=1,
PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H00000000,
BorderStyle=1,Outline=2,Shadow=0,
Alignment=2,MarginV=35
```

**`natural-sentence`** (falls du diesen Modus erfindest) : Narrativ, Doku, Bildung. 4-7-Wort-Chunks, Satz-Schreibung, Umbruch bei natürlichen Pausen, `MarginV=60-80`, größere Schrift für Lesbarkeit, etwas breitere Max-Width. Kein mitgeliefertes force_style: entwirf eins, wenn du es brauchst.

Erfinde einen dritten Stil, wenn keiner passt. Hard Rules: Untertitel ZULETZT (Regel 1), Output-Timeline-Offsets (Regel 5).

## Animationen (auf Wunsch)

Animationen passen zum Content und zur Brand. **Hol Palette, Schrift und Bildsprache aus dem Gespräch**: nie einen Default annehmen. Wenn der Nutzer nichts gesagt hat, schlag in der Strategie-Phase eine Palette vor und warte auf Bestätigung, bevor du irgendwas baust.

**Tool-Optionen:**

Wähle die Engine pro Animations-Slot. Greif nicht automatisch zu Remotion, nur weil die Animation web-nah ist.

- **HyperFrames** : Browser-native HTML/CSS/GSAP-Video-Kompositionen: Produkt-UI-Motion, Website-to-Video- oder Mockup-to-Video-Captures, kinetische Typografie, Landingpage-/Storyboard-Promos, datengetriebene UI-States, transparente WebM-Overlays und Clips, die deterministisches Frame-Capture plus HyperFrames-Lint/Validate/Render-Checks brauchen. Am besten, wenn die Animation wie eine Web-Komposition statt als React-Component-Tree gebaut und verifiziert werden soll.
- **Remotion** : React/CSS-Kompositionen mit Component-State, wiederverwendbaren React-Primitives oder einem bestehenden Remotion-Brand-System. Am besten, wenn der Nutzer explizit React/Remotion verlangt oder wenn React-Komposition das einfachere Authoring-Modell ist.
- **Manim** : formale Diagramme, State-Machines, Gleichungs-Herleitungen, Graph-Morphs. Lies `skills/manim-video/SKILL.md` und seine References für Tiefe.
- **PIL + PNG-Sequenz + ffmpeg** : einfache Overlay-Cards: Counter, Typewriter-Text, einzelne Bar-Reveals, progressive Draws. Schnell zu iterieren, jede Ästhetik, die du willst. Das Launch-Video nutzte das.

Für HyperFrames-Slots den Slot in `edit/animations/slot_<id>/` mit `npx --yes hyperframes init . --example blank --non-interactive --skip-skills` scaffolden, die HTML-Komposition dort bauen, die zum Slot passenden HyperFrames-Checks laufen lassen (`lint`, `validate` und einen Draft-Render, wenn praktikabel), dann das finale Overlay-Video mit `npx --yes hyperframes render . -o render.mp4` oder `--format webm -o render.webm` erzeugen, wenn Alpha nötig ist. Zeig den EDL-Overlay-`file` auf den tatsächlich gerenderten Pfad.

Für Remotion-Slots das Remotion-Projekt isoliert im selben Slot-Verzeichnis halten, mit `npx create-video@latest` scaffolden oder Remotion dort lokal installieren, die Komposition mit dem projekt-lokalen `remotion render`-Befehl nach `render.mp4` rendern und Dauer und Dimensionen mit `ffprobe` verifizieren.

Keine ist Pflicht. Erfinde Hybride, wenn es nützt (z.B. PIL-Hintergrund mit einer HyperFrames- oder Remotion-Schicht darüber).

**Dauer-Faustregeln, kontextabhängig:**

- **Sync-to-Narration-Erklärungen.** Ein Zuschauer muss den Content bei 1× erfassen. Grober Boden 3s, typisch 5-7s für einfache Cards, 8-14s für komplexe Diagramme. Das Launch-Video lief mit 5-7s pro einfacher Card.
- **Beat-synced Akzente** (Musikvideo, schnelle Montage). 0.5-2s ist okay: sie sind visuelle Akzente, keine Information. Die "lesbar bei 1×"-Regel wird zu *"erkennbar bei 1×"*, nicht *"voll erfassbar."*
- **Letzten Frame ≥ 1s halten** vor dem Schnitt (universell).
- **Über Voiceover:** Gesamtdauer ≥ `narration_length + 1s` (universell).
- **Nie unabhängige Elemente parallel enthüllen**: das Auge kann nicht zwei neue Dinge gleichzeitig verfolgen. Ein Ding, Pause, nächstes Ding.

**Animations-Payoff-Timing (Regel für Sync-to-Narration):** hol den Timestamp des Payoff-Wortes. Starte das Overlay `reveal_duration` Sekunden früher, damit der Landing-Frame mit dem gesprochenen Payoff-Wort zusammenfällt. Ohne diesen Sync wirkt die Animation losgelöst.

**Easing** (universell, nie `linear`, sieht robotisch aus):

```python
def ease_out_cubic(t):    return 1 - (1 - t) ** 3
def ease_in_out_cubic(t):
    if t < 0.5: return 4 * t ** 3
    return 1 - (-2 * t + 2) ** 3 / 2
```

`ease_out_cubic` für einzelne Reveals (langsames Landen). `ease_in_out_cubic` für kontinuierliche Draws.

**Typing-Text-Anker-Trick:** auf die Breite des VOLLEN Strings zentrieren, nicht die Teil-String-Breite, sonst rutscht der Text während des Reveals nach links.

**Beispiel-Palette** (das Launch-Video, eine Ästhetik unter unendlich vielen):
- Hintergrund `(10, 10, 10)` Near-Black
- Akzent `#FF5A00` / `(255, 90, 0)` Orange
- Labels `(110, 110, 110)` Dim-Gray
- Schrift: Menlo Bold unter `/System/Library/Fonts/Menlo.ttc` (Index 1)
- ≤ 2 Akzentfarben, ~40% Leerraum, minimales Chrome
- Ergebnis: Terminal-/Retro-Tech-Feel

Das ist ein Stil. Wenn die Brand warm und serif ist, nutz das. Wenn sie bunt und verspielt ist, nutz das. Wenn der Nutzer dir einen Styleguide gegeben hat, folg ihm. Wenn nicht, schlag einen vor und bestätige.

**Parallel-Sub-Agent-Brief** : jede Animation ist ein Sub-Agent, gespawnt über das `Agent`-Tool. Jeder Prompt ist self-contained (Sub-Agents haben keinen Parent-Kontext). Enthalte:

1. Ein-Satz-Ziel: *"Bau EINE Animation: [Spec]. Nichts sonst."*
2. Absoluter Output-Pfad (`<edit>/animations/slot_<id>/render.mp4`)
3. Exakte technische Spec: Auflösung, fps, Codec, pix_fmt, CRF, Dauer
4. Stil-Palette als konkrete Werte (RGB-Tupel, Hex oder Referenz auf ein Design-System)
5. Font-Pfad mit Index
6. Frame-für-Frame-Timeline (was wann passiert, mit Easing)
7. Anti-Liste ("kein Chrome, keine Extras, keine Titel, außer angegeben")
8. Code-Pattern-Referenz (Helfer inline kopieren, nicht über Slots hinweg importieren)
9. Deliverable-Checkliste (Skript, Render, Dauer via ffprobe verifizieren, Report)
10. **"Stell keine Fragen. Wenn etwas mehrdeutig ist, wähle die naheliegendste Interpretation und mach weiter."**

Ein Sub-Agent = eine Datei (eindeutige Dateinamen, parallele Agents überschreiben sich nicht).

## Output-Spec

Match die Source, außer der Nutzer hat etwas Konkretes verlangt. Übliche Ziele: `1920×1080@24` cineastisch, `1920×1080@30` Screen-Content, `1080×1920@30` Vertical-Social, `3840×2160@24` 4K-Kino, `1080×1080@30` quadratisch. `render.py` setzt die Skalierung per Default auf 1080p aus jeder Source; übergib `--filter` oder editiere den Extract-Befehl für andere Ziele. Lohnt zu fragen, welches Liefer-Format wichtig ist.

## EDL-Format

```json
{
  "version": 1,
  "sources": {"C0103": "/abs/path/C0103.MP4", "C0108": "/abs/path/C0108.MP4"},
  "ranges": [
    {"source": "C0103", "start": 2.42, "end": 6.85,
     "beat": "HOOK", "quote": "...", "reason": "Cleanest delivery, stops before slip at 38.46."},
    {"source": "C0108", "start": 14.30, "end": 28.90,
     "beat": "SOLUTION", "quote": "...", "reason": "Only take without the false start."}
  ],
  "grade": "warm_cinematic",
  "overlays": [
    {"file": "edit/animations/slot_1/render.mp4", "start_in_output": 0.0, "duration": 5.0}
  ],
  "subtitles": "edit/master.srt",
  "total_duration_s": 87.4
}
```

`grade` ist ein Preset-Name oder roher ffmpeg-Filter. `overlays` sind gerenderte Animations-Clips. `subtitles` ist optional und wird ZULETZT angewandt.

## Memory : `project.md`

Häng eine Sektion pro Session an `<edit>/project.md` an:

```markdown
## Session N - YYYY-MM-DD

**Strategy:** one paragraph describing the approach
**Decisions:** take choices, cuts, grades, animations + why
**Reasoning log:** one-line rationale for non-obvious decisions
**Outstanding:** deferred items
```

Beim Start `project.md` lesen, falls vorhanden, und die letzte Session in einem Satz zusammenfassen, bevor du fragst, ob fortgesetzt werden soll.

## Anti-Patterns

Dinge, die unabhängig vom Stil konsistent scheitern:

- **Hierarchische vor-berechnete Codec-Formate** mit USABILITY-/Ton-Tags/Shot-Layern. Over-Engineering. Aus dem Transkript im Moment der Entscheidung ableiten.
- **Handgetunte Moment-Scoring-Funktionen.** Das LLM wählt besser als jede Heuristik, die du schreiben wirst.
- **Whisper-SRT / Phrasen-Output.** Verliert Sub-Sekunden-Lückendaten. Immer Wort-genau wörtlich.
- **Whisper lokal auf CPU laufen lassen.** Langsam und es normalisiert Filler. Nutz gehostetes Scribe.
- **Untertitel in die Base brennen, bevor Overlays komponiert sind.** Overlays verdecken sie. (Hard Rule 1.)
- **Single-Pass-Filtergraph, wenn du Overlays hast.** Encodiert doppelt. Nutz Pro-Segment-Extract → Concat.
- **Lineares Animations-Easing.** Sieht robotisch aus. Immer cubic.
- **Harte Audio-Schnitte an Segment-Grenzen.** Hörbare Pops. (Hard Rule 3.)
- **Typing-Text auf den Teil-String zentriert.** Text rutscht nach links, während er wächst.
- **Sequentielle Sub-Agents für mehrere Animationen.** Immer parallel.
- **Schneiden, bevor die Strategie bestätigt ist.** Niemals.
- **Gecachte Sources neu transkribieren.** Unveränderliche Outputs unveränderlicher Inputs.
- **Annehmen, was für ein Video es ist.** Erst schauen, dann fragen, zuletzt schneiden.
