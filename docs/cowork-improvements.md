# agency-os-video — Verbesserungen für Cowork

> Stand: v2.1.3 · geprüft am 2026-06-16 gegen `packages/video-engine/` (Quelle) und die vendorte Kopie in `plugins/agency-os-video/skills/video-shortform/`.
> Kontext: Aus einer echten Cowork-Schnitt-Session (Reels „Test 2"). Cowork mountet Remote-Plugins **read-only**, hat ein **45-s-Limit pro Shell-Call** und killt **Hintergrund-Prozesse** beim Call-Ende. Claude Code (Terminal) hat diese Einschränkungen nicht.

---

## Designprinzip: Checks statt Umgebungs-Raten

Statt „Cowork vs. Claude Code" hart zu unterscheiden, die **Fähigkeit zur Laufzeit ermitteln** und sich anpassen:

- **Probe, wenn der Test billig und eindeutig ist** (Schreibrecht, `ffmpeg`/`ffprobe` vorhanden, Netz für Scribe). → der passende Pfad wird automatisch gewählt.
- **Idempotenz / Fail-safe, wenn sich die Fähigkeit nicht sauber testen lässt** (Call-Zeitlimit, Prozess-Lebensdauer). → die Operation so bauen, dass die Umgebung egal ist.
- **Bei Unsicherheit auf den konservativeren Pfad defaulten.**

So bleibt der Claude-Code-Pfad unverändert, und Cowork „gewinnt" automatisch, ohne dass der Code wissen muss, wo er läuft.

---

## Bereits umgesetzt (verifiziert)

- **Overlap-freie Captions** — `packages/video-engine/helpers/render.py` (~Z. 422–436): Cue-Ende wird auf den Start des nächsten Cues geclamped. Behebt das „Hochspringen" gestapelter Untertitel (das eigentliche Problem — Single-Line ist dafür nicht nötig). ✔ (v2.1.2)
- **Safe-Zone-Untertitel** — `render.py` `SUB_FORCE_STYLE` `MarginV=90` mit dokumentierter Begründung (UI-Zone der Plattformen). ✔ (v2.1.0)
- **Kein Logo** mehr im Default-Composite. ✔ (v2.1.2)
- **Nie auf Schwarzbild starten/enden.** ✔ (v2.1.1)
- **Sprechende Dateinamen / `{slug}.mp4`-Output.** ✔ (v2.1.2/2.1.3)
- **Loudnorm Two-Pass** über Temp-Datei. ✔

---

## Noch offen — priorisiert

### P1 — venv nicht ins (read-only) Skill-Root
**Problem:** `packages/video-engine/scripts/setup.sh` (Z. 8/9/32/57) setzt `ROOT = Skill-Root`, `cd "$ROOT"`, baut `uv venv` dort und schreibt `.ready` dorthin. `SKILL.md` (Z. 25/75/112) hardcodet `$SK/.venv/bin/python`. In Cowork ist der Plugin-Mount read-only (`fuse.bindfs (ro,…)`) → `uv venv` bricht mit „Read-only file system (os error 30)" ab.
**Gilt für Claude Code?** **Nein.** Dort ist das Skill-Verzeichnis beschreibbar, `setup.sh` läuft wie vorgesehen. Reines Cowork-Problem.
**Lösung über Probe (rückwärtskompatibel):** Schreibtest im Skill-Root; nur bei Misserfolg auf einen Cache ausweichen.

```bash
if ( : > "$ROOT/.wtest" ) 2>/dev/null; then
  rm -f "$ROOT/.wtest"; VENV_DIR="$ROOT/.venv"          # beschreibbar (Claude Code) -> wie bisher
else
  VENV_DIR="${VIDEO_ENGINE_VENV:-${XDG_CACHE_HOME:-$HOME/.cache}/agency-os/video-engine/$SKILL}"
fi                                                       # read-only (Cowork) -> Cache
```

**Wichtig:** dieselbe Auflösung muss auch **zur Laufzeit** greifen, nicht nur im Setup — sonst sucht `SKILL.md` weiter nach `$SK/.venv/bin/python`, das im read-only-Fall nie existiert. Lösung: ein kleiner `scripts/resolve-venv.sh` (read-only ausführbar ist ok), den **`setup.sh`, `doctor.sh` und die Helper-Aufrufe** gemeinsam nutzen (`PY="$("$SK/scripts/resolve-venv.sh")/bin/python"`) → eine einzige Wahrheit.
**Nicht** ins Brain/`{context}` legen: ist git-getrackt und wird Mac↔Linux synchronisiert — ein ARM-Linux-venv ist auf dem Mac nutzlos.

### P2 — Render robust gegen Abbruch + Cowork-Zeitlimit
**Problem:** `render.py` extrahiert bei jedem Lauf **alle** Segmente neu (kein Skip für vorhandene `clips_*/seg_NN.mp4`). Bei ~100 s 4K (~1,5× Echtzeit Decode) passt der monolithische Lauf (Extract → Concat → Subtitles → Loudnorm) nicht in einen 45-s-Call; Hintergrund-Prozesse werden gekillt. Ein abgebrochener ffmpeg lässt eine **korrupte** MP4 zurück (`moov atom not found`).
**Gilt für Claude Code?** Der **Zeitlimit-/Hintergrund-Treiber: nein** — dort läuft der Render in einem Durchgang durch. Der **robuste Teil (atomar + resumierbar): überall sinnvoll**, schützt vor korrupten Teildateien bei jedem Abbruch (ffmpeg-Fehler, Ctrl-C, Ruhezustand).
**Lösung über Idempotenz (keine Umgebungs-Probe nötig):**
- Per-Segment **Skip-if-exists** + `ffprobe`-Gültigkeitscheck (kaputte/teilweise Datei → neu rendern).
- **Atomar schreiben:** nach `seg_NN.tmp.mp4` rendern, bei Erfolg auf den finalen Namen umbenennen.
- Dann gilt automatisch: Claude Code = ein Durchgang; Cowork = denselben Befehl mehrfach aufrufen, er macht dort weiter, wo er abgebrochen ist. Optional `--budget-seconds`, um bewusst in Blöcken zu laufen.

### P5 — CI format-agnostisch einlesen
**Problem:** Der Renderer erwartet die CI-Werte (Caption-Farbe, Font …) als **YAML-Frontmatter** in `ci.md`. Das wird aber nicht immer so geliefert — mal Frontmatter, mal Markdown-Tabelle. Das ist **nicht brand-spezifisch**, sondern ein reines Einlese-/Format-Thema.
**Gilt für Claude Code?** Ja — plattformunabhängig.
**Lösung:** Eine Einlese-Schicht, die die CI **normalisiert** und das Ergebnis als **Parameter** an den Renderer übergibt — der Renderer bleibt damit unabhängig vom Dokumentformat:
- Ist **Frontmatter** vorhanden → Werte direkt durchreichen.
- Sonst (z. B. **Tabelle**) → die nötigen Werte daraus extrahieren und genauso als Parameter übergeben.
- In beiden Fällen die Farbe von **Hex → ASS-BGR** konvertieren (`#FED760` → `&H0060D7FE`) und einen **Font-Fallback** anwenden, wenn die Brand-Font-Datei fehlt.

---

## Was wo greift (Übersicht)

| Punkt | Treiber | Claude Code nötig? | Lösungsmuster |
|---|---|---|---|
| P1 venv-Ort | read-only Mount | nein (Cowork-only) | **Probe** (Schreibtest) + gemeinsamer Resolver |
| P2 Render-Robustheit | Zeitlimit / Abbruch | Zeitlimit nein · Atomar/Resume ja (überall gut) | **Idempotenz** (skip-if-exists, temp→rename) |
| P5 CI einlesen | CI-Format variiert | ja | Frontmatter ODER Tabelle → normalisiert als Parameter |

---

## Anmerkung zur Persistenz (warum P1/P2 so gelöst werden)
Coworks Rechen-Sandbox ist ephemer (venv, `/tmp`, installierte Pakete, kopierte Skills verschwinden). **Verbundene Ordner** (z. B. das Brain via virtiofs) sind dagegen echte, dauerhafte Festplatte. Darum: venv & Zwischenstände gehören in den **ephemeren** Cache (rebuildbar), Deliverables in den **verbundenen** Ordner.
