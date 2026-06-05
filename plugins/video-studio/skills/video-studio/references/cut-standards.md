# Cut-Standards (Pflicht)

Diese Regeln sind **nicht verhandelbar**. Claude muss sie bei jedem Schnitt anwenden, sonst klingt der Cut entweder gehetzt oder traege.

---

## Pre-Cut-Checks (Pflicht vor jedem Cut)

Vor dem Schnitt immer diese drei Schritte ausfuehren:

1. **Transkript-Packing:**
   ```bash
   uv run --project ./video-use python ./video-use/helpers/pack_transcripts.py \
     --edit-dir "projects/<projektname>" --silence-threshold 0.4
   ```

2. **Silence-Detection auf Source:**
   ```bash
   ffmpeg -hide_banner -nostats -i raw/<projekt>/<file>.mp4 \
     -af "silencedetect=noise=-30dB:duration=0.25" -f null - 2>&1 | grep "silence_"
   ```

3. **Vergleichen und verdaechtige Sub-Slices re-scriben:**
   - Verdaechtig: einsilbiges Wort mit Dauer > 1.5s
   - Gaps mit Audio, die die Silence-Map nicht komplett als still markiert
   - Suspekte Stammer, Atmer, Doppelversuche

   Audio-Sub-Slice extrahieren (bei Verdacht):
   ```bash
   ffmpeg -y -hide_banner -nostats -i raw/<projekt>/<file>.mp4 \
     -ss <start_sec> -to <end_sec> -vn -ac 1 -ar 16000 -c:a pcm_s16le \
     /tmp/_slice.wav
   ```

   An ElevenLabs Scribe schicken:
   ```bash
   KEY=$(grep '^ELEVENLABS_API_KEY=' .env | cut -d= -f2)
   curl -sS -X POST "https://api.elevenlabs.io/v1/speech-to-text" \
     -H "xi-api-key: $KEY" \
     -F "file=@/tmp/_slice.wav;type=audio/wav" \
     -F "model_id=scribe_v1" \
     -F "language_code=de" \
     -F "timestamps_granularity=word" \
     -F "diarize=false"
   ```

---

## Cut-Padding pro Cut-Typ

| Cut-Typ | Tail (nach Wort) | Lead (vor Wort) | Hinweis |
|---|---|---|---|
| Mid-sentence (Komma) | 100ms | 80ms | Konstruktion setzt sich fort |
| Sentence-boundary (Punkt, ?, !) | 200ms | 130-150ms | Satz endet |
| Video-Anfang | - | 130-150ms | Opener, Lead-Padding vor erstem Wort |
| Video-Ende | 600-700ms | - | Nach **echtem** Word-End (via Last-Word-Two-Step) |

**Cut-Typ erkennen:** letztes Wort vor dem Cut endet mit `,` und Satz setzt fort = Mid. Mit `.`, `?` oder `!` = Boundary. Letzte Range im EDL = Video-Ende.

---

## Last-Word-Two-Step (Pflicht fuer Video-Ende)

Das letzte Wort eines Videos ist kritisch. Full-Context Scribe markiert es oft 1-2 Sekunden zu spaet, weil Atemzug-Decay als Word-Tail gerechnet wird. Deshalb ist ein zwei-stufiger Prozess Pflicht:

### Schritt 1: Isolieren und Re-Scriben
Letztes Wort des Videos extrahieren und nochmal an Scribe schicken. Beispiel:
- Full-Context Scribe gibt: `'schneiden.' 65.06-66.92` (Dauer 1.86s, offensichtlich falsch)
- Slice `ffmpeg -ss 64.06 -to 67.92` + Scribe-Call
- Slice-Transkription gibt: `'schneiden.' 65.04-65.42` (Dauer 0.38s, korrekt)

### Schritt 2: Echten Word-End nutzen
Range-End berechnen:
```
Range-End = echter Word-End (aus Slice) + 600-700ms Atemraum
```

Zahlenbeispiel:
- Echter Word-End: 65.42s
- Video-Ende-Tail: 630ms (0.63s)
- Range-End: 65.42 + 0.63 = 66.05s

---

## EDL-Format mit _padding_params

Jede `edl.json` muss einen `_padding_params`-Block enthalten. Keine willkuerlichen Magic-Numbers. Padding ist dokumentiert und nachjustierbar:

```json
{
  "sources": {
    "name": "raw/myprojekt/take_001.mp4"
  },
  "grade": null,
  "_padding_params": {
    "mid_sentence_tail_ms": 100,
    "mid_sentence_lead_ms": 80,
    "sentence_boundary_tail_ms": 200,
    "sentence_boundary_lead_ms": 140,
    "video_end_tail_ms": 630
  },
  "ranges": [
    {
      "start": 2.5,
      "end": 8.3,
      "cut_type": "mid_sentence"
    },
    {
      "start": 8.5,
      "end": 15.8,
      "cut_type": "sentence_boundary"
    }
  ]
}
```

---

## Cut-Plan und Bestaetigung

Vor jedem Cut:

1. **Plan auf Deutsch schreiben** (Plain Language, keine Markup-Slang)
   - Kurze Zusammenfassung der Pre-Cut-Checks (Versprecher-Findings)
   - Gewaehltes Padding pro Range mit Begruendung
   - Zeitstempel und Worte, die gekuerzt werden

2. **Warten auf Nutzer-OK** bevor Render startet

3. **Korrektionen:** gleiche Werkzeuge und Workflow nutzen, nicht raten

---

## grade auf Cowork/Linux

`grade: "auto"` funktioniert einwandfrei. (Nur auf Windows waere es broken, dort `grade: null`. In Cowork irrelevant.)
