# feedback.md - Feedback-Routing (keine Log-Liste)

*Diese Datei ist **kein** chronologischer Korrektur-Log. Eine Korrektur wird **direkt dorthin geschrieben, wo sie greift** (Enforcement-Ort), nicht hier gesammelt. Grund: ein langes Log wird nicht gelesen, also greifen die Regeln nicht.*

Pfade unten sind Rollen-Platzhalter (aufgelöst über `.agency-os/architecture.md`, sonst Standard-Ordnername).

---

## Erkennung: wann der Reflex greift

Achte auf:
- *"nicht so, lieber so…"* / *"das will ich nicht"* / *"mach das künftig anders"*
- *"genau so, perfekt"* (positive Bestätigung zählt auch, nicht nur Korrekturen)
- *"bitte kürzer / länger / anders"*
- **Implizite Korrekturen:** Der User formuliert um, was ich geschrieben habe
- Eine bestätigte nicht-offensichtliche Präferenz (*"eigentlich…"*, *"merk dir…"*)

---

## Der Reflex (sofort, nicht batchen)

Wenn so ein Signal kommt:

1. **Regel + Why + How-to-apply** sofort an den passenden Enforcement-Ort schreiben (Routing-Tabelle unten). Sofort, weil das Kontext-Window die Korrektur sonst verliert und sie meist gleich wieder gebraucht wird.
2. Vor dem Schreiben einmal knapp zusammenfassen, *was* geschrieben wird. Läuft der Brain-Zugriff über ein externes Schreib-Tool ohne eigene Schutzschicht (z.B. ein MCP-Server mit Schreibrechten), den Write nur mit Bestätigung des Users im aktuellen Turn machen.
3. Nie fragen *"soll ich das merken?"*, einfach an den Enforcement-Ort schreiben (nur der Write aus Schritt 2 braucht ggf. die Bestätigung). Knapp bestätigen wo es gelandet ist (*"Gemerkt in {Ort}."*), dann weitermachen. Kein Drama.

**Why immer mitschreiben:** Die Regel allein sagt *was*, das Why erlaubt das Urteil in Grenzfällen. Format am Ziel-Ort: Regel → **Why:** → **How to apply:**.

---

## Routing: wohin welche Korrektur

| Art der Korrektur | Enforcement-Ort |
|---|---|
| **Voice / Slop / KI-Tells** (Pattern, Tabu, Pointe) | das Voice-Profil unter `{context}/brand/voice-profile.md` (falls vorhanden) |
| **Brain-Mechanik / Hygiene / Loops / Tags / Reflexe** | die zentrale Anweisungsdatei des Brains (z.B. `CLAUDE.md`) |
| **Ingest / Genauigkeit / Note-Prinzipien / Ablage** | die zentrale Anweisungsdatei des Brains (z.B. `CLAUDE.md`) |
| **Sub-Agent-Briefing** (Content-Rewrites, Research) | die jeweilige Projekt-Note unter `{projects}/` |
| **Content-Format / Kanal** (Carousel, Reel, Newsletter) | die jeweilige SOP unter `{knowledge}/` (z.B. `{knowledge}/sops/`) |
| **ICP / Naming / Positionierung / Zielgruppen-Sprache** | das ICP-File unter `{context}/` (im Template: `zielgruppe.md`) |
| **Persona-/Rollen-spezifisch** (falls eine Rollen-Struktur existiert) | die jeweilige `{roles}/{rolle}/role.md` |
| **Externe Systeme / API / Webhooks / Secrets** | die System-/Tool-Doku unter `{knowledge}/` |
| **Framework / Methode** (Grenzen, Negativ-Hinweise) | die jeweilige Note unter `{ip}/` |

**Strukturell?** Wenn die Korrektur ein Brain-Prinzip ist (Architektur, Workflow), zusätzlich in der zentralen Anweisungsdatei des Brains verankern.

**Optionales Beispiel, schreibgeschützte Skill-Ordner:** In manchen Umgebungen (z.B. Cowork) ist der Skill-Ordner aus der laufenden Session nicht editierbar. Korrekturen an aktiven Skills (z.B. `/agency-os-capture`, `/agency-os-lint`) dann **nicht** als losen Paste-Block liefern, sondern als **selbst-ausführbares Claude-Code-Briefing**: eine `.md`-Datei mit Kontext (eine Zeile, was sich ändert und warum), exaktem Datei-Pfad + Anker-Stelle, fertigem Einfüge-Block und Grep-Verifikation am Schluss. Self-contained schreiben, Claude Code hat den Chat-Kontext nicht. Der User kippt es in Claude Code und lässt es ausführen.

---

## Faustregel

*Wenn du diese Datei aufmachst, um eine Korrektur **einzutragen**: falsch. Hier steht nur, **wohin** sie gehört. Schreib sie dorthin.*
