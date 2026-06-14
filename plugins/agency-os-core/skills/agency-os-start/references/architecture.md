# Architektur (Brain-Pfad-Auflösung)

Die Brain-Ordner heißen nicht in jedem Brain gleich (mal `08-wiki/`, mal `08-knowledge/`, manchmal gar nicht). Skills sprechen Ordner deshalb über ihre **Rolle** an, nicht über den festen Namen.

## Auflösungsregel (jeder Skill, jeder Pfad)

Pro benötigter Rolle in dieser Reihenfolge:

1. **Architektur-Datei zuerst:** Existiert `.agency-os/architecture.md` im Brain-Root und nennt die Rolle, nutze den dort hinterlegten Pfad.
2. **Sonst Rolle/Glob:** Such den Ordner über sein Muster, der kanonische Default-Name ist die erste Wahl (z.B. Logs = `*logs*`, Wissen = `08-*` bzw. `*wiki*`/`*knowledge*`, Strategie = `*strategy*`).
3. **Sonst überspringen:** Wird nichts gefunden, den jeweiligen Schritt auslassen, nicht blockieren.

## Rollen → Default-Pfad

| Rolle | Default | Inhalt |
|---|---|---|
| `inbox` | `00-inbox/` | Ersterfassung, Captures |
| `context` | `01-context/` | User-Profil, Zielgruppe, Tool-/Brand-Kontext, Exporte |
| `strategy` | `02-strategy/` | Arbeitsspeicher + offene Loops |
| `working-memory` | `02-strategy/hot.md` | Current Focus, Active Threads, Key Numbers |
| `open-loops` | `02-strategy/open-loops.md` | offene Tasks/Entscheidungen |
| `sales` | `04-sales/` | Leads, Pipeline |
| `clients` | `05-clients/` | Kunden |
| `projects` | `06-projects/` | Projekte |
| `roles` | `07-org/` | Rollen/Personas (optional, siehe Start-Skill Step 8) |
| `knowledge` | `08-wiki/` | Wiki/Knowledge/SOPs/Systeme |
| `ip` | `09-ip/` | Patterns, Frameworks, OS-Kandidaten |
| `logs` | `10-logs/` | Tages-Logs (`YYYY-MM-DD.md`) |
| `archive` | `11-archive/` | Archiv |

## Datei im Brain (`.agency-os/architecture.md`)

Der **start-Skill pflegt diese Datei automatisch**: Bei jedem Start wird die Top-Level-Struktur gescannt und mit der Datei abgeglichen - fehlt sie, wird sie aus der erkannten Struktur geschrieben; ändert sich die Struktur später (Ordner umbenannt/entfernt/neu), werden die betroffenen Zeilen aktualisiert (Drift-Check). Die Datei wird committet und gilt damit für alle Klone; ein Brain kann sie auch von Hand vorgeben.

Format: eine Zeile pro Rolle, fehlende Zeilen fallen auf Default/Glob zurück.

```markdown
# Agency OS - Architektur

- inbox: 00-inbox/
- context: 01-context/
- working-memory: 02-strategy/hot.md
- open-loops: 02-strategy/open-loops.md
- logs: 10-logs/
- knowledge: 08-knowledge/
```
