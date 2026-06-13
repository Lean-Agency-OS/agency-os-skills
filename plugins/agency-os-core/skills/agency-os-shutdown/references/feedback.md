# feedback.md — Feedback-Routing (keine Log-Liste mehr)

*Diese Datei ist **kein** chronologischer Korrektur-Log mehr. Eine Korrektur wird **direkt dorthin geschrieben, wo sie greift** (Enforcement-Ort) — nicht hier gesammelt. Grund: ein 700-Zeilen-Log wird nicht gelesen, also greifen die Regeln nicht. Die alte Log-History liegt vollständig in git (Commit `788e16f`, `git show 788e16f:feedback.md`).*

---

## Erkennung — wann der Reflex greift

Achte auf:
- *"nicht so, lieber so…"* / *"das will ich nicht"* / *"mach das künftig anders"*
- *"genau so, perfekt"* (positive Bestätigung zählt auch, nicht nur Korrekturen)
- *"bitte kürzer / länger / anders"*
- **Implizite Korrekturen:** Markus formuliert um, was ich geschrieben habe
- Eine bestätigte nicht-offensichtliche Präferenz (*"eigentlich…"*, *"merk dir…"*)

---

## Der Reflex (sofort, nicht batchen)

Wenn so ein Signal kommt:

1. **Regel + Why + How-to-apply** sofort an den passenden Enforcement-Ort schreiben (Routing-Tabelle unten). Sofort, weil das Kontext-Window die Korrektur sonst verliert und sie meist gleich wieder gebraucht wird.
2. Brain-Write **nur mit Markus' Bestätigung im aktuellen Turn** (Obsidian-MCP hat keine READ_ONLY-Wall — siehe [`systeme.md` § Obsidian](08-wiki/systeme.md)). Vorher einmal zusammenfassen *was* geschrieben wird.
3. Nie fragen *"soll ich das merken?"* — einfach an den Enforcement-Ort schreiben (nur der Brain-Write braucht den Check aus Schritt 2). Knapp bestätigen wo es gelandet ist (*"Gemerkt in {Ort}."*), dann weitermachen. Kein Drama.

**Why immer mitschreiben:** Die Regel allein sagt *was*, das Why erlaubt das Urteil in Grenzfällen. Format am Ziel-Ort: Regel → **Why:** → **How to apply:**.

---

## Routing — wohin welche Korrektur

| Art der Korrektur | Enforcement-Ort |
|---|---|
| **Voice / Slop / KI-Tells** (Pattern, Tabu, Pointe) | [`voice-profile.md`](01-context/brand/voice-profile.md) (Anti-Patterns sind dort eingearbeitet; universell → zusätzlich ins Kunden-Template) |
| **Brain-Mechanik / Hygiene / Loops / Tags / Persönlichkeit / Reflexe** | [`OS.md`](OS.md) |
| **Ingest / Genauigkeit / Note-Prinzipien / IP-vs-Business / Skill-Ablage** | [`OS.md`](OS.md) |
| **Sub-Agent-Briefing** (Content-Rewrites, Research) | [`founder-notes-hebel.md`](06-projects/plattform/founder-notes-hebel.md) |
| **Content-Format / Kanal** (Carousel, Reel, Newsletter) | die jeweilige SOP in [`08-wiki/sops/`](08-wiki/sops/_index.md) |
| **ICP / Naming / Positionierung / Zielgruppen-Sprache** | [`zielgruppe.md`](01-context/zielgruppe.md) (+ `/icp`-Skill) |
| **Persona-spezifisch** (CTO Linus, CMO Mara, …) | die jeweilige [`07-org/{rolle}/role.md`](07-org/) |
| **Externe Systeme / API / Webhooks / Obsidian / Secrets** | [`systeme.md`](08-wiki/systeme.md) |
| **Framework / Methode** (Grenzen, Negativ-Hinweise) | die jeweilige `09-ip/`-Note |

**Strukturell?** Wenn die Korrektur ein Brain-Prinzip ist (Architektur, Workflow, Persona-Switching), zusätzlich in [`OS.md`](OS.md) verankern.

**Schreibgesperrt — Claude-Code-Briefing statt Paste-Block:** `.claude/skills/` ist aus der Cowork-Session nicht editierbar. Korrekturen an aktiven Skills (z.B. `anti-patterns.md`, `/icp`, `/rechnung`) **nicht** als losen Paste-Block liefern, sondern als **selbst-ausführbares Claude-Code-Briefing**: eine `.md`-Datei mit Kontext (eine Zeile, was sich ändert und warum), exaktem Datei-Pfad + Anker-Stelle, fertigem Einfüge-Block und Grep-Verifikation am Schluss. Self-contained schreiben — Claude Code hat den Chat-Kontext nicht. Markus kippt es in Claude Code und lässt es ausführen.

---

## Faustregel

*Wenn du diese Datei aufmachst, um eine Korrektur **einzutragen** — falsch. Hier steht nur, **wohin** sie gehört. Schreib sie dorthin.*
