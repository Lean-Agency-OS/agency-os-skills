---
name: carousel
description: >
  Baut Carousel-Posts (10 Slides, Instagram/LinkedIn) nach der
  4-Bausteine-Formel: Hook → Build → Payoff → CTA. Geführter Workflow:
  Setup (Ziel/CTA/Thema) → 5 Hook-Varianten zur Auswahl → vollständiger
  Build → Quality-Checks gegen das ICP → Slide-Texte + Caption + HTML-Preview.
  Triggern bei: "bau mir einen Carousel", "Carousel-Post zu", "Carousel-Idee",
  "Slides für Instagram", "Karussell-Post", "Carousel erstellen".
---

# Carousel-Builder

Baut einen 10-Slide-Carousel von der Idee bis zu fertigen Slide-Texten, Caption und HTML-Preview. Methodik: 4-Bausteine-Formel (`references/4-bausteine-formel.md`) + Slide-Anatomie (`references/slide-anatomy.md`).

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

### Phase 3: Vollständiger Build (automatisch)

Slides 3-7 (Build), Slide 8 (Payoff), Slide 9 (Bridge/Stakes/Proof), Slide 10 (CTA) nach `references/slide-anatomy.md` texten.

### Phase 4: Quality-Checks + Caption (automatisch)

- **Atomaritäts-Check:** Steht jede Slide alleine UND verkauft die nächste mit?
- **ICP-Check:** Trifft mindestens eine dokumentierte Spannung? Sprache aus dem Profil? (Bei Fail: einmal nachschärfen, bei zweitem Fail dem User die Schwachstelle zeigen)
- **Caption** schreiben (Instagram + LinkedIn-Variante), Voice-Profile anwenden falls vorhanden.

### Phase 5: Preview + Iteration (Stop-Punkt)

Self-contained HTML-Preview bauen (alle 10 Slides untereinander im 4:5-Format, CI-Farben, darunter die Caption) und speichern. User iteriert pro Slide oder Caption.

### Phase 6: Speichern

Nach dem Go alles ablegen unter:

```
06-knowledge/content/carousels/[YYYY-MM-DD]-[slug]/
├── slides.md      ← alle Slide-Texte strukturiert
├── caption.md     ← IG + LinkedIn Caption
└── preview.html   ← Preview
```

**Index-Pflege:** Neue Ordner in der `## Aktuell vorhanden`-Sektion von `06-knowledge/_index.md` verlinken.

## Abgrenzung

- Kein automatisches Posten — Export ist Text + Preview, das Designen/Posten passiert im Tool der Wahl (Canva, Figma, nativ)
- Keine Reels/Videos
- Comment-for-X-Mechanik braucht ein Auto-DM-Tool (z.B. Manychat) — ohne das den Direktlink-CTA wählen

## Hard-Stops

- Kein ICP-Profil vorhanden (erst icp-Setup)
- User hat in Phase 1 oder 2 nicht bestätigt
- ICP-Check zweimal hintereinander fail → Schwachstelle offenlegen statt drüberbügeln
