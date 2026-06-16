# Transkriptions-Policy

Welche Engine wofuer, warum Word-Level Pflicht ist, und was passiert, wenn
Scribe nicht erreichbar ist. Diese Regeln gelten fuer jede Transkription in
den video-* Skills.

## Drei Einsatzweisen

| Modus | Aufruf | Wann | Output | Voraussetzung |
|---|---|---|---|---|
| **Scribe** (Default) | `transcribe.py <v>` | Der **echte** Schnitt-Transkript, immer wenn geschnitten wird. | Verbatim, Diarisierung, Audio-Events, **Word-Timestamps** -> `<stem>.json` | `ELEVENLABS_API_KEY` + Netz |
| **Whisper Text-only (Gist)** | `transcribe.py <v> --text-only` | Viele Files rein, schnell wissen **was gesprochen wird**. Kein Schnitt. | Nur Volltext, **keine** Timestamps -> `<stem>.txt` (+ `gist.md` im Batch) | `.[whisper]`, kein Key/Netz |
| **Whisper mit Timestamps** | automatisch als Fallback (oder `--engine whisper`) | **Fallback**, wenn Scribe nicht erreichbar ist (kein Netz / down). | Word-Timestamps, Volltext, **keine** Diarisierung -> `<stem>.json` | `.[whisper]`, kein Key/Netz |

**Wichtig: die zwei Whisper-Modi nicht verwechseln.**
- Text-only (`--text-only`) ist der schnelle Ueberblick. Er schreibt `.txt`,
  ist **kein** Cut-Artefakt und taugt nicht zum Schneiden (keine Timestamps).
- Der Fallback braucht zwingend Timestamps (sonst kann der Schnitt nicht
  arbeiten) und laeuft daher **immer** mit `word_timestamps=True`, nie als
  Text-only.

Scribe und der Timestamp-Whisper schreiben **dasselbe JSON-Format** nach
`<edit>/transcripts/<stem>.json` (`words[]` mit `type`/`start`/`end`/`text`/
`speaker_id`). Damit laufen `pack_transcripts.py`, `render.py` und
`timeline_view.py` unveraendert, egal welche der beiden die Daten erzeugt hat.
Der Text-only-Gist landet bewusst getrennt als `.txt`, damit er die Cut-Daten
nicht ueberschreibt.

## Harte Regel: immer Word-Level, nie nur Volltext

Der Schnitt schneidet auf **Wortgrenzen** (siehe [hard-rules.md](hard-rules.md),
Regeln 6-8). Ein Transkript ohne Wort-Timestamps ist fuer den Cut wertlos.
Deshalb:

- **Nie** der SRT-/Phrasen-Modus von Scribe (verliert Sub-Sekunden-Luecken).
- **Nie** ein Whisper-Modus, der nur den Gesamttext liefert. Der lokale Pfad
  laeuft mit `word_timestamps=True` : auch der Fallback behaelt die Zeitmarken.

## Engine-Wahl (von aussen entschieden)

```bash
# Gist: viele Files, nur "was wird gesprochen", lokal, schnell:
$PY helpers/transcribe_batch.py "$RAWDIR" --text-only      # -> *.txt + gist.md

# Akkurater Schnitt-Transkript (Default, faellt bei Bedarf auf Whisper zurueck):
$PY helpers/transcribe.py "{video}" --edit-dir "$EDIT"
```

Reihenfolge in der Praxis: erst `--text-only` fuer den Ueberblick (schreibt
`.txt`/`gist.md`, ruehrt die Cut-Daten nicht an), dann der Default-Scribe-Lauf
fuer den finalen, diarisierten Transkript (`.json`), sobald die Strategie steht.
`--force` brauchst du nur, um eine bestehende **`.json`** zu ersetzen, z.B. ein
Fallback-Whisper-Transkript durch das echte Scribe-Ergebnis, sobald wieder Netz
da ist.

## Fallback-Kette (Scribe nicht erreichbar)

Default-Verhalten beim `scribe`-Pfad: schlaegt der API-Call fehl, wird
automatisch der lokale Whisper-Pfad genommen, **mit** Word-Timestamps. So
bekommst du immer ein schneidbares Transkript, auch offline.

```
scribe
  -> Retry mit Backoff (429 / 5xx, mehrfach)
  -> wenn weiter nicht erreichbar UND Fallback aktiv:
       lokales whisper (Word-Timestamps, KEINE Diarisierung)
       JSON wird markiert: "fallback_from": "scribe", "fallback_reason": "..."
```

- Steuerung: `--no-fallback` erzwingt scribe-only (harter Abbruch statt
  stillem Qualitaetsverlust).
- Voraussetzung fuer den Fallback: das `.[whisper]`-Extra muss installiert
  sein. Das ist **nur beim Skill mit lokaler Transkription** der Fall
  (`video-footage-mining`, Marker `.needs-whisper`). Die Scribe-Cut-Skills
  (`video-shortform`, `video-roughcut`, `video-captions`) installieren es bewusst
  nicht und sind Scribe-only: ist Scribe nicht erreichbar, brechen sie mit
  klarer Meldung ab, statt leise auf lokales Whisper zu degradieren.
- **Folge fuer den Schnitt:** Ein Fallback-Transkript hat keine Sprecher-IDs.
  Bei Multi-Speaker-Material fehlt die Sprecher-Trennung : pruefe das `engine`-
  bzw. `fallback_from`-Feld im JSON, bevor du dich auf Diarisierung verlaesst.

## Caching

Pro Source ein Transkript (`<stem>.json`). Existiert es, wird nicht neu
transkribiert. Neu erzwingen nur mit `--force` (z.B. Rough-Pass durch Scribe
ersetzen, oder ein Fallback-Transkript spaeter durch das echte Scribe-Ergebnis
austauschen, sobald wieder Netz da ist).
