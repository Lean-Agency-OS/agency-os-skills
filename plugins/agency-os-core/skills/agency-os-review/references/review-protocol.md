# Review-Protokoll — Agency OS

Am besten Sonntag abend oder Montag morgen. Jeden Schritt einzeln mit dem User durchgehen — nicht alles auf einmal.

> **Brain-Pfade:** Alle Pfade hier sind Defaults. Auflösung pro Pfad: `.agency-os/architecture.md` (falls vorhanden) → sonst per Rolle/Muster suchen (Default-Name zuerst) → sonst Schritt überspringen. Default-Tabelle: `agency-os-start/references/architecture.md`.

---

## Vor dem ersten Wort: Brain lesen

Bevor du eine Frage stellst oder etwas präsentierst:

- `{working-memory}` — Current Focus, Active Threads, Key Numbers
- `{open-loops}` — alle offenen Loops, Aging-Check (Einträge mit Datum > 2 Wochen)
- `{logs}/` — letzte 3-7 Tages-Files, neueste zuerst
- Falls eine Rollen-/Org-Struktur mit Wetten existiert (z.B. `{roles}/<rolle>/_wetten.md`): aktive Wetten, ob sich was bewegt hat. Sonst überspringen.

Erst lesen. Dann denken. Dann anfangen.

---

## Schritt 1: Inbox leeren

1. Lies alle Files in `{inbox}/` (typisch: `_index.md` und lose Captures).
2. Falls leer: kurz benennen, weiter.
3. Falls Items vorhanden: jedes einzeln zeigen, dann fragen:
   - **Machen** - Als Loop in `{open-loops}` eintragen (Format: `- [ ] [YYYY-MM-DD] Titel → Link`)
   - **Projekt** - Als `{projects}/{name}/_index.md` anlegen oder bestehendes updaten
   - **Klient/Lead** - In `{clients}/` oder `{sales}/leads/`
   - **IP/Lernstoff** - In `{ip}/patterns/` oder `{ip}/os-kandidaten/`
   - **Löschen** - Entfernen, kein Archiv nötig wenn wertlos
4. Nach Verarbeitung: Inbox leeren (keine Leichen stehen lassen).

---

## Schritt 2: Open Loops prüfen + altern lassen

1. Lies `{open-loops}` vollständig.
2. **Aging-Marker setzen:** Jeder Loop mit Datum older als 14 Tage bekommt einen Kommentar `#aging` (direkt in der Zeile, am Ende).
3. Pro altem Loop mit dem User klären: *"Noch relevant? Erledigt? Oder eskalieren zu einer Entscheidung?"*
   - Erledigt: `[x]` setzen, wird beim nächsten Ingest ins Log transferiert und gelöscht
   - Nicht mehr relevant: löschen
   - Eskalation nötig: `#entscheidung` Tag hinzufügen und in der aktuellen Session ansprechen
4. Neue Loops aus dem Review direkt hier eintragen, nicht in einem separaten To-Do-System.

**Loop-Aging-Regel:** Ein Loop der 4 Wochen alt ist ohne Bewegung, ist entweder eine versteckte Entscheidung oder ein stiller Verzicht. Beides ist valide — aber beides muss bewusst sein.

---

## Schritt 3: Projekte updaten

1. Lies `{projects}/_index.md` für die aktive Projektliste.
2. Frag: *"Was hat sich bei den Projekten bewegt?"*
3. Status in den jeweiligen `{projects}/{name}/_index.md` aktualisieren (Frontmatter: `proposal/active/done`).
4. Abgeschlossene Projekte: in `{archive}/projekte/` verschieben, `{projects}/_index.md` bereinigen.
5. `{working-memory}` prüfen: Spiegeln die Active Threads noch die Realität? Wenn nicht, `{working-memory}` aktualisieren.

---

## Schritt 4: Muster spiegeln — der eigentliche Review

Das ist der Schritt, der den Review vom Abhaken unterscheidet.

**Drei Kategorien, die du aktiv prüfst:**

**a) Faktische Spiegelung** — Was ist tatsächlich passiert vs. was war geplant?
Beispiel: *"Laut Log warst du 4 von 5 Tagen im Operativen, kein einziger Marketing-Block."*

**b) Muster-Spiegelung** — Was passiert wiederholt, ohne dass es bewusst entschieden wurde?
Beispiel: *"Das ist die dritte Woche in Folge, wo Klienten-Arbeit die eigene Content-Pipeline verdrängt."*
Wenn ein Muster da ist: aussprechen. Auch wenn unangenehm. Besonders dann.

**c) Wetten-Check** (nur falls eine Wetten-Struktur existiert, z.B. `{roles}/<rolle>/_wetten.md`) — Haben sich aktive Wetten bewegt? Gibt es neue Evidenz, die eine Wette stützt oder widerlegt?

**Dann: eine Frage stellen, die trifft.**

Eine Frage. Nicht fünf. Der User hat keinen Mangel an Optionen, er hat einen Mangel an Klarheit.

Gute Fragen für Reviews:
- *"Was hast du diese Woche vermieden, obwohl du wusstest, dass es dran wäre?"*
- *"Was wäre anders gelaufen, wenn du auf die Wette letzte Woche gewettet hättest?"*
- *"Was ist das eigentliche Problem hinter dem Loop, der schon 3 Wochen hängt?"*
- *"Was wäre der kleinste Schritt, der die Situation in 7 Tagen sichtbar verändert?"*

**Anti-Patterns in diesem Schritt:**
- Kein Schmeicheln (*"tolle Woche"*, *"du machst das gut"*). Das tötet die Spiegel-Funktion.
- Keine Liste mit "5 Optionen". Wenn du aus dem Review eine Empfehlung ziehst, sag sie.
- Keine Therapie-Sprech (*"das muss schwer sein"*). *"Was hält dich ab?"* schon.
- Kein Beschönigen wenn die Woche dünn war. Dünn benennen.

---

## Schritt 5: Weekly Log schreiben

Tages-Log `{logs}/YYYY-MM-DD.md` (heutiges Datum) anlegen oder ergänzen:

```markdown
## [YYYY-MM-DD] <name>-session | weekly-review KW{WW}

**Was ist passiert:** 3-5 Punkte, konkret, mit Datums-Anker.

**Was lief gut:** Substanzielles, was wir wiederholen oder ausbauen sollten.

**Was hakte:** Hindernisse, gebrochene Routinen, verlorene Wetten, Verschiebungen.

**Muster:** 1-2 Beobachtungen die in Einzelpunkten untergehen.

**Key Learning:** 1-3 Sätze. Was bleibt.
```

Kein generischer Management-Sprech. Kein künstliches Auffüllen wenn die Woche dünn war.

---

## Schritt 6: Nächste Woche planen

1. Frag: *"Was sind die Top 3 für nächste Woche?"*
2. Prioritäten klar benennen (kein Alias-Liste mit 10 Items):
   - **P0** (muss diese Woche): max. 3 Items
   - **P1** (sollte diese Woche): weitere wichtige Items
   - **P2** (nice to have / falls Zeit bleibt)
3. In `{open-loops}` als neue Einträge oder Update bestehender Einträge — oder in `{working-memory}` als Current Focus wenn es wirklich das Wichtigste ist.
4. Abschluss: *"Review fertig."* Kein Motivations-Outro.

---

## Atomare Note, wenn Einsicht entsteht

Wenn aus dem Review ein Pattern, eine Methode oder eine Klient-Erkenntnis entsteht, die wert ist zu kompoundieren:

- Pattern über Klienten hinweg - `{ip}/patterns/`
- Methode/Framework-Idee - `{ip}/os-kandidaten/`
- Selbst-Erkenntnis des Users - das User-Profil in `{context}/` ergänzen
- Klient-Insight - `{clients}/{name}/{name}.md` ergänzen

Frag: *"Soll ich das als Note ablegen?"* Nicht autonom schreiben.

---

## Regeln

- Geduldig — Review braucht Zeit, kein Hetzen
- Jeden Schritt einzeln durchgehen
- Keine destruktiven Änderungen: alte Logs/Reviews bleiben, auch revidierte
- Markdown-Links in alle neuen Einträge
- Datum immer ISO-Format (`YYYY-MM-DD`)
- Wenn Logs fehlen für einzelne Tage: im Review-Log benennen, nicht aus dem Bauch füllen
- Wenn der User der Spiegelung widerspricht und das Brain das Gegenteil belegt: mit Zitat dagegen halten, nicht einknicken

---

## Edge Cases

- **Inbox leer und Logs fehlen:** Review trotzdem machen mit dem was da ist, Datenlücken benennen.
- **Loops aus der Vorwoche bereits in `{working-memory}` eingetragen:** Kein Doppel-Eintrag — nur prüfen ob der Stand noch stimmt.
- **Mehrere Projekte mit unklarem Status:** Eskalieren als `#entscheidung` Loop, nicht stellvertretend entscheiden.
- **User ist im Stress-Modus:** Schritt 4 (Muster-Spiegelung) trotzdem nicht überspringen. Gerade dann ist er relevant — aber Spiegelung kommt vor Frage, erst Resonanz dann Schärfe.
- **Review-Modus zieht sich über mehrere Turns:** Aktiv bleiben, nicht resetten. Wenn der User eine konkrete Aufgabe stellt (*"schreib mir X"*), Modus verlassen und liefern, dann zurück.
