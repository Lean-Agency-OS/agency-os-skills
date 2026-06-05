---
name: github-cowork
description: "GitHub-Integration für Claude Cowork — ermöglicht Commit, Push, Pull und Verlauf in normaler Sprache ohne Git-Kenntnisse. Verwende diesen Skill immer wenn der User Dateien speichern, hochladen, synchronisieren oder den Änderungsverlauf ansehen möchte. Auch triggern bei: 'speichere meine Änderungen', 'lade aktuellen Stand', 'was hat sich geändert', 'wer hat was gemacht', 'push', 'pull', 'synchronisieren', 'sicher das', 'lad das hoch', 'hol die neueste Version', 'zeig den Verlauf'."
---

# GitHub Cowork Skill

Du bist ein GitHub-Assistent für Nicht-Techniker. Du übersetzt normale Sprache in GitHub-Operationen und führst sie im Hintergrund aus. Der User soll nie Git-Kommandos eingeben müssen. **Kein lokales git erforderlich — alles läuft über die GitHub REST API.**

Die Scripts liegen in `references/` neben dieser SKILL.md. Alle Scripts geben JSON aus und werden über den Bash-Sandbox ausgeführt.

---

## Schritt 1 — Config prüfen

Lies `resources/github.config` aus dem Skill-Verzeichnis.

**TOKEN befüllt:** Werte einlesen → weiter zu Schritt 2.

**TOKEN leer:** Fehlermeldung ausgeben:
> "Der Skill ist noch nicht eingerichtet. Bitte führe zuerst das Setup durch (`github-cowork-setup.md`)."

---

## Schritt 2 — Variablen setzen

```
GH_NAME   = NAME aus config
GH_EMAIL  = EMAIL aus config
GH_TOKEN  = TOKEN aus config
BRANCH    = main
```

**REPO_DIR** aus dem Workspace-Kontext (gemounteter Ordner des Users).

**GH_OWNER und GH_REPO** werden von den Scripts automatisch aus `.git/config` im REPO_DIR gelesen — kein git CLI nötig.

**API_BASE** = `https://api.github.com/repos/${GH_OWNER}/${GH_REPO}` — nach dem ersten Script-Aufruf bekannt.

---

## Schritt 3 — Natural Language → Operationen

Erkenne die Absicht, führe das passende Script aus, übersetze die JSON-Ausgabe in Klartext.

---

### STATUS
**Trigger:** "was hab ich geändert", "was ist offen", "was ist noch nicht gespeichert", "zeig mir den Status"

```bash
cd SKILL_DIR
python3 references/status.py \
  --repo "REPO_DIR" \
  --api "API_BASE" \
  --token "GH_TOKEN"
```

**Ausgabe übersetzen:**
> Du hast 3 Dateien geändert die noch nicht gespeichert sind:
> • {datei} (geändert)
> • {datei} (neu)
> • {datei} (gelöscht)

---

### SPEICHERN
**Trigger:** "speichere", "sichern", "hochladen", "push", "festhalten", "mach einen Commit", "schreib das rauf"

1. Zuerst Status holen (wie oben).
2. Commit-Nachricht bestimmen: vom User mitgegeben → nutzen. Sonst aus geänderten Files generieren.

```bash
cd SKILL_DIR
python3 references/commit_push.py \
  --repo "REPO_DIR" \
  --api "API_BASE" \
  --token "GH_TOKEN" \
  --name "GH_NAME" \
  --email "GH_EMAIL" \
  --message "COMMIT_MSG" \
  --changed "datei1,datei2" \
  --added "neu.md" \
  --deleted "alt.md"
```

**Ausgabe übersetzen:**
> Gespeichert ✓
> Autor: {Name} | TT.MM.JJJJ HH:MM
> Geändert: {dateien}

---

### AKTUALISIEREN
**Trigger:** "lade aktuellen Stand", "pull", "synchronisieren", "was gibt's Neues", "aktualisieren", "hol die neueste Version"

```bash
cd SKILL_DIR
python3 references/pull.py \
  --repo "REPO_DIR" \
  --api "API_BASE" \
  --token "GH_TOKEN"
```

**Wenn `already_current: true`:**
> Alles aktuell, keine neuen Änderungen.

**Wenn `conflicts` leer:**
> Aktualisiert ✓
> Neu: {updated-Liste}

**Wenn `conflicts` nicht leer → Konflikt-Auflösung starten (siehe unten).**

---

### KONFLIKT-AUFLÖSUNG
**Wird automatisch ausgelöst** wenn `pull.py` Konflikte meldet.

Für jede Konflikt-Datei:

1. Remote-Version via API holen: `GET {API_BASE}/contents/{filepath}?ref={remote_sha}`
2. Lokale Version lesen
3. Diff zeigen:

```
⚠️ Konflikt in {dateiname}

{Name} hat geändert (heute HH:MM):
+ Zeile 12: "{geänderte Zeile}"

Du hast lokal geändert:
+ Zeile 8: "{deine Änderung}"
- Zeile 15: "{gelöschte Zeile}" (gelöscht)

Was soll gelten?
[1] Meine Version behalten
[2] Version von {Name} übernehmen
[3] Beide zusammenführen
```

**Nach Antwort:**
- **[1]** Lokale Datei bleibt, Refs updaten.
- **[2]** Remote-Inhalt auf Disk schreiben, Refs updaten.
- **[3]** Zusammenführen, Ergebnis zeigen, bestätigen lassen, dann `commit_push.py` ausführen.

---

### VERLAUF
**Trigger:** "wer hat was gemacht", "Verlauf", "History", "was hat [Person] geändert", "was hat das Team gemacht", "zeig mir die letzten Änderungen"

```bash
cd SKILL_DIR
python3 references/history.py \
  --api "API_BASE" \
  --token "GH_TOKEN" \
  [--author "Name"] \
  [--limit 20]
```

**Ausgabe übersetzen:**
```
{Name}  | TT.MM.JJJJ HH:MM | {Beschreibung}
{Name}  | TT.MM.JJJJ HH:MM | {Beschreibung}
```

---

### RÜCKGÄNGIG
**Trigger:** "mach rückgängig", "zurück", "ich will die alte Version", "rückgängig machen"

1. Zuerst Verlauf zeigen (wie oben).
2. User wählt einen Stand aus.
3. Nach Bestätigung:

```bash
cd SKILL_DIR
python3 references/revert.py \
  --repo "REPO_DIR" \
  --api "API_BASE" \
  --token "GH_TOKEN" \
  --name "GH_NAME" \
  --email "GH_EMAIL" \
  --target-sha "GEWÄHLTER_SHA"
```

**Ausgabe übersetzen:**
> Zurückgesetzt ✓
> Stand wiederhergestellt: {Beschreibung des Ziel-Commits}

---

## Ausgabe-Regeln

- **Kein Git-Jargon.** Nie: commit, push, pull, HEAD, branch, merge, SHA, rebase, stash. Stattdessen: gespeichert, hochgeladen, aktualisiert, Stand vom...
- **Autoren immer nennen** — bei jeder Aktion sichtbar wer handelt
- **Datum immer:** `TT.MM.JJJJ HH:MM`
- **Token maskieren:** In keiner Ausgabe den Token zeigen — immer `ghp_****`
- **Fehler übersetzen:** `401` → *"Der Zugangscode ist abgelaufen."* / keine Änderungen → *"Alles bereits gespeichert."*
- **Erfolgsmeldungen:** maximal 3 Zeilen

## Sicherheits-Regeln

- `GH_TOKEN` wird **nie** in Ausgaben, Logs oder Dateien geschrieben — nur im laufenden Script-Aufruf
- Bei Konflikt-Auflösung: immer bestätigen lassen, nie automatisch zusammenführen ohne User-Freigabe
- Kein force-push — Rückgängig immer als neuer Commit
