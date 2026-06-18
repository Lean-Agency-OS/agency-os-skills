---
name: agency-os-github
version: 1.0.0
description: Offene Änderungen sauber auf GitHub sichern (committen + pullen mit Rebase + pushen) und Konflikte auflösen, damit alles für alle verfügbar und auf dem neuesten Stand ist. Verwende wenn der User "sichere die offenen Änderungen", "offene Änderungen sichern", "committen", "commit", "sichern", "verfügbar machen", "speichern für alle", "sauber machen", "aktualisieren", "neuesten Stand holen", "pull", "mergen", "Konflikt auflösen" oder den Copy-Paste-Prompt aus dem Session-Start-Hinweis nutzt.
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git push) Bash(git push *) Bash(git pull *) Bash(git rebase *)
---

# Agency OS - Github

Offene Änderungen sichern, damit sie nicht nur lokal liegen, sondern für alle verfügbar sind. Sprich in einfacher, nicht-technischer Sprache. "Sichern" statt "committen", "verfügbar machen" statt "pushen". Git-Begriffe nur, wenn der User sie selbst nutzt.

## Bash-Regeln (Prompt-Vermeidung)

Damit dieser Skill ohne unnötige Permission-Rückfragen läuft, beim Bauen von Befehlen:
- **Lesen/Status** (`git status`, `git diff`, `git log`) ist read-only und läuft prompt-frei. Keine Command-Substitution `$(...)` und keine Backticks drumherum bauen.
- **Keine Interpreter** (`python3`/`node`/`perl`/`awk`) für Ad-hoc-Logik.
- Die Git-Schritte dieses Skills (`git add`, `git commit`, `git push`, `git pull --rebase`, `git rebase --continue/--abort`) sind über `allowed-tools` im Frontmatter **prompt-frei erlaubt**. Der Schutz ist hier **nicht** der Permission-Prompt, sondern die **Klartext-Rückfrage im Workflow**: erst Änderungen zusammenfassen + Commit-Vorschlag bestätigen lassen (Schritt 4 / Regel „nie ohne Bestätigung committen"), dann sichern. `mv`/`rm` und andere mutierende Shell-Befehle bleiben bestätigungspflichtig.

## Workflow

1. **Status holen** (still): `git status --porcelain` und `git diff --stat` für den Überblick. Bei Bedarf `git status` für untracked Ordnerinhalte.
2. **Nichts offen?** Kurz bestätigen: "Alles sauber, hier liegt nichts Ungesichertes." Ende.
3. **Etwas offen?** Die Änderungen in einfacher Sprache zusammenfassen, gruppiert nach Thema, nicht als rohe Dateiliste. Beispiel:
   - "Du hast diese Woche am Content-Mining-Skill und an der OS-Anleitung gearbeitet."
   - "Dazu kommen zwei neue Tageslogs."
4. **Vorschlag machen:** Eine sinnvolle Commit-Aufteilung vorschlagen (meist 1 Commit, bei klar getrennten Themen mehrere) inkl. kurzer Commit-Message auf Deutsch. Den User bestätigen lassen.
5. **Sichern:** Nach Bestätigung `git add` der besprochenen Files + `git commit`. Nie `git add -A` blind über alles, wenn der User nur einen Teil sichern wollte.
6. **Aktualisieren (Pull mit Rebase):** Vor dem Hochladen den neuesten Stand vom Remote holen und die eigenen Commits sauber obendrauf setzen: `git pull --rebase`. So bleibt die History linear, keine unnötigen Merge-Commits. Gibt es dabei Konflikte → Abschnitt "Bei Konflikten". Nach erfolgreichem Pull das **Pull-Datum** ins lokale State-File schreiben (siehe Abschnitt "Lokaler State").
7. **Verfügbar machen:** Nach erfolgreichem Rebase `git push`. Wenn der Rebase die History umgeschrieben hat und der Push abgelehnt wird, NICHT blind `--force` nutzen — erst prüfen, ob jemand anderes auf der Branch arbeitet. Bei eigener Feature-Branch ist `git push --force-with-lease` okay, auf `main` vorher kurz Rücksprache. Nach erfolgreichem Push das **Push-Datum** ins State-File schreiben.

Auch wenn lokal nichts zu committen ist (Schritt 2), darf der User trotzdem „aktualisieren" wollen → dann nur Schritt 6 (`git pull --rebase`) ausführen, um den neuesten Stand zu holen.

## Output

Commit + Pull (Rebase) + Push der besprochenen Änderungen, Pull-/Push-Datum in `.agency-os/state.md` (lokal, nicht committet), plus Klartext-Feedback im Chat ("Erledigt, ist jetzt gesichert").

## Lokaler State (`.agency-os/state.md`)

Hält fest, wann zuletzt aktualisiert (Pull) und gesichert (Push) wurde. **Lokal pro Arbeitskopie, steht in `.gitignore`, wird nie committet** — sonst gäbe es bei jedem Pull Konflikte und falsche Daten auf anderen Klonen.

- Datum/Uhrzeit immer per `date '+%Y-%m-%d %H:%M'` holen, nicht raten.
- Ordner ggf. anlegen, Datei überschreiben (immer nur der aktuellste Stand):

```markdown
# Agency OS - Lokaler State

> Lokal pro Arbeitskopie. Nicht committen. Wird von agency-os-github gepflegt.

- Zuletzt aktualisiert (Pull): YYYY-MM-DD HH:MM
- Zuletzt gesichert (Push): YYYY-MM-DD HH:MM
```

Beim Schreiben nur das jeweils ausgeführte Feld aktualisieren, das andere unverändert lassen.

## Bei Konflikten (während `git pull --rebase`)

Ein Konflikt heißt nur: dieselbe Stelle wurde an zwei Orten geändert. In einfacher Sprache erklären, nicht mit Git-Begriffen erschlagen.

1. **Konfliktdateien finden:** `git status` zeigt die betroffenen Files (unter "Unmerged paths").
2. **Pro Datei verstehen:** Konfliktmarker (`<<<<<<<`, `=======`, `>>>>>>>`) lesen. Oben steht der Remote-Stand, unten der eigene.
3. **Auflösen nach Sinn, nicht mechanisch:**
   - Sind es **unterschiedliche, ergänzende Inhalte** (z. B. zwei neue Einträge in einem Index/Log): beide behalten, sinnvoll zusammenführen.
   - Ist es **dieselbe Stelle mit echtem Widerspruch:** dem User die zwei Varianten in Klartext zeigen und ihn entscheiden lassen, welche gewinnt. Nicht raten.
4. **Marker entfernen**, Datei sauber speichern, dann `git add <datei>`.
5. **Weiter:** `git rebase --continue`. Nächster Konflikt → wiederholen.
6. **Wenn es zu unklar oder riskant wird:** `git rebase --abort` (bringt alles in den Zustand vor dem Pull zurück), dem User erklären was kollidiert und gemeinsam entscheiden.
7. Nach sauberem Rebase weiter mit Schritt 7 (push).

Regeln für Konflikte:
- Nie eine Seite blind verwerfen (`-X ours`/`-X theirs`) ohne Rücksprache, außer der User sagt explizit, welche Version gewinnen soll.
- Bei inhaltlichen Widersprüchen immer den User entscheiden lassen, nie selbst eine Variante „erfinden".
- Nach dem Auflösen kurz in Klartext zusammenfassen, was zusammengeführt wurde.

## Commit-Message-Konvention

- Deutsch, knapp, im Imperativ oder als kurze Beschreibung
- Bei Skills/OS-Änderungen Präfix wie `feat:`, `fix:`, `chore:`, `refactor:` okay, aber kein Zwang

## Regeln

- Nie automatisch committen ohne Bestätigung des Users.
- Nie blind alles sichern, wenn der User nur einen Teil meinte, erst nachfragen.
- `.claude/settings.local.json` und andere private/lokale Files bleiben außen vor (stehen i.d.R. in `.gitignore`).
- Sensible oder versehentlich offene Files (Secrets, große Binaries, `.env`) vor dem Sichern flaggen statt mitcommitten.
- Wenn die Branch nicht die Main-Branch ist oder ein offener Merge/Rebase läuft, kurz hinweisen bevor gesichert wird.
- Klartext-Feedback nach dem Sichern: "Erledigt, ist jetzt gesichert" (+ Hinweis, falls noch nicht gepusht).
