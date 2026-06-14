# Carousel Slide-Anatomie (10 Slides)

Self-contained Struktur-Spec für 10-Slide-Carousels. Methodik-Basis: [`4-bausteine-formel.md`](4-bausteine-formel.md).
Visuelles (Farben, Fonts, Foto, Brand-Mark) kommt aus dem Layout-Template + der Brand-CI, nicht hier.

**Standard:** 10 Slides (Sweetspot 8-10).

## Atomaritäts-Prinzip

Jede Slide leistet zwei Dinge gleichzeitig:
1. **Alleine stehen** — wer nur diese eine Slide sieht/screenshottet, hat einen kompletten Mini-Mehrwert.
2. **Die nächste mitverkaufen** — Cliff-Hanger oder Pattern-Trigger zum Weiter-Swipen.

Schließt aus: "Slide 4 ergibt nur Sinn, wenn man Slide 3 gelesen hat." Grund: Instagram serviert bei einer
zweiten Impression oft **Slide 2 als Cover** statt Slide 1, jede Slide kann also der Einstieg sein.

## Pflicht-Setup vor der Slide-Generierung

Jedes Carousel verkauft etwas. Vorab klären (sonst kein Aufbau):
1. **Conversion-Ziel** (Lead-Magnet / Tripwire / Erstgespräch).
2. **Comment-Wort** für Slide 10 (4-7 Buchstaben, All-Caps, ein Wort, JTBD-spezifisch).
3. **Build-Subtyp** (Story / Liste / Steps - genau einer, durchgängig).
4. **Ziel-Metrik** (Saves für Wert-Carousels, Shares für emotionale).

## 10-Slide-Struktur

| Slide | Baustein | Subtyp | Wörter | Visual:Text | Aufgabe |
|-------|----------|--------|--------|-------------|---------|
| 1 | Hook | Visual Hook | 6-10 | 70/30 | Stop-the-Scroll in <2 Sek. Mind Gap, löst nichts auf. Einer der 6 Hook-Typen. |
| 2 | Hook | Rehook | 15-25 | Modus-Wechsel zu Slide 1 | Eigenständiger Hook im **anderen Modus** (Slide 1 grafisch → 2 textlastig oder umgekehrt). Standalone-fähig. Wiederholt Slide 1 NICHT. |
| 3 | Build | Story/Liste/Steps | 25-40 | 30/70 | Algorithmus-Schwelle (Completion entscheidet sich hier). Diagnostiziert. |
| 4 | Build | (gleicher Subtyp) | 25-40 | 30/70 | Vertieft die Diagnose. |
| 5 | Build | (gleicher Subtyp) | 25-40 | 30/70 | Framework / System-Map. Authority. |
| 6 | Build | (gleicher Subtyp) | 25-40 | 30/70 | Mockup / Beweis / Konkretheit. |
| 7 | Build | (gleicher Subtyp) | 25-40 | 30/70 | Taktischer / dichtester Punkt. |
| 8 | Payoff | Insight ODER Umsetzung | 15-25 | 30/70 | EIN Insight (Reframe) ODER EIN Schritt. Niemals beides. |
| 9 | Payoff | Bridge/Stakes/Proof | 15-25 | 30/70 | Bereitet CTA vor. **Kein konkurrierender CTA.** |
| 10 | CTA | Microoffer | 10-20 | 60/40 | Foto + ein Comment-Wort + klares Angebot. |

**Build-Subtyp-Konsistenz:** innerhalb eines Carousels EIN Subtyp durchgängig, nicht mischen.

## Slide 9 — drei zulässige Varianten (genau eine)

- **Bridge mit Open Loop:** *"Der schnellste Weg, das zu installieren? [Lead-Magnet]. Swipe →"*
- **Stakes-Raise:** Kosten des Nicht-Handelns, möglichst quantifiziert.
- **Specificity-Proof:** ein konkretes Mini-Resultat aus dem Lead-Magnet.

Wahl: Stakes-Raise wenn Schmerz quantifizierbar; Proof wenn der Lead-Magnet konkrete Findings liefert; sonst Bridge.

## Ein-CTA-Prinzip (Pflicht)

Genau ein CTA pro Carousel, auf Slide 10. Slide 9 enthält **niemals** einen konkurrierenden CTA
(kein Save-/Folge-/Send-Aufruf). Zwei CTAs = geteilte Aufmerksamkeit = beide underperformen.

## Slide 10 (CTA) — Specs

Foto (der Person/Marke) + EIN Comment-Wort + klares Angebot. Pattern:
*"Willst du [JTBD-Framing]? Kommentiere [WORT] - ich schick's dir per DM."*

Comment-Wort: 4-7 Buchstaben, All-Caps, genau ein Wort, keine Sonderzeichen, JTBD-spezifisch
(*"AUDIT"* schlägt *"INFO"*). Braucht ein Auto-DM-Tool (z.B. Manychat) mit exact-match Keyword.
Verboten: mehr als eine Action, vage Aufforderung, Nummer als Trigger, Text-only ohne Foto.

## Atomaritäts-Check (vor Render, pro Slide)

1. **Stehende Frage:** Bei nur dieser Slide - versteht man etwas Neues/Nützliches?
2. **Akzent:** genau ein Akzent-Element (außer reine Mockups)?
3. **Sog zur nächsten:** Open Loop / Cliff-Hanger / Listenposition?
4. **Wortzahl im Range** (Tabelle oben)?
5. **Visual-Anteil** stimmig (Slide 1+10 ~60% Visual, 2-9 ~30%)?
6. **Brand-Mark:** Topbar mit Brand-Name + Seiten-Index?
7. **Foot:** Handle + Weiter-Pfeil (außer Slide 10: End-Marker)?

1, 3 oder 4 nicht erfüllt → Slide neu schreiben, nicht produzieren.

## Hook-Regeln Slide 1

- **Max 12 Wörter**, Lesezeit < 2 Sek, Payoff-Versprechen bis Slide 3 einlösen.
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
- 8-10 Slides werden deutlich häufiger gespeichert als Single-Photos.
- Top-Carousels: Swipe bis Slide 3 ~65%+, Completion bis Slide 10 ~55%+.
- Algorithmus-Signale (Prio): Watch/Dwell Time > Sends per Reach > Likes per Reach.
