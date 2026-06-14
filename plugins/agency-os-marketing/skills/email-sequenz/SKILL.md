---
name: email-sequenz
version: 1.0.0
description: >
  Plant und schreibt eine mehrteilige, automatisierte E-Mail-Strecke (Welcome, Nurture, Re-Engagement,
  Launch, Post-Purchase): Anzahl, Ziel je Mail, Timing und Bogen - jede Mail nach der 4-Bausteine-Formel,
  genau ein CTA pro Mail. Liest Positionierung + ICP + Voice. Triggern bei: "E-Mail-Sequenz", "Email-Sequenz",
  "Drip-Kampagne", "Automation", "Welcome-Strecke", "Nurture-Sequenz", "Onboarding-Mails", "Launch-Sequenz",
  "Re-Engagement-Mails", "Mailstrecke", "/email-sequenz".
---

# E-Mail-Sequenz

Plant + schreibt eine **mehrteilige automatisierte Strecke** (nicht eine Einzel-Mail - das ist `/newsletter-email`).
Jede Mail folgt der 4-Bausteine-Formel (Hook → Build → Payoff → CTA), die Strecke folgt einem Bogen mit Timing.

## Methodik

**Kanonische Methodik (Pflicht lesen vor Phase 1):**
- [`references/sequenz-typen.md`](references/sequenz-typen.md) - Sequenz-Typen, Bogen je Typ, Mail-Anzahl, Timing, Ziel je Mail, Per-Mail-Aufbau (4-Bausteine), No-Gos.

## Pfade & Fundament

Keine hartkodierten Pfade. Ordner über `.agency-os/architecture.md` auflösen (Rollen `marketing`, `context`), sonst per Muster.

**Fundament lesen** (aus `{context}/brands/{brand}/`, Fallback projektweit):
- `positionierung.md` - Angebot + Differenzierung (wohin die Strecke führt).
- `icp.md` - Spannungen, Sprache, Kernproblem.
- `voice-profile.md` - Ton auf alle Mails.

## Workflow

### 1. Setup (Stop-Punkt, frageweise)

1. **Typ + Ziel:** welche Strecke (Welcome / Nurture / Re-Engagement / Launch / Post-Purchase) und ihr eines Ziel.
2. **Auslöser + Liste:** was startet die Strecke (Opt-in/Lead-Magnet, Kauf, Inaktivität), an wen.
3. **Angebot/CTA-Ziel:** worauf die Strecke hinarbeitet (aus `positionierung.md`).
4. **Story-/Material-Input:** echte Stories, Cases, Beweise (bei Story-Mails). Nichts erfinden.

### 2. Bogen planen (automatisch)

Nach `references/sequenz-typen.md` den Bogen festlegen: **Anzahl Mails**, **Ziel je Mail**, **Timing/Abstände**.
Jede Mail bekommt genau eine Aufgabe (z.B. ausliefern → Quick Win → Story/Authority → Soft Offer → Hard Offer).
Pro Mail ein Messaging-Pillar/Beweis als Anker.

### 3. Mails schreiben (automatisch)

Pro Mail: **Betreff** (40-60 Zeichen, klar vor clever, spezifisch) + **Vorschautext** + Body nach 4-Bausteine (Hook ohne Gruß → Build → Payoff → **ein** CTA).
Voice anwenden. Über die Strecke einen roten Faden halten (Rückbezüge, steigende CTA-Intensität).

### 4. Qualitäts-Check (automatisch)

- Jede Mail genau ein CTA, eine Aufgabe? Betreff klar + spezifisch (40-60 Zeichen)? Vorschautext ergänzt den Betreff?
- Bogen stimmig (Intensität steigt, kein Bruch)? Timing realistisch?
- Diagnose statt Lehre? Kein erfundenes Material?
- Optional ICP-Check (`/icp` Bewerten) auf die Hook-/Angebots-Mails.

### 5. Vorschau + Bestätigung (Stop-Punkt)

Bogen-Übersicht (Mail-Liste mit Ziel + Timing) + alle Mails im Chat zeigen. *"Passt das? 'go' zum Speichern, sonst sag, was anders soll."*
Iteration pro Mail/Bereich, nur das Geänderte neu schreiben.

### 6. Speichern

Nach "go" als `{marketing}/email-sequenzen/[slug].md` (Slug aus Typ/Ziel). Frontmatter: Typ, Auslöser, Ziel,
Mail-Anzahl, Timing. Darunter die Bogen-Übersicht + jede Mail als eigene Sektion (Betreff + Body + Versand-Offset).
Falls Teil einer Kampagne/eines Lead-Magnets: dort verlinken.

## Output

`{marketing}/email-sequenzen/[slug].md` - Frontmatter (Typ, Auslöser, Ziel, Mail-Anzahl, Timing), Bogen-Übersicht
und jede Mail als eigene Sektion (Betreff + Body + Versand-Offset).

## Verwandte Skills

- Mehrteilige automatisierte Strecke - eine **einzelne** Newsletter-Mail ist `/newsletter-email`.
- Kein Cold-Outreach (kalte Erstansprache ist ein eigener Use-Case).
- Kein Versand/Tool-Setup - die fertigen Mails werden im ESP/der Automation eingebaut.

## Hard-Stops

- `references/sequenz-typen.md` fehlt → Skill nicht nutzbar.
- Mehrere CTAs pro Mail → auf einen reduzieren.
- Story-Mail ohne echtes Material → nicht erfinden, zurückfragen.
- Kein explizites "go" → kein Speichern.
