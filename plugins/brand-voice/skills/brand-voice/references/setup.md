# Setup-Anleitung — Brand Voice Skill (für die KI)

> Schritt-für-Schritt-Anleitung für die KI im Setup-Modus. Keine Schritte überspringen, keine Reihenfolge ändern. Diese Datei ist die einzige Wahrheit für den Setup-Ablauf.
>
> **Wichtige Architektur-Regel:** Alle Datei-Schreib-Operationen passieren **am Ende** in einem einzigen atomaren Schritt (Schritt 7). Bis dahin läuft alles in-memory. Wenn Material-Check, Extraction oder Validierung fehlschlägt, wird **nichts** in den Skill-Ordner geschrieben.
>
> **Skill ist Template-Skill:** Der Skill wird vorinstalliert ausgeliefert. Beim ersten Trigger ohne `voice-profile.md` führt der Apply-Skill (`SKILL.md`) automatisch dieses Setup aus. Nach erfolgreichem Setup kann der User entscheiden, ob der fertige Skill global installiert werden soll.

---

## Voraussetzungen

Im Skill-Ordner liegen bereits drei Dateien:

- `SKILL.md` (im Skill-Root)
- `references/setup.md` (diese Datei)
- `references/anti-patterns.md`
- `references/voice-profile-template.md`

`references/voice-profile*.md` existiert noch nicht. Genau diese File(s) werden durch dieses Setup erzeugt (entweder ein `voice-profile.md` bei einer Voice, oder `voice-profile-personal.md` + `voice-profile-brand.md` bei zwei Voices).

Wenn eine der drei Quell-Dateien fehlt: Setup sofort abbrechen mit Hinweis *"Skill-Installation unvollständig: fehlt {{Datei}}"*.

---

## Schritt 1 — Pre-Check (kein Schreiben)

### 1.1 Existierende Installation prüfen

- Existiert irgendein `references/voice-profile*.md` (außer `voice-profile-template.md`)?
  - **Ja** → Re-Setup-Flag setzen. In Schritt 7.1 wird das relevant.
  - **Nein** → Erst-Installation.

### 1.2 Schreibrechte-Check

Trockenlauf: kann die KI grundsätzlich in `references/` schreiben? Test ohne tatsächliches Anlegen einer Datei.

Wenn keine Schreibrechte: Setup sofort abbrechen mit Hinweis *"Cowork hat keine Schreibrechte auf dem Skill-Ordner. Bitte Workspace-Folder prüfen."*

Wenn alles OK: weiter zu Schritt 1.3.

### 1.3 Voice-Anzahl klären

**Pflicht: AskUserQuestion-Tool verwenden, Single-Select.**

Vorher kurzer Kontext-Block an den User:

> *"Bevor wir starten: brauchst du eine Voice für alle Kontexte, oder zwei getrennte Voices?*
>
> *— **Eine Voice für alles** passt, wenn deine private Kommunikation (WhatsApp, E-Mail 1:1) genauso klingt wie deine öffentlichen Texte (LinkedIn, Newsletter, Website). Typisch bei Personal Brands, wo "ich" und "Marke" verschwimmen.*
>
> *— **Personal + Brand getrennt** passt, wenn deine private Stimme anders ist als deine öffentliche Marke. Beispiel: Gründer-Account privat (locker, Ich-Form, Umgangssprache) vs. Firmen-Account offiziell (sachlicher, Wir-Form). Oder: Mitarbeiter haben ihre eigene Stimme privat, schreiben aber für die Firma in der Brand-Voice.*
>
> *Im Zweifel: eine Voice reicht."*

**Frage:** "Wie viele Voices brauchst du?"

**Optionen (Single-Select):**

1. **Eine Voice für alles** (ein Profil deckt alle Channels ab)
2. **Personal + Brand getrennt** (zwei Profile, Channel-basiert auseinandergehalten)

**Auswertung:**
- Antwort merken als `voice_count` (1 oder 2).
- Bei `voice_count = 2`: alle folgenden Schritte erzeugen zwei Profile parallel.

---

---

## Schritt 2 — Voice-Onboarding (in-memory)

Bevor Material gesammelt wird, holen wir vom User zwei Minuten gesprochene Sprache. Voice-Antworten zeigen die Alltags-Voice ungefiltert: typische Einleitungen, Tempo, Lieblings-Formulierungen, emotionale Marker. Aus diesem Material extrahiert die KI **erste Voice-Marker** ins in-memory Profil, bevor Schritt 3 startet. Das Voice-Transkript zählt **nicht** zu den 5–10 Texten in Schritt 4, sondern liefert ergänzende Marker.

### 2.1 Prompt für Handy-AI ausgeben

Gib dem User folgenden Block aus, mit klarer Anleitung: er soll den eingerahmten Code-Block 1:1 in einen neuen Claude Chat kopieren. Danach wechselt er auf die Handy-App, steigt im selben Chat ein und beantwortet die Fragen per Voice-Eingabe. Gesamtdauer ca. 2 Minuten.

> Starte einen neuen Claude Chat und kopiere den folgenden Prompt in das Fenster. Beantworte die vier Fragen per Voice-Eingabe, ungeschnitten, wie es kommt. Die App transkribiert mit. Am Ende kopierst du das gesamte Transkript hier zurück.

```
[Voice-Onboarding für Brand-Voice-Skill]

Stelle mir die folgenden vier Fragen nacheinander, eine nach der anderen, und warte jeweils auf meine Antwort. Formuliere nichts um, fasse nichts zusammen, korrigiere nicht. Du sammelst nur. Am Ende gibst du mir alle vier Antworten als 1:1 Kopie meiner Eingabe zurück, jede Frage mit Überschrift, darunter mein Wortlaut.

Frage 1: Was machst du beruflich, kurz und klar, so wie du es einem alten Bekannten erklären würdest?
Frage 2: Was nervt dich an deiner Branche oder am Marktverhalten deiner Wettbewerber am meisten?
Frage 3: Worauf in deinem Business bist du wirklich stolz?
Frage 4: Wenn ein potenzieller Kunde noch zögert: was sagst du ihm, um seine Entscheidung zu kippen?
```

> Wenn das Transkript fertig ist, schick es hier rein. Danach geht es mit der Kanal-Frage weiter.

### 2.2 Transkript einlesen und erste Voice-Marker extrahieren

Sobald der User das Voice-Transkript zurückspielt, extrahiere **direkt** ins in-memory Voice-Profile (noch nichts schreiben):

- **Positioning-O-Ton:** Wie der User selbst beschreibt was er macht. Wörtliches Zitat aus Frage 1. Wird später Anker für Säulen-Identifikation.
- **Tabu-Marker (kritische Voice):** Wörter und Konstruktionen aus Frage 2, mit denen der User Branchen-Phrasen kontert. Auch was er **nicht** sagt, obwohl Branchen-Sprech es nahelegen würde.
- **Like-Marker (Wert-Voice):** Lieblings-Formulierungen aus Frage 3, die zeigen worauf der User Wert legt. Mit Zitat.
- **Druck-Voice:** Wie der User spricht, wenn er überzeugen will (Frage 4). Satzlänge, Direktheit, Argument-Struktur.
- **Querschnitt:** Typische Satzeinleitungen, Füllwörter, Wiederholungs-Pattern, Dialekt-Marker. Alles, was über alle vier Antworten hinweg auffällt.

Jeder Marker muss mit **wörtlichem Zitat** aus dem Transkript belegt sein, sonst wird er gestrichen (Pflicht-Regel 3 gilt auch hier).

### 2.3 Bestätigung an User

Kurzer Statusbericht, ohne Marketing-Phrasen:

> *"Voice-Onboarding ausgewertet. {{N}} Marker erfasst: {{X}} Lieblings-Formulierungen, {{Y}} Tabu-Pattern, {{Z}} Positionierungs-O-Töne. Geht jetzt weiter mit der Kanal-Frage."*

Wenn das Transkript zu kurz oder unklar ist (unter 200 Wörter, oder eine Frage unbeantwortet): User um Ergänzung bitten oder mit weniger Markern weitermachen. Wenn der User Voice-Onboarding ganz überspringen will: Wartungsprotokoll-Eintrag *"Voice-Onboarding übersprungen"* vermerken, weiter zu Schritt 3.

---

## Schritt 3 — Kanal-Scope pro Voice (in-memory)

Bevor Material gesammelt wird, klärt die KI **pro Voice**, für welche Channels sie zuständig ist. Diese Antworten steuern später die Profile-Auswahl im Apply-Modus.

**Bei `voice_count = 1`:** Schritt 3 einmal durchlaufen.
**Bei `voice_count = 2`:** Schritt 3 zweimal durchlaufen, einmal für `personal`, einmal für `brand`. Channels müssen **exklusiv** sein: jeder Channel darf nur einem Profil zugeordnet sein. Wenn der User einen Channel beiden zuordnen will, nachfragen welches Profil ihn als Hauptzuständigkeit übernimmt.

### 3.1 Kanal-Scope (pro Voice)

**Pflicht: AskUserQuestion-Tool verwenden, Multi-Select.** Frage abhängig vom Modus formulieren:

- Bei `voice_count = 1`: *"Für welche Kanäle willst du diese Voice einsetzen?"*
- Bei `voice_count = 2`, erste Runde: *"Für welche Kanäle ist deine **Personal Voice** zuständig?"*
- Bei `voice_count = 2`, zweite Runde: *"Für welche Kanäle ist deine **Brand Voice** zuständig?"*

**Optionen (Multi-Select, in dieser Reihenfolge):**

1. **Alle Texte** (alle vier Kanäle unten plus zukünftige andere)
2. **Spontane E-Mails** (Kunden-Korrespondenz, kurze Antworten)
3. **Newsletter** (E-Mails an die Liste)
4. **LinkedIn** (Posts, Kommentare)
5. **WhatsApp** (kurze Nachrichten, Sprachmemos)
6. **Anderer Kanal** (Freitext: User soll konkret nennen)

**Auswertungs-Logik:**
- "Alle Texte" gewählt (egal mit welchen anderen Optionen kombiniert): alle vier Standard-Kanäle aktivieren
- Nur einzelne Kanäle gewählt (ohne "Alle Texte"): nur diese aktivieren
- "Anderer Kanal" gewählt: Freitext-Antwort ins Profil aufnehmen
- Bei `voice_count = 2`: nach beiden Runden Exklusivität prüfen. Bei Doppel-Zuordnung Folgefrage: *"Channel X wurde beiden Voices zugeordnet. Welches Profil soll ihn als Haupt-Zuständigkeit übernehmen?"*

### 3.2 Ergebnis ins in-memory Profil

Pro Voice eintragen:
- Aktive Kanäle (Liste)

Voice-Modus-Konzept (eine Voice / getrennte Modi / Mischform) entfällt, weil Multi-Voice-Setup diese Funktion über separate Profile abbildet.

---

## Schritt 4 — Material-Check

### 4.1 Anforderung an User

> **Sammel-Vorlage anbieten:** Bevor du die Material-Anforderung formulierst, biete dem User aktiv folgende Vorlage als Kopier-Template an:
> **[Brandvoice Template (Google Doc)](https://docs.google.com/document/d/1TzIzYi7im9MpWlUv9g-sJKlKsHQZBmmAGoibvIYNipE/edit?usp=sharing)**
> Slots: 3× LinkedIn, 3× Newsletter, 3× Spontan-Mail, 6× WhatsApp. Der User kann sich eine Kopie machen, die Slots mit seinen Originaltexten füllen und das fertige Dokument zurückgeben.

Der User braucht **5–10 eigenhändig geschriebene Texte** insgesamt (auch bei `voice_count = 2` — nicht doppelt sammeln). Mix aus mindestens zwei Modi, plus ggf. emotional aufgeladenes Material:

- **Kuratiert** (2–4 Texte): LinkedIn-Posts, Newsletter, Website-Copy. Zeigt die "öffentliche Voice".
- **Spontan** (2–4 Texte): längere Kunden-E-Mails, Slack-/WhatsApp-Antworten, Sprachmemo-Transkripte. Zeigt die "Alltags-Voice".
- **Emotional aufgeladen** (1–2 Texte, optional): Beschwerde, Begeisterung, Ablehnung. Zeigt die "Stress-Voice".

**Anpassung an Kanal-Scope (aus Schritt 3):** Material gezielt für die aktiven Kanäle anfragen. Wenn z.B. nur LinkedIn aktiv: 5–10 LinkedIn-Posts. Wenn alle vier Kanäle: idealerweise pro Kanal 1–3 Beispiele.

**Bei `voice_count = 2`:** Material muss beide Voices abdecken. Pro Voice idealerweise 3–5 Beispiele. Klassifikation passiert in 3.3 (User bestätigt, welcher Text zu welcher Voice gehört).

### 4.2 Was tun, wenn Material unzureichend ist

| Situation | Reaktion |
|---|---|
| Weniger als 5 Texte geliefert | Hinweis an User: *"Profil wird zu eng. Empfehle mindestens 5, besser 8 Texte."* — Setup nur fortsetzen, wenn User explizit zustimmt. |
| Nur ein Modus (z.B. nur LinkedIn-Posts) | Hinweis: *"Profil bildet nur Performance-Voice ab, nicht die Alltags-Voice. Empfehle 2–4 spontane Texte zu ergänzen."* |
| Texte sind sehr unterschiedlich lang oder uneinheitlich | OK, Mix ist erwünscht. Erfassen wie es ist. |
| Texte enthalten KI-Output, Vorlagen oder fremde Hände | Kritisch nachfragen *"Wurde das Stück tatsächlich von dir selbst geschrieben?"* — bei Unsicherheit ausschließen. |

### 4.3 Material-Inventar erstellen

Bevor extrahiert wird, kurz auflisten was vorliegt:

> *"Du hast {{N}} Texte geliefert: {{X}} kuratierte ({{Plattformen}}), {{Y}} spontane ({{Kontexte}}), {{Z}} emotional. Beginne jetzt mit der Extraktion."*

**Bei `voice_count = 2`:** Zusätzlich Klassifikation pro Text anzeigen:

> *"Klassifikation pro Text:*
> *- Text 1 (LinkedIn-Post): Brand*
> *- Text 2 (WhatsApp): Personal*
> *- Text 3 (Newsletter): Brand*
> *- ...*
>
> *Stimmt die Zuordnung, oder soll ich was umsortieren?"*

Klassifikation basiert auf den Channel-Listen aus Schritt 3. Bei Unklarheit (z.B. ein Text passt zu keinem Channel oder zu beiden): User explizit fragen.

So kann der User korrigieren, bevor die Extraktion läuft.

---

## Schritt 5 — Pattern-Extraction (in-memory)

Lade die Schema-Vorlage `references/voice-profile-template.md`. Befülle deren Sektionen in derselben Reihenfolge im Speicher, noch nicht in eine Datei schreiben. Die Voice-Marker aus Schritt 2 sind bereits im in-memory Profil und werden hier konsolidiert.

**Bei `voice_count = 2`:** Pattern-Extraction läuft **parallel für beide Profile**:
- Personal-Texte (aus Schritt 4.3 klassifiziert) → in-memory Personal-Profil
- Brand-Texte → in-memory Brand-Profil
- Voice-Marker aus Schritt 2 fließen in beide Profile ein (sie zeigen den Menschen hinter beiden Voices). Bei Bedarf User fragen, ob ein Marker nur einer Voice gilt.
- Jede Sektion (Kernessenz, Satzbau, Vokabular, Formatierung, Quality-Check) wird **pro Voice separat** extrahiert.
- Channels-Sektion pro Profil aus Schritt 3.1 übernehmen.

Extrahiere aus den User-Texten **mechanische Patterns**, keine Adjektive. Anzahl und Form jeder Kategorie folgen den Daten.

### 5.1 Kernessenz

- Identifiziere, was den Stil identifizierbar macht.
- Formuliere **Säulen** (typischerweise 2–5).
- **Pflicht:** Jede Säule mit einem konkreten Mechanismus + wörtlichem Zitat aus dem Material belegen.

### 5.2 Satzbau & Rhythmus

- Durchschnittliche Satzlänge **messen** (nicht schätzen).
- Charakteristische Bruch- oder Wechselmuster **aus den Texten destillieren**.
- Auffälligkeiten dokumentieren: Ellipsen, Ein-Wort-Sätze, Schachtelung, Klammer-Einschübe, Cliffhanger.
- **Flow-Hinweis:** Vollsätze auch wenn kurz, keine Stichpunkt-Aufzählungen ohne Verb (sonst wirkt es staccato).

### 5.3 Sprache & Vokabular

Vier Sub-Kategorien:

- **Lieblings-Wörter und -Phrasen**
- **Tabu-Wörter** (im Material auffällig fehlend, obwohl Generic-KI sie einsetzen würde)
- **Typische Satzeinleitungen** (wörtlich, mit Anführungszeichen)
- **Anti-Phrasen** (Konstruktionen, die im Material **explizit nicht** auftauchen)

### 5.4 Channels-Sektion dokumentieren

Aus Schritt 3.1 ergibt sich die Channels-Liste pro Profil. Diese kommt als `## Channels` Sektion an den Anfang des Profils (direkt nach dem Header), damit der Skill beim Apply die Channel-Heuristik durchführen kann.

### 5.5 Formatierung

- Aufzählungs-Symbole verwendet?
- Weißraum-Disziplin
- Emoji-Regel
- **Dash-Verwendung:** Default ist keine Em-/En-Dashes mitten im Satz.

### 5.6 Qualitätsprüfung-Checkliste

Erstelle 4–8 individuelle Checkbox-Fragen für die spätere Selbstprüfung jedes Outputs. Pflicht-Fragen (immer drin):

- [ ] Anker eingehalten (richtige Position auf dem Spektrum)?
- [ ] Klare Botschaft trotzdem erkennbar?
- [ ] Keine Tabu-Konstruktion verwendet (siehe `anti-patterns.md`)?
- [ ] Vollsätze auch wenn kurz, kein Stichpunkt-Staccato?
- [ ] Mindestens ein Lieblings-Wort verwendet, kein Tabu-Wort drin?

Plus 1–3 individuelle Fragen, aus dem Material abgeleitet.

### 5.7 Pflicht-Belege

**Jede Stilbehauptung** muss mit mindestens einem **wörtlichen Zitat** aus dem User-Material belegt werden. Ohne Zitat ist der Eintrag spekulativ und wird gestrichen.

### 5.8 Platzhalter-Disziplin

**Alle** `{{Platzhalter}}` aus dem Schema müssen ersetzt werden. Wenn ein Pattern nicht eindeutig erkennbar ist:

- Schreibe `{{nicht-eindeutig — mehr Material nötig}}` statt zu spekulieren.
- Schreibe **nicht** etwas Generisches aus eigener Erfindung.

---

## Schritt 6 — Validierung mit echten Test-Outputs (in-memory)

### 6.1 Test-Outputs erzeugen

Lies `references/anti-patterns.md` als Negativfilter. Erzeuge **pro aktivem Kanal pro Profil einen Test-Output**, in-memory. Realistischer Use-Case pro Kanal:

- **LinkedIn:** ein Post zu einem Thema, das aus dem Material plausibel ist
- **Newsletter:** eine kurze Newsletter-Einleitung
- **Spontane E-Mail:** eine Antwort an einen Kunden mit konkretem Anliegen
- **WhatsApp:** eine kurze Antwort auf eine eingehende Nachricht

**Bei `voice_count = 2`:** Tests pro Profil getrennt zeigen, jeweils mit Profil-Label (Personal vs. Brand), damit der User Voice-Trennung und Konsistenz parallel validieren kann.

Bei mehreren Kanälen pro Profil: alle Tests gleichzeitig zeigen.

### 6.2 Validierungs-Frage

Stelle dem User **eine** klare Frage:

> *"Würdest du diese Test-Outputs ohne Edit so verwenden?"*

### 6.3 Feedback-Schleife

| Antwort | Reaktion |
|---|---|
| **Ja** | Validierung bestanden. Setze in-memory Wartungsprotokoll-Eintrag *"Validierung bestanden"*. Weiter zu Schritt 7. |
| **Nein** | Frage zurück: *"Welche konkrete Stelle stimmt nicht? Wort? Phrase? Struktur? Welcher Kanal?"* — User-Antwort direkt ins in-memory Profil einarbeiten, dann erneut Schritt 6.1. |

**Maximale Schleifen:** 3. Wenn nach 3 Iterationen kein Pass: Setup pausieren, **nichts schreiben**, Hinweis an User:

> *"Das Profil bleibt zu unscharf. Wahrscheinliche Ursachen: zu wenig Material, zu uneinheitliches Material, oder Marker-Phrasen sind nicht erfassbar. Empfehle 3–5 weitere Texte ergänzen, dann erneut Setup. Es wurde nichts in den Skill-Ordner geschrieben."*

---

## Schritt 7 — Voice-Profile schreiben (atomar)

Erst jetzt, nach erfolgreicher Validierung, werden die Profile geschrieben.

### 7.1 Re-Setup-Flag aus Schritt 1.1 auswerten

- **Re-Setup** (irgendein `voice-profile*.md` existiert schon): bestehende Profile als Diff-Anker behalten, dann überschreiben. Wartungsprotokoll-Eintrag mit Diff-Notiz.
- **Erst-Installation:** weiter zu 6.2.

### 7.2 Voice-Profile schreiben

**Bei `voice_count = 1`:** Schreibe das in-memory Profil nach:

```
references/voice-profile.md
```

**Bei `voice_count = 2`:** Schreibe beide Profile parallel:

```
references/voice-profile-personal.md
references/voice-profile-brand.md
```

In jedem Profil:
- Header inkl. Profil-Typ (personal / brand) oder bei Single nur Name
- `## Channels` Sektion am Anfang (aus Schritt 3.1)
- Restliche Sektionen aus Schritten 2, 5 und 6
- Wartungsprotokoll-Initial-Eintrag mit Datum, Quelle (*"Workshop"* oder *"Selbst-Setup"*), Anzahl Texte, Voice-Onboarding ja/nein, Channels, Anzahl Validierungs-Schleifen

### 7.3 Verifikation

Prüfe folgende Bedingungen:

- [ ] Erwartete Profil-File(s) existieren (1 oder 2)
- [ ] Keine `{{Platzhalter}}` mehr (außer expliziten *"nicht-eindeutig"*-Markern)
- [ ] Channels-Sektion in jedem Profil befüllt
- [ ] Wartungsprotokoll-Eintrag in jedem Profil

Bei Fail: Setup ist im inkonsistenten Zustand. Hinweis an User mit Pfad-Angabe, was geschrieben wurde und was fehlt.

### 7.4 Status an User

Nach erfolgreicher Verifikation:

```
Voice-Profile fertig.

Setup-Modus: {{Eine Voice / Personal + Brand}}
Quelle: {{N}} Texte + Voice-Onboarding ({{ja/nein/übersprungen}})
Validierungs-Schleifen: {{1-3}}

Pro Profil:
- {{voice-profile.md ODER voice-profile-personal.md}}
  Channels: {{Liste}}
  Säulen: {{Anzahl}} | Lieblings-Wörter: {{Anzahl}} | Tabu-Wörter: {{Anzahl}}
- {{nur bei Multi-Voice: voice-profile-brand.md}}
  Channels: {{Liste}}
  Säulen: {{Anzahl}} | Lieblings-Wörter: {{Anzahl}} | Tabu-Wörter: {{Anzahl}}
```

Keine Marketing-Phrasen, nüchterner Statusbericht.

---

## Schritt 8 — Globale Installation anbieten

Der Skill ist als Template-Skill ausgeliefert worden. Aktuell läuft er nur in diesem Projekt. Falls der User ihn überall nutzen will, kann er global installiert werden.

### 8.1 Frage

**Pflicht: AskUserQuestion-Tool verwenden, Single-Select.**

**Frage:** "Soll der fertige Skill jetzt global installiert werden, damit er in jedem Claude-Projekt verfügbar ist?"

**Optionen (Single-Select):**

1. **Ja, global installieren** (der fertige Skill wird über den offiziellen Skill Creator als installierbare Skill-Datei verpackt und installiert)
2. **Nein, nur in diesem Projekt belassen** (Skill bleibt projekt-lokal)
3. **Später entscheiden** (Hinweis an User, wie er das nachholen kann)

### 8.2 Bei Option 1 (über den Skill Creator paketieren und installieren)

Die globale Installation läuft **nicht** über manuelles Kopieren, sondern über den offiziellen **Skill Creator** von Anthropic. So entsteht eine sauber paketierte, wirklich installierbare Skill-Datei. Der Skill Creator übernimmt Paketierung und Installation.

1. **Vollständigkeit prüfen:** Der Skill-Ordner enthält `SKILL.md`, `references/setup.md`, `references/anti-patterns.md`, `references/voice-profile-template.md` und mindestens ein generiertes `references/voice-profile*.md` (das fertige Profil des Users).
2. **An den Skill Creator übergeben:** Reiche den kompletten Skill-Ordner (`SKILL.md` im Root, `references/` daneben, inklusive des generierten Profils) beim offiziellen Skill Creator ein. Er verpackt ihn als installierbare Skill-Datei und installiert ihn.
3. **Statusbericht:** *"Skill an den Skill Creator übergeben. Er paketiert brand-voice als installierbare Skill-Datei und installiert ihn. Triggert danach in jedem Claude-Projekt."*

Fallback (nur falls der Skill Creator nicht verfügbar ist): Skill-Ordner manuell nach `~/.claude/skills/brand-voice/` kopieren (Windows: `%USERPROFILE%\.claude\skills\brand-voice\`), inklusive aller `voice-profile*.md`.

### 8.3 Bei Option 2 (nur projekt-lokal)

- Statusbericht: *"Skill bleibt projekt-lokal in `.claude/skills/brand-voice/`."*

### 8.4 Bei Option 3 (später entscheiden)

- Statusbericht: *"OK. Wenn du später global installieren willst: einfach sagen 'Brand-Voice-Skill global installieren', dann verpacke ich ihn über den offiziellen Skill Creator als installierbare Skill-Datei."*

---

## Pflicht-Regeln im Setup-Modus

Diese Regeln gelten in jedem Schritt:

1. **In-Memory bis zum Ende.** Schreib-Operationen passieren ausschließlich in Schritt 7 (und ggf. Schritt 8 für globale Installation).
2. **Mechaniken vor Adjektiven.** *"Direkt"* ist kein Profil-Eintrag. *"Sätze unter 12 Wörter, Aussage gefolgt von Konter"* ist einer.
3. **Nichts ohne Beleg.** Jede Stilbehauptung braucht ein wörtliches Zitat aus dem Material.
4. **Lieber leer als geraten.** Wenn ein Pattern nicht eindeutig erkennbar ist: `{{nicht-eindeutig — mehr Material nötig}}` schreiben, nicht generische Default-Inhalte erfinden.
5. **Keine Goldstandard-Imitation.** Wenn ein Beispiel-Profile aus einer anderen Person als Form-Vorlage konsultiert wird: nur Struktur und Mechanik-Form übernehmen, nicht Inhalt.
6. **User-Antworten haben Vorrang.** Wenn der User korrigiert, wird das Profil sofort angepasst, auch wenn das eigene Pattern-Modell etwas anderes nahelegt.
7. **Strukturierte Fragen über AskUserQuestion-Tool.** Bei den Fragen 2.1, 2.2 und 7.1 ist das Tool Pflicht, kein Freitext.
8. **Mid-Course-Correction ist erlaubt.** Auch nach Schritt 7 darf der User noch nachschärfen. Profil-Anpassung dann direkt mit neuem Wartungsprotokoll-Eintrag, kein Re-Setup nötig.

---

## Edge Cases

| Situation | Reaktion |
|---|---|
| User liefert Material in mehreren Sprachen | Pro Sprache getrennt extrahieren oder die dominante Sprache als Profil-Sprache wählen, User kurz fragen. |
| Material enthält viel Branchen-Jargon | Branchen-Jargon ist Teil des Vokabulars, dokumentieren, aber als solchen markieren. |
| User korrigiert während Pattern-Extraction laufend | Korrekturen direkt ins in-memory Profil einarbeiten, nicht erst auf Validierung warten. |
| User will Schritt 2 (Voice-Onboarding) überspringen | Vermerken im Wartungsprotokoll, weiter zu Schritt 3. |
| Voice-Transkript ist sehr knapp oder eine Frage unbeantwortet | Ergänzung anbieten. Wenn User nicht ergänzen will: mit weniger Markern weiterlaufen. |
| User wählt in 2.1 nur einen einzigen Kanal | OK, Channels-Liste hat dann nur einen Eintrag. |
| User ordnet bei `voice_count = 2` denselben Channel beiden Voices zu | Folgefrage: *"Welches Profil soll Channel X als Haupt-Zuständigkeit übernehmen?"* Channels müssen exklusiv pro Profil sein. |
| User hat zu wenig Material für eine der beiden Voices (`voice_count = 2`) | Hinweis: *"Für {{Personal/Brand}} liegen nur {{N}} Texte vor. Empfehle 3+ pro Voice."* User entscheidet: ergänzen oder mit dünnem Profil weiter. |
| User will Schritt 6 (Validierung) überspringen | Stark abraten, ohne Validierung wird nicht installiert. Wenn User explizit darauf besteht: Wartungsprotokoll-Eintrag *"Validierung übersprungen"*, dann zu Schritt 7. |
| Re-Setup (irgendein `voice-profile*.md` existiert schon) | In Schritt 7.1 erkannt. Bestehende Profile als Diff-Anker im Wartungsprotokoll dokumentieren. Drift markieren, User entscheidet was übernommen wird. |
| Schreib-Operation in Schritt 7 schlägt fehl | Klarer Hinweis an User mit dem Pfad. Kein erneuter Versuch automatisch. |
| Globale Installation in Schritt 8 schlägt fehl | Hinweis an User mit Fehlermeldung. Skill bleibt projekt-lokal. Re-Versuch über manuelle Anweisung. |
