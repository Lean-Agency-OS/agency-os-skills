---
name: kampagnen-plan
version: 1.0.2
description: >
  Plant eine zielgebundene Marketing-Kampagne von EINEM Ziel über Funnel, Kanäle und Assets bis zu
  KPIs und Timeline - und orchestriert, welche Asset-Skills (carousel, reel-skript, newsletter-email,
  captions, …) dafür laufen. Schreibt einen Kampagnen-Plan in den Marketing-Ordner. Liest Positionierung
  + ICP + Voice als Fundament. Triggern bei: "Kampagne planen", "Kampagnen-Plan", "Launch planen",
  "Go-to-Market", "wie bringen wir X raus", "Aktion planen", "/kampagnen-plan".
---

# Kampagnen-Plan

Du planst als **Senior Campaign-Lead**: du orchestrierst ein Ziel über Funnel, Kanäle und Assets, statt Einzelstücke zu sammeln. Konsistenz auf das eine Ziel schlägt Menge. **Dein Ziel:** das eine Kampagnen-Ziel erreichen: messbar mehr Leads, Calls oder Verkäufe.

Plant **eine** zielgebundene Kampagne (ein Ziel, befristet, mehrere Kanäle) und legt fest, **welche
Asset-Skills** dafür laufen. Output: ein Kampagnen-Plan, der die Einzel-Skills zu einer Pipeline bündelt.

## Pfade & Fundament

Keine hartkodierten Pfade. Ordner über `.agency-os/architecture.md` auflösen (Rollen `marketing`, `context`,
`logs`), sonst per Muster. `{marketing}`/`{context}`/`{logs}` unten sind die aufgelösten Pfade.

**Fundament lesen** (aus `{context}/brands/{brand}/`, Fallback projektweit):
- `positionierung.md` - Angebot, Differenzierung, Messaging-Pillars (der rote Faden der Kampagne).
- `icp.md` - Zielgruppe, Spannungen, Sprache.
- `voice-profile.md` - Ton für alle Texte.

Fehlt die Positionierung: Kampagne trotzdem planbar, aber empfehlen, sie mit `/positionierung` zu schärfen -
ohne klares Angebot zerfasert jede Kampagne.

## Workflow

### 1. Setup (Stop-Punkt, frageweise)

Eine Frage nach der anderen:
1. **Ziel:** *Ein* messbares Ziel (z.B. 50 Leads für Lead-Magnet X, 20 Erstgespräche, Launch von Y). Genau eines.
2. **Zielgruppe:** welches ICP-Segment (aus `icp.md`).
3. **Angebot & CTA:** was wird angeboten, was ist die eine gewünschte Handlung (aus `positionierung.md`).
4. **Zeitraum:** Start/Ende, grobe Phasen (z.B. Tease → Launch → Nachfass).
5. **Kanäle:** wo gespielt wird (LinkedIn, Instagram, Newsletter, Paid, …) - realistisch zur Kapazität.

Zusammenfassung zeigen, auf OK warten.

### 2. Funnel + Asset-Plan (automatisch)

Das Ziel über einen Funnel auf konkrete Assets herunterbrechen und **jedem Asset den passenden Skill** zuordnen:

| Funnel-Stufe | Zweck | Mögliche Assets → Skill |
|---|---|---|
| Awareness | Reichweite, Problem sichtbar machen | Carousel → `/carousel`, Reel → `/reel-skript`, Post-Caption → `/instagram-caption` / `/linkedin-caption` |
| Consideration | Vertrauen, Tiefe | Newsletter → `/newsletter-email`, Carousel-Serie, Case-Study |
| Conversion | die eine Handlung | Landingpage, Angebots-Mail, Comment-for-X-CTA |

- Pro Asset: Kanal, Kernbotschaft (an einem Messaging-Pillar verankert), grober Termin/Phase.
- Nur Assets planen, für die es einen Skill oder einen klaren manuellen Weg gibt. Lücken (z.B. Landingpage, Paid) offen benennen.
- **Konsistenz:** jedes Asset trägt dasselbe Angebot + denselben CTA Richtung Ziel.

### 3. KPIs + Messung (automatisch)

Pro Funnel-Stufe eine Kennzahl + Zielwert (z.B. Awareness: Reach/Saves; Consideration: Klicks/Antworten;
Conversion: Leads/Calls). Eine **Nordstern-Metrik** = das Kampagnen-Ziel. Festhalten, wie gemessen wird.

### 4. Vorschau + Bestätigung (Stop-Punkt)

Den vollständigen Plan im Chat zeigen (Ziel, Zielgruppe, Angebot/CTA, Funnel→Asset→Skill-Tabelle, Timeline,
KPIs). Abschlussfrage: *"Passt der Plan? 'go' zum Speichern, sonst sag, was anders soll."*

### 5. Schreiben

Nach "go" als `{marketing}/kampagnen/[YYYY-MM-DD]-[slug]/plan.md` ablegen (Slug: kebab-case aus dem Ziel).
Frontmatter: Status (`geplant`/`aktiv`/`abgeschlossen`), Zeitraum, Ziel, Nordstern-KPI. Darunter der Plan +
die Asset-Liste mit Status pro Asset.

### 6. Abschluss + Übergabe

- **Nächste Schritte:** die geplanten Asset-Skills nennen, die jetzt gestartet werden können (z.B. *"Starte mit `/carousel` für Asset 1, `/newsletter-email` für die Launch-Mail."*).
- **In den Takt einplanen:** auf `/content-kalender` verweisen, um die Kampagnen-Assets zu terminieren.
- **Log:** kurzer Eintrag im Tages-Log `{logs}/[YYYY-MM-DD].md` (Kampagne angelegt, Ziel).

## Output

`{marketing}/kampagnen/[YYYY-MM-DD]-[slug]/plan.md` - der Kampagnen-Plan mit Frontmatter (Status, Zeitraum,
Ziel, Nordstern-KPI), Funnel→Asset→Skill-Tabelle, Timeline, KPIs und Asset-Liste mit Status pro Asset.

## Verwandte Skills

- **Abgrenzung zum Content-Kalender:** Kampagne = **ziel­getriebener, befristeter Push** mit Funnel und KPIs. Der laufende Veröffentlichungs-Takt ist `content-kalender`. Die Kampagnen-Assets werden dort eingeplant.
- Ein Ziel pro Kampagne. Mehrere Ziele → mehrere Kampagnen.
- Plant + orchestriert, **produziert die Assets nicht selbst** - das machen die jeweiligen Skills.
- Laufender Redaktions-Takt ist `content-kalender`, das Fundament `positionierung`.

## Hard-Stops

- Mehr als ein Ziel → erst auf eines fokussieren.
- Kein explizites "go" → nicht schreiben.
- Asset ohne Bezug zum Ziel/CTA → raus aus dem Plan (jedes Asset zahlt auf das eine Ziel ein).
