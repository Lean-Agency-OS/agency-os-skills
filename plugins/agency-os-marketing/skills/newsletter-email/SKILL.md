---
name: newsletter-email
version: 1.0.0
description: >
  Schreibt eine versandfertige Newsletter-E-Mail nach der 4-Bausteine-Formel
  (Hook -> Build -> Payoff -> Invitation). Diagnose-Ton statt Lehr-Ton,
  Mid-Funnel-Asset, genau ein CTA. Geführter Workflow: Interview (Payoff ->
  Build -> Invitation -> Hook, eine Frage nach der anderen) -> optional
  Story-Context -> Draft -> 3 Betreffzeilen + Qualitäts-/ICP-Check -> Approval
  -> Speichern + Log. Liest das Voice-/ICP-/Positionierungs-Profil des Projekts,
  falls vorhanden. Triggern bei: "schreib mir einen Newsletter",
  "Newsletter schreiben", "neue Newsletter-Ausgabe", "E-Mail für meine Liste",
  "schreib eine Mail an meine Liste", "Newsletter-Entwurf", "Newsletter optimieren".
---

# Newsletter-E-Mail

Schreibt **eine** Newsletter-E-Mail pro Aufruf, fertig zum Versand. Diagnose-Ton (nicht
Lehr-Ton), Mid-Funnel-Asset, genau ein CTA. Methodik: 4-Bausteine-Formel, angewandt auf E-Mail.

## Methodik

**Kanonische Methodik (Pflicht lesen vor Phase 1):**
- [`references/email-anatomy.md`](references/email-anatomy.md) — Hook/Build/Payoff/Invitation auf
  E-Mail, Build-Subtypen, Betreffzeilen-Muster, Qualitäts-Checkliste, No-Gos, Länge.

Existiert im Projekt eine eigene 4-Bausteine-Quelle (z.B. eine IP-Note `4-bausteine-formel.md`),
hat die zusätzlich Vorrang für die Marken-Substanz.

---

## Pfade & Fundament

Dieser Skill kennt **keine hartkodierten Pfade**. Wo gelesen und geschrieben wird, leitest du aus
der Selbstbeschreibung des Projekts ab, genau dafür ist das Markdown-Brain da.

1. **Struktur-Quelle lesen.** Im Projekt-Root die Quelle der Wahrheit für die Struktur öffnen
   (`OS.md`, ersatzweise `README.md` oder das Root-`_index.md`) und über die `_index.md`-Navigation
   verstehen, wie das Projekt organisiert ist.
2. **Kontext-Quellen finden** (alle optional, fürs Briefing) aus `{context}/brands/{brand}/`
   (Fallback projektweit): ICP (`icp.md`), Positionierung (`positionierung.md`),
   Voice-Profile (`voice-profile.md`). Was nicht existiert, wird übersprungen.
3. **Ziel-Ordner für die Mail bestimmen.** Den Ort wählen, an dem E-Mail-Kampagnen liegen oder
   thematisch hingehören. Im Marketing-/Content-Bereich (`{marketing}`, z.B. `{marketing}/content/email/kampagnen/`). Liegen
   schon frühere Kampagnen dort, dorthin. Gibt es noch keinen klaren Ort, den nach der
   Projekt-Logik plausibelsten Ordner vorschlagen und **einmal kurz rückversichern**, bevor du schreibst.
4. **Index pflegen.** Entsteht ein neuer Ordner, ihn im zuständigen `_index.md` verlinken.

### Kontext laden (vor Phase 1)

Die in der Ablage gefundenen Kontext-Quellen lesen, falls vorhanden:
- **ICP / Zielgruppe** — wer liest, was packt ihn. Daraus kommen Spannungen, Sprache, Kernproblem.
- **Positionierung / Brand-Substanz** — wofür steht die Marke. Daraus kommt der **Positionierungs-Anker**
  jeder Mail (z.B. der Primär-Archetype, der Diagnose-Winkel, die Test-Reaktion). Diese Anker werden
  **aus dem Profil abgeleitet, nicht hier hartkodiert** — so klingt jede Mail nach der jeweiligen Marke.
- **Voice-Profile** — Stimme, Rhythmus, Stilmerkmale. Auf alle Texte anwenden.

**Kernprinzip (markenneutral):** Diagnostizieren, nicht lehren. Die gewünschte Reaktion auf jede
Mail ist *"Das ist genau meine Situation."* statt *"Guter Tipp."* Lehren = low authority,
Diagnose = high authority. Wie diese Diagnose konkret klingt, kommt aus dem ICP-/Positionierungs-Profil.

Fehlen ICP und Voice-Profile beide: Mail trotzdem schreibbar, aber am Ende empfehlen, ICP- und
Voice-Profil anzulegen (`/icp`, `/brand-voice`) — Positionierung und Ton leben davon.

---

## Workflow

Sechs Phasen. Stop-Punkte mit User-Entscheidung: **1** (Interview, frageweise), **4** (Betreffzeilen
sind Teil von Phase 5), **5** (Approval). Alles andere läuft automatisch.

### Phase 1: Interview (Pflicht, Stop-Punkt frageweise)

Bevor irgendetwas geschrieben wird, interviewen. Fragen **nacheinander als normalen Chat-Text** —
KEINE Multiple-Choice, KEIN AskUserQuestion-Tool. Freitext-Antworten. Eine Frage, warten, dann die nächste.

Reihenfolge folgt der **Denk-Reihenfolge**, der Hook kommt zuletzt.

**Frage 1 — Payoff:** *"Was soll der Leser nach dem Lesen anders machen oder anders denken? Was ist der Shift?"*
→ ableiten: **Do** (handelt anders) oder **Insight** (denkt anders).

**Frage 2 — Build:** *"Wie willst du dahin kommen? Hast du eine Story, einzelne Punkte, oder einen Schritt-für-Schritt-Prozess? Gib mir den Input."*
→ ableiten: **Story**, **List** oder **Steps**.

**Frage 3 — Invitation:** *"Was ist der nächste Schritt für den Leser? Wohin soll der CTA führen?"*
→ z.B. Lead-Magnet, Workshop, Antwort-CTA, Erstgespräch, Blogartikel.

**Frage 4 — Hook:** *"Gibt es ein Wort, ein Bild oder eine Situation, die das Thema auf den Punkt bringt?"*
→ Kein Hook-Input? OK — der Hook wird in Phase 3 aus fertigem Build + Payoff abgeleitet.

→ Phase 2.

### Phase 2: Story-Context (automatisch, nur bei Build-Subtyp Story)

Bei Build-Subtyp **Story**: echtes Story-Material aus dem Projekt ziehen statt erfinden.
- Existiert ein `/story-context`-Skill (oder eine vergleichbare Story-/Call-Quelle im Projekt),
  mit dem Thema als Query aufrufen und 5-10 passende Stories, Kunden-O-Töne und Erkenntnisse holen.
- Existiert keine solche Quelle: nach echtem Story-Input beim User fragen. **Nichts erfinden.**

Bei **List** oder **Steps**: Phase 2 überspringen → Phase 3.

### Phase 3: Draft schreiben (automatisch)

1. **Voice laden** — `/brand-voice` (oder das gefundene Voice-Profile) anwenden.
2. **Body in LESE-Reihenfolge:** Hook → Build → Payoff → Invitation. Struktur und Regeln je Baustein
   stehen in [`references/email-anatomy.md`](references/email-anatomy.md).
3. **Signatur** aus dem Voice-/Brand-Profil verwenden (Abbinder + Name). Existiert keine festgelegte
   Signatur, eine schlichte verwenden und beim Approval kurz rückfragen.

### Phase 4: Betreffzeilen + Qualitätscheck (automatisch)

1. **3 Betreffzeilen-Varianten** nach den Mustern in `references/email-anatomy.md` (40-60 Zeichen,
   klar vor clever, spezifisch) + je ein **Vorschautext**.
2. **Variante wählen** — die klarste + spezifischste, Begründung in 1-2 Sätzen.
3. **Qualitäts-Checkliste** aus `references/email-anatomy.md` durchgehen.
4. **ICP-Check** mit `/icp` Modus *Bewerten* auf Hook + Payoff + CTA (falls ICP-Profil vorhanden).
   Fail → einmal automatisch nachschärfen (max 1 Iteration).

### Phase 5: Approval (Stop-Punkt)

Komplette Mail im Chat ausgeben:
- 3 Betreffzeilen-Varianten (je mit Vorschautext) + Begründung der Wahl
- Vollständiger Body (Hook → Build → Payoff → Invitation + Signatur)
- Abschlussfrage: *"Welche Stelle passt noch nicht? Oder 'go' zum Speichern."*

**Iterations-Loop:** Feedback pro Bereich (Betreff, Hook, Story-Beat, Payoff, CTA). Nur den
geänderten Bereich neu schreiben, Rest unverändert lassen. **"Go" → Phase 6.**

### Phase 6: Speichern + Log (automatisch)

1. **Datei anlegen** im in der Ablage bestimmten Ordner. Naming-Vorschlag (an die Projekt-Konvention
   anpassen): `{YYYY}-w{KW}-nl{N}-{slug}.md` (slug = kebab-case aus Betreff/Thema, max 4 Wörter).
   Frontmatter: Status, Versand-Datum, Thema, Payoff-Typ, Build-Typ, CTA. Darunter die 3
   Betreff-Varianten + Begründung und die vollständige Mail.
2. **Ausgabe an den User:** Link/Pfad zur Datei, plus genutzte Story-Quellen (falls Phase 2).
3. **Log** — falls das Projekt ein Tages-/Aktivitäts-Log führt (`{logs}/{YYYY-MM-DD}.md`),
   einen kurzen Eintrag ergänzen: Thema, Payoff-Typ, Build-Typ, CTA, Betreff-Wahl, Output-Pfad.

---

## Output

Eine Markdown-Datei im in der Ablage bestimmten Ziel-Ordner (z.B. `{marketing}/content/email/kampagnen/`),
Naming `{YYYY}-w{KW}-nl{N}-{slug}.md`. Frontmatter (Status, Versand-Datum, Thema, Payoff-Typ, Build-Typ, CTA)
+ 3 Betreff-Varianten mit Begründung + vollständige Mail. Kein Versand. Optional ein Log-Eintrag im
Tages-Log.

---

## Verwandte Skills

**Erlaubte Skills im Workflow:**

- `/brand-voice` — Stimme auf alle Texte anwenden
- `/icp` Modus *Bewerten* — Hook/Payoff/CTA gegen das ICP testen
- `/story-context` (falls im Projekt vorhanden) — echte Stories + O-Töne (Phase 2)

KEINE anderen spezifischen Content-Skills (z.B. `/linkedin-content`, `/carousel`). Gemeinsame
Frameworks gehören als Projekt-Note, nicht als Skill-zu-Skill-Aufruf.

**Abgrenzung:**

- Kein Versand — die fertige Mail versendet der User manuell über sein ESP.
- Kein Cold-Email (anderer Use-Case, kalte Outreach).
- Keine mehrteilige Sequenz/Drip — eine einzelne Newsletter-Mail pro Aufruf.
- Keine LinkedIn-/Social-Variante (das ist `/linkedin-content` bzw. `/carousel`).

## Hard-Stops

- `references/email-anatomy.md` fehlt → Skill nicht nutzbar, Hinweis geben.
- Build-Subtyp Story, aber keine echte Story-Quelle und kein User-Input → nicht erfinden, zurückfragen.
- ICP-Check zweimal hintereinander fail → Hook/Payoff/CTA grundsätzlich neu denken statt drüberbügeln.
- User sagt nicht explizit "go"/"passt" → kein Speichern.
