---
name: carousel
version: 2.0.0
description: >
  Baut Carousel-Posts (10 Slides, 1080x1350, Instagram/LinkedIn) nach der
  4-Bausteine-Formel: Hook -> Build -> Payoff -> CTA. Geführter Workflow:
  Setup (Ziel/CTA/Thema, eine Frage nach der anderen) -> Story-Context aus
  Coaching-Calls holen -> 5 Hook-Varianten zur Auswahl -> vollständiger Build
  aller 10 Slides ins HTML -> Quality-Checks gegen das ICP -> Preview-Render
  (render.py) -> erst nach "Go" Final-Render zu PNG + PDF.
  Triggern bei: "bau mir einen Carousel", "Carousel-Post zu", "Carousel-Idee",
  "Slides für Instagram", "Karussell-Post", "Carousel erstellen".
---

# Carousel-Builder

Baut einen 10-Slide-Carousel von der Idee bis zu fertigen PNGs + PDF + Caption.
Methodik: 4-Bausteine-Formel + Slide-Anatomie.

**Kanonische Quellen (Pflicht lesen vor Phase 1):**
- [`03-marketing/specs/carousel-design-system-v1.md`](03-marketing/specs/carousel-design-system-v1.md) — Brand-Spec (Farben, Typo, Layout)
- [`03-marketing/specs/carousel-slide-anatomy-v1.md`](03-marketing/specs/carousel-slide-anatomy-v1.md) — 4-Bausteine auf 10 Slides, Hook-Typen, Atomaritäts-Regeln
- [`09-ip/4-bausteine-formel.md`](09-ip/4-bausteine-formel.md) — Hook -> Build -> Payoff -> CTA (kanonisch)

**Resources (im Skill-Ordner):**
- `resources/template.html` — 10-Slide-Starter mit Marcus' Design-System fest verbaut (Coral-Akzent, Open Sans ExtraBold, Light + Cinema Edition). Wird als `carousel.html` in den Output-Ordner kopiert. Das ist der Render-Input.
- `resources/preview-template.html` — IG-Mobile-Mockup mit Platzhaltern (`{{CAROUSEL_STYLES}}`, `{{SLIDES}}`, `{{CAPTION}}`, `{{TOTAL}}`, `{{HANDLE}}`, `{{BRAND}}`). Wird von `render.py` befüllt.
- `resources/render.py` — erzeugt standardmäßig NUR `preview.html` (Iterations-Modus, kein Chromium). Mit `--final` zusätzlich 10x PNG (1080x1350) + 1x PDF. **Regel: während der Iteration (Phase 5) immer ohne `--final`. PNGs + PDF erst nach dem "Go" in Phase 6 mit `--final`.**

**Bilder-Pflicht (base64):**
Alle Brand-Asset-Bilder im Slide-HTML MÜSSEN als base64-Data-URI eingebettet werden, damit die `preview.html` self-contained ist. `render.py` macht das automatisch für alle Pfade, die auf `01-context/positionierung/brand-assets/` zeigen. Korrekte Referenz im Template: `../../../../01-context/positionierung/brand-assets/{file}`.

---

## Kontext laden (Pflicht, vor Phase 1)

- `01-context/angebot/agency-os-icp.md` — ICP-Profil: Spannungen, Sprache, Kernproblem. **Fehlt es:** Hard-Stop, erst ICP-Setup machen.
- `01-context/brand/voice-profile.md` — Voice-Profile (Markus' Stimme). Auf alle Texte anwenden.
- Design-System: in `resources/template.html` fest verbaut (Coral `#E85F33`, Cream `#F2EBDD`, Black `#0F0F0E`, Open Sans ExtraBold, JetBrains Mono). Kein externes CI-File nötig.

---

## Workflow-Phasen

### Phase 1: Setup (Stop-Punkt)

Nacheinander klären, nicht alles auf einmal:
1. **Conversion-Ziel:** Was soll der Carousel verkaufen? (Lead-Magnet, Erstgespräch, Produkt — jeder Carousel verkauft etwas)
2. **CTA-Mechanik:** Comment-for-X (Wort wählen: 4-7 Buchstaben, All-Caps, JTBD-spezifisch) ODER Direktlink ODER Profil-CTA
3. **Thema:** Worum geht's inhaltlich? Welches ICP-Problem wird diagnostiziert?
4. **Build-Subtyp:** Story, Liste oder Steps (genau einer)
5. **Edition:** Light (Cream-Hintergrund, 70% des Feeds) ODER Cinema (Black-Hintergrund, 30%)

Zusammenfassung zeigen, auf OK warten.

**Danach automatisch (kein Stop):** `/story-context` aufrufen mit dem Thema als Query.
Stories, ICP-O-Töne und Erkenntnisse aus dem Coaching-Call-Brain holen (Top-5-10 Results).
Auswahl der relevantesten Snippets für Phase 3 notieren.

### Phase 2: Hook-Auswahl (Stop-Punkt)

5 Hook-Varianten generieren (Visual Hook + Rehook, verschiedene Hook-Typen aus der Slide-Anatomy-Spec).
Prüfen gegen Hook-Regeln: max 12 Wörter Slide 1, mind. eine ICP-Spannung aktiv, ein Coral-Akzent.
User wählt eine Variante.

### Phase 3: Vollständiger Build ins HTML (automatisch)

Hier wird **das vollständige HTML gebaut** — alle 10 Slides in einem Rutsch, kein Render.

1. **Output-Ordner anlegen:** `03-marketing/content/carousels/[YYYY-MM-DD]-[slug]/` (Slug: kebab-case aus dem Thema, max 4 Wörter).
2. **Starter kopieren:** `resources/template.html` -> `carousel.html` in den Output-Ordner.
3. **Edition einsetzen:** Light vs Cinema laut Phase-1-Wahl (CSS-Swap in `carousel.html`).
4. **Brand-Konstanten eintragen:** `LEAN AGENCY` und `@markusvieghofer_com` sind im Template bereits gesetzt — nur prüfen, dass keine `{{...}}`-Tokens übrig bleiben.
5. **Slides texten:** Slide 1-2 (Hook + Rehook aus Phase 2), Slides 3-7 (Build im gewählten Subtyp, Story-Context-Material einweben), Slide 8 (Payoff), Slide 9 (Bridge/Stakes/Proof), Slide 10 (CTA + Foto aus `01-context/positionierung/brand-assets/`) nach Slide-Anatomy-Spec.
   - Genau **ein** Coral-Akzent (`class="acc"`) pro Slide.
   - Bild-Assets immer als `../../../../01-context/positionierung/brand-assets/{datei}` referenzieren.
   - Foto-Auswahl Slide 10: Sales-Carousel -> `1.png`, Story -> `2.png`, Reflexion -> `3.png`, sonst `2.png`.

**Vollständigkeits-Assertion (Pflicht nach Schritt 5):**
```
grep -o '{{[^}]*}}' carousel.html
```
Darf **keine** Treffer zurückliefern. Jeder noch offene `{{...}}`-Token ist ein Build-Fehler — vor dem Weitermachen beheben.

Läuft ohne User-Interaktion bis zum Ende.

### Phase 4: Quality-Checks + Caption (automatisch)

- **Atomaritäts-Check (7 Punkte aus Slide-Anatomy):** Jede Slide standalone lesbar? Genau ein Coral-Akzent? Wortzahl im Range (Slide 1: 6-10, Slides 3-9: 25-40, Slide 10: 10-20)?
- **ICP-Check:** Trifft mindestens eine ICP-Spannung? Sprache aus dem Profil? (Bei Fail: einmal nachschärfen. Bei zweitem Fail dem User die Schwachstelle zeigen.)
- **Caption** schreiben (Instagram + LinkedIn-Variante). Voice-Profile anwenden. Als `caption.md` in den Output-Ordner ablegen.

### Phase 5: Preview-Render + Iteration (Stop-Punkt)

Vom Projekt-Root aus rendern, **ohne `--final`** — schreibt nur `preview.html` (kein Chromium, keine PNGs):

```bash
python3 skills/carousel/resources/render.py \
  03-marketing/content/carousels/[YYYY-MM-DD]-[slug]/carousel.html \
  03-marketing/content/carousels/[YYYY-MM-DD]-[slug]/ \
  --handle "@markusvieghofer_com" --brand "LEAN AGENCY"
```

Die `preview.html` ist self-contained (Bilder als base64) und zeigt alle 10 Slides im IG-Mobile-Mockup mit der Caption. Link an den User. User iteriert pro Slide oder Caption: `carousel.html` (oder `caption.md`) anpassen -> `render.py` **ohne `--final`** erneut -> Tab reloaden. **Während der gesamten Iteration nie `--final`** — Voll-Render kostet ~30s Chromium.

### Phase 6: Final-Render (erst nach "Go")

Erst wenn der User explizit "go"/"passt" sagt, **einmalig** mit `--final`:

```bash
python3 skills/carousel/resources/render.py \
  03-marketing/content/carousels/[YYYY-MM-DD]-[slug]/carousel.html \
  03-marketing/content/carousels/[YYYY-MM-DD]-[slug]/ \
  --handle "@markusvieghofer_com" --brand "LEAN AGENCY" --final
```

Erzeugt 10x PNG (1080x1350) + `full-carousel.pdf`. Danach liegt im Ordner:

```
03-marketing/content/carousels/[YYYY-MM-DD]-[slug]/
├── carousel.html                    <- Render-Input (gefülltes Template)
├── caption.md                       <- IG + LinkedIn Caption
├── preview.html                     <- klickbare Browser-Vorschau
├── slide-01.png ... slide-10.png    <- Instagram (Slides hochladen)
└── full-carousel.pdf                <- optional LinkedIn-Document-Post
```

**Pre-Flight vor Ausgabe:** Ratio 4:5 (1080x1350, nie 3:4 -> IG-Auto-Crop), keine Emojis im Slide-Text (Renderer hat keine Emoji-Font), alte PNGs aus einer früheren Slide-Zahl löschen.

**Log-Eintrag:** Neuen Carousel in `10-logs/[YYYY-MM-DD].md` unter einer `## Carousel`-Sektion kurz eintragen (Slug + Thema + CTA-Wort).

---

## Render-Stack (Setup für Phase 6)

`render.py --final` nutzt **Playwright** (Chromium headless) + **Pillow**. Einmalige Installation:

```bash
pip install playwright pillow --break-system-packages
python3 -m playwright install chromium
```

Der Preview-Modus (Phase 5, ohne `--final`) braucht das NICHT — `preview.html` wird ohne Chromium geschrieben.

---

## Erlaubte Skills im Workflow

- `/brand-voice` — Markus' Stimme auf alle Texte anwenden
- `/icp` Modus *Bewerten* — Hook/CTA-Check gegen ICP
- `/story-context` — Stories + ICP-O-Töne aus Coaching-Calls (Phase 1, nach Setup-OK)

KEINE anderen spezifischen Skills (z.B. `/linkedin-content`).

---

## Abgrenzung

- Kein automatisches Posten — Export ist PNG + PDF + Caption, das Posten passiert manuell
- Keine Reels/Videos (das ist `/reel-ideation`)
- Comment-for-X-Mechanik braucht ein Auto-DM-Tool (z.B. Manychat) — ohne das den Direktlink-CTA wählen

## Hard-Stops

- Kein ICP-Profil (`01-context/angebot/agency-os-icp.md`) vorhanden -> erst ICP-Setup
- User hat in Phase 1 oder 2 nicht bestätigt
- Vollständigkeits-Assertion schlägt an (noch `{{...}}`-Tokens nach Phase 3)
- ICP-Check zweimal hintereinander fail -> Schwachstelle offenlegen statt drüberbügeln
- Playwright nicht installiert -> kein `--final`-Render, Setup-Hinweis geben (Preview-Modus geht trotzdem)
- User sagt nicht explizit "go"/"passt" -> kein Final-Render
