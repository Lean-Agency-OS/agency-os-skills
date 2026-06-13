# Motion-Style (Projekt-Ergaenzungen zu hyperframes)

Foundation: hyperframes house-style.md / visual-styles.md. Dieses Dokument enthaelt NUR die projekt-spezifischen Regeln, die ueber hyperframes hinausgehen.

## Anchor-Word-Sync

Animation triggert **mit** dem gesprochenen Wort aus dem Transkript, +/-100ms Toleranz. Nicht davor (Spoiler-Effekt), nicht danach (Verzoegerungs-Effekt).

Word-Timestamps kommen aus `master.json` (ElevenLabs Scribe oder Whisper). Composition nutzt `gsap.to()` mit exakten t-Werte fuer den Start jeder Overlay-Animation:

```javascript
const wordStart = transcriptData.words[i].start_time_ms; // in Millisekunden
gsap.to(element, {
  opacity: 1,
  duration: 0.3,
  delay: wordStart / 1000 + 0.05, // +50ms Lead-Zeit als Puffer
});
```

Regel: Lead-Zeit vor dem Wort maximal 100ms, Tail nach dem Wort maximal 100ms.

## Render-Defaults

- **4K:** 3840x2160 (16:9) oder 2160x3840 (9:16) @ 60fps
- **1080p:** 1920x1080 (16:9) oder 1080x1920 (9:16) @ 30fps
- **Speaker-Video vor Bundle-Render:** All-Intra-Keyframes PFLICHT (`-g 1` ffmpeg / `keyframe_interval: 1` in Render-Config)
  - Begruendung: Scrubbar im Editor + Transkript-Sync ohne Key-Frame-Latenz

## Font-Ergaenzungen (ueber hyperframes hinaus)

Basis: hyperframes visual-styles.md / house-style.md (Font-Discovery + verbotene Fonts). Zusaetzlich:

**Wenn Brand-Guidelines Playfair Display, Fraunces oder Cormorant Garamond zwingen:** Nutze sie fuer serifftypograefie, aber NUR fuer Display/Headlines, niemals Body-Text.

**Default Mono-Stack (wenn nicht vorgegeben):** JetBrains Mono oder Berkeley Mono (nicht Courier, nicht Courier New).

## Easing-Praeferenz (Projekt-Minimum)

hyperframes deckt Easings bereits ab. Zusaetzliche Projekt-Regel:

Pro Szene **mindestens 3 verschiedene Easings verwenden**. Wenn mehrere Elemente sequenziell einfahren, gestaffelt nach:
1. Erstes Element: `power3.out`
2. Zweites Element: `sine.inOut`
3. Drittes+ Element: `elastic.out` oder `back.out` (je nach Energielevel)

NIEMALS `linear` (wirkt maschinell).
