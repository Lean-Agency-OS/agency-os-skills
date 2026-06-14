---
name: reel-skript
version: 1.0.0
description: >
  Plant ein versandfertiges Reel/Short-Skript nach der 4-Bausteine-Formel
  (Hook -> Build -> Payoff -> CTA). Diagnose-Ton statt Lehr-Ton, kurzes
  Vertical-Video-Asset, genau ein CTA. Geführter Workflow: Interview (Payoff ->
  Build -> CTA -> Hook, eine Frage nach der anderen) -> optional Story-Context ->
  Draft (gesprochenes Skript + On-Screen-Text + Shot-Regie + Caption) ->
  3 Hook-Varianten + Qualitäts-/ICP-Check -> Approval -> Speichern + Log.
  Liest das Voice-/ICP-/Positionierungs-Profil des Projekts, falls vorhanden.
  Plant nur (kein Rendern, das macht video-studio). Triggern bei: "plan mir ein Reel",
  "Reel planen", "Reel-Skript", "Reel-Idee", "Reel-Konzept", "Short planen",
  "Instagram Reel", "TikTok-Video planen", "YouTube Short planen", "Reel optimieren".
---

# Reel-Skript

Plant **ein** Reel/Short pro Aufruf, fertig zum Drehen/Schneiden. Diagnose-Ton (nicht
Lehr-Ton), kurzes Vertical-Asset (9:16), genau ein CTA. Methodik: 4-Bausteine-Formel, angewandt auf Reel.

## Methodik

**Kanonische Methodik (Pflicht lesen vor Phase 1):**
- [`references/reel-anatomy.md`](references/reel-anatomy.md) — Hook/Build/Payoff/CTA auf
  Reel, Build-Subtypen, Hook-Muster (Sekunde 0-3), On-Screen-Text, Qualitäts-Checkliste, No-Gos, Länge.

---

## Pfade & Fundament

Dieser Skill kennt **keine hartkodierten Pfade**. Wo gelesen und geschrieben wird, leitest du aus
der Selbstbeschreibung des Projekts ab, genau dafür ist das Markdown-Brain da.

1. **Architektur lesen.** Existiert im Projekt-Root `.agency-os/architecture.md` (die Rolle→Pfad-Map,
   gepflegt vom `agency-os-start`-Skill), diese zuerst lesen — sie sagt dir, wo `context`, `marketing`, `logs` usw.
   liegen, auch wenn die Ordner abweichend benannt sind. Fehlt sie: ersatzweise die Struktur-Quelle
   des Projekts öffnen (`OS.md`, sonst `README.md` oder das Root-`_index.md`) und über die
   `_index.md`-Navigation verstehen, wie das Projekt organisiert ist.
2. **Kontext-Quellen finden** (alle optional, fürs Briefing) aus `{context}/brands/{brand}/` (Fallback
   projektweit): ICP (`icp.md`), Positionierung (`positionierung.md`), Voice-Profile (`voice-profile.md`).
   Was nicht existiert, wird übersprungen.
3. **Ziel-Ordner für das Reel bestimmen.** Im Marketing-/Content-Bereich (`{marketing}`, z.B. `{marketing}/content/reels/`).
   Liegen schon frühere Reels dort, dorthin. Gibt es noch keinen klaren Ort, den nach der Projekt-Logik
   plausibelsten Ordner vorschlagen und **einmal kurz rückversichern**, bevor du schreibst.
4. **Index pflegen.** Entsteht ein neuer Ordner, ihn im zuständigen `_index.md` verlinken.

### Kontext laden (vor Phase 1)

Die in der Ablage gefundenen Kontext-Quellen lesen, falls vorhanden:
- **ICP / Zielgruppe** — wer scrollt, was stoppt den Daumen. Daraus kommen Spannungen, Sprache, Kernproblem.
- **Positionierung / Brand-Substanz** — wofür steht die Marke. Daraus kommt der **Positionierungs-Anker**
  jedes Reels (z.B. der Primär-Archetype, der Diagnose-Winkel). Diese Anker werden **aus dem Profil
  abgeleitet, nicht hier hartkodiert** — so klingt jedes Reel nach der jeweiligen Marke.
- **Voice-Profile** — Stimme, Rhythmus, Stilmerkmale. Auf Skript und Caption anwenden.

**Kernprinzip (markenneutral):** Diagnostizieren, nicht lehren. Die gewünschte Reaktion auf jedes
Reel ist *"Das ist genau meine Situation."* statt *"Guter Tipp."* Lehren = low authority,
Diagnose = high authority. Wie diese Diagnose konkret klingt, kommt aus dem ICP-/Positionierungs-Profil.

Fehlen ICP und Voice-Profile beide: Reel trotzdem planbar, aber am Ende empfehlen, ICP- und
Voice-Profil anzulegen (`/icp`, `/brand-voice`) — Positionierung und Ton leben davon.

---

## Workflow

Sechs Phasen. Stop-Punkte mit User-Entscheidung: **1** (Interview, frageweise), **5** (Approval).
Alles andere läuft automatisch.

### Phase 1: Interview (Pflicht, Stop-Punkt frageweise)

Bevor irgendetwas geschrieben wird, interviewen. Fragen **nacheinander als normalen Chat-Text** —
KEINE Multiple-Choice, KEIN AskUserQuestion-Tool. Freitext-Antworten. Eine Frage, warten, dann die nächste.

Reihenfolge folgt der **Denk-Reihenfolge**, der Hook kommt zuletzt.

**Frage 1 — Payoff:** *"Was soll der Zuschauer nach dem Reel anders machen oder anders denken? Was ist der Shift?"*
→ ableiten: **Do** (handelt anders) oder **Insight** (denkt anders).

**Frage 2 — Build:** *"Wie willst du dahin kommen? Hast du eine Story, einzelne Punkte, oder einen Schritt-für-Schritt-Prozess? Gib mir den Input."*
→ ableiten: **Story**, **List** oder **Steps**.

**Frage 3 — CTA:** *"Was ist der nächste Schritt für den Zuschauer? Wohin soll der CTA führen (in-Video + Caption)?"*
→ z.B. Lead-Magnet, Profil-Link, Kommentar-Trigger ("schreib X"), Folgen, Erstgespräch.

**Frage 4 — Hook:** *"Gibt es einen Satz, ein Bild oder eine Situation für die ersten 3 Sekunden, die das Thema sofort auf den Punkt bringt?"*
→ Kein Hook-Input? OK — der Hook wird in Phase 3 aus fertigem Build + Payoff abgeleitet.

Zusätzlich kurz klären, falls nicht offensichtlich: **Plattform** (Instagram Reel / TikTok / YouTube Short)
und **Format** (Talking-Head, Voiceover über B-Roll, Text-on-Screen ohne Stimme). Steuert Skript-Stil und Länge.

→ Phase 2.

### Phase 2: Story-Context (automatisch, nur bei Build-Subtyp Story)

Bei Build-Subtyp **Story**: echtes Story-Material aus dem Projekt ziehen statt erfinden.
- Existiert ein `/story-context`-Skill (oder eine vergleichbare Story-/Call-Quelle im Projekt),
  mit dem Thema als Query aufrufen und 5-10 passende Stories, Kunden-O-Töne und Erkenntnisse holen.
- Existiert keine solche Quelle: nach echtem Story-Input beim User fragen. **Nichts erfinden.**

Bei **List** oder **Steps**: Phase 2 überspringen → Phase 3.

### Phase 3: Draft schreiben (automatisch)

1. **Voice laden** — `/brand-voice` (oder das gefundene Voice-Profile) anwenden.
2. **Skript in LESE-/SEH-Reihenfolge:** Hook → Build → Payoff → CTA. Struktur und Regeln je Baustein
   stehen in [`references/reel-anatomy.md`](references/reel-anatomy.md). Pro Beat ausgeben:
   - **Gesprochener Text / VO** (was gesagt wird)
   - **On-Screen-Text** (Caption-Overlay, kurz)
   - **Shot/Visual** (was zu sehen ist: Einstellung, B-Roll, Schnitt-Idee)
3. **Caption für den Post** (Hook-Zeile + 1-3 Sätze + CTA + optional Hashtags) aus dem Voice-Profil.
4. Bei fehlender festgelegter CTA-/Caption-Konvention eine schlichte verwenden und beim Approval kurz rückfragen.

### Phase 4: Hook-Varianten + Qualitätscheck (automatisch)

1. **3 Hook-Varianten** für Sekunde 0-3 nach den Mustern in `references/reel-anatomy.md`
   (gesprochene Eröffnungszeile + On-Screen-Text + Visual-Idee). Daumen-Stopp, Zeigarnik, spezifisch.
2. **Variante wählen** — die stärkste Daumen-Stopp-Wirkung, Begründung in 1-2 Sätzen.
3. **Qualitäts-Checkliste** aus `references/reel-anatomy.md` durchgehen.
4. **ICP-Check** mit `/icp` Modus *Bewerten* auf Hook + Payoff + CTA (falls ICP-Profil vorhanden).
   Fail → einmal automatisch nachschärfen (max 1 Iteration).

### Phase 5: Approval (Stop-Punkt)

Komplettes Reel-Skript im Chat ausgeben:
- 3 Hook-Varianten + Begründung der Wahl
- Vollständiges Skript je Beat (Gesprochen / On-Screen-Text / Shot) in Reihenfolge Hook → Build → Payoff → CTA
- Post-Caption
- Geschätzte Länge in Sekunden
- Abschlussfrage: *"Welche Stelle passt noch nicht? Oder 'go' zum Speichern."*

**Iterations-Loop:** Feedback pro Bereich (Hook, Story-Beat, Payoff, CTA, Caption). Nur den
geänderten Bereich neu schreiben, Rest unverändert lassen. **"Go" → Phase 6.**

### Phase 6: Speichern + Log (automatisch)

1. **Datei anlegen** im in der Ablage bestimmten Ordner. Naming-Vorschlag (an die Projekt-Konvention
   anpassen): `{YYYY}-w{KW}-reel{N}-{slug}.md` (slug = kebab-case aus Hook/Thema, max 4 Wörter).
   Frontmatter: Status, geplantes Datum, Plattform, Format, Thema, Payoff-Typ, Build-Typ, CTA. Darunter
   die 3 Hook-Varianten + Begründung und das vollständige Skript + Caption.
2. **Ausgabe an den User:** Link/Pfad zur Datei, plus genutzte Story-Quellen (falls Phase 2).
   Hinweis: Produktion/Schnitt aus Rohmaterial läuft über `/video-studio` (Plugin agency-os-video).
3. **Log** — falls das Projekt ein Tages-/Aktivitäts-Log führt (`{logs}/{YYYY-MM-DD}.md`),
   einen kurzen Eintrag ergänzen: Thema, Payoff-Typ, Build-Typ, CTA, Hook-Wahl, Output-Pfad.

---

## Output

Eine Markdown-Datei im in der Ablage bestimmten Ziel-Ordner (z.B. `{marketing}/content/reels/`),
Naming `{YYYY}-w{KW}-reel{N}-{slug}.md`. Frontmatter (Status, geplantes Datum, Plattform, Format, Thema,
Payoff-Typ, Build-Typ, CTA) + 3 Hook-Varianten mit Begründung + vollständiges Skript (Gesprochen /
On-Screen-Text / Shot pro Beat) + Post-Caption. Kein Rendern/Schnitt (das macht `/video-studio`).
Optional ein Log-Eintrag im Tages-Log.

---

## Verwandte Skills

**Erlaubte Skills im Workflow:**

- `/brand-voice` — Stimme auf Skript + Caption anwenden
- `/icp` Modus *Bewerten* — Hook/Payoff/CTA gegen das ICP testen
- `/story-context` (falls im Projekt vorhanden) — echte Stories + O-Töne (Phase 2)

KEINE anderen spezifischen Content-Skills (z.B. `/linkedin-content`, `/carousel`, `/newsletter-email`).
Gemeinsame Frameworks gehören als Projekt-Note, nicht als Skill-zu-Skill-Aufruf.

**Abgrenzung:**

- **Kein Rendern/Schnitt** — dieser Skill plant nur das Skript. Das fertige Video aus Rohmaterial
  produziert `/video-studio` (Plugin agency-os-video).
- Keine statischen Slides (das ist `/carousel`).
- Keine E-Mail/Newsletter (das ist `/newsletter-email`).
- Keine LinkedIn-/Text-Social-Variante (das ist `/linkedin-content`).
- Ein einzelnes Reel pro Aufruf, keine ganze Serie.

## Hard-Stops

- `references/reel-anatomy.md` fehlt → Skill nicht nutzbar, Hinweis geben.
- Build-Subtyp Story, aber keine echte Story-Quelle und kein User-Input → nicht erfinden, zurückfragen.
- ICP-Check zweimal hintereinander fail → Hook/Payoff/CTA grundsätzlich neu denken statt drüberbügeln.
- User sagt nicht explizit "go"/"passt" → kein Speichern.
