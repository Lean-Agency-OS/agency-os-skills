---
name: linkedin-caption
version: 1.0.0
description: >
  Schreibt einen versandfertigen LinkedIn-Post-Text (Caption) zu einem bestehenden
  Asset (Bild, Dokument/PDF, Grafik, Video) nach der 4-Bausteine-Formel
  (Hook -> Build -> Payoff -> CTA). Diagnose-Ton statt Lehr-Ton, genau ein CTA.
  Geführter Workflow: Interview (Asset -> Payoff -> Build -> CTA -> Hook, eine
  Frage nach der anderen) -> optional Story-Context -> Draft (Post-Text +
  Hashtags) -> 3 Hook-Varianten + Qualitäts-/ICP-Check -> Approval -> Speichern + Log.
  Liest das Voice-/ICP-/Positionierungs-Profil des Projekts, falls vorhanden.
  Triggern bei: "schreib mir eine LinkedIn-Caption", "LinkedIn-Text zum Post",
  "LinkedIn-Caption", "Text für meinen LinkedIn-Post", "Caption für das LinkedIn-Bild",
  "LinkedIn-Post-Text", "LinkedIn-Caption optimieren".
---

# LinkedIn-Caption

Schreibt **einen** LinkedIn-Post-Text pro Aufruf zu einem bereits vorhandenen Asset (Bild, Dokument,
Grafik, Video). Diagnose-Ton (nicht Lehr-Ton), genau ein CTA. Methodik: 4-Bausteine-Formel, angewandt auf den LinkedIn-Text.

## Methodik

**Kanonische Methodik (Pflicht lesen vor Phase 1):**
- [`references/caption-anatomy.md`](references/caption-anatomy.md) — Hook/Build/Payoff/CTA auf den
  LinkedIn-Text, Build-Subtypen, Hook-Muster (Truncation nach 2-3 Zeilen), Hashtags, Qualitäts-Checkliste, No-Gos, Länge.

---

## Pfade & Fundament

Dieser Skill kennt **keine hartkodierten Pfade**. Wo gelesen und geschrieben wird, leitest du aus
der Selbstbeschreibung des Projekts ab, genau dafür ist das Markdown-Brain da.

1. **Architektur lesen.** Existiert im Projekt-Root `.agency-os/architecture.md` (die Rolle→Pfad-Map,
   gepflegt vom `agency-os-start`-Skill), diese zuerst lesen — sie sagt dir, wo `context`, `marketing`, `logs` usw.
   liegen, auch wenn die Ordner abweichend benannt sind. Fehlt sie: ersatzweise die Struktur-Quelle
   des Projekts öffnen (`OS.md`, sonst `README.md` oder das Root-`_index.md`) und über die
   `_index.md`-Navigation verstehen, wie das Projekt organisiert ist.
2. **Kontext-Quellen finden** (alle optional, fürs Briefing) aus `{context}/brands/{brand}/`
   (Fallback projektweit): ICP (`icp.md`), Positionierung (`positionierung.md`),
   Voice-Profile (`voice-profile.md`). Was nicht existiert, wird übersprungen.
3. **Ziel-Ordner für den Post bestimmen.** Den Ort wählen, an dem Social-Content/LinkedIn-Posts liegen
   oder thematisch hingehören. Im Marketing-/Content-Bereich (`{marketing}`, z.B. `{marketing}/content/linkedin/`). Liegen schon
   frühere Posts dort, dorthin. Gibt es noch keinen klaren Ort, den nach der Projekt-Logik
   plausibelsten Ordner vorschlagen und **einmal kurz rückversichern**, bevor du schreibst.
4. **Index pflegen.** Entsteht ein neuer Ordner, ihn im zuständigen `_index.md` verlinken.

### Kontext laden (vor Phase 1)

Die in der Ablage gefundenen Kontext-Quellen lesen, falls vorhanden:
- **ICP / Zielgruppe** — wer liest, was packt ihn beruflich. Daraus kommen Spannungen, Sprache, Kernproblem.
- **Positionierung / Brand-Substanz** — wofür steht die Marke. Daraus kommt der **Positionierungs-Anker**
  jedes Posts. Diese Anker werden **aus dem Profil abgeleitet, nicht hier hartkodiert** — so klingt jeder
  Post nach der jeweiligen Marke.
- **Voice-Profile** — Stimme, Rhythmus, Stilmerkmale. Auf den ganzen Text anwenden.

**Kernprinzip (markenneutral):** Diagnostizieren, nicht lehren. Die gewünschte Reaktion ist
*"Das ist genau meine Situation."* statt *"Guter Tipp."* Lehren = low authority, Diagnose = high authority.
Wie diese Diagnose konkret klingt, kommt aus dem ICP-/Positionierungs-Profil.

Fehlen ICP und Voice-Profile beide: Post trotzdem schreibbar, aber am Ende empfehlen, ICP- und
Voice-Profil anzulegen (`/icp`, `/brand-voice`) — Positionierung und Ton leben davon.

---

## Workflow

Sechs Phasen. Stop-Punkte mit User-Entscheidung: **1** (Interview, frageweise), **5** (Approval).
Alles andere läuft automatisch.

### Phase 1: Interview (Pflicht, Stop-Punkt frageweise)

Bevor irgendetwas geschrieben wird, interviewen. Fragen **nacheinander als normalen Chat-Text** —
KEINE Multiple-Choice, KEIN AskUserQuestion-Tool. Freitext-Antworten. Eine Frage, warten, dann die nächste.

**Frage 0 — Asset:** *"Was ist das Asset (Bild, Dokument/PDF, Grafik, Video) und was ist darauf zu sehen? Worum geht's im Post?"*
→ Der Text begleitet das Asset, er wiederholt es nicht, er liefert den Gedanken dahinter.

Danach die 4 Bausteine in **Denk-Reihenfolge** (Hook zuletzt):

**Frage 1 — Payoff:** *"Was soll der Leser nach dem Lesen anders machen oder anders denken? Was ist der Shift?"*
→ ableiten: **Do** (handelt anders) oder **Insight** (denkt anders).

**Frage 2 — Build:** *"Wie willst du dahin kommen? Story, einzelne Punkte, oder ein kurzer Prozess? Gib mir den Input."*
→ ableiten: **Story**, **List** oder **Steps**.

**Frage 3 — CTA:** *"Was ist der nächste Schritt? Wohin soll der CTA führen (z.B. Kommentar-Trigger, Repost, DM, Link im ersten Kommentar)?"*

**Frage 4 — Hook:** *"Gibt es einen Satz oder eine Situation, die die ersten zwei Zeilen auf den Punkt bringt?"*
→ Kein Hook-Input? OK — der Hook wird in Phase 3 aus fertigem Build + Payoff abgeleitet.

→ Phase 2.

### Phase 2: Story-Context (automatisch, nur bei Build-Subtyp Story)

Bei Build-Subtyp **Story**: echtes Story-Material aus dem Projekt ziehen statt erfinden.
- Existiert ein `/story-context`-Skill (oder eine vergleichbare Story-/Call-Quelle im Projekt),
  mit dem Thema als Query aufrufen und passende Stories, Kunden-O-Töne und Erkenntnisse holen.
- Existiert keine solche Quelle: nach echtem Story-Input beim User fragen. **Nichts erfinden.**

Bei **List** oder **Steps**: Phase 2 überspringen → Phase 3.

### Phase 3: Draft schreiben (automatisch)

1. **Voice laden** — `/brand-voice` (oder das gefundene Voice-Profile) anwenden.
2. **Post-Text in LESE-Reihenfolge:** Hook (erste 1-2 Zeilen) → Build → Payoff → CTA. Struktur und
   Regeln je Baustein stehen in [`references/caption-anatomy.md`](references/caption-anatomy.md).
   LinkedIn bricht nach 2-3 Zeilen mit "… mehr" um — der Hook muss davor zünden. Viel Whitespace,
   kurze Zeilen.
3. **Hashtags** nach den Regeln in `references/caption-anatomy.md` (3-5, themen-/nischenspezifisch).

### Phase 4: Hook-Varianten + Qualitätscheck (automatisch)

1. **3 Hook-Varianten** (erste 1-2 Zeilen) nach den Mustern in `references/caption-anatomy.md`
   (Daumen-Stopp, Zeigarnik, spezifisch, lesbar vor der Truncation).
2. **Variante wählen** — die stärkste Wirkung, Begründung in 1-2 Sätzen.
3. **Qualitäts-Checkliste** aus `references/caption-anatomy.md` durchgehen.
4. **ICP-Check** mit `/icp` Modus *Bewerten* auf Hook + Payoff + CTA (falls ICP-Profil vorhanden).
   Fail → einmal automatisch nachschärfen (max 1 Iteration).

### Phase 5: Approval (Stop-Punkt)

Kompletten Post-Text im Chat ausgeben:
- 3 Hook-Varianten + Begründung der Wahl
- Vollständiger Post-Text (Hook → Build → Payoff → CTA)
- Hashtags
- Abschlussfrage: *"Welche Stelle passt noch nicht? Oder 'go' zum Speichern."*

**Iterations-Loop:** Feedback pro Bereich (Hook, Build, Payoff, CTA, Hashtags). Nur den geänderten
Bereich neu schreiben, Rest unverändert lassen. **"Go" → Phase 6.**

### Phase 6: Speichern + Log (automatisch)

1. **Datei anlegen** im in der Ablage bestimmten Ordner. Naming-Vorschlag (an die Projekt-Konvention
   anpassen): `{YYYY}-w{KW}-li{N}-{slug}.md` (slug = kebab-case aus Hook/Thema, max 4 Wörter).
   Frontmatter: Status, geplantes Datum, Asset-Typ, Thema, Payoff-Typ, Build-Typ, CTA. Darunter die
   3 Hook-Varianten + Begründung, der vollständige Post-Text und die Hashtags.
2. **Ausgabe an den User:** Link/Pfad zur Datei, plus genutzte Story-Quellen (falls Phase 2).
3. **Log** — falls das Projekt ein Tages-/Aktivitäts-Log führt (`{logs}/{YYYY-MM-DD}.md`),
   einen kurzen Eintrag ergänzen: Thema, Payoff-Typ, Build-Typ, CTA, Hook-Wahl, Output-Pfad.

---

## Output

Eine Markdown-Datei im in der Ablage bestimmten Ziel-Ordner (z.B. `{marketing}/content/linkedin/`),
Naming `{YYYY}-w{KW}-li{N}-{slug}.md`. Frontmatter (Status, geplantes Datum, Asset-Typ, Thema, Payoff-Typ,
Build-Typ, CTA) + 3 Hook-Varianten mit Begründung + vollständiger Post-Text + Hashtags. Erstellt kein
Bild/Video/Dokument. Optional ein Log-Eintrag im Tages-Log.

---

## Verwandte Skills

**Erlaubte Skills im Workflow:**

- `/brand-voice` — Stimme auf den Text anwenden
- `/icp` Modus *Bewerten* — Hook/Payoff/CTA gegen das ICP testen
- `/story-context` (falls im Projekt vorhanden) — echte Stories + O-Töne (Phase 2)

KEINE anderen spezifischen Content-Skills. Gemeinsame Frameworks gehören als Projekt-Note,
nicht als Skill-zu-Skill-Aufruf.

**Abgrenzung:**

- **Schreibt nur den Post-Text** zu einem bestehenden Asset — erstellt kein Bild/Video/Dokument.
- Keine Instagram-Caption (`/instagram-caption`), kein Newsletter (`/newsletter-email`),
  kein Reel-Skript (`/reel-skript`), kein Carousel (`/carousel`).
- Ein einzelner Post pro Aufruf, keine Serie.

## Hard-Stops

- `references/caption-anatomy.md` fehlt → Skill nicht nutzbar, Hinweis geben.
- Build-Subtyp Story, aber keine echte Story-Quelle und kein User-Input → nicht erfinden, zurückfragen.
- ICP-Check zweimal hintereinander fail → Hook/Payoff/CTA grundsätzlich neu denken statt drüberbügeln.
- User sagt nicht explizit "go"/"passt" → kein Speichern.
