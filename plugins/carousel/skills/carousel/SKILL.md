---
name: carousel
description: >
  Baut Carousel-Posts (10 Slides, 1080×1350, Instagram/LinkedIn) nach der
  4-Bausteine-Formel: Hook → Build → Payoff → CTA. Geführter Workflow:
  Setup (Ziel/CTA/Thema, eine Frage nach der anderen) → 5 Hook-Varianten zur
  Auswahl → vollständiger Build aller 10 Slides ins HTML → Quality-Checks gegen
  das ICP → Preview-Render (render.py) → erst nach "Go" Final-Render zu PNG + PDF.
  Triggern bei: "bau mir einen Carousel", "Carousel-Post zu", "Carousel-Idee",
  "Slides für Instagram", "Karussell-Post", "Carousel erstellen".
---

# Carousel-Builder

Baut einen 10-Slide-Carousel von der Idee bis zu fertigen PNGs + PDF + Caption. Methodik: 4-Bausteine-Formel (`references/4-bausteine-formel.md`) + Slide-Anatomie (`references/slide-anatomy.md`).

**Resources (im Skill-Ordner):**
- `resources/template.html` — generischer, CI-getriebener 10-Slide-Starter (1080×1350, 4:5). Wird als `carousel.html` in den Output-Ordner kopiert und gefüllt. Das ist der Render-Input.
- `resources/preview-template.html` — statisches IG-Mobile-Mockup mit Platzhaltern (`{{CAROUSEL_STYLES}}`, `{{SLIDES}}`, `{{CAPTION}}`, `{{TOTAL}}`, `{{HANDLE}}`, `{{BRAND}}`). Wird von `render.py` befüllt.
- `resources/render.py` — erzeugt standardmäßig NUR `preview.html` (Iterations-Modus, kein Chromium). Mit `--final` zusätzlich 10× PNG (1080×1350) + 1× PDF. **Regel: während der Iteration (Phase 5) immer ohne `--final`. PNGs + PDF erst nach dem "Go" in Phase 6 mit `--final`.**

## Kontext laden (Pflicht, vor Phase 1)

- `01-context/zielgruppe.md` — ICP-Profil: Spannungen, Sprache, Kernproblem. **Fehlt es:** Hard-Stop, erst ICP-Setup empfehlen (icp-Plugin), denn Hooks ohne ICP sind Raterei.
- `01-context/brand/voice.md` — Voice-Profile, falls vorhanden: auf alle Texte anwenden.
- `01-context/brand/ci.md` — Farben/Schriften für die Preview, falls vorhanden. Fehlt es: neutrales Design (dunkler Hintergrund, eine Akzentfarbe, serifenlose Schrift) und am Ende empfehlen, die CI zu hinterlegen.

## Workflow-Phasen

### Phase 1: Setup (Stop-Punkt)

Nacheinander klären, nicht alles auf einmal:
1. **Conversion-Ziel:** Was soll der Carousel verkaufen? (Lead-Magnet, Erstgespräch, Produkt — jeder Carousel verkauft etwas)
2. **CTA-Mechanik:** Comment-for-X (mit Auto-DM-Tool, falls vorhanden) ODER Direktlink ODER Profil-CTA
3. **Thema:** Worum geht's inhaltlich? Welches ICP-Problem wird diagnostiziert?
4. **Build-Subtyp:** Story, Liste oder Steps (genau einer)

Zusammenfassung zeigen, auf OK warten.

### Phase 2: Hook-Auswahl (Stop-Punkt)

5 Hook-Varianten generieren (Visual Hook + Rehook, verschiedene Hook-Typen aus der Formel-Referenz), gegen die Hook-Regeln und das ICP-Profil prüfen. User wählt.

### Phase 3: Vollständiger Build ins HTML (automatisch)

Hier wird **das vollständige HTML gebaut** — alle 10 Slides in einem Rutsch, kein Render.

1. **Output-Ordner anlegen:** `06-knowledge/content/carousels/[YYYY-MM-DD]-[slug]/` (Slug: kebab-case aus dem Thema, max 4 Wörter).
2. **Starter kopieren:** `resources/template.html` → `carousel.html` in den Output-Ordner.
3. **CI einsetzen:** in `carousel.html` die `:root`-Variablen (`--bg`, `--fg`, `--accent`, `--accent-fg`, `--font-display`, `--font-mono`) aus `01-context/brand/ci.md` ersetzen sowie `{{BRAND}}` und `{{HANDLE}}`. Fehlt `ci.md`: neutrale Defaults lassen, am Ende empfehlen die CI zu hinterlegen. **Nach Phase 3 darf kein `{{...}}`-Token mehr im File stehen.**
4. **Slides texten:** Slide 1-2 (Hook + Rehook aus Phase 2), Slides 3-7 (Build im gewählten Subtyp), Slide 8 (Payoff), Slide 9 (Bridge/Stakes/Proof), Slide 10 (CTA) nach `references/slide-anatomy.md`. Akzent-Wort pro Slide via `class="acc"`. Bild-Assets immer als `01-context/brand/[datei]` referenzieren (base64-Einbettung macht `render.py`).

Läuft ohne User-Interaktion bis zum Ende.

### Phase 4: Quality-Checks + Caption (automatisch)

- **Atomaritäts-Check:** Steht jede Slide alleine UND verkauft die nächste mit?
- **ICP-Check:** Trifft mindestens eine dokumentierte Spannung? Sprache aus dem Profil? (Bei Fail: einmal nachschärfen, bei zweitem Fail dem User die Schwachstelle zeigen)
- **Caption** schreiben (Instagram + LinkedIn-Variante), Voice-Profile anwenden falls vorhanden. Als `caption.md` in den Output-Ordner ablegen (wird von `render.py` oben in der Preview angezeigt).

### Phase 5: Preview-Render + Iteration (Stop-Punkt)

Vom Projekt-Root aus rendern, **ohne `--final`** — schreibt nur `preview.html` (kein Chromium, keine PNGs):

```bash
python3 <plugin>/skills/carousel/resources/render.py \
  06-knowledge/content/carousels/[YYYY-MM-DD]-[slug]/carousel.html \
  06-knowledge/content/carousels/[YYYY-MM-DD]-[slug]/ \
  --handle "[@handle aus ci.md]" --brand "[Marke aus ci.md]"
```

Die `preview.html` ist self-contained (Bilder als base64) und zeigt alle 10 Slides im IG-Mobile-Mockup mit der Caption. Link an den User. User iteriert pro Slide oder Caption: `carousel.html` (oder `caption.md`) anpassen → `render.py` **ohne `--final`** erneut → Tab reloaden. **Während der gesamten Iteration nie `--final`** — Voll-Render kostet ~30s Chromium und ist beim Iterieren Verschwendung.

### Phase 6: Final-Render (erst nach "Go")

Erst wenn der User explizit "go"/"passt" sagt, **einmalig** mit `--final`:

```bash
python3 <plugin>/skills/carousel/resources/render.py \
  06-knowledge/content/carousels/[YYYY-MM-DD]-[slug]/carousel.html \
  06-knowledge/content/carousels/[YYYY-MM-DD]-[slug]/ \
  --handle "[@handle]" --brand "[Marke]" --final
```

Erzeugt 10× PNG (1080×1350) + `full-carousel.pdf`. Danach liegt im Ordner:

```
06-knowledge/content/carousels/[YYYY-MM-DD]-[slug]/
├── carousel.html                    ← Render-Input (gefülltes Template)
├── caption.md                       ← IG + LinkedIn Caption
├── preview.html                     ← klickbare Browser-Vorschau
├── slide-01.png … slide-10.png      ← Instagram (Slides hochladen)
└── full-carousel.pdf                ← optional LinkedIn-Document-Post
```

**Pre-Flight vor Ausgabe:** Ratio 4:5 (1080×1350, nie 3:4 → IG-Auto-Crop), keine Emojis im Slide-Text (Renderer hat keine Emoji-Font), gerenderte PNGs mit Custom-Visualisierungen kurz selbst anschauen, alte PNGs aus einer früheren Slide-Zahl löschen.

**Index-Pflege:** Neuen Ordner in der `## Aktuell vorhanden`-Sektion von `06-knowledge/_index.md` verlinken.

## Render-Stack (Setup für Phase 6)

`render.py --final` nutzt **Playwright** (Chromium headless) + **Pillow**. Einmalige Installation:

```bash
pip install playwright pillow --break-system-packages
python3 -m playwright install chromium
```

Der Preview-Modus (Phase 5, ohne `--final`) braucht das NICHT — `preview.html` wird ohne Chromium geschrieben.

## Abgrenzung

- Kein automatisches Posten — Export ist PNG + PDF + Caption, das Posten passiert manuell
- Keine Reels/Videos
- Comment-for-X-Mechanik braucht ein Auto-DM-Tool (z.B. Manychat) — ohne das den Direktlink-CTA wählen

## Hard-Stops

- Kein ICP-Profil vorhanden (erst icp-Setup)
- User hat in Phase 1 oder 2 nicht bestätigt
- ICP-Check zweimal hintereinander fail → Schwachstelle offenlegen statt drüberbügeln
- Playwright nicht installiert → kein `--final`-Render, Setup-Hinweis geben (Preview-Modus geht trotzdem)
- User sagt nicht explizit "go"/"passt" → kein Final-Render
