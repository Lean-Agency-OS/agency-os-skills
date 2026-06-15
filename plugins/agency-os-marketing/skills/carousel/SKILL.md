---
name: carousel
version: 2.1.0
description: >
  Baut Carousel-Posts (flexible Slide-Zahl, 1080x1350, Instagram/LinkedIn) nach der 4-Bausteine-Formel
  (Hook -> Build -> Payoff -> CTA): Preflight (CI + Template) -> geführtes Setup -> Hook-Auswahl ->
  Build aller Slides ins HTML -> Quality-/ICP-Check -> Preview-Render -> nach "Go" Final-Render zu
  PNG + PDF + Caption. Layout-Templates und Brand-CI liegen im Brain (mehrere Templates möglich),
  Pfade über .agency-os/architecture.md. Triggern bei: "bau mir einen Carousel", "Carousel-Post zu",
  "Carousel-Idee", "Slides für Instagram", "Karussell-Post", "Carousel erstellen".
---

# Carousel-Builder

Baut einen Carousel (flexible Slide-Zahl) von der Idee bis zu fertigen PNGs + PDF + Caption.

## Methodik

[`references/4-bausteine-formel.md`](references/4-bausteine-formel.md) + [`references/slide-anatomy.md`](references/slide-anatomy.md) (beide vor dem Bauen lesen).

## Pfade & Fundament

Keine hartkodierten Pfade. Ordner werden über ihre **Rolle** aus `.agency-os/architecture.md` aufgelöst
(`agency-os-start` pflegt die Datei), sonst per Muster gesucht. `{context}`/`{marketing}`/`{logs}` unten sind
diese aufgelösten Pfade.

- **Brand:** aktive Brand unter `{context}/brands/`. Nur eine → die; mehrere → die mit `brand-config.md` `status: active`. Kein fester Default-Name.
- **Brand-CI:** `{context}/brands/{brand}/ci.md` (Frontmatter: `colors`, `fonts`, `handle`, `name`, `assets_dir`, `logo`). Angelegt/gepflegt von `/brand-ci` (dort liegt das Schema + Beispiel). Gleiche `ci.md` nutzt auch `/video-studio`. Die CI fließt beim **Template-Generieren** ins Layout (s.u.); beim Bauen liefert sie `assets_dir`/`handle`/`name` für den Render.
- **ICP:** `{context}/brands/{brand}/icp.md` (Fallback projektweites ICP). Auf alle Texte anwenden.
- **Voice:** `{context}/brands/{brand}/voice-profile.md` (Fallback projektweit). Auf alle Texte anwenden.

### Templates (Layout, im Brain)

Layouts liegen unter `{marketing}/content/carousels/00-templates/*.html` - **mehrere möglich** (verschiedene Layouts,
sprechende Dateinamen). Jedes Template hat die Brand-CI bereits im `:root` eingebacken. Es gibt **kein**
Render-Default aus dem Plugin; der Seed wird nur einmal benutzt, um das erste Template zu generieren.

### Resources (Plugin)

- `resources/templates/standard.html` — **ein** Seed-Layout. Nur zur Erst-Generierung eines Brain-Templates.
- `resources/preview-template.html` — IG-Mobile-Mockup, von `render.py` befüllt.
- `resources/render.py` — schreibt standardmäßig nur `preview.html` (kein Chromium); mit `--final` zusätzlich pro Slide ein PNG (1080x1350) + PDF. Args `--handle`/`--brand`/`--assets-dir` aus der CI. Bettet Brand-Assets aus `--assets-dir` als base64 ein - in die Preview **und** beim Final-Render, sodass im HTML keine relativen Rück-Pfade nötig sind (Windows-safe).

---

## Workflow

### Preflight (Pflicht, vor Phase 1)

1. **Pfade + Brand** auflösen (s.o.).
2. **CI prüfen:** Existiert `{context}/brands/{brand}/ci.md`? Wenn **nein** → Warnung *"Keine Brand-CI gefunden - ohne CI wird das Ergebnis generisch. Empfehlung: mit `/brand-ci` eine `ci.md` anlegen."*
3. **Template prüfen:** Liegt mind. ein `*.html` in `{marketing}/content/carousels/00-templates/`?
   - **Keins/Ordner fehlt:** ein Template aus dem Seed `resources/templates/standard.html` **generieren** - Seed kopieren, `colors`/`fonts` aus der CI in den `:root` und `name`/`handle` in die Slides einbacken, unter sprechendem Namen in `{marketing}/content/carousels/00-templates/` ablegen, User informieren (wo es liegt, frei anpassbar). Ohne CI: generisch mit Platzhaltern.
   - **Genau eins:** das nehmen. **Mehrere:** in Phase 1 zur Auswahl stellen.
4. **Fehlt CI oder Template und die Warnung wird ignoriert** (User will trotzdem weiter): best-effort generisch bauen.

### Phase 1: Setup (Stop-Punkt)

Eine Frage nach der anderen, nicht alles auf einmal:
1. **Conversion-Ziel:** Was verkauft der Carousel? (Lead-Magnet, Erstgespräch, Produkt - jeder verkauft etwas)
2. **CTA-Mechanik:** Comment-for-X (Wort: 4-7 Buchstaben, All-Caps, JTBD-spezifisch) ODER Direktlink ODER Profil-CTA
3. **Thema:** Welches ICP-Problem wird diagnostiziert?
4. **Build-Subtyp:** Story, Liste oder Steps (genau einer)
5. **Template:** falls mehrere in `{marketing}/content/carousels/00-templates/`, hier auswählen
6. **Edition:** Light ODER Cinema (falls das gewählte Template beide Varianten hat)

Zusammenfassung zeigen, auf OK warten. **Danach automatisch:** falls vorhanden `/story-context` mit dem Thema
als Query aufrufen, relevante Stories/O-Töne für Phase 3 notieren. Keine Story-Quelle → echtes Material beim
User erfragen, nichts erfinden.

### Phase 2: Hook-Auswahl (Stop-Punkt)

5 Hook-Varianten generieren (Visual Hook + Rehook, Hook-Typen aus der Slide-Anatomy). Regeln: max 12 Wörter
Slide 1, mind. eine ICP-Spannung, ein Akzent. User wählt eine.

### Phase 3: Build ins HTML (automatisch)

1. **Output-Ordner:** `{marketing}/content/carousels/[YYYY-MM-DD]-[slug]/` (Slug: kebab-case aus dem Thema, max 4 Wörter).
2. **Template kopieren:** das gewählte `{marketing}/content/carousels/00-templates/{name}.html` -> `carousel.html` im Output-Ordner. Die CI ist im Template schon drin - **kein** CI-Einsetzen mehr.
3. **Slides texten** (nach Slide-Anatomy, flexible Länge): **Slide 1-2** Hook + Rehook → **Build** (variabel viele Slides, gewählter Subtyp durchgängig, Story-Material einweben - so lang wie das Thema trägt, darf kurz sein) → **Payoff** (1-2 Slides, optional eine Bridge/Stakes/Proof-Slide davor) → **letzte Slide** CTA + Foto. Genau **ein** Akzent (`class="acc"`) pro Slide. Bild-Assets project-root-relativ als `{assets_dir}/{datei}` referenzieren (kein `../`; `render.py` bettet sie base64 ein). Nicht benötigte Slides aus dem Template-Starter entfernen und den Seiten-Index (`X / N`) an die finale Slide-Zahl anpassen.
4. **Assertion:** `grep -o '{{[^}]*}}' carousel.html` muss leer sein - offene `{{...}}`-Tokens sind ein Build-Fehler, vor dem Weitermachen beheben.

### Phase 4: Quality + Caption (automatisch)

- **Atomarität (Slide-Anatomy):** Jede Slide standalone lesbar? Ein Akzent? Wortzahl im Range je Rolle (Hook-Slide 1: 6-10, Rehook/Build/Payoff: 15-40, CTA: 10-20)?
- **ICP-Check:** mind. eine ICP-Spannung, Sprache aus dem Profil. Fail → einmal nachschärfen, beim zweiten Fail Schwachstelle offenlegen.
- **Caption** (Instagram + LinkedIn) mit Voice-Profile schreiben, als `caption.md` in den Output-Ordner.

### Phase 5: Preview + Iteration (Stop-Punkt)

Vom Projekt-Root rendern, **ohne `--final`** (nur `preview.html`, kein Chromium):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/carousel/resources/render.py \
  {marketing}/content/carousels/[YYYY-MM-DD]-[slug]/carousel.html \
  {marketing}/content/carousels/[YYYY-MM-DD]-[slug]/ \
  --handle "{handle}" --brand "{name}" --assets-dir "{assets_dir}"
```

`preview.html` (self-contained) an den User. User iteriert in `carousel.html`/`caption.md` -> erneut **ohne `--final`** rendern -> Tab reloaden. Während der Iteration nie `--final`.

### Phase 6: Final-Render (erst nach "Go")

Erst auf explizites "go"/"passt", **einmal** mit `--final` (gleicher Befehl + `--final`). Erzeugt ein PNG pro Slide + `full-carousel.pdf`:

```
{marketing}/content/carousels/[YYYY-MM-DD]-[slug]/
├── carousel.html      <- Render-Input        ├── preview.html    <- Browser-Vorschau
├── caption.md         <- IG + LinkedIn        ├── slide-01..NN.png <- Instagram
└── full-carousel.pdf  <- optional LinkedIn-Document-Post
```

- **Pre-Flight:** Ratio 4:5 (1080x1350, nie 3:4), keine Emojis im Slide-Text (Renderer hat keine Emoji-Font), alte PNGs einer früheren Slide-Zahl löschen.
- **Log:** kurzer Eintrag im Tages-Log `{logs}/[YYYY-MM-DD].md` unter `## Carousel` (Slug + Thema + CTA-Wort).

---

## Render-Stack (einmalig, für `--final`)

```bash
pip install playwright pillow --break-system-packages
python3 -m playwright install chromium
```

Der Preview-Modus (ohne `--final`) braucht das nicht.

---

## Output

Output-Ordner `{marketing}/content/carousels/[YYYY-MM-DD]-[slug]/` mit:

```
{marketing}/content/carousels/[YYYY-MM-DD]-[slug]/
├── carousel.html      <- Render-Input        ├── preview.html    <- Browser-Vorschau
├── caption.md         <- IG + LinkedIn        ├── slide-01..NN.png <- Instagram
└── full-carousel.pdf  <- optional LinkedIn-Document-Post
```

Kein automatisches Posten. Kurzer Eintrag im Tages-Log `{logs}/[YYYY-MM-DD].md` unter `## Carousel`.

## Verwandte Skills

**Erlaubte Skills:**

- `/brand-voice` — Stimme der Brand auf alle Texte
- `/icp` Modus *Bewerten* — Hook/CTA gegen ICP
- `/story-context` (falls vorhanden) — echte Stories + O-Töne (Phase 1)

**Abgrenzung:**

- Kein automatisches Posten - Export ist PNG + PDF + Caption.
- Keine Reels/Videos (`/reel-skript` bzw. `/video-studio`), keine Caption-only-Posts (`/instagram-caption`, `/linkedin-caption`).
- Comment-for-X braucht ein Auto-DM-Tool - ohne das den Direktlink-CTA wählen.

## Hard-Stops

- Mehr als **20 Slides** -> kürzen (hartes Instagram-Carousel-Limit). Sinnvolle Spanne: 5-20.
- User hat in Phase 1 oder 2 nicht bestätigt.
- Assertion schlägt an (offene `{{...}}`-Tokens).
- ICP-Check zweimal fail -> Schwachstelle offenlegen statt drüberbügeln.
- Playwright fehlt -> kein `--final` (Preview geht trotzdem).
- Kein explizites "go"/"passt" -> kein Final-Render.
