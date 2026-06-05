# Secrets-Konvention für Agency-OS-Plugins

Wie Plugins in diesem Marketplace mit API-Keys, Tokens und Environment-Variablen umgehen. Gilt für jedes Plugin — bestehende und künftige.

## Grundsatz

**Nie Secrets in den Plugin-Ordner schreiben.** Der Plugin-Ordner ist der Cache (`~/.claude/plugins/cache/{marketplace}/{plugin}/{version}/`) — er wird bei jedem Update ersetzt. Alles, was eine Installation "besitzt", gehört ins persistente Daten-Verzeichnis.

## Drei Ebenen

| Ebene | Beispiel | Ort |
|---|---|---|
| **Plugin-eigene Secrets** (nur dieses Plugin braucht sie) | ELEVENLABS_API_KEY (video-studio), GitHub-Token (github-cowork) | `${CLAUDE_PLUGIN_DATA}/.env` bzw. Config-Datei dort |
| **OS-globale Variablen** (mehrere Skills brauchen sie) | Auto-DM-Tool-Key, Notion-Token | `.env` im OS-Root des Kunden (gitignored, `.env.example` als Inventar) |
| **Persönliche Secrets des Betreibers** | Markus' eigene Tokens | Keychain-Pattern (nur Claude Code / Host-Shell — in der Cowork-Sandbox nicht verfügbar) |

## `${CLAUDE_PLUGIN_DATA}`

- Auflösung: Umgebungsvariable `CLAUDE_PLUGIN_DATA`; falls nicht gesetzt, dokumentierter Pfad `~/.claude/plugins/data/{plugin-name}/`
- Wird beim ersten Zugriff angelegt, **überlebt Plugin-Updates** (Cache tut das nicht)
- Gehört dort auch hin: installierte Dependencies (venv, node_modules), Caches, Setup-Marker

In Skripten immer mit Fallback auflösen:

```bash
DATA="${CLAUDE_PLUGIN_DATA:-$HOME/.claude/plugins/data/<plugin-name>}"
```

```python
data_dir = os.environ.get("CLAUDE_PLUGIN_DATA",
    os.path.expanduser("~/.claude/plugins/data/<plugin-name>"))
```

## Auflösungs-Reihenfolge (für jeden Skill, der eine Variable braucht)

1. Bereits gesetzte Umgebungsvariable
2. `${CLAUDE_PLUGIN_DATA}/.env` (plugin-eigen)
3. `<os-root>/.env` (OS-global)
4. Fehlt → Setup-Flow: User fragen, an den richtigen Ort schreiben (global, wenn mehrere Skills die Variable brauchen, sonst plugin-lokal)

## Regeln für Plugin-Autoren

- `.env.example` im Plugin dokumentiert, welche Variablen das Plugin braucht — die echte `.env` entsteht erst beim Setup im Daten-Verzeichnis
- Setup-Marker (`.ready`) trägt die Plugin-Version → Doctor erkennt nach einem Update, dass Dependencies neu installiert werden müssen, **ohne** dass der User seinen Key neu eintragen muss
- Secrets nie in Ausgaben, Logs oder committete Dateien — in Bestätigungen maskieren
- Referenz-Implementierungen: `plugins/video-studio/skills/video-studio/scripts/setup.sh` (Bash) und `plugins/github-cowork/skills/github-cowork/references/helpers.py` (Python)

## Offen / zu verifizieren

- Verhalten von `${CLAUDE_PLUGIN_DATA}` in der Cowork-Sandbox (Host-Home vs. Sandbox) — Teil des E2E-Tests
