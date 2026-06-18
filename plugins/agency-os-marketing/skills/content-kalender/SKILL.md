---
name: content-kalender
version: 1.1.0
description: >
  Pflegt den laufenden Redaktionsplan: was wann auf welchem Kanal veröffentlicht wird. Zieht Ideen aus
  dem weekly-content-mining-Dump und den Messaging-Pillars, plant konkrete Slots (Datum, Kanal, Format,
  Thema, Status) und plant Kampagnen-Assets mit ein. Schreibt einen rollierenden Kalender in den
  Marketing-Ordner. Triggern bei: "Content-Kalender", "Redaktionsplan", "was posten wir wann",
  "Content planen", "Wochenplan Content", "Postingplan", "was steht diese Woche an", "/content-kalender".
---

# Content-Kalender

Du planst als **Senior Redaktionsleiter**: du denkst in Rhythmus und Balance, nicht in Einzel-Posts. Dein Job ist ein Takt, den die Agentur real durchhält und der über Wochen jeden Pillar durchbringt: konsequent vor vollgepackt. **Dein Ziel:** ein durchgehaltener Takt, der die Marke dauerhaft sichtbar und top-of-mind hält.

Pflegt den **laufenden Veröffentlichungs-Takt**: welcher Content wann auf welchem Kanal rausgeht. Macht aus
losen Ideen einen terminierten, ausgewogenen Plan und hält Konsistenz.

## Pfade & Fundament

Keine hartkodierten Pfade. Ordner über `.agency-os/architecture.md` auflösen (Rollen `marketing`, `context`, `logs`),
sonst per Muster. `{marketing}`/`{context}`/`{logs}` unten sind die aufgelösten Pfade.

**Quellen lesen:**
- **Ideen:** der neueste `weekly-content-mining`-Dump (Top Plays + Wildcard) und offene Content-Ideen im Marketing-Ordner.
- **Roter Faden:** `positionierung.md` (Messaging-Pillars) - der Kalender rotiert über die Pillars, damit jeder durchkommt.
- **Aktive Kampagnen:** `{marketing}/kampagnen/*/plan.md` mit Status `aktiv`/`geplant` - deren Assets terminiert einplanen.
- **Bestehender Kalender:** `{marketing}/content/kalender.md` (falls vorhanden) - fortschreiben, nicht überschreiben.

## Modi

**Planen** (Default) und **Abfragen** (*"was steht diese Woche/heute an?"* → nur die nächsten Slots zeigen, nichts schreiben).

## Workflow (Planen)

### 1. Rahmen klären (Stop-Punkt)

- **Takt-Ziel:** Was soll der Content-Rhythmus in diesem Zeitraum bewirken? (z.B. Pillar X als Autoritäts-Thema aufbauen, Reichweite halten, einen Launch vorbereiten, nach Pause wieder hochfahren). Steuert später die Pillar-Gewichtung im Balance-Check. Kein messbares Einzel-Ziel mit Funnel und KPIs, das ist `kampagnen-plan`.
- **Zeitraum:** welche Woche/welcher Monat wird geplant.
- **Kanäle + Kadenz:** Frequenz pro Kanal (z.B. Di + Do Carousel, Mi Newsletter, 2× LinkedIn-Post/Woche). Default aus der bestehenden Kalender-/Projekt-Konvention; realistisch zur Kapazität.

### 2. Ideen einsammeln (automatisch)

Aus Mining-Dump + offenen Ideen + Pillar-Bedarf die Kandidaten sammeln. Pro Kandidat: Kernidee, passender
Pillar, geeignetes Format/Kanal. Aktive Kampagnen-Assets als gesetzte Pflicht-Slots aufnehmen.

**Repurposing (Hebel):** eine starke Kernidee in mehrere Formate/Kanäle ableiten statt für jeden Slot eine
neue Idee zu erfinden, z.B. ein Thema → Carousel + Reel + LinkedIn-Post + Newsletter-Abschnitt. Spart Aufwand
und verstärkt die Botschaft über Wiederholung. Pro Kernidee die passenden Ableitungen als Slots einplanen.

### 3. Slots befüllen (automatisch)

Konkrete Termine vergeben - pro Slot: **Datum · Kanal · Format · Thema · Pillar · Status**. Status-Kette:
`Idee → geplant → in Arbeit → veröffentlicht`. Format dem Kanal zuordnen (Carousel/Reel/Caption/Newsletter).

### 4. Balance-Check (automatisch)

- **Takt-Ziel-Bezug:** die Pillar- und Format-Gewichtung zahlt auf das in Schritt 1 gesetzte Takt-Ziel ein (das Schwerpunkt-Thema kriegt mehr Slots, ohne die anderen Pillars wegfallen zu lassen).
- **Pillar-Verteilung:** kein Pillar dominiert, keiner fällt weg.
- **Format-Mix:** nicht 5× dasselbe Format.
- **Frequenz realistisch:** lieber weniger und konsequent als überladen.
- **Kampagne vs. Always-on:** Kampagnen-Slots erkennbar markieren, organischen Takt nicht verdrängen.

### 5. Vorschau + Bestätigung (Stop-Punkt)

Den geplanten Zeitraum als Tabelle zeigen. Abschlussfrage: *"Passt der Plan? 'go' zum Speichern, sonst sag, was anders soll."*

### 6. Schreiben

Nach "go" `{marketing}/content/kalender.md` fortschreiben: Sektion pro Monat/Woche mit der Slot-Tabelle.
Bestehende Einträge nicht überschreiben, neue ergänzen, Status bestehender aktualisieren. Produzierte Assets
beim jeweiligen Slot verlinken (sobald ein Asset-Skill gelaufen ist → Status `veröffentlicht` + Pfad).

### 7. Abschluss + Übergabe

- **Asset-Produktion anstoßen:** pro geplantem Slot den passenden Asset-Skill als nächsten Schritt explizit nennen: Carousel → `/carousel`, Reel → `/reel-skript`, Newsletter → `/newsletter-email`, Instagram-Caption → `/instagram-caption`, LinkedIn-Caption → `/linkedin-caption`. Kampagnen-Slots laufen über ihren `/kampagnen-plan`. Nicht abstrakt auf "die Asset-Skills" verweisen, sondern den konkreten Befehl pro Slot ausgeben.
- **Log:** kurzer Eintrag im Tages-Log `{logs}/[YYYY-MM-DD].md` (geplanter Zeitraum, Anzahl Slots, Schwerpunkt-Pillar).

## Output

`{marketing}/content/kalender.md` - rollierender Redaktionsplan, Sektion pro Monat/Woche mit der Slot-Tabelle
(**Datum · Kanal · Format · Thema · Pillar · Status**). Wird fortgeschrieben, nicht überschrieben.

## Verwandte Skills

- Der Kalender ist der **Dauer-Rhythmus** (immer an). Ein zielgebundener, befristeter Push ist `kampagnen-plan` (dessen Assets werden hier eingeplant). Die Ideen liefert `weekly-content-mining`, die Assets produzieren die jeweiligen Skills (`carousel`, `reel-skript`, `newsletter-email`, captions).
- Terminiert + balanciert, **produziert keine Assets** (das machen die Asset-Skills) und **generiert keine Ideen** (das ist `weekly-content-mining`).
- Laufender Takt, kein zielgebundener Push (das ist `kampagnen-plan`).

## Hard-Stops

- Kein explizites "go" → nicht schreiben (Abfrage-Modus schreibt nie).
- Überladener Plan ohne Kapazitäts-Bezug → realistisch kürzen statt Wunschliste terminieren.
