# Carousel Slide-Anatomie

Self-contained Struktur-Spec für Carousels. Methodik-Basis: [`4-bausteine-formel.md`](4-bausteine-formel.md).
Visuelles (Farben, Fonts, Foto, Brand-Mark) kommt aus dem Layout-Template + der Brand-CI, nicht hier.

**Länge ist flexibel** - keine feste Slide-Zahl. Fix sind nur die Rollen-Anker; der Build dazwischen ist so
lang wie das Thema es braucht (Sweetspot gesamt ~8-10, geht aber auch kürzer). **Spanne: 5 (Minimal) bis
20 Slides** - 20 ist das harte Instagram-Carousel-Limit, nie mehr. Feste Anker:

- **Hook** = die **ersten zwei** Slides (Visual Hook + Rehook).
- **Build** = der Rest dazwischen, **variabel** (1 bis viele Slides, darf kurz sein).
- **Payoff** = **1-2 Slides direkt vor dem CTA** (darf kurz sein, notfalls in eine Slide gefaltet).
- **CTA** = die **letzte** Slide.

## Atomaritäts-Prinzip

Jede Slide leistet zwei Dinge gleichzeitig:
1. **Alleine stehen** — wer nur diese eine Slide sieht/screenshottet, hat einen kompletten Mini-Mehrwert.
2. **Die nächste mitverkaufen** — Cliff-Hanger oder Pattern-Trigger zum Weiter-Swipen.

Schließt aus: "Slide 4 ergibt nur Sinn, wenn man Slide 3 gelesen hat." Grund: Instagram serviert bei einer
zweiten Impression oft **die zweite Slide als Cover** statt der ersten, jede Slide kann also der Einstieg sein.

## Pflicht-Setup vor der Slide-Generierung

Jedes Carousel verkauft etwas. Vorab klären (sonst kein Aufbau):
1. **Conversion-Ziel** (Lead-Magnet / Tripwire / Erstgespräch).
2. **Comment-Wort** für die CTA-Slide (4-7 Buchstaben, All-Caps, ein Wort, JTBD-spezifisch).
3. **Build-Subtyp** (Story / Liste / Steps - genau einer, durchgängig).
4. **Ziel-Metrik** (Saves für Wert-Carousels, Shares für emotionale).

## Struktur (rollen-basiert)

| Rolle | Position | Anzahl | Wörter | Visual:Text | Aufgabe |
|-------|----------|--------|--------|-------------|---------|
| **Hook (Visual Hook)** | Slide 1 | 1 | 6-10 | 70/30 | Stop-the-Scroll in <2 Sek. Mind Gap, löst nichts auf. Einer der 6 Hook-Typen. |
| **Hook (Rehook)** | Slide 2 | 1 | 15-25 | Modus-Wechsel zu Slide 1 | Eigenständiger Hook im **anderen Modus** (grafisch ↔ textlastig). Standalone-fähig. Wiederholt Slide 1 NICHT. |
| **Build** | Mitte | **variabel** (kann kurz sein) | 25-40 | 30/70 | Diagnostiziert in einem durchgehenden Subtyp: Setup → Vertiefung → Framework/Beweis → dichtester Punkt. So viele Slides wie das Thema trägt, nicht mehr. Die erste Build-Slide ist die Algorithmus-/Completion-Schwelle. |
| **Payoff** | vor dem CTA | 1-2 | 15-25 | 30/70 | EIN Insight (Reframe) ODER EIN Umsetzungs-Schritt. Optional direkt davor eine Bridge/Stakes/Proof-Slide. Darf in eine Slide gefaltet werden. |
| **CTA** | letzte Slide | 1 | 10-20 | 60/40 | Foto + ein Comment-Wort + klares Angebot. |

**Build-Subtyp-Konsistenz:** innerhalb eines Carousels EIN Subtyp durchgängig, nicht mischen.

**Minimal-Carousel:** Hook (2) + Build (mind. 1) + Payoff (1) + CTA (1). Mehr Build nur, wenn das Thema es trägt.

## Payoff-Slide(s) — Varianten

Die Payoff-Slide bringt EIN Insight ODER EINE Umsetzung. Eine **optionale** Slide direkt davor (Bridge/Stakes/Proof)
bereitet den CTA vor (genau eine Variante wählen):
- **Bridge mit Open Loop:** *"Der schnellste Weg, das zu installieren? [Lead-Magnet]. Swipe →"*
- **Stakes-Raise:** Kosten des Nicht-Handelns, möglichst quantifiziert.
- **Specificity-Proof:** ein konkretes Mini-Resultat aus dem Lead-Magnet.

Wahl: Stakes-Raise wenn Schmerz quantifizierbar; Proof wenn der Lead-Magnet konkrete Findings liefert; sonst Bridge.
Ist das Thema knapp, entfällt diese Vorbereitungs-Slide und der Payoff steht direkt vor dem CTA.

## Ein-CTA-Prinzip (Pflicht)

Genau ein CTA pro Carousel, auf der **letzten** Slide. Die Payoff-/Bridge-Slides davor enthalten **niemals**
einen konkurrierenden CTA (kein Save-/Folge-/Send-Aufruf). Zwei CTAs = geteilte Aufmerksamkeit = beide underperformen.

## CTA-Slide — Specs

Foto (der Person/Marke) + EIN Comment-Wort + klares Angebot. Pattern:
*"Willst du [JTBD-Framing]? Kommentiere [WORT] - ich schick's dir per DM."*

Comment-Wort: 4-7 Buchstaben, All-Caps, genau ein Wort, keine Sonderzeichen, JTBD-spezifisch
(*"AUDIT"* schlägt *"INFO"*). Braucht ein Auto-DM-Tool (z.B. Manychat) mit exact-match Keyword.
Verboten: mehr als eine Action, vage Aufforderung, Nummer als Trigger, Text-only ohne Foto.

## Atomaritäts-Check (vor Render, pro Slide)

1. **Stehende Frage:** Bei nur dieser Slide - versteht man etwas Neues/Nützliches?
2. **Akzent:** genau ein Akzent-Element (außer reine Mockups)?
3. **Sog zur nächsten:** Open Loop / Cliff-Hanger / Listenposition?
4. **Wortzahl im Range** der jeweiligen Rolle (Tabelle oben)?
5. **Visual-Anteil** stimmig (Hook-Slide 1 + CTA-Slide ~60% Visual, Build/Payoff ~30%)?
6. **Brand-Mark:** Topbar mit Brand-Name + Seiten-Index?
7. **Foot:** Handle + Weiter-Pfeil (außer letzte Slide: End-Marker)?

1, 3 oder 4 nicht erfüllt → Slide neu schreiben, nicht produzieren.

## Hook-Regeln Slide 1

- **Max 12 Wörter**, Lesezeit < 2 Sek, Payoff-Versprechen bis zur ersten Build-Slide einlösen.
- Default-Pattern: **Numeric + Kontrast** (*"3 X, die Y killen"*).
- Mind. eine Hook-Psychologie aktiv: Curiosity, FOMO, Greed, Defensiveness, Relief, Disbelief.
- Verboten: *"Scroll for…"*/*"Tag someone"* (Low-Intent-Strafe), >12 Wörter, >1 Akzent-Wort, generische Sprache ohne Zahl/Kontrast.

## Rehook-Regeln Slide 2

- Eigener Hook in anderem Modus als Slide 1, **standalone** (wird als Cover re-serviert).
- Pattern: Reframe (*"Du dachtest X. Eigentlich Y."*) oder konkretes Schmerz-Szenario.
- Verboten: Slide 1 wiederholen, Aufwärm-Sprache (*"In diesem Carousel zeige ich dir…"*), zu früher CTA, >15 Wörter.

## Pattern-Interrupt

Visual-Type-Wechsel alle 2-3 Slides (Richtlinie, keine starre Pflicht). Roter Faden bleibt durchgängig.

## Engagement-Benchmarks 2026 (Orientierung)

- Carousels: höchste Engagement-Rate aller IG-Formate; Saves zählen ~5×, DM-Shares ~15× wie Likes.
- Carousels mit ~8-10 Slides werden deutlich häufiger gespeichert als Single-Photos (Orientierung, kein Muss).
- Top-Carousels: hohe Swipe-Through-Rate auf die ersten Build-Slides, Completion bis zur CTA-Slide hoch halten.
- Algorithmus-Signale (Prio): Watch/Dwell Time > Sends per Reach > Likes per Reach.
