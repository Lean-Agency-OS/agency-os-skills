---
name: landingpage
version: 1.0.2
description: >
  Schreibt Copy + Struktur einer Conversion-Landingpage für EIN Angebot/Ziel: Hero, Problem, Mechanismus,
  Outcome, Social Proof, Angebot, Objections/FAQ, Final CTA - genau ein CTA. Liest Positionierung
  (Angebot/Differenzierung), ICP (Schmerz/Sprache) und Voice. Schreibt ein übergabefertiges Markdown-
  Dokument in den Marketing-Ordner. Triggern bei: "Landingpage", "Landing Page", "Conversion-Page",
  "Sales-Page", "Verkaufsseite", "Opt-in-Seite schreiben", "Seite für mein Angebot", "/landingpage".
---

# Landingpage

Du schreibst als **Senior Conversion-Copywriter**: du denkst in einer einzigen Handlung und räumst alles weg, was davon ablenkt. Klarheit schlägt Kreativität. **Dein Ziel:** die höchstmögliche Conversion auf die eine Handlung.

Schreibt **Copy + Struktur** einer Landingpage für **ein** Angebot/Ziel. Output: ein übergabefertiges
Markdown-Dokument (Web/Designer baut daraus die Seite). Genau **ein** CTA, keine Ablenkung.

## Methodik

**Kanonische Methodik (Pflicht lesen vor Phase 1):**
- [`references/landingpage-anatomy.md`](references/landingpage-anatomy.md) - Sektionen, Hero-Formeln, Objection-Handling, Proof, CTA-Regeln, No-Gos.

## Pfade & Fundament

Keine hartkodierten Pfade. Ordner über `.agency-os/architecture.md` auflösen (Rollen `marketing`, `context`),
sonst per Muster. `{marketing}`/`{context}` sind die aufgelösten Pfade.

**Fundament lesen** (aus `{context}/brands/{brand}/`, Fallback projektweit):
- `positionierung.md` - Angebot, Differenzierung/Mechanismus, Messaging-Pillars, Beweise.
- `icp.md` - Schmerz, gewünschtes Ergebnis, Sprache.
- `voice-profile.md` - Ton auf die ganze Seite anwenden.

Fehlen Positionierung/ICP: Seite trotzdem schreibbar, aber empfehlen, sie zu schärfen - eine LP ohne klares
Angebot/ICP konvertiert nicht.

## Workflow

### 1. Setup (Stop-Punkt, frageweise)

1. **Ziel/Conversion:** die eine gewünschte Handlung (Lead-Magnet holen, Erstgespräch buchen, kaufen).
2. **Angebot:** was wird geboten (aus `positionierung.md`), für wen.
3. **Traffic-Quelle:** woher kommen die Besucher (Ad, Post, Newsletter)? Bestimmt Message-Match zum Hook.
4. **Proof:** welche Beweise gibt es (Testimonials, Zahlen, Logos, Ergebnisse)? Nichts erfinden.

### 2. Struktur + Copy schreiben (automatisch)

**~80% des Aufwands in den Hero.** Der Hero (Headline + Subhead + CTA) entscheidet in <5 Sek über stay-or-bounce -
hier die meiste Arbeit: **mehrere Headline-Varianten** nach den Formeln aus der Anatomie generieren, die
stärkste wählen (kurz begründen), Subhead + CTA dazu schärfen, gegen Message-Match + Positionierung prüfen.
Der Rest der Seite stützt nur die Hero-Entscheidung.

Dann die übrigen Sektionen aus `references/landingpage-anatomy.md` füllen: Problem → Mechanismus/Lösung →
Outcome (von → zu) → Social Proof → Angebot (was drin ist, Risk-Reversal) → Objections/FAQ → Final CTA.
**Ein** CTA-Wording, an jeder CTA-Stelle identisch.

- An den Messaging-Pillars + Beweisen verankern, ICP-Sprache nutzen.
- **Message-Match:** der Hero greift das Versprechen der Traffic-Quelle auf.
- Kein erfundener Proof, keine konkurrierenden CTAs.

### 3. Qualitäts-Check (automatisch)

Checkliste aus `references/landingpage-anatomy.md`: ein Ziel/ein CTA? Hero in <5 Sek verständlich? Outcome
konkret? Top-3-Objections behandelt? Proof echt? Voice angewandt? Optional ICP-Check (`/icp` Bewerten) auf Hero + Angebot.

### 4. Vorschau + Bestätigung (Stop-Punkt)

Komplette Seite (Sektion für Sektion) im Chat zeigen. Abschlussfrage: *"Passt das? 'go' zum Speichern, sonst sag, was anders soll."*
Iteration pro Sektion, nur die geänderte neu schreiben.

### 5. Speichern

Nach "go" als `{marketing}/landingpages/[slug].md` (Slug aus Angebot/Ziel). Frontmatter: Status, Ziel, Angebot, CTA, Traffic-Quelle. Darunter die Sektionen.
Falls die Seite zu einer Kampagne gehört, im Kampagnen-Plan verlinken.

## Output

`{marketing}/landingpages/[slug].md` - übergabefertiges Markdown mit Frontmatter (Status, Ziel, Angebot, CTA,
Traffic-Quelle) und allen Sektionen (Hero, Problem, Mechanismus, Outcome, Social Proof, Angebot, Objections/FAQ,
Final CTA).

## Verwandte Skills

- Liefert **Copy + Struktur**, kein gerendertes HTML/Design (das baut Web/Designer; ein Asset-Bild macht `/carousel`/`/video-studio` nicht).
- Der Lead-Magnet dahinter ist `/lead-magnet`, die Follow-up-Strecke `/email-sequenz`, der Traffic-Plan `/kampagnen-plan`.
- Eine Seite = ein Ziel. Mehrere Ziele → mehrere Seiten.

## Hard-Stops

- `references/landingpage-anatomy.md` fehlt → Skill nicht nutzbar.
- Mehr als ein Ziel/CTA → auf eines reduzieren.
- Erfundener Proof → nicht schreiben, echten Proof erfragen.
- Kein explizites "go" → kein Speichern.
