# Capture-Routing

Wenn der User etwas festhalten will, kategorisiere automatisch und schreibe in die korrekte Datei. Pfade sind root-relativ (der Skill laeuft vom Brain-Root).

---

## Kategorien und Zieldateien

| Kategorie | Erkennung | Zieldatei | Sektion |
|---|---|---|---|
| **TASK** | Konkrete Aufgabe, klares Ergebnis, braucht Aktion | `02-strategy/current-priorities.md` | Passende Prioritaet (P0/P1/P2) oder thematische Sektion |
| **IDEE** | Vage, braucht Reifung, kein klarer naechster Schritt | `00-inbox/capture.md` | Append am Ende |
| **LOOP** | Wartet auf jemanden oder etwas Externes | `02-strategy/open-loops.md` | `## Wartend auf...` |
| **ENTSCHEIDUNG** | Muss entschieden werden, Optionen vorhanden | `02-strategy/open-loops.md` | `## Offene Entscheidungen` (+ Tag `#entscheidung`) |
| **QUICK NOTE** | Fakt, Zahl, Beobachtung, Kontext-Snippet | `00-inbox/capture.md` | Append am Ende |

**Faustregel:** Im Zweifel -> `00-inbox/capture.md`. Wird beim naechsten Ingest oder Review korrekt einsortiert.

---

## Format je Zieldatei

**`02-strategy/current-priorities.md`** (Tasks):
```
- [ ] [YYYY-MM-DD] **Titel** -> Kurzbeschreibung. [datei.md](../<ordner>/datei.md)
```
Prioritaeten: `P0` heute/morgen · `P1` diese Woche · `P2` spaeter. In die passende thematische Sektion oder Prioritaet einsortieren.

**`02-strategy/open-loops.md`** (Loops + Entscheidungen):
```
- [ ] [YYYY-MM-DD] **Titel** -> wartet auf ... [datei.md](../<ordner>/datei.md)
- [ ] [YYYY-MM-DD] **Titel** -> ... #entscheidung
```
Loops in `## Wartend auf...`, Entscheidungen in `## Offene Entscheidungen`. Marker: `[ ]`, `#entscheidung` am Ende, `[x]` = erledigt.

**`00-inbox/capture.md`** (Ideen + Quick Notes):
```
- [YYYY-MM-DD] {Gedanke oder Quick Note}
```
Append am Ende. Existiert die Datei noch nicht, anlegen. Beim naechsten Ingest/Review einsortiert und entfernt.

---

## Cross-Link-Regeln

Wenn ein Item klar zugeordnet werden kann, Link direkt im Eintrag setzen. Die Zieldateien liegen alle eine Ebene tief (`02-strategy/`, `00-inbox/`), also Cross-Links mit **`../`** davor:
- Klient: `[name](05-clients/{name}/{name}.md)`
- Projekt: `[name](06-projects/{name}.md)`
- Lead / Sales: `[name](04-sales/leads/{name}/{name}.md)`
- Rolle: `[rolle](07-org/{rolle}/role.md)`
- IP / Framework: `[name](09-ip/{name}.md)`

---

## Routing-Hinweis nach Capture (was beim naechsten Ingest passiert)

Beim Bestaetigen immer mitliefern, wohin das Item beim naechsten `/ingest` weiterwandert:

| Eintrag-Typ | Wandert beim Ingest nach |
|---|---|
| Klient-Bezug | `05-clients/{name}/` |
| Projekt-Bezug | `06-projects/{name}.md` |
| Sales-Lead | `04-sales/leads/{name}/` |
| Marketing-Idee | `03-marketing/content/ideen.md` |
| Methode / Framework | `09-ip/{name}.md` |
| Strategie-Entscheidung | bleibt in `02-strategy/open-loops.md` bis entschieden |
| Rollen-Task | `07-org/{rolle}/_todos.md` |
| Unsortiert | bleibt in `00-inbox/capture.md` bis naechstes Review |

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
| "Morgen Klaus anrufen wegen Command-Center" | TASK | `02-strategy/current-priorities.md` | `- [ ] [2026-06-11] **Klaus anrufen wegen E-Mail-Command-Center** -> Naechster Hebel nach Overload-Session. [klaus-buchroithner.md](05-clients/klaus-buchroithner/klaus-buchroithner.md)` |
| "Idee: Newsletter mit Case-Study-Format testen" | IDEE | `00-inbox/capture.md` | `- [2026-06-11] Idee: Newsletter mit Case-Study-Format testen` |
| "Ben Klinger wartet auf AI-First-Playbook-Launch" | LOOP | `02-strategy/open-loops.md` | `- [ ] [2026-06-11] **Ben Klinger: Nachfassen wenn AI-First-Playbook live** -> [slide-funnels.md](04-sales/leads/slide-funnels/slide-funnels.md)` |
| "Soll ich Skool wirklich noch mal evaluieren?" | ENTSCHEIDUNG | `02-strategy/open-loops.md` | `- [ ] [2026-06-11] **Skool Community re-evaluieren?** -> Letzte Evaluation in [skool-community-evaluation.md](02-strategy/skool-community-evaluation.md) #entscheidung` |
| "Bottleneck Audit hat heute 2 Completions gehabt" | QUICK NOTE | `00-inbox/capture.md` | `- [2026-06-11] Bottleneck Audit: 2 Completions heute (Key Numbers beim naechsten Ingest updaten)` |
| "Mario braucht noch die AP2-Verifikation" | TASK | `02-strategy/current-priorities.md` | `- [ ] [2026-06-11] **Mario AP2 verifizieren** -> [lastenheft.md](06-projects/mario-grabner-brain-build/lastenheft.md)` |
