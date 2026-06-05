# Capture-Routing

Wenn der User etwas festhalten will, kategorisiere automatisch.

## Kategorien

| Kategorie | Erkennung | Zieldatei | Sektion |
|---|---|---|---|
| **TASK** | Konkrete Aufgabe, klares Ergebnis, braucht Aktion | `02-strategy/current-priorities.md` | Passende Priorität (P0/P1/P2) |
| **IDEE** | Vage, braucht Reifung, kein klarer nächster Schritt | `00-inbox/capture.md` | Append am Ende |
| **LOOP** | Wartet auf jemanden/etwas Externes | `02-strategy/open-loops.md` | Sektion "Wartend auf..." |
| **ENTSCHEIDUNG** | Muss entschieden werden, Optionen vorhanden | `02-strategy/open-loops.md` | Sektion "Offene Entscheidungen" |

## Prioritäten für Tasks

- **P0** - Heute oder morgen erledigen
- **P1** - Diese Woche
- **P2** - Später / Mittelfristig

## Regeln

- Im Zweifel → IDEE in Inbox (wird beim Review sortiert)
- Relative Daten in absolute umwandeln ("Donnerstag" → konkretes Datum)
- **Kunden-Bezug automatisch verlinken:** Wenn ein Item einem Kunden zugeordnet werden kann, Markdown-Link `[kunde](../03-clients/{kunde}/_index.md)` im Eintrag setzen. Cross-Filter über die Verlinkung möglich. (Pfad relativ zur Datei, in die geschrieben wird, z.B. `02-strategy/current-priorities.md` → `../03-clients/{kunde}/_index.md`)
- **Projekt-Bezug:** Markdown-Link `[projekt](../04-projects/{projekt}/_index.md)` analog
- Personen: `[name](../05-org/{name}.md)` für Team, `[name](../03-clients/{kunde}/stakeholder/{name}.md)` für externe
- Immer bestätigen: "Gespeichert in `dateiname.md` als [Kategorie]."
- Dann fragen: "Noch was?"
- Append-only: nichts überschreiben, immer hinzufügen

## Beispiele

| User-Input | Kategorie | Datei | Eintrag (mit Markdown-Links) |
|---|---|---|---|
| "Morgen 3 LinkedIn-Posts für Acme schreiben" | TASK (P0) | `02-strategy/current-priorities.md` | `- [ ] 3 LinkedIn-Posts für [acme](../03-clients/acme/_index.md) schreiben` |
| "Acme will CPA < 25€" | LOOP / KPI-Info | `02-strategy/open-loops.md` oder direkt `03-clients/acme/kpis.md` | je nach User-Intent fragen |
| "Idee: Newsletter-Refresh für BetaCorp" | IDEE | `00-inbox/capture.md` | `- Newsletter-Refresh für [betacorp](../03-clients/betacorp/_index.md) - aufgekommen 2026-05-13` |
| "Sandra wartet auf Briefing-Approval" | LOOP | `02-strategy/open-loops.md` | `Wartet auf Sandra ([sandra](../03-clients/acme/stakeholder/sandra.md)) - Briefing-Approval seit 2026-05-13` |
