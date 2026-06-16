# Secrets-Konvention für Agency-OS-Plugins

Wie die agency-os-Plugins mit API-Keys und Tokens umgehen. Gilt für jedes Plugin — bestehende und künftige.

## Grundsatz

Secrets liegen im **Brain**, nie im Plugin-Ordner. Zwei Gründe:

- Der Plugin-Ordner ist der Cache (`~/.claude/plugins/cache/{marketplace}/{plugin}/{version}/`) und wird bei jedem Update ersetzt. Was eine Installation "besitzt", darf dort nicht liegen.
- Das Brain ist zur Laufzeit ohnehin gemountet (die Skills lösen `{context}` auf, wie sie auch ihre anderen Kontext-Pfade auflösen) und liegt in einem **privaten** Repo. Ein committeter Key ist dort sicher genug und an **einem** Ort für alle Spokes.

## Ort: `{context}/secrets.env`

- Eine `KEY=VALUE`-Datei im Brain, aufgelöst über `.agency-os/architecture.md` (Rolle `context`), sonst per Muster `*context*`.
- **Committet** im privaten Brain-Repo (kein gitignore nötig). Vorlage: `secrets.env.example` im jeweiligen Skill.
- Beispiel: `ELEVENLABS_API_KEY=...` für die `video-*`-Skills.

## Auflösungs-Reihenfolge (für jeden Skill, der einen Key braucht)

1. Bereits gesetzte Umgebungsvariable (z.B. vom Host injiziert).
2. `{context}/secrets.env` im Brain.
3. Fehlt → Setup-Flow: User bitten, den Key in `{context}/secrets.env` einzutragen (Vorlage zeigen). **Nie** in den Skill-Ordner schreiben.

## Dependencies & Caches (kein Secret, aber verwandt)

venv, `node_modules`, Chromium und der `.ready`-Marker liegen im **Skill-Root** und werden von `setup.sh` gebaut (gitignored). Ersetzt ein Update den Cache, fehlt `.ready` → `setup.sh` baut idempotent neu.

> Tradeoff: schwere Deps (z.B. Chromium) werden nach einem Update neu geladen. Ein persistentes Daten-Verzeichnis (`${CLAUDE_PLUGIN_DATA}`) wäre eine spätere Optimierung, ist aktuell aber nicht implementiert.

## Regeln für Plugin-Autoren

- `secrets.env.example` im Skill dokumentiert die gebrauchten Variablen — die echte Datei lebt im Brain.
- `setup.sh` / `doctor.sh` lesen den Key über den aufgelösten `{context}`-Pfad (vom Skill als Argument übergeben), nie aus dem Skill-Ordner.
- Setup-Marker (`.ready`) trägt die Plugin-Version → Doctor erkennt nach einem Update, dass Dependencies neu installiert werden müssen, **ohne** dass der User seinen Key neu eintragen muss.
- Secrets nie in Ausgaben, Logs oder committete Skill-Dateien — in Bestätigungen maskieren.
- Referenz-Implementierung: `plugins/agency-os-video/skills/video-shortform/scripts/{setup,doctor}.sh` (Bash).
