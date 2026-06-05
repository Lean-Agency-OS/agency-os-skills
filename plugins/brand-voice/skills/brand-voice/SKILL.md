---
name: brand-voice
description: >
  Wendet ein vorhandenes Voice-Profile auf neue Texte an, oder führt das Setup
  aus, wenn das Profil noch nicht existiert. Triggert bei jeder Anfrage nach
  Text in der eigenen Stimme: E-Mails, LinkedIn-Posts, Newsletter, Sales-Copy,
  WhatsApp-Antworten. Auch triggern bei: "schreib in meiner Voice",
  "klingt das nach mir", "schreib mir eine E-Mail in meiner Stimme",
  "beantworte das in meinem Stil", "mach daraus einen Post in meiner Voice",
  "prüf das auf meine Voice", "Brand-Voice einrichten",
  "Setup für Voice-Skill machen", "Lass uns das Setup für meine Brand-Voice machen", "/brand-voice".

  Wenn das Voice-Profile noch nicht existiert: Skill startet automatisch das
  Setup über references/setup.md.
---

# Brand Voice Skill

Dieser Skill schreibt Texte in der dokumentierten Voice des Users. Er hat zwei Modi:

- **Setup-Modus** (wenn noch kein Voice-Profile existiert): Skill folgt der Anleitung in `references/setup.md` und führt den vollständigen Setup-Prozess aus.
- **Apply-Modus** (wenn mindestens ein Voice-Profile da ist): Skill schreibt oder prüft Texte in der dokumentierten Voice.

Der Skill unterstützt **eine ODER zwei Voices** (Personal + Brand). Im Setup wird das geklärt.

Mögliche Profil-Files im `references/` Ordner:
- `voice-profile.md` — bei "eine Voice für alles"
- `voice-profile-personal.md` und `voice-profile-brand.md` — bei "Personal + Brand getrennt"

Der Skill nutzt diese Files im selben Skill-Ordner:

- `references/voice-profile*.md` — ein oder zwei individuelle Voice-Profile (vom Setup geschrieben, am Anfang noch nicht da)
- `references/voice-profile-template.md` — die leere Schema-Vorlage (Referenz für das Setup)
- `references/anti-patterns.md` — universelle KI-Tells als Negativfilter
- `references/setup.md` — die Setup-Anleitung, die der Skill bei fehlendem Profil ausführt

---

## Schritt 1 — Voice-Profile-Check (IMMER ZUERST)

Vor jeder Antwort:

1. Scanne `references/` nach Files mit dem Muster `voice-profile*.md`, ausgenommen `voice-profile-template.md`.
2. Bestimme den Modus:
   - **Kein Profil gefunden** → Setup starten (siehe unten), keinen Voice-Text generieren.
   - **`voice-profile.md` gefunden** (Single-Voice-Modus) → weiter zu Schritt 2.
   - **`voice-profile-personal.md` und/oder `voice-profile-brand.md` gefunden** (Multi-Voice-Modus) → weiter zu Schritt 1.5 (Profile-Auswahl).
3. Wenn ein gefundenes Profil noch unbearbeitete `{{Platzhalter}}` enthält (außer expliziten *"nicht-eindeutig"*-Markern): Setup als unvollständig markieren, User informieren, Setup re-triggern lassen oder mit Lücken weiterarbeiten.

---

## Schritt 1.5 — Profile-Auswahl (nur im Multi-Voice-Modus)

Wenn zwei Profile da sind, entscheide welches geladen wird:

1. **Channel-Heuristik:** Lies aus jedem Profil die `## Channels` Sektion. Vergleiche mit dem User-Kontext (welcher Channel wird angesprochen — explizit "LinkedIn-Post" oder implizit "schreib mir eine Mail").
2. **Eindeutige Zuordnung:** Wenn der Channel nur in einem Profil dokumentiert ist → dieses Profil laden, kein Nachfragen.
3. **Kontextuelle Tendenz:** Wenn keine explizite Channel-Nennung, aber der Kontext klar auf eine Voice deutet (z.B. "Antwort an einen Kunden, der nach unserem Service fragt" → Brand; "schreib meinem Co-Founder zurück" → Personal) → diese Voice nehmen, ohne Nachfragen.
4. **Echte Mehrdeutigkeit (50/50):** Wenn ein Channel in beiden Profilen vorkommt ODER kein Kontext-Signal erkennbar → `AskUserQuestion`: *"Personal oder Brand?"* — Erst nach Antwort weitermachen.

Sobald das Profil bestimmt ist, weiter zu Schritt 2.

### Setup starten

Dem User kurz mitteilen, was passiert:

> *"Voice-Profile ist noch nicht eingerichtet. Ich starte jetzt das Setup, dauert insgesamt etwa 15 bis 20 Minuten und braucht von dir 5 bis 10 eigenhändig geschriebene Texte plus 2 Minuten gesprochene Sprache. Wenn du gerade keine Zeit hast, sag Bescheid, dann mache ich nur die ursprüngliche Antwort und wir holen das Setup später nach."*

Wenn der User OK gibt: lies `references/setup.md` und folge der Anleitung dort Schritt für Schritt. Setup wird vom Skill selbst durchgeführt, nicht ausgelagert.

Wenn der User das Setup jetzt nicht machen will: gib eine Antwort auf seine ursprüngliche Frage in **neutraler Voice** (ohne Voice-Profil-Anpassung), und vermerke, dass der Skill ohne Setup nicht in der Brand-Voice schreiben kann.

---

## Schritt 2 — Profile laden (Apply-Modus)

Lies das in Schritt 1/1.5 bestimmte Voice-Profile komplett. Lies `references/anti-patterns.md` als Negativfilter.

---

## Schritt 3 — Text generieren

Halte dich an:
- Kernessenz und Säulen
- Anker und Spektrum (falls dokumentiert)
- Satzbau-Rhythmus (Längen, Bruchmuster, Auffälligkeiten)
- Vokabular: nutze Lieblings-Wörter und -Phrasen, vermeide Tabu-Wörter
- **Tabu-Konstruktionen** beachten (siehe Quality-Check und anti-patterns.md)
- Formatierung-Regeln (Pfeile, Bullets, Weißraum, Emoji-Default, Dash-Default)

---

## Schritt 4 — Anti-Slop-Check

Prüfe vor Ausgabe gegen `references/anti-patterns.md`. Pflicht-Filter (in dieser Reihenfolge):

1. **Em-Dash und En-Dash entfernen** (— und –) mitten im Satz. Default-Ersatz: Punkt, Doppelpunkt oder Komma. Ausnahme nur, wenn `voice-profile.md` Em-Dash explizit als Stilmittel dokumentiert.
2. **Pol-Setzungs-Slop entfernen** ("Nicht X. Sondern Y.", "Ich sag das nicht, weil X. Sondern weil Y.", "Es geht nicht um X. Es geht um Y."). Statt diese Konstruktionen: direkt sagen.
3. Keine generischen KI-Helper-Phrasen (*"Ich hoffe das hilft", "großartige Frage", "gerne stehe ich zur Verfügung"*).
4. Keine Adjektiv-Cluster ohne Beleg (*"warm und kompetent und nahbar"*).
5. Keine Stichpunkt-Aufzählungen ohne Verb (z.B. *"Team überlastet, Projekte langsam, irgendwer muss her"*). Stattdessen Vollsätze auch wenn kurz.
6. Bullet- und Emoji-Reflex unterdrücken, wenn das Profil Prosa fordert.

Wenn auch nur eine Stelle durchrutscht: streichen oder umschreiben.

---

## Schritt 5 — Qualitätsprüfung

Gehe die individuelle Checkbox-Liste am Ende von `voice-profile.md` durch. Bei jedem Nein-Punkt: Text anpassen, erneut prüfen.

---

## Schritt 6 — Ausgabe

Liefere den finalen Text. Bei Bedarf zusätzlich:
- Eine 1-Satz-Begründung, welches Voice-Element wo eingesetzt wurde
- Alternative-Variante, wenn der User eine zweite Version explizit anfordert

---

## Update / Re-Setup

Wenn der User nach erfolgreichem Initial-Setup nachschärfen will (Korrektur an einzelnen Mechaniken, neue Tabus, Voice-Drift): direkt ins Profil eintragen mit neuem Wartungsprotokoll-Eintrag. Mid-Course-Correction ist erlaubt und nicht dasselbe wie Re-Setup.

Re-Setup (komplette Neu-Extraktion mit neuem Material) ist nur sinnvoll, wenn der User nach längerer Zeit oder größeren Veränderungen das Profil komplett neu aufbauen will. Dann wird `setup.md` erneut durchlaufen.

---

## Globale Installation nachträglich

Wenn der User zu einem späteren Zeitpunkt entscheidet, den Skill global zu installieren (nachdem er beim ersten Setup "später" gewählt hat oder "nur projekt-lokal"): folge Schritt 8 aus `references/setup.md`.

---

## Pflicht-Regeln

1. **Mechaniken vor Adjektiven.** Output folgt den dokumentierten Mechaniken im Voice-Profile, nicht generischer KI-Sprache.
2. **Kein Voice-Sound ohne Substanz.** Wenn generische KI-Sauce durchrutscht: entfernen.
3. **Format folgt Profil, nicht Standard-KI-Struktur.** Wenn das Profil sagt *"keine Bullet-Listen"*, dann auch wenn die Frage nach einer Aufzählung ruft.
4. **Setup wird vom Skill selbst geführt.** Bei fehlendem Profil nicht auf einen separaten manuellen Workshop verweisen, sondern setup.md selbst abarbeiten (mit User-Mitarbeit für Material und Validierung).
