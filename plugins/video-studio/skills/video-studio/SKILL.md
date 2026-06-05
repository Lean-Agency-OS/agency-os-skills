---
name: video-studio
description: Schneidet Roh-Videos zu fertigen Reels/Shorts/Clips - Transkript, Schnitt, Untertitel, Motion Graphics, Render. Triggert bei "schneid das Video", "mach ein Reel draus", "bau ein Short aus diesem Video", "/video", "/reel", "kuerz das Video", "Untertitel aufs Video", "video-studio". Brand-aware ueber 01-context/brands/{brand}/, nutzt brand-voice + icp. Output in 07-content/reels/{datum-slug}/.
---

# Skill: video-studio

**Zweck:** Aus einem Roh-Video ein sendefertiges Reel/Short bauen. EIN Einstiegspunkt - die Engines laufen intern dahinter, der Nutzer sieht nur diesen Skill.

**Brand-Wahl:** Gibt es unter `01-context/brands/` genau eine Brand mit `brand-config.md` auf `status: active`, ist sie der Default. Bei mehreren aktiven Brands: fragen.

**Zwei Phasen:** Phase 1 = Schnitt + Untertitel (reines ffmpeg). Phase 2 = Motion Graphics via hyperframes (braucht Chromium).

---

## Struktur (alles in diesem Skill, self-contained)

**Code** (in diesem Skill-Ordner, wird bei Plugin-Updates ersetzt):
- `engines/video-use/` - Schnitt-Engine-Quellcode (Python, ElevenLabs Scribe, ffmpeg).
- `engines/hyperframes/` - Motion-Graphics-Engine (package.json; Install landet im Daten-Verzeichnis).
- `references/cut-standards.md` - **die** Quelle fuer Padding, Silence-Checks, Last-Word-Two-Step, EDL-Format.
- `references/motion-style.md` - projekt-eigene Motion-Regeln (Anchor-Word-Sync, Render-Defaults).
- `engines/video-use/SKILL.md` - die Hard Rules der Schnitt-Engine (Referenz, kein eigener Trigger).

**Daten** (persistent, ueberleben Plugin-Updates — liegen im Plugin-Daten-Verzeichnis):
- `$DATA/.env` - `ELEVENLABS_API_KEY`
- `$DATA/venv/` - Python-Env der Schnitt-Engine
- `$DATA/hyperframes/node_modules/` - Node-Deps inkl. hyperframes-Skill (house-style.md / visual-styles.md)
- `$DATA/chromium-cache/` + `$DATA/.chromium-path` - Chromium fuer Motion Graphics
- `$DATA/.ready` - Setup-Marker (mit Plugin-Version)

Abkuerzungen in den Befehlen unten, vor dem ersten Befehl einmal ermitteln:
- `VS` = **absoluter Pfad des Ordners, in dem diese SKILL.md liegt** (bei Plugin-Installation der Plugin-Ordner im Cache, bei manueller Installation `.claude/skills/video-studio`)
- `DATA` = `${CLAUDE_PLUGIN_DATA}`, falls nicht gesetzt: `~/.claude/plugins/data/video-studio`

---

## Phase 0: Setup-Gate (PFLICHT, still)

1. `bash $VS/scripts/doctor.sh`. Bei `OFFEN .ready` oder `OFFEN Plugin aktualisiert` -> `bash $VS/scripts/setup.sh`, Ausgabe zeigen, doctor erneut.
2. Bei `OFFEN ELEVENLABS_API_KEY` -> Nutzer bitten, Key in `$DATA/.env` einzutragen, dann stoppen.
3. Bei `FEHLT ffmpeg/node/python` -> Hard-Stop (Umgebung ohne Tools).

Nur wenn Doctor sauber -> weiter.

---

## Phase 1: Brief + Plan (Stop-Punkt, Deutsch)

**1a. Inputs:** Roh-Video-Pfad; Brand (siehe Brand-Wahl oben); Format `9:16` (default), `16:9` oder `1:1`; Untertitel ja/nein; Motion Graphics ja/nein.

**1b. Ordner:** `07-content/reels/{YYYY-MM-DD}-{kebab-slug}/`, Media-Unterordner `_work/` (gitignored).

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

## Phase 2: Transkribieren

```bash
VS={absoluter Pfad dieses Skill-Ordners}
DATA={Plugin-Daten-Verzeichnis, siehe oben}
PY=$DATA/venv/bin/python
EDIT=07-content/reels/{slug}/_work/edit
set -a; . "$DATA/.env"; set +a
$PY $VS/engines/video-use/helpers/transcribe.py "{video}" --edit-dir "$EDIT"
$PY $VS/engines/video-use/helpers/pack_transcripts.py --edit-dir "$EDIT" --silence-threshold 0.4
```

Transkript ist gecached (kein Re-Transkribieren, ausser Source aenderte sich).

---

## Phase 3: Schnitt planen (LLM-Reasoning)

**Pflicht-Lektuere zuerst:**
- `$VS/references/cut-standards.md` - Padding-Tabelle, Pre-Cut-Checks, Last-Word-Two-Step, EDL-Format.
- `$VS/engines/video-use/SKILL.md` - Hard Rules (nie im Wort schneiden, Subtitles zuletzt im Filter, 30ms Audio-Fades, etc.).

Aus `{EDIT}/takes_packed.md` den Cut planen, Silence-Map + verdaechtige Sub-Slices laut cut-standards.md pruefen. EDL als JSON mit `_padding_params`-Block schreiben. Drill-down nur bei Bedarf via `timeline_view.py`.

---

## Phase 4: Render

```bash
VS={absoluter Pfad dieses Skill-Ordners}
DATA={Plugin-Daten-Verzeichnis, siehe oben}
PY=$DATA/venv/bin/python
set -a; . "$DATA/.env"; set +a
$PY $VS/engines/video-use/helpers/render.py "{EDIT}/edl.json" \
  -o "07-content/reels/{slug}/_work/final.mp4" --build-subtitles
```

Untertitel-Ton vor dem Burn-in via `brand-voice`-Skill gegen das Brand-Profil pruefen. Subtitle-Farbe/Font aus `01-context/brands/{brand}/ci.md`.

---

## Phase 5: Motion Graphics (optional, hyperframes)

Nur wenn in Phase 1 gewuenscht. Voraussetzung: Chromium (Doctor zeigt OK).

- Lektuere: `$VS/references/motion-style.md` (Anchor-Word-Sync, Render-Defaults) + hyperframes-Skill in `$DATA/hyperframes/node_modules/hyperframes/dist/skills/hyperframes/SKILL.md`.
- Brand: Farben/Fonts/Logo aus `01-context/brands/{brand}/ci.md`. Hooks/CTA via `icp`-Skill.
- Compositions bauen, Puppeteer-Render (Executable-Path aus `$DATA/.chromium-path`), Overlays nach cut-standards/motion-style ueber den Cut legen.

---

## Phase 6: Self-Eval + Ablegen

- **Self-Eval (einmal):** fertigen Cut gegen die EDL pruefen (Schnitt-im-Wort + Untertitel-Leaks) per `timeline_view`-Stichproben an den Schnitt-Raendern. Nicht pro Render.
- **Ablage (OS-Convention):** `07-content/reels/{slug}/_index.md` schreiben (getrackt), Media bleibt in `_work/` (gitignored):

```markdown
# {Titel}
- Brand: {brand}  | Format: {9:16}
- Hook: {1 Satz}
- Status: Rohschnitt fertig
- Render: _work/final.mp4
- Datum: {YYYY-MM-DD}
```

- Daily-Log-Notiz in `08-logs/{YYYY-MM-DD}.md` ergaenzen.

---

## Kontext-Bridge (Pflicht, Projekt-Skills haben Vorrang)

- **brand-voice** fuer Untertitel-/Text-Ton (`01-context/brands/{brand}/voice-profile.md`, Fallback `voice.md`).
- **icp** fuer Hook/CTA-Bewertung (`01-context/brands/{brand}/icp.md`).
- **CI** aus `01-context/brands/{brand}/ci.md` (Farben, Fonts, Logo).
