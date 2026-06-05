# video-studio

Ein Claude-Skill für KI Video Editing: Schnitt + Untertitel + Motion Graphics. **Dieses Repo ist der Skill** - zum Ausliefern den Ordner nach `<os>/.claude/skills/video-studio/` kopieren.

Zwei Workflows:
1. **Edit:** Rohvideo -> Transkription (ElevenLabs Scribe) -> Schnitt -> Motion Graphics -> Render
2. **Pure-Animation:** Storyboard -> Hyperframes-Compositions -> Render (ohne Rohvideo)

## Inhalt
```
SKILL.md      Orchestrator + Workflow (Einstieg)
references/    cut-standards.md, motion-style.md, video-editing-workflow.md
engines/       video-use/ (Schnitt, Python) + hyperframes/ (Motion Graphics, npm)
scripts/       setup.sh, doctor.sh
.env.example   ELEVENLABS_API_KEY etc.
deploy.sh      kopiert den Skill in ein Kunden-OS
```
manim ist entfernt: alle Animationen (auch Diagramme/Daten) laufen über hyperframes.

## Ausliefern
```bash
bash deploy.sh /pfad/zum/kunden-os
```
Kopiert den Skill nach `<os>/.claude/skills/video-studio/` (ohne Dev/Runtime). Im Ziel-OS (Claude Cowork):
```bash
bash .claude/skills/video-studio/scripts/setup.sh   # Engines installieren (uv + npm + Chromium)
# ELEVENLABS_API_KEY in .claude/skills/video-studio/.env eintragen
bash .claude/skills/video-studio/scripts/doctor.sh  # pruefen
```
Dann natürlichsprachig, z.B.: *"Schneid mir das Video … zu einem Reel."* Brand kommt aus `01-context/brands/{brand}/`, Output nach `07-content/reels/{slug}/`.

## Voraussetzungen (im Ziel-OS / Sandbox)
ffmpeg (mit libass), node 22+, python 3.10+, uv. In Claude Cowork vorinstalliert (Chromium wird per setup.sh nachgezogen).

## Docs
- [SKILL.md](SKILL.md) - Operating Manual
- [references/cut-standards.md](references/cut-standards.md) - Schnitt-Standards (Pflicht)
- [references/motion-style.md](references/motion-style.md) - Motion-Ergänzungen zu hyperframes
- [engines/video-use/UPSTREAM.md](engines/video-use/UPSTREAM.md) - Engine-Herkunft
