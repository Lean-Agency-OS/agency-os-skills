# video-engine (Dev-Quelle, NICHT ausgeliefert)

Geteilte Engine fuer die `agency-os-video` Skills: Transkription (ElevenLabs Scribe / lokales Whisper),
Schnitt-/Render-Helfer (ffmpeg), Grade/LUT, B-Roll, NLE-Export und die Motion-Graphics-Anbindung
(hyperframes). Plus die kanonischen Referenz-Docs (`references/`).

## Warum hier und nicht im Plugin?

Ein Skill ist **self-contained**: zur Laufzeit laedt die Cowork-Sandbox nur den jeweiligen Skill-Ordner,
nicht den Plugin-Baum. Ein geteilter Engine-Ordner neben den Skills waere also zur Laufzeit nicht da.
Darum lebt der Code **einmal hier** und wird per `tools/sync-engine.sh` in jeden `video-*` Skill kopiert
(gevendort). Die `marketplace.json` liefert nur `./plugins/agency-os-video` aus, dieser `packages/`-Ordner
wird nie als Plugin verpackt.

## Workflow

1. Code **nur hier** in `packages/video-engine/` editieren.
2. `bash tools/sync-engine.sh` ausfuehren: kopiert die pro Skill gebrauchte Teilmenge in
   `plugins/agency-os-video/skills/<skill>/`.
3. Aenderungen committen (Quelle **und** die gevendorten Kopien, da die Kopien ausgeliefert werden).

## Teilmenge pro Skill

Siehe Manifest in `tools/sync-engine.sh`. Kurzfassung:

| Skill | Helfer (zzgl. ffmpeg_utils + transcribe + pack) | hyperframes |
|---|---|---|
| video-shortform | render, grade, broll, timeline_view | ja |
| video-roughcut | export_nle, timeline_view | nein |
| video-captions | render | nein |
| video-footage-mining | transcribe_batch | nein |
