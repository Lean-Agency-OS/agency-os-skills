---
name: carousel
version: 4.0.0
description: >
  Baut Carousel-Posts (flexible Slide-Zahl, 1080x1350, Instagram/LinkedIn) nach der 4-Bausteine-Formel
  (Hook -> Build -> Payoff -> CTA): Preflight (CI + Template) -> geführtes Setup -> Hook-Auswahl ->
  Slide-Texte zuerst NUR im Chat (Quality-/ICP-Check immer, Iteration bis "passt") -> dann
  Output-Weiche: HTML-Render (Preview, nach "Go" Final-Render zu PNG + PDF) ODER Push in ein
  verbundenes Design-Tool (z.B. Canva-Connector; tool-agnostisch, Connectoren werden zur Laufzeit
  gecheckt). Layout-Templates und Brand-CI liegen im Brain (mehrere Templates möglich),
  Pfade über .agency-os/architecture.md. Triggern bei: "bau mir einen Carousel", "Carousel-Post zu",
  "Carousel-Idee", "Slides für Instagram", "Karussell-Post", "Carousel erstellen".
---

# Carousel-Builder

Du baust als **Senior Content-Designer**: du denkst in Daumenstopp und Slide-Flow, nicht in hübschen Kacheln. Jeder Slide verdient den nächsten, oder er fliegt raus. **Dein Ziel:** Content, der gespeichert und geteilt wird und neue passende Follower in den Funnel zieht.

Baut einen Carousel (flexible Slide-Zahl) von der Idee bis zum fertigen Asset. **Text vor Design:**
die Slide-Texte entstehen und iterieren zuerst nur im Chat. Erst wenn sie stehen, entscheidet der
User den Output-Weg:

- **Weg A - HTML-Render:** Build ins Brain-Template, Preview, nach "Go" PNG + PDF (wie gehabt).
- **Weg B - Design-Tool-Push:** die fertigen Texte strukturiert an ein verbundenes Design-Tool
  übergeben (z.B. Canva-Connector). Der Skill enthält nichts Tool-Spezifisches: er prüft zur
  Laufzeit, welche Design-Connectoren verfügbar sind, und nutzt deren Möglichkeiten.

## Methodik

[`references/4-bausteine-formel.md`](references/4-bausteine-formel.md) + [`references/slide-anatomy.md`](references/slide-anatomy.md) (beide vor dem Bauen lesen).

## Pfade & Fundament

Keine hartkodierten Pfade. Ordner werden über ihre **Rolle** aus `.agency-os/architecture.md` aufgelöst
(`agency-os-start` pflegt die Datei), sonst per Muster gesucht. `{context}`/`{marketing}`/`{logs}` unten sind
diese aufgelösten Pfade.

- **Brand-CI:** `{context}/brand/ci.md` (Frontmatter: `colors`, `fonts`, `handle`, `name`, `assets_dir`, `logo`). Angelegt/gepflegt von `/brand-ci` (dort liegt das Schema + Beispiel). Gleiche `ci.md` nutzt auch `/video-shortform`. Die CI fließt beim **Template-Generieren** ins Layout (s.u.); beim Bauen liefert sie `assets_dir`/`handle`/`name` für den Render.
- **ICP:** `{context}/zielgruppe.md`. Auf alle Texte anwenden.
- **Voice:** `{context}/brand/voice-profile.md`. Auf alle Texte anwenden.
- **Brand-Config (optional):** `{context}/brand/brand-config.md`, falls vorhanden. Liefert Carousel-Inputs wie `hashtags_base`, `cta_mode`/`cta_default_url`, `ig_handle`/`li_handle`, `slide_format`, `default_slide_count`. Vorhandene Werte nicht im Setup abfragen, sondern übernehmen; fehlt die Datei, alles im Setup klären.

### Templates (Layout, im Brain)

Layouts liegen unter `{marketing}/content/carousels/00-templates/*.html` - **mehrere möglich** (verschiedene Layouts,
sprechende Dateinamen). Jedes Template hat die Brand-CI bereits im `:root` eingebacken. Es gibt **kein**
Render-Default aus dem Plugin; der Seed wird nur einmal benutzt, um das erste Template zu generieren.

### Resources (Plugin)

- `resources/templates/standard.html`: **ein** Seed-Layout. Nur zur Erst-Generierung eines Brain-Templates.
- `resources/preview-template.html`: IG-Mobile-Mockup, von `render.py` befüllt.
- `resources/render.py`: schreibt standardmäßig nur `preview.html` (kein Chromium); mit `--final` zusätzlich pro Slide ein PNG (1080x1350) + PDF. Args `--handle`/`--brand`/`--assets-dir` aus der CI. Bettet Brand-Assets aus `--assets-dir` als base64 ein - in die Preview **und** beim Final-Render, sodass im HTML keine relativen Rück-Pfade nötig sind (Windows-safe).

---

## Workflow

### Preflight (Pflicht, vor Phase 1)

1. **Pfade** auflösen (s.o.).
2. **CI prüfen:** Existiert `{context}/brand/ci.md`? Wenn **nein** → Warnung *"Keine Brand-CI gefunden - ohne CI wird das Ergebnis generisch. Empfehlung: mit `/brand-ci` eine `ci.md` anlegen."* Warnung ignoriert → best-effort generisch weiter.

### Phase 1: Setup (Stop-Punkt)

Eine Frage nach der anderen, nicht alles auf einmal:
1. **Conversion-Ziel:** Was verkauft der Carousel? (Lead-Magnet, Erstgespräch, Produkt - jeder verkauft etwas)
2. **CTA-Mechanik:** Comment-for-X (Wort: 4-7 Buchstaben, All-Caps, JTBD-spezifisch) ODER Direktlink ODER Profil-CTA
3. **Thema:** Welches ICP-Problem wird diagnostiziert?
4. **Build-Subtyp:** Story, Liste oder Steps (genau einer)

Template- und Edition-Fragen kommen **nicht** hierher, die gehören zu Weg A (Phase 7A).

Zusammenfassung zeigen, auf OK warten. **Danach:** bei Build-Subtyp Story echtes Material für Phase 3 beim
User erfragen, nichts erfinden.

### Phase 2: Hook-Auswahl (Stop-Punkt)

5 Hook-Varianten generieren (Visual Hook + Rehook, Hook-Typen aus der Slide-Anatomy). Regeln: max 12 Wörter
Slide 1, mind. eine ICP-Spannung, ein Akzent. User wählt eine.

### Phase 3: Slide-Texte schreiben (automatisch, NUR Text, kein HTML)

**In dieser Phase entsteht kein HTML und keine Vorschau.** Slides texten nach Slide-Anatomy,
Voice-Profile anwenden, flexible Länge: **Slide 1-2** Hook + Rehook → **Build** (variabel viele
Slides, gewählter Subtyp durchgängig, Story-Material einweben - so lang wie das Thema trägt, darf
kurz sein) → **Payoff** (1-2 Slides, optional eine Bridge/Stakes/Proof-Slide davor) → **letzte
Slide** CTA. Genau **ein** Akzent-Wort pro Slide (im Chat **fett** markieren).

### Phase 4: Quality + ICP (automatisch, läuft immer)

- **Atomarität (Slide-Anatomy):** Jede Slide standalone lesbar? Ein Akzent? Wortzahl im Range je Rolle (Hook-Slide 1: 6-10, Rehook/Build/Payoff: 15-40, CTA: 10-20)?
- **ICP-Check:** mind. eine ICP-Spannung, Sprache aus dem Profil. Fail → einmal nachschärfen, beim zweiten Fail Schwachstelle offenlegen.

Es wird nie ein ungecheckter Text ausgegeben. **Keine Post-Caption:** der Skill liefert nur die Slides.

### Phase 5: Text-Approval im Chat (Stop-Punkt)

Alle Slide-Texte nummeriert im Chat ausgeben (Rolle + Text + Akzent je Slide).
Abschlussfrage: *"Welche Slide passt noch nicht? Oder 'passt' für den nächsten Schritt."*

**Iterations-Loop:** Feedback pro Slide, nur die genannte Slide neu texten, Rest unverändert.
Erst bei **"passt"** → Phase 6.

### Phase 6: Speichern + Output-Weiche (Stop-Punkt)

1. **Output-Ordner anlegen:** `{marketing}/content/carousels/[YYYY-MM-DD]-[slug]/` (Slug: kebab-case aus dem Thema, max 4 Wörter).
2. **Texte speichern** (beide Wege): `slides.md` (Slide-Texte je Rolle + Akzent + gewählter Hook) in den Output-Ordner.
3. **Design-Connectoren checken:** Welche Design-Tool-Connectoren sind in der Umgebung verfügbar (z.B. Canva, Figma als MCP-Tools)? Nichts hartkodieren, tatsächlich vorhandene Tools zählen.
4. **Weiche als Frage an den User:**
   - **Weg A - HTML rendern:** Preview + PNG/PDF über den eingebauten Renderer.
   - **Weg B - Push zu {gefundene Tools}:** nur anbieten, wenn mind. ein Design-Connector verbunden ist. Keiner verbunden → kurz sagen, dass z.B. der Canva-Connector diesen Weg freischalten würde, und Weg A anbieten.

### Weg A, Phase 7A: Build ins HTML + Preview (Stop-Punkt)

1. **Template prüfen:** Liegt mind. ein `*.html` in `{marketing}/content/carousels/00-templates/`?
   - **Keins/Ordner fehlt:** ein Template aus dem Seed `resources/templates/standard.html` **generieren** - Seed kopieren, `colors`/`fonts` aus der CI in den `:root` und `name`/`handle` in die Slides einbacken, unter sprechendem Namen in `{marketing}/content/carousels/00-templates/` ablegen, User informieren (wo es liegt, frei anpassbar). Ohne CI: generisch mit Platzhaltern.
   - **Genau eins:** das nehmen. **Mehrere:** kurz auswählen lassen. **Edition** (Light/Cinema) klären, falls das Template beide hat.
2. **Template kopieren:** das gewählte Template -> `carousel.html` im Output-Ordner. Die CI ist im Template schon drin - **kein** CI-Einsetzen mehr.
3. **Approvte Texte aus Phase 5 einsetzen**, nichts neu texten. Genau **ein** Akzent (`class="acc"`) pro Slide. Bild-Assets project-root-relativ als `{assets_dir}/{datei}` referenzieren (kein `../`; `render.py` bettet sie base64 ein). Nicht benötigte Slides aus dem Template-Starter entfernen und den Seiten-Index (`X / N`) an die finale Slide-Zahl anpassen.
4. **Assertion:** `grep -o '{{[^}]*}}' carousel.html` muss leer sein - offene `{{...}}`-Tokens sind ein Build-Fehler, vor dem Weitermachen beheben.
5. **Preview rendern** vom Projekt-Root, **ohne `--final`** (nur `preview.html`, kein Chromium):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/carousel/resources/render.py \
  {marketing}/content/carousels/[YYYY-MM-DD]-[slug]/carousel.html \
  {marketing}/content/carousels/[YYYY-MM-DD]-[slug]/ \
  --handle "{handle}" --brand "{name}" --assets-dir "{assets_dir}"
```

`preview.html` (self-contained) an den User. Iteration hier betrifft nur noch **Layout/Optik**
(Text steht seit Phase 5; Textänderungen zurück in `slides.md` spiegeln) -> erneut **ohne
`--final`** rendern -> Tab reloaden. Während der Iteration nie `--final`.

### Weg A, Phase 8A: Final-Render (erst nach "Go")

Erst auf explizites "go"/"passt", **einmal** mit `--final` (gleicher Befehl + `--final`). Erzeugt ein PNG pro Slide + `full-carousel.pdf`:

```
{marketing}/content/carousels/[YYYY-MM-DD]-[slug]/
├── slides.md          <- approvte Slide-Texte  ├── preview.html    <- Browser-Vorschau
├── carousel.html      <- Render-Input          ├── slide-01..NN.png <- Instagram
└── full-carousel.pdf  <- optional LinkedIn-Document-Post
```

- **Pre-Flight:** Ratio 4:5 (1080x1350, nie 3:4), keine Emojis im Slide-Text (Renderer hat keine Emoji-Font), alte PNGs einer früheren Slide-Zahl löschen.
- **Log:** kurzer Eintrag im Tages-Log `{logs}/[YYYY-MM-DD].md` unter `## Carousel` (Slug + Thema + CTA-Wort + Output-Weg).

### Weg B, Phase 7B: Design-Tool-Push (nur bei verbundenem Connector)

Tool-agnostisch: der Skill kennt keine Tool-Details, er nutzt die Fähigkeiten des verbundenen
Connectors. Vorgehen:

1. **Struktur übergeben:** die approvten Slide-Texte aus `slides.md` strukturiert an den Connector
   geben (pro Slide: Rolle, Text, Akzent-Wort; dazu Slide-Zahl, Format 1080x1350, Handle/Brand aus
   der CI, falls vorhanden).
2. **Bestmöglichen Mechanismus des Tools nutzen.** Beispiel Canva-Connector: existiert ein
   Brand-Template mit benannten Textfeldern, Design daraus erstellen und Felder befüllen;
   sonst ein Design aus der strukturierten Vorgabe generieren lassen. Bei anderen Tools analog
   das nehmen, was deren Tools hergeben. Nichts simulieren: kann der Connector kein Design
   anlegen, das sagen und Weg A anbieten.
3. **Ergebnis-Link** (Design-URL o.ä.) an den User geben. Feinschliff passiert im Design-Tool,
   nicht im Skill. Kein Render, kein PNG-Export durch den Skill.
4. **Log** wie in Phase 8A (Output-Weg: Name des Tools).

---

## Render-Stack (einmalig, für `--final`)

```bash
pip install playwright pillow --break-system-packages
python3 -m playwright install chromium
```

Der Preview-Modus (ohne `--final`) braucht das nicht.

---

## Output

Immer: Output-Ordner `{marketing}/content/carousels/[YYYY-MM-DD]-[slug]/` mit `slides.md`
(approvte Slide-Texte). Keine Post-Caption.

- **Weg A (HTML):** zusätzlich `carousel.html`, `preview.html`, nach "Go" `slide-01..NN.png` + `full-carousel.pdf`.
- **Weg B (Design-Tool):** zusätzlich der Design-Link aus dem verbundenen Connector; Dateien entstehen dort, nicht im Brain.

Kein automatisches Posten. Kurzer Eintrag im Tages-Log `{logs}/[YYYY-MM-DD].md` unter `## Carousel`.

## Verwandte Skills

**Erlaubte Skills:**

- `/brand-voice`: Stimme der Brand auf alle Texte
- `/icp` Modus *Bewerten*: Hook/CTA gegen ICP

**Abgrenzung:**

- Kein automatisches Posten - Export ist PNG + PDF (Weg A) oder ein Design im verbundenen Tool (Weg B).
- Keine Post-Caption: der Skill liefert nur die Slides.
- Keine Reels/Videos (`/reel-skript` bzw. `/video-shortform`), keine Caption-only-Posts (`/instagram-caption`, `/linkedin-caption`).
- Comment-for-X braucht ein Auto-DM-Tool - ohne das den Direktlink-CTA wählen.

## Hard-Stops

- Mehr als **20 Slides** -> kürzen (hartes Instagram-Carousel-Limit). Sinnvolle Spanne: 5-20.
- User hat in Phase 1 oder 2 nicht bestätigt.
- Kein "passt" in Phase 5 -> kein HTML-Build, kein Design-Tool-Push (Text zuerst).
- Weg B ohne tatsächlich verbundenen Design-Connector -> nicht anbieten, nichts simulieren.
- Assertion schlägt an (offene `{{...}}`-Tokens).
- ICP-Check zweimal fail -> Schwachstelle offenlegen statt drüberbügeln.
- Playwright fehlt -> kein `--final` (Preview geht trotzdem).
- Kein explizites "go"/"passt" -> kein Final-Render.
