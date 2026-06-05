# Weekly Review Protokoll

Am besten Sonntag abend oder Montag morgen. Jeden Schritt einzeln mit dem User durchgehen.

---

## Schritt 1: Inbox leeren

1. Lies `00-inbox/capture.md` (falls vorhanden) und sonstige Files in `00-inbox/`
2. Falls leer: "Inbox ist leer - weiter zum nächsten Schritt."
3. Falls Items vorhanden: Jedes Item einzeln zeigen und fragen:
   - **Machen** → Als Task in `02-strategy/current-priorities.md` eintragen (P0/P1/P2)
   - **Planen** → Als Projekt in `04-projects/{name}/_index.md` oder als Loop in `02-strategy/open-loops.md`
   - **Löschen** → Entfernen
4. Nach Verarbeitung: Inbox leeren (Header behalten falls capture.md)

---

## Schritt 2: Open Loops prüfen

1. Lies `02-strategy/open-loops.md`
2. Loops älter als 2 Wochen markieren
3. Pro altem Loop fragen: "Noch relevant? Erledigt? Oder eskalieren?"
4. Aktualisieren: Erledigtes in "Erledigt" Sektion verschieben, Irrelevantes löschen

---

## Schritt 3: Projekte updaten

1. Frage: "Was hat sich bei den Projekten bewegt?"
2. Status in den jeweiligen `04-projects/{name}/_index.md` aktualisieren
3. Abgeschlossene Projekte: in den Archiv-Ordner verschieben (der `*-archive/`-Ordner im OS-Root, Unterordner `projects/`)

---

## Schritt 4: Reflexion

3 Fragen stellen (einzeln):

1. **Was lief gut diese Woche?**
2. **Was war schwierig?**
3. **Was nimmst du mit? (Key Learning)**

Antworten werden im Weekly Log festgehalten.

---

## Schritt 5: Weekly Log schreiben

Im Logs-Ordner (`*-logs/`) als `weekly-{{JAHR}}-W{{KW}}.md` schreiben (oder anhängen falls existiert):

```markdown
# KW {{KW}} ({{Datumsbereich}})

## Highlights
- [...]

## Schwierig
- [...]

## Key Learning
[1-3 Sätze]
```

---

## Schritt 6: Nächste Woche planen

1. Frage: "Was sind die Top 3 für nächste Woche?"
2. In `02-strategy/current-priorities.md` unter neuer KW eintragen:
   - **P0** (heute/morgen): Top 3
   - **P1** (diese Woche): weitere wichtige Items
3. Abschluss: "Review fertig. Guter Start in die Woche!"

---

## Regeln

- Geduldig - nicht hetzen
- Jeden Schritt einzeln durchgehen, nicht alles auf einmal
- Markdown-Links in alle Einträge (`[kunde](../03-clients/{kunde}/_index.md)`, `[projekt](../04-projects/{projekt}/_index.md)`)
- Datum im ISO-Format (`YYYY-MM-DD`)
