# Capture-Routing

Wenn der User etwas festhalten will, kategorisiere automatisch und schreibe in die korrekte Datei. Pfade sind root-relativ (der Skill laeuft vom Brain-Root).

> **Brain-Pfade:** Alle Pfade hier sind Defaults, keine festen Namen. Auflösung pro Pfad: `.agency-os/architecture.md` (falls vorhanden) → sonst per Rolle/Muster suchen (Default-Name zuerst) → sonst Default-Pfad anlegen/verwenden. Default-Tabelle: `agency-os-start/references/architecture.md`.

---

## Kategorien und Zieldateien

| Kategorie | Erkennung | Zieldatei | Sektion |
|---|---|---|---|
| **TASK** | Konkrete Aufgabe, klares Ergebnis, braucht Aktion | `{strategy}/current-priorities.md` | Passende Prioritaet (P0/P1/P2) oder thematische Sektion |
| **IDEE** | Vage, braucht Reifung, kein klarer naechster Schritt | `{inbox}/capture.md` | Append am Ende |
| **LOOP** | Wartet auf jemanden oder etwas Externes | `{open-loops}` | `## Wartend auf...` |
| **ENTSCHEIDUNG** | Muss entschieden werden, Optionen vorhanden | `{open-loops}` | `## Offene Entscheidungen` (+ Tag `#entscheidung`) |
| **QUICK NOTE** | Fakt, Zahl, Beobachtung, Kontext-Snippet | `{inbox}/capture.md` | Append am Ende |

**Faustregel:** Im Zweifel -> `{inbox}/capture.md`. Wird beim naechsten Ingest oder Review korrekt einsortiert.

---

## Format je Zieldatei

**`{strategy}/current-priorities.md`** (Tasks):
```
- [ ] [YYYY-MM-DD] **Titel** -> Kurzbeschreibung. [datei.md](../<ordner>/datei.md)
```
Prioritaeten: `P0` heute/morgen · `P1` diese Woche · `P2` spaeter. In die passende thematische Sektion oder Prioritaet einsortieren.

**`{open-loops}`** (Loops + Entscheidungen):
```
- [ ] [YYYY-MM-DD] **Titel** -> wartet auf ... [datei.md](../<ordner>/datei.md)
- [ ] [YYYY-MM-DD] **Titel** -> ... #entscheidung
```
Loops in `## Wartend auf...`, Entscheidungen in `## Offene Entscheidungen`. Marker: `[ ]`, `#entscheidung` am Ende, `[x]` = erledigt.

**`{inbox}/capture.md`** (Ideen + Quick Notes):
```
- [YYYY-MM-DD] {Gedanke oder Quick Note}
```
Append am Ende. Existiert die Datei noch nicht, anlegen. Beim naechsten Ingest/Review einsortiert und entfernt.

---

## Cross-Link-Regeln

Wenn ein Item klar zugeordnet werden kann, Link direkt im Eintrag setzen. Die Zieldateien liegen alle eine Ebene tief (`{strategy}/`, `{inbox}/`), also Cross-Links mit **`../`** davor:
- Klient: `[name]({clients}/{name}/{name}.md)`
- Projekt: `[name]({projects}/{name}.md)`
- Lead / Sales: `[name]({sales}/leads/{name}/{name}.md)`
- Rolle: `[rolle]({roles}/{rolle}/role.md)`
- IP / Framework: `[name]({ip}/{name}.md)`

---

## Routing-Hinweis nach Capture (was beim naechsten Ingest passiert)

Beim Bestaetigen immer mitliefern, wohin das Item beim naechsten `/ingest` weiterwandert:

| Eintrag-Typ | Wandert beim Ingest nach |
|---|---|
| Klient-Bezug | `{clients}/{name}/` |
| Projekt-Bezug | `{projects}/{name}.md` |
| Sales-Lead | `{sales}/leads/{name}/` |
| Marketing-Idee | `{marketing}/content/ideen.md` |
| Methode / Framework | `{ip}/{name}.md` |
| Strategie-Entscheidung | bleibt in `{open-loops}` bis entschieden |
| Rollen-Task | `{roles}/{rolle}/_todos.md` |
| Unsortiert | bleibt in `{inbox}/capture.md` bis naechstes Review |

---

## Regeln

- Append-only: nichts ueberschreiben, immer hinzufuegen
- Relative Zeitangaben in absolute umwandeln ("Donnerstag" -> konkretes Datum)
- Datum immer mitschiessen: `[YYYY-MM-DD]`
- Keine Tiefenverarbeitung hier (das ist Job von `/ingest`)
- Nach dem Schreiben: Bestaetigung + Routing-Hinweis + "Noch was?"

---

## Beispiele

| User-Input | Kategorie | Datei | Eintrag |
|---|---|---|---|
| "Morgen Anna anrufen wegen Onboarding" | TASK | `{strategy}/current-priorities.md` | `- [ ] [2026-06-11] **Anna anrufen wegen Onboarding** -> Naechster Schritt nach Kickoff. [anna-beispiel.md]({clients}/anna-beispiel/anna-beispiel.md)` |
| "Idee: Newsletter mit Case-Study-Format testen" | IDEE | `{inbox}/capture.md` | `- [2026-06-11] Idee: Newsletter mit Case-Study-Format testen` |
| "Kunde Müller wartet auf das Angebot" | LOOP | `{open-loops}` | `- [ ] [2026-06-11] **Kunde Müller: Nachfassen wenn Angebot raus** -> [mueller.md]({sales}/leads/mueller/mueller.md)` |
| "Soll ich Tool X wirklich noch mal evaluieren?" | ENTSCHEIDUNG | `{open-loops}` | `- [ ] [2026-06-11] **Tool X re-evaluieren?** -> Letzte Evaluation in [tool-x-evaluation.md]({strategy}/tool-x-evaluation.md) #entscheidung` |
| "Landingpage hatte heute 2 Conversions" | QUICK NOTE | `{inbox}/capture.md` | `- [2026-06-11] Landingpage: 2 Conversions heute (Key Numbers beim naechsten Ingest updaten)` |
| "Projekt Y braucht noch die finale Freigabe" | TASK | `{strategy}/current-priorities.md` | `- [ ] [2026-06-11] **Projekt Y: finale Freigabe einholen** -> [lastenheft.md]({projects}/projekt-y/lastenheft.md)` |
