---
name: reel-skript
version: 2.1.0
description: >
  Plant ein Reel/Short als Bullet-Point-Skript nach der 4-Bausteine-Formel
  (Hook -> Build -> Payoff -> CTA), in zwei Modi. Modus Skript (Standard):
  Interview (Payoff -> Build -> CTA -> Hook, eine Frage nach der anderen) ->
  Bullet Points in genau vier Bereichen, beim Hook je 3 Vorschläge für den
  gesprochenen und den On-Screen-Hook ->
  Qualitäts-/ICP-Check (immer) -> Approval -> Speichern + Log. Modus Regie
  (optional, zweiter Schritt auf Nachfrage): Shot-Regie, B-Roll-Ideen und
  Schnitt-Hinweise, ergänzt in derselben Datei.
  Diagnose-Ton statt Lehr-Ton, kurzes Vertical-Video-Asset, genau ein CTA.
  Liest das Voice-/ICP-/Positionierungs-Profil des Projekts, falls vorhanden.
  Plant nur (kein Rendern, das macht video-shortform). Triggern bei: "plan mir ein Reel",
  "Reel planen", "Reel-Skript", "Reel-Idee", "Reel-Konzept", "Short planen",
  "Instagram Reel", "TikTok-Video planen", "YouTube Short planen", "Reel optimieren",
  "/reel-skript".
---

# Reel-Skript

Du schreibst als **Senior Short-Form-Creator**: du denkst in den ersten 3 Sekunden und im Daumenstopp. Jede Sekunde kämpft gegen das Weiterwischen. **Dein Ziel:** Reichweite über die eigene Bubble hinaus, die neue passende Zuschauer bringt.

Plant **ein** Reel/Short pro Aufruf. Diagnose-Ton (nicht Lehr-Ton), kurzes Vertical-Asset (9:16),
genau ein CTA. Methodik: 4-Bausteine-Formel, angewandt auf Reel.

## Zwei Modi

- **Skript (Standard):** Interview, dann Bullet-Point-Skript in genau vier Bereichen
  (Hook / Build / Payoff / CTA). **Kein ausformuliertes Wort-für-Wort-Skript:** die Bullets
  sind Sprech-Anker, ausformuliert wird beim Dreh.
- **Regie (optional, zweiter Schritt):** vertieft das gespeicherte Bullet-Skript visuell:
  Shot-Regie, B-Roll-Ideen, Schnitt-Hinweise. Wird nach dem Speichern einmal aktiv angeboten
  und läuft nur, wenn der User es will (Phase 7).

## Methodik

**Kanonische Methodik (Pflicht lesen vor Phase 1):**
- [`references/reel-anatomy.md`](references/reel-anatomy.md): Hook/Build/Payoff/CTA auf
  Reel, Build-Subtypen, Hook-Muster (Sekunde 0-3), On-Screen-Text, Qualitäts-Checkliste, No-Gos, Länge.

---

## Pfade & Fundament

Dieser Skill kennt **keine hartkodierten Pfade**. Wo gelesen und geschrieben wird, leitest du aus
der Selbstbeschreibung des Projekts ab, genau dafür ist das Markdown-Brain da.

1. **Architektur lesen.** Existiert im Projekt-Root `.agency-os/architecture.md` (die Rolle→Pfad-Map,
   gepflegt vom `agency-os-start`-Skill), diese zuerst lesen: sie sagt dir, wo `context`, `marketing`, `logs` usw.
   liegen, auch wenn die Ordner abweichend benannt sind. Fehlt sie: ersatzweise die Struktur-Quelle
   des Projekts öffnen (`OS.md`, sonst `README.md` oder das Root-`_index.md`) und über die
   `_index.md`-Navigation verstehen, wie das Projekt organisiert ist.
2. **Kontext-Quellen finden** (alle optional, fürs Briefing): Zielgruppe/ICP (`{context}/zielgruppe.md`),
   Positionierung (`{context}/positionierung.md`), Voice-Profile (`{context}/brand/voice-profile.md`).
   Was nicht existiert, wird übersprungen.
3. **Ziel-Ordner für das Reel bestimmen.** Im Marketing-/Content-Bereich (`{marketing}`, z.B. `{marketing}/content/reels/`).
   Liegen schon frühere Reels dort, dorthin. Gibt es noch keinen klaren Ort, den nach der Projekt-Logik
   plausibelsten Ordner vorschlagen und **einmal kurz rückversichern**, bevor du schreibst.
4. **Index pflegen.** Entsteht ein neuer Ordner, ihn im zuständigen `_index.md` verlinken.

### Kontext laden (vor Phase 1)

Die in der Ablage gefundenen Kontext-Quellen lesen, falls vorhanden:
- **ICP / Zielgruppe:** wer scrollt, was stoppt den Daumen. Daraus kommen Spannungen, Sprache, Kernproblem.
- **Positionierung / Brand-Substanz:** wofür steht die Marke. Daraus kommt der **Positionierungs-Anker**
  jedes Reels (z.B. der Primär-Archetype, der Diagnose-Winkel). Diese Anker werden **aus dem Profil
  abgeleitet, nicht hier hartkodiert**, so klingt jedes Reel nach der jeweiligen Marke.
- **Voice-Profile:** Stimme, Rhythmus, Stilmerkmale. Auf Skript und Caption anwenden.

**Kernprinzip (markenneutral):** Diagnostizieren, nicht lehren. Die gewünschte Reaktion auf jedes
Reel ist *"Das ist genau meine Situation."* statt *"Guter Tipp."* Lehren = low authority,
Diagnose = high authority. Wie diese Diagnose konkret klingt, kommt aus dem ICP-/Positionierungs-Profil.

Fehlen ICP und Voice-Profile beide: Reel trotzdem planbar, aber am Ende empfehlen, ICP- und
Voice-Profil anzulegen (`/icp`, `/brand-voice`): Positionierung und Ton leben davon.

---

## Workflow

Sieben Phasen. Phasen 1-6 sind der Modus **Skript**, Phase 7 ist der Modus **Regie** (optional).
Stop-Punkte mit User-Entscheidung: **1** (Interview, frageweise), **5** (Approval), **7** (nur auf
Nachfrage). Alles andere läuft automatisch.

### Phase 1: Interview (Pflicht, Stop-Punkt frageweise)

Bevor irgendetwas geschrieben wird, interviewen. Fragen **nacheinander als normalen Chat-Text**:
KEINE Multiple-Choice, KEIN AskUserQuestion-Tool. Freitext-Antworten. Eine Frage, warten, dann die nächste.

Reihenfolge folgt der **Denk-Reihenfolge**, der Hook kommt zuletzt.

**Frage 1 - Payoff:** *"Was soll der Zuschauer nach dem Reel anders machen oder anders denken? Was ist der Shift?"*
→ ableiten: **Do** (handelt anders) oder **Insight** (denkt anders).

**Frage 2 - Build:** *"Wie willst du dahin kommen? Hast du eine Story, einzelne Punkte, oder einen Schritt-für-Schritt-Prozess? Gib mir den Input."*
→ ableiten: **Story**, **List** oder **Steps**.

**Frage 3 - CTA:** *"Was ist der nächste Schritt für den Zuschauer? Wohin soll der CTA führen?"*
→ z.B. Lead-Magnet, Profil-Link, Kommentar-Trigger ("schreib X"), Folgen, Erstgespräch.

**Frage 4 - Hook:** *"Gibt es einen Satz, ein Bild oder eine Situation für die ersten 3 Sekunden, die das Thema sofort auf den Punkt bringt?"*
→ Kein Hook-Input? OK, der Hook wird in Phase 3 aus fertigem Build + Payoff abgeleitet.

Zusätzlich kurz klären, falls nicht offensichtlich: **Plattform** (Instagram Reel / TikTok / YouTube Short)
und **Format** (Talking-Head, Voiceover über B-Roll, Text-on-Screen ohne Stimme). Steuert Skript-Stil und Länge.

→ Phase 2.

### Phase 2: Story-Material (nur bei Build-Subtyp Story)

Bei Build-Subtyp **Story**: echtes Story-Material verwenden statt erfinden. Nach echtem
Story-Input beim User fragen. **Nichts erfinden.**

Bei **List** oder **Steps**: Phase 2 überspringen → Phase 3.

### Phase 3: Bullet-Skript schreiben (automatisch)

1. **Voice laden:** `/brand-voice` (oder das gefundene Voice-Profile) anwenden.
2. **Bullet-Skript in LESE-/SEH-Reihenfolge**, genau vier Bereiche: Hook → Build → Payoff → CTA.
   Regeln je Baustein stehen in [`references/reel-anatomy.md`](references/reel-anatomy.md).
   **Kein ausformuliertes Skript:** pro Bereich Bullet Points als Sprech-Anker.
   - **Hook (3 Ebenen):** 3 Vorschläge **gesprochener Hook** (nach den Hook-Mustern der Anatomy,
     Daumen-Stopp, Zeigarnik, spezifisch) + 3 Vorschläge **On-Screen-Hook** (3-5 Wörter, bleibt
     die ersten Sekunden im Bild). Gesprochen und On-Screen greifen ineinander, nicht doppelt
     dasselbe. **Visueller Hook** nur, wenn das Format ihn hergibt (bei Talking-Head oft nicht):
     dann 1-3 Bild-Ideen, sonst explizit weglassen.
   - **Build / Payoff / CTA:** Bullets aus dem Interview-Material (Phase 1/2), ein Gedanke pro
     Bullet, in Sprech-Reihenfolge. Nichts dazuerfinden, was im Interview nicht vorkam.

Der Output besteht ausschließlich aus diesen vier Bereichen. Keine Post-Caption.

### Phase 4: Qualitäts- + ICP-Check (automatisch, läuft immer)

1. **Qualitäts-Checkliste** aus `references/reel-anatomy.md` durchgehen (auf Bullets und
   Hook-Vorschläge angewandt).
2. **ICP-Check** mit `/icp` Modus *Bewerten* auf alle Hook-Vorschläge + Payoff + CTA (falls
   ICP-Profil vorhanden). Fail → einmal automatisch nachschärfen (max 1 Iteration).

Es wird nie ein ungecheckter Output ausgegeben.

### Phase 5: Approval (Stop-Punkt)

Komplettes Bullet-Skript im Chat ausgeben, genau vier Bereiche:
- **Hook:** 3 Vorschläge gesprochener Hook + 3 Vorschläge On-Screen-Hook (+ visuelle Hook-Ideen,
  falls sinnvoll)
- **Build / Payoff / CTA:** je als Bullet Points
- Geschätzte Länge in Sekunden
- Abschlussfrage: *"Welche Stelle passt noch nicht? Oder 'go' zum Speichern."*

**Iterations-Loop:** Feedback pro Bereich (Hook, Build, Payoff, CTA). Nur den
geänderten Bereich neu schreiben, Rest unverändert lassen. **"Go" → Phase 6.**

### Phase 6: Speichern + Log (automatisch)

1. **Datei anlegen** im in der Ablage bestimmten Ordner. Naming-Vorschlag (an die Projekt-Konvention
   anpassen): `{YYYY}-w{KW}-reel{N}-{slug}.md` (slug = kebab-case aus Hook/Thema, max 4 Wörter).
   Frontmatter: Status, geplantes Datum, Plattform, Format, Thema, Payoff-Typ, Build-Typ, CTA. Darunter
   das Bullet-Skript in den vier Bereichen (Hook mit den 3+3 Vorschlägen).
2. **Ausgabe an den User:** Link/Pfad zur Datei, plus genutzte Story-Quellen (falls Phase 2).
   Hinweis: Produktion/Schnitt aus Rohmaterial läuft über `/video-shortform` (Plugin agency-os-video).
3. **Log:** falls das Projekt ein Tages-/Aktivitäts-Log führt (`{logs}/{YYYY-MM-DD}.md`),
   einen kurzen Eintrag ergänzen: Thema, Payoff-Typ, Build-Typ, CTA, Output-Pfad.
4. **Regie anbieten:** einmal kurz fragen: *"Willst du noch in die Regie gehen (Shots, B-Roll,
   Schnitt-Ideen)?"* Ja → Phase 7. Nein → fertig.

### Phase 7: Regie (optional, nur auf Nachfrage)

Vertieft das gespeicherte Bullet-Skript visuell, Bereich für Bereich entlang der Bullets:

- **Shot/Einstellung** je Beat (Talking-Head, Perspektive, Location, Wechsel)
- **B-Roll-Ideen** dort, wo sie einen Bullet verstärken
- **Schnitt-Hinweise** (Cut-Rhythmus, Pattern-Interrupt, Tempo)

Ergebnis im Chat zeigen, Feedback-Loop wie in Phase 5. **"Go"** → Regie-Block als Abschnitt
`## Regie` in derselben Datei ergänzen (keine neue Datei), Log-Eintrag um "Regie ergänzt" erweitern.

---

## Output

Eine Markdown-Datei im in der Ablage bestimmten Ziel-Ordner (z.B. `{marketing}/content/reels/`),
Naming `{YYYY}-w{KW}-reel{N}-{slug}.md`. Frontmatter (Status, geplantes Datum, Plattform, Format, Thema,
Payoff-Typ, Build-Typ, CTA) + Bullet-Skript in genau vier Bereichen: Hook (3 gesprochene + 3
On-Screen-Vorschläge, optional visuelle Hook-Ideen), Build, Payoff, CTA. Keine Post-Caption. Nach
Phase 7 zusätzlich ein Abschnitt `## Regie` (Shots, B-Roll, Schnitt-Hinweise) in derselben Datei.
Kein Rendern/Schnitt (das macht `/video-shortform`). Optional ein Log-Eintrag im Tages-Log.

---

## Verwandte Skills

**Erlaubte Skills im Workflow:**

- `/brand-voice`: Stimme auf Bullets und Hook-Vorschläge anwenden
- `/icp` Modus *Bewerten*: Hooks/Payoff/CTA gegen das ICP testen

KEINE anderen spezifischen Content-Skills (z.B. `/linkedin-caption`, `/carousel`, `/newsletter-email`).
Gemeinsame Frameworks gehören als Projekt-Note, nicht als Skill-zu-Skill-Aufruf.

**Abgrenzung:**

- **Kein Rendern/Schnitt:** dieser Skill plant nur das Skript. Das fertige Video aus Rohmaterial
  produziert `/video-shortform` (Plugin agency-os-video).
- Keine Post-Caption: der Skill liefert nur das Bullet-Skript.
- Keine statischen Slides (das ist `/carousel`).
- Keine E-Mail/Newsletter (das ist `/newsletter-email`).
- Keine LinkedIn-/Text-Social-Variante (das ist `/linkedin-caption`).
- Ein einzelnes Reel pro Aufruf, keine ganze Serie.

## Hard-Stops

- `references/reel-anatomy.md` fehlt → Skill nicht nutzbar, Hinweis geben.
- Build-Subtyp Story, aber keine echte Story-Quelle und kein User-Input → nicht erfinden, zurückfragen.
- ICP-Check zweimal hintereinander fail → Hook/Payoff/CTA grundsätzlich neu denken statt drüberbügeln.
- User sagt nicht explizit "go"/"passt" → kein Speichern.
