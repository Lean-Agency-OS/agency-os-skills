---
name: positionierung
version: 1.0.0
description: >
  Legt die Positionierung an oder aktualisiert sie: schreibt `positionierung.md` (Kategorie,
  Differenzierung, Beweise, Positioning-Statement, Messaging-Pillars, Angebot) in den Brand-Kontext.
  Das strategische Fundament - "warum gewinnen wir, was bieten wir wem an" - das ICP, Brand-Voice
  und alle Marketing-Skills als Anker lesen. Scannt zuerst den Kontext, geführtes Interview, schreibt
  erst nach Bestätigung. Triggern bei: "Positionierung", "Positionierung festlegen", "Messaging",
  "wofür stehen wir", "Differenzierung", "Value Proposition", "Angebot definieren", "Offer", "/positionierung".
---

# Positionierung

Schreibt die **Positionierung** als `positionierung.md` in den Brand-Ordner: wofür die Marke steht, wogegen
sie antritt, was sie einzigartig macht und was sie konkret anbietet. Das ist das **strategische Fundament** -
`icp` (wer), `brand-voice` (wie klingen), `brand-ci` (wie aussehen) und alle Marketing-Skills (carousel,
newsletter, captions, später kampagnen-plan) lesen es als **Positionierungs-Anker**.

## Pfade

Keine hartkodierten Pfade. Den `context`-Ordner über `.agency-os/architecture.md` auflösen
(`agency-os-start` pflegt die Map), sonst per Muster `*context*`. Ziel: `{context}/brands/{brand}/positionierung.md`.

- **Brand bestimmen:** Ordner unter `{context}/brands/`. Nur einer → der; mehrere → die mit `brand-config.md` `status: active`; neue Brand → Slug + Name erfragen, Ordner anlegen.
- **Existiert `positionierung.md` schon:** laden, aktuellen Stand zeigen, im **Update-Modus** nur das Genannte ändern. Sonst **Anlege-Modus**.

## Was das Dokument enthält

1. **Zielkunde** - für wen ist es (Verweis auf `icp.md`, nicht duplizieren).
2. **Kategorie / Alternative** - in welcher Kategorie konkurriert die Marke; was tut der Kunde sonst (Status quo, Wettbewerber, "nichts tun").
3. **Differenzierung** - was die Marke einzigartig kann, das die Alternativen nicht bieten (1-3 Punkte).
4. **Beweise** - warum das glaubwürdig ist (Ergebnisse, Methode, Erfahrung, Zahlen).
5. **Positioning-Statement** - 1-2 Sätze: *Für [Zielkunde], die [Problem], ist [Marke] das [Kategorie], das [Differenzierung] - anders als [Alternative], weil [Beweis].*
6. **Messaging-Pillars** - 3-4 Kernbotschaften, die in jedem Asset wiederkehren.
7. **Angebot (Offer)** - das konkrete Angebot: Job-to-be-Done, versprochene Transformation (von → zu), Format/Lieferung, optional Preis-Anker.
8. **Sprache** - die scharfen, eigenen Begriffe + die zu vermeidenden weichen Begriffe (an `icp.md` gekoppelt).

## Workflow

### 1. Kontext scannen (vor dem Interview)

Erst schauen, was schon da ist, statt blind zu fragen:
- **Bestehende `positionierung.md`** → Update-Modus, alle Abschnitte vorbelegen.
- **`icp.md`** → Zielkunde, Spannungen, Problem, scharfe Sprache (Pflicht-Lektüre, wird verlinkt nicht kopiert).
- **`voice-profile.md`** → Ton, damit das Statement nach der Marke klingt.
- **Angebots-/Sales-/Offer-Notizen, About-/Über-uns-Texte, frühere Decks** im Kontext → Differenzierung, Beweise, Angebot ableiten.

Gefundene Werte als **Vorschläge** ins Interview übernehmen. Was nicht gefunden wird, normal erfragen.

### 2. Interview (Stop-Punkt, gruppiert)

Pro Gruppe die gescannten Vorschläge zeigen, bestätigen/anpassen lassen, nur Fehlendes aktiv erfragen.
Eine Gruppe nach der anderen (der User darf auch mehr auf einmal liefern):

1. **Kategorie & Alternative:** *"In welcher Kategorie wirst du gesehen, und was macht dein Kunde heute stattdessen?"*
2. **Differenzierung:** *"Was kannst du, das die Alternativen nicht bieten? Was ist dein unfairer Vorteil?"*
3. **Beweise:** *"Warum glaubt man dir das? Ergebnisse, Methode, Zahlen, Erfahrung."*
4. **Angebot:** *"Was genau bietest du an? Welche Transformation (von → zu), in welchem Format?"*

Aus den Antworten **Positioning-Statement + 3-4 Messaging-Pillars ableiten** (nicht erfragen - synthetisieren und vorschlagen). Zielkunde + Sprache aus `icp.md` ziehen.

**Schärfe-Prinzip:** Differenzierung muss konkret und überprüfbar sein, keine Allerwelts-Claims (*"beste Qualität", "kundenorientiert"*). Falls vorhanden, mit `/icp` Modus *Bewerten* gegen das ICP testen: trifft die Positionierung den Nerv?

### 3. Vorschau + Bestätigung (Stop-Punkt)

Die fertige `positionierung.md` (alle Abschnitte + abgeleitetes Statement + Pillars) im Chat zeigen.
Abschlussfrage: *"Passt das? 'go' zum Speichern, sonst sag, was anders soll."* Ohne "go" → nicht schreiben.

### 4. Schreiben

Nach "go" `{context}/brands/{brand}/positionierung.md` schreiben (Anlege-Modus) bzw. die geänderten
Abschnitte aktualisieren (Update-Modus, Rest unverändert). Auf `icp.md` und `voice-profile.md` verlinken.
Ordner ggf. anlegen.

### 5. Abschluss

Pfad ausgeben. Hinweis: ICP, Brand-Voice und die Marketing-Skills nutzen die Positionierung ab jetzt als
Anker. Falls beim Scan Lücken auffielen (kein ICP, kein Angebot scharf): kurz benennen und auf `/icp` bzw.
eine Angebots-Schärfung hinweisen.

## Abgrenzung

- **Strategie, kein Asset.** Schreibt nur das Fundament-Dokument, keine Posts/Mails/Ads.
- `icp` = WER (Zielgruppe), `brand-voice` = WIE klingen, `brand-ci` = WIE aussehen, **positionierung = WARUM gewinnen / WAS anbieten**.
- Keine Kampagnen-/Redaktionsplanung (das sind `kampagnen-plan` bzw. `content-kalender`).

## Hard-Stops

- Kein explizites "go" → nicht schreiben.
- Differenzierung bleibt generisch/austauschbar → nachschärfen, nicht speichern (eine unscharfe Positionierung schadet mehr als keine).
- Brand unklar (mehrere Ordner, keine Wahl) → erst klären, nicht raten.
