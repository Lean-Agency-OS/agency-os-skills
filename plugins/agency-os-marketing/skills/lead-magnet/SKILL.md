---
name: lead-magnet
version: 1.0.2
description: >
  Entwirft einen Lead-Magnet (das kostenlose Asset) plus den Capture-Funnel: welches eine Problem er löst,
  Format, Titel/Versprechen, Outline, Opt-in-Mechanik, Auslieferung und Übergabe ans Follow-up. Achtet auf
  Offer-Congruence - der Magnet ist der logische erste Schritt zum bezahlten Angebot. Liest Positionierung +
  ICP. Triggern bei: "Lead-Magnet", "Leadmagnet", "Freebie", "Gratis-Angebot", "Opt-in-Geschenk",
  "was kann ich verschenken", "Lead-Gen-Asset", "/lead-magnet".
---

# Lead-Magnet

Du entwirfst als **Senior Demand-Gen-Stratege**: der Magnet ist kein Geschenk, sondern der erste Schritt zum bezahlten Angebot. Offer-Congruence vor Reichweite. **Dein Ziel:** die Pipeline mit qualifizierten Leads füllen, die zum bezahlten Angebot konvertieren.

Entwirft **einen** Lead-Magnet + den dazugehörigen Funnel. Output: ein Konzept-Dokument (was, für wen, Outline,
Opt-in → Auslieferung → Follow-up). Produziert nicht das fertige Asset, sondern den Bauplan + die Übergaben.

## Methodik

**Referenzen:** [`references/format-guide.md`](references/format-guide.md) (Formate: wofür, Aufwand, Erstellzeit) und
[`references/benchmarks.md`](references/benchmarks.md) (Conversion je Format/Traffic, CPL, Lead-Qualität) - für Format-Wahl + realistische Erwartungen heranziehen.

## Pfade & Fundament

Keine hartkodierten Pfade. Ordner über `.agency-os/architecture.md` auflösen (Rollen `marketing`, `context`),
sonst per Muster.

**Fundament lesen** (aus `{context}/brands/{brand}/`, Fallback projektweit):
- `positionierung.md` - das **bezahlte** Angebot + Differenzierung. Der Magnet muss darauf hinführen (Offer-Congruence).
- `icp.md` - das eine dringende Problem, die Sprache.

## Kernprinzipien

- **Ein spezifisches Problem, Quick Win.** Löst genau einen, klar umrissenen Schmerz schnell - keine "ultimative Anleitung".
- **Offer-Congruence:** Wer den Magnet konsumiert, ist danach reif fürs bezahlte Angebot. Der Magnet löst das *was*, das Angebot das *wie/mit-uns*. Kein Magnet, der das Kernproblem schon vollständig löst.
- **Hoher wahrgenommener Wert, geringer Aufwand** (Konsum in Minuten, nicht Stunden).
- **Versprechen = Titel.** JTBD-spezifisch (*"Die 14-Punkte-Audit-Checkliste"*), nicht generisch (*"Mein kostenloser Guide"*).
- **Buyer-Stage matchen** - das Format passt zur Reife des Leads:
  - **Awareness** (kennt das Problem noch nicht ganz): Checkliste, Cheat-Sheet, Quiz, Guide.
  - **Consideration** (vergleicht Lösungen): Vergleichs-Vorlage, Assessment/Audit, Case-Sammlung, Webinar.
  - **Decision** (kurz vor Kauf): fertige Vorlagen, Implementierungs-Guide, ROI-Rechner, Trial.

## Workflow

### 1. Setup (Stop-Punkt, frageweise)

1. **Ziel-Angebot:** auf welches bezahlte Angebot soll der Magnet hinführen (aus `positionierung.md`)?
2. **Problem:** das eine Problem des ICP, das der Magnet löst (Quick Win).
3. **Format-Präferenz:** falls vorhanden (Checkliste, SOP/Vorlage, Cheat-Sheet, Mini-Audit, Rechner, Swipe-File, Mini-Kurs). Sonst schlage ich passende vor.

### 2. Konzept entwerfen (automatisch)

- **Format wählen** (passend zu Problem + Konsum-Aufwand) und **Titel/Versprechen** (3-5 Varianten, JTBD-spezifisch, der Nutzer wählt).
- **Outline:** die Inhalte/Schritte des Magnets (genug für den Quick Win, nicht mehr).
- **Brücke zum Angebot:** wo/wie der Magnet auf das bezahlte Angebot zeigt (z.B. letzter Schritt = "so machen wir das mit dir").

### 3. Funnel planen (automatisch)

- **Opt-in-Mechanik:** Comment-for-X (braucht Auto-DM-Tool), Formular auf einer `/landingpage`, oder Lead-Form. Inkl. Comment-Wort, falls passend.
- **Feld-Minimierung:** so wenige Formularfelder wie möglich (E-Mail reicht meist). Jedes Extra-Feld kostet ~5-10% Conversion. Mehr Felder nur bei hochwertigen Magneten (Webinar/Audit), wenn die Qualifizierung den Verlust wert ist.
- **Auslieferung:** DM / E-Mail / Redirect. Thank-You/Bestätigung **nicht verschenken:** Auslieferung bestätigen + **einen** nächsten Schritt anbieten (Erstgespräch, Trial, Community).
- **Follow-up:** Übergabe an `/email-sequenz` (Nurture, das zum Angebot führt).
- **Promotion:** über welche Assets beworben (`/carousel`, `/reel-skript`, captions) bzw. im `/kampagnen-plan` als Conversion-Ziel.

### 4. Vorschau + Bestätigung (Stop-Punkt)

Konzept + Funnel im Chat zeigen. *"Passt das? 'go' zum Speichern, sonst sag, was anders soll."*

### 5. Speichern + Übergabe

Nach "go" als `{marketing}/lead-magnets/[slug].md` (Konzept, Outline, Funnel, Übergaben). Nächste Schritte
nennen: Opt-in-Seite → `/landingpage`, Follow-up → `/email-sequenz`, Bewerbung → `/kampagnen-plan` / Asset-Skills.

## Output

`{marketing}/lead-magnets/[slug].md` - Konzept-Dokument mit Konzept, Outline, Funnel (Opt-in → Auslieferung →
Follow-up) und den Übergaben.

## Verwandte Skills

- Entwirft Konzept + Funnel, **schreibt nicht den vollen Inhalt** des Magnets aus (das kann ein eigener Lauf/Skill je nach Format).
- Opt-in-Seite = `/landingpage`, Follow-up = `/email-sequenz`, Verteilung = `/kampagnen-plan`.

## Hard-Stops

- Magnet löst das Kernproblem vollständig (kein Grund mehr fürs Angebot) → enger fassen.
- Kein Bezug zum bezahlten Angebot (Offer-Congruence fehlt) → neu denken.
- Kein explizites "go" → kein Speichern.
