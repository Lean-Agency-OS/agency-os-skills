---
name: instagram-story
version: 1.0.0
description: >
  Plant Instagram-Stories als Frame-für-Frame-Drehplan (Bullets, kein Rendern, gebaut wird in
  der IG-App), in zwei Modi. Modus Bewerben: nimmt ein bestehendes Content-Asset (Reel, Carousel)
  und baut einen Teaser-Story-Bogen mit Open Loop, der auf den Post zieht, ohne den Payoff zu
  spoilern; welches Reel gemeint ist, wird bei Unklarheit zuerst erfragt. Modus BTS:
  eigenstaendiger Story-Content mit eigenem Wert (Behind-the-Scenes, Mini-Serie, Umfrage, Quiz)
  aus echtem Material, gemeinsames Brainstorming im Chat, dann ein Bogen.
  Qualitaets-/ICP-Check immer, Approval, Speichern + Log. Liest Voice-/ICP-/Positionierungs-Profil,
  falls vorhanden. Triggern bei: "Story planen", "Story-Idee", "Story zum Reel", "bewirb das Reel
  in der Story", "BTS-Content", "Behind the Scenes", "Story-Serie", "Umfrage-Story",
  "/instagram-story".
---

# Instagram-Story

Du planst als **Senior Story-Creator**: Stories sind der Nähe-Kanal, roh schlägt Hochglanz,
und jeder Frame verdient den nächsten Tap. **Dein Ziel:** Bestands-Follower binden und in
Richtung Post oder Angebot bewegen, ohne dass es nach Werbung riecht.

Plant **einen** Story-Bogen pro Aufruf, fertig zum Umsetzen in der IG-App. Der Skill liefert
Konzept + Drehplan als Bullets, keine Grafiken, kein Rendern.

## Zwei Modi

- **Bewerben:** ein bestehendes Content-Asset (Reel oder Carousel) als Story anteasern, damit
  der Post gesehen wird. Teaser-Bogen mit Open Loop, Auflösung gibt es nur im Post.
- **BTS (Eigenständig):** Story-Content, der für sich steht: Behind-the-Scenes, Mini-Serie,
  Umfrage, Quiz. Baut die Nähe auf, die ein geschnittenes Reel nicht leisten kann. Nur aus
  echtem Material, nichts erfinden.

Modus aus dem Trigger ableiten ("bewirb das Reel" vs. "BTS-Idee"); unklar → eine kurze Frage.

## Methodik

**Kanonische Methodik (Pflicht lesen vor dem Bauen):**
- [`references/story-anatomy.md`](references/story-anatomy.md): Frame-Regeln, Teaser-Bogen-Muster,
  BTS-Formate, Interaktions-Sticker, Qualitäts-Checkliste, No-Gos.

---

## Pfade & Fundament

Keine hartkodierten Pfade. Ordner über `.agency-os/architecture.md` auflösen (gepflegt von
`agency-os-start`); fehlt sie, Struktur-Quelle des Projekts (`OS.md`, `README.md`, Root-`_index.md`)
lesen. `{context}`/`{marketing}`/`{logs}` sind aufgelöste Rollen.

**Kontext laden (alle optional, was fehlt, wird übersprungen):**
- **ICP:** `{context}/zielgruppe.md`: wer schaut, welche Spannung zieht.
- **Positionierung:** `{context}/positionierung.md`: wofür die Marke steht.
- **Voice:** `{context}/brand/voice-profile.md`: auf alle Overlay-Texte und gesprochenen Parts anwenden.
- **Material-Quellen für BTS:** falls das Projekt Content-Mining-Notizen führt (z.B. Ergebnisse
  von `/weekly-content-mining` im Marketing-Bereich), dort nach echten Momenten der Woche suchen.

Fehlen ICP und Voice beide: Story trotzdem planbar, am Ende `/icp` und `/brand-voice` empfehlen.

---

## Workflow

### Phase 1: Modus + Input (Stop-Punkt, frageweise)

Fragen nacheinander als normaler Chat-Text, KEINE Multiple-Choice, kein AskUserQuestion-Tool.

**Modus Bewerben:**
1. **Asset benennen lassen:** Welches Reel (oder Carousel) beworben wird, muss klar sein.
   Ergibt es sich aus dem direkten Kontext (User hat es genannt oder gerade damit gearbeitet),
   das nehmen. Sonst **zuerst nachfragen**: *"Welches Reel soll die Story bewerben?"*
   **Nicht** ungefragt im Brain suchen und raten.
2. **Asset im Brain auffinden:** erst mit der Antwort das benannte Asset im Brain suchen
   (z.B. unter `{marketing}/content/reels/` bzw. `{marketing}/content/carousels/`) und Hook,
   Kernaussage, Payoff und CTA erfassen. Nicht auffindbar → User um Kurzbeschreibung bitten.
   Der Payoff wird in der Story NICHT verraten.
3. **Ziel klären, falls unklar:** Post-Ansicht (Reel-Sticker/Link) oder Kommentar-Trigger des Posts.

**Modus BTS:**
1. **Material einsammeln:** *"Was ist diese Woche wirklich passiert, das deine Follower sehen
   dürfen? (Projekt, Kunde, Panne, Entscheidung, Einblick)"* Zusätzlich vorhandene
   Mining-Notizen im Brain sichten. **Nichts erfinden.**
2. **Gemeinsam brainstormen, was geteilt werden kann:** echtes Sparring im Chat, kein
   Vorschlags-Automat. Claude bringt Ideen aus dem Material ein (je 1 Zeile: Format + Kern),
   der User ergänzt, verwirft, kombiniert; nachfragen, weiterdrehen. Weiter zu Phase 2 erst,
   wenn der User eine Idee festlegt.

Zusätzlich kurz klären, falls nicht offensichtlich: **Format-Typ** (Kamera-Story/Talking,
Foto + Text, reine Text-Frames, Umfrage/Quiz).

### Phase 2: Story-Bogen bauen (automatisch)

Frame-für-Frame-Drehplan nach [`references/story-anatomy.md`](references/story-anatomy.md),
2-7 Frames. Pro Frame als Bullets:

- **Bild:** was zu sehen ist (Szene, Selfie, Screen, Foto)
- **Text-Overlay:** kurz, ohne Ton verständlich, Safe-Zones beachten
- **Sticker/Interaktion:** Umfrage, Quiz, Slider, Link, Reel-Sticker (max. eine prominente
  Interaktion pro Bogen)
- **Gesprochen** (nur bei Kamera-Story): Stichpunkt, kein Wortlaut

Genau **ein** CTA am Ende des Bogens. Voice-Profile auf alle Texte anwenden.

### Phase 3: Qualitäts- + ICP-Check (automatisch, läuft immer)

1. **Qualitäts-Checkliste** aus der Story-Anatomy durchgehen.
2. **ICP-Check** mit `/icp` Modus *Bewerten* auf Frame 1 + CTA (falls ICP-Profil vorhanden).
   Fail → einmal automatisch nachschärfen (max 1 Iteration).

Es wird nie ein ungecheckter Bogen ausgegeben.

### Phase 4: Approval (Stop-Punkt)

Kompletten Bogen im Chat ausgeben: Modus, Ziel, Frames nummeriert (Bild / Overlay /
Sticker / Gesprochen), geschätzte Frame-Zahl. Abschlussfrage:
*"Welcher Frame passt noch nicht? Oder 'go' zum Speichern."*

**Iterations-Loop:** Feedback pro Frame, nur den genannten Frame neu planen, Rest unverändert.
**"Go" → Phase 5.**

### Phase 5: Speichern + Log (automatisch)

1. **Datei anlegen** unter `{marketing}/content/stories/` (Ordner bei Bedarf anlegen und im
   zuständigen `_index.md` verlinken). Naming-Vorschlag (an Projekt-Konvention anpassen):
   `{YYYY}-w{KW}-story{N}-{slug}.md`. Frontmatter: Modus, Status, geplantes Datum, Format-Typ,
   Ziel/CTA, beworbenes Asset (nur Modus Bewerben). Darunter der Frame-Plan.
2. **Ausgabe an den User:** Pfad zur Datei. Hinweis: gebaut wird die Story in der IG-App.
3. **Log:** falls das Projekt ein Tages-Log führt (`{logs}/{YYYY-MM-DD}.md`), kurzer Eintrag:
   Modus, Thema, CTA, Output-Pfad.

---

## Output

Eine Markdown-Datei unter `{marketing}/content/stories/`, Naming `{YYYY}-w{KW}-story{N}-{slug}.md`:
Frontmatter + Frame-für-Frame-Drehplan (Bild / Text-Overlay / Sticker / Gesprochen). Keine
Grafiken, kein Rendern, keine Caption. Optional ein Log-Eintrag im Tages-Log.

---

## Verwandte Skills

**Erlaubte Skills im Workflow:**

- `/brand-voice`: Stimme auf Overlays und gesprochene Parts anwenden
- `/icp` Modus *Bewerten*: Frame 1 + CTA gegen das ICP testen

**Abgrenzung:**

- Kein Rendern, keine Story-Grafiken: die Story wird in der Instagram-App gebaut.
- Kein Reel-Skript (das ist `/reel-skript`), keine Slides (das ist `/carousel`).
- Keine Caption: Stories haben keine.
- Ein Story-Bogen pro Aufruf, keine ganze Serie auf Vorrat.

## Hard-Stops

- `references/story-anatomy.md` fehlt → Skill nicht nutzbar, Hinweis geben.
- Modus BTS ohne echtes Material vom User oder aus dem Brain → nicht erfinden, zurückfragen.
- Modus Bewerben: kein benanntes Asset → nachfragen, nie raten. Nicht auffindbar und keine
  Beschreibung vom User → stoppen.
- ICP-Check zweimal hintereinander fail → Bogen grundsätzlich neu denken statt drüberbügeln.
- User sagt nicht explizit "go"/"passt" → kein Speichern.
