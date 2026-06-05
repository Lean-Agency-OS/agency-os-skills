# Video Editing Workflow

Step-by-step Referenz fuer Claude.

## Edit-Workflow (mit Rohvideo)

1. Nutzer legt Roh-MP4 in `raw/<projektname>/`
2. Nutzer sagt: *"Edit @raw/<projektname>/<datei>.mp4 in eine Folge."*
3. **Transkript** mit ElevenLabs Scribe (Default) oder Whisper-Fallback. Output: `projects/<name>/transcripts/master.json` + `master.srt`
4. **Pre-Cut-Checks und Cut-Plan auf Deutsch:** Cut-Standards (Padding, Silence-Checks, Last-Word-Two-Step, EDL-Format): siehe [cut-standards.md](cut-standards.md). Plan mit Versprecher-Findings + Padding pro Range -> wartet auf Nutzer-OK
6. **Cut-Apply** -> `projects/<name>/clips/edited.mp4`
7. **Workflow-Branch (Pflicht-Frage):**
   - Direkt Hyperframes - Claude baut Compositions, braucht Brand
   - Claude Design - Claude exportiert nur Transcript, wartet aufs Bundle
8. **Storyboard** auf Deutsch -> wartet auf Nutzer-OK
9. **Compositions bauen** (eine pro Szene, parallel via Sub-Agents wo sinnvoll)
10. **Preview** auf localhost:3002 (Hyperframes) oder localhost:3030 (Bundle)
11. **Iteration** auf Feedback
12. **Final-Render** unter `projects/<name>/renders/final.mp4` (1920x1080 / 30fps default, 1080x1920 fuer Shorts)
13. **Self-Eval** per `timeline_view`-Pattern bevor Preview gezeigt wird

## Pure-Animation-Workflow (ohne Rohvideo)

Identisch ab Schritt 7 - Nutzer beschreibt das Video, Claude erzeugt Storyboard und baut.


## Claude-Design-Bundle-Pipeline

Wenn Nutzer eine HTML aus claude.ai liefert:

### 1. Bundle entpacken

Single HTML enthaelt `<script type="__bundler/manifest">`. Per-Entry `compressed: true` (gzip) oder `false` (raw base64). Files nach `projects/<name>/_bundle_assets/<uuid>.<ext>`.

### 2. Format-Check VOR Patches

| | Format A (Hyperframes-runtime) | Format B (React+Babel+Stage) |
|---|---|---|
| Groesse | ~400 KB | ~1.5 MB |
| Mount-Target | `#main` | `#root` |
| Player-API | `window.__player` direkt | Stage hat `useTime()` muss gepatcht werden |
| Patches noetig | **NEIN** | **JA** (3 Patches) |

Detection: `_bundle_assets/*.jsx` -> Format B. Extracted JS mit `var HyperShader` -> Format A.

### 3. Render-Mode-Patches (NUR Format B)

- **App:** `{!renderMode && <TweaksPanel>...}` ausblenden in renderMode
- **Stage:** `window.__setStageTime(t)` exponieren, kein rAF-Loop
- **Video:** NUR `video.currentTime = t`, NIEMALS `video.play()` / `video.pause()`

**`?render=1` ist eine Falle.** Stattdessen `evaluateOnNewDocument`:
```js
await page.evaluateOnNewDocument(() => {
  window.__renderMode = true;
  window.__hfVideoUrl = "/assets/speaker.mp4";
});
await page.goto("http://localhost:3034/");  // KEIN ?render=1
```

### 4. Speaker-Video All-Intra-Keyframes (PFLICHT)

```bash
ffmpeg -i clips/edited.mp4 \
  -c:v libx264 -preset fast -crf 18 \
  -g 1 -keyint_min 1 -sc_threshold 0 \
  -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k \
  assets/speaker.mp4
```

Sonst snappt `video.currentTime = t` zum naechsten Keyframe und Speaker haengt.

### 5. Render

- `waitUntil: "load"` (NICHT `networkidle0`)
- Auf `window.__renderReady === true` pollen bevor Frame-Capture
- Audio aus `assets/speaker.mp4` muxen
- chrome-headless-shell aus `~/.cache/hyperframes/chrome/...`

### Anti-Patterns

- NICHT `npx hyperframes preview` fuer Bundles (StaticGuard rejected)
- NICHT `npx hyperframes render` direkt aufs Bundle (gleicher Reject)
- NICHT `page.screencast()` (laggt, dropped frames)
- NICHT Render ohne Keyframe-Conversion (Speaker haengt)
