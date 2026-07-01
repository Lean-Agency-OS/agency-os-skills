# Secrets-Konvention für Agency-OS-Plugins

Wie die agency-os-Plugins mit API-Keys und Tokens umgehen. Gilt für jedes Plugin — bestehende und künftige.

## Grundsatz

Secrets liegen im **Brain**, nie im Plugin-Ordner. Zwei Gründe:

- Der Plugin-Ordner ist der Cache (`~/.claude/plugins/cache/{marketplace}/{plugin}/{version}/`) und wird bei jedem Update ersetzt. Was eine Installation "besitzt", darf dort nicht liegen.
- Das Brain ist zur Laufzeit ohnehin gemountet (die Skills lösen `{context}` auf, wie sie auch ihre anderen Kontext-Pfade auflösen) und liegt in einem **privaten** Repo. Ein committeter Key ist dort sicher genug und an **einem** Ort für alle Spokes.

## Ort: `{context}/secrets.env`

- Eine `KEY=VALUE`-Datei im Brain, aufgelöst über `.agency-os/architecture.md` (Rolle `context`), sonst per Muster `*context*`.
- **Committet** im privaten Brain-Repo (kein gitignore nötig). Vorlage: `secrets.env.example` im jeweiligen Skill.
- Beispiele: `ELEVENLABS_API_KEY=...` für die `video-*`-Skills, `GITHUB_TOKEN=...` für `agency-os-github` (nur in Cowork gebraucht, siehe unten).

## Sonderfall: `agency-os-github` (SSH vs. PAT)

Die Sicherung läuft in zwei Umgebungen mit unterschiedlichem Git-Zugang:

- **Mac (Claude Code):** SSH-Schlüssel in `~/.ssh`, nativer Push/Pull. Kein Secret nötig.
- **Cowork:** isolierte Sandbox ohne SSH-Schlüssel. Hier braucht der Skill `GITHUB_TOKEN` (feingranularer PAT, nur das Brain-Repo, „Contents: Read and write").

`scripts/resolve-git-auth.sh` entscheidet **fähigkeitsbasiert** (nicht per OS-Rateraten, denn Claude Code läuft unter macOS/Windows/Linux): ist ein SSH-Schlüssel vorhanden, wird nativer SSH-Zugang genutzt; sonst wird auf einen PAT zurückgefallen und der Token-Zugang in der **sandbox-lokalen** globalen Git-Config eingerichtet (insteadOf-Rewrite SSH->HTTPS plus `~/.git-credentials`). Die Remote-Adresse im Repo (`.git/config`) wird **nie** angefasst — sie ist mit dem Mac geteilt und bleibt auf SSH; der Token landet nie im Repo und nie auf dem Mac. Cowork wird zusätzlich über mehrere beobachtete Marker zusammen positiv erkannt (Hostname `claude` + Fuse-Mounts `~/mnt/outputs` und `~/mnt/uploads` + `CLAUDE_CODE_TMPDIR`/`CLAUDE_TMPDIR`); diese Erkennung steuert **nur** den Shared-Token-Fallback (siehe unten), nie die primäre SSH-vs-PAT-Entscheidung.

**Geteilt vs. persönlich.** Hier zeigt sich eine zweite Secret-Klasse: `GITHUB_TOKEN` ist ein **persönliches** Credential pro Arbeitskopie und darf **nicht** in die committete `{context}/secrets.env` (die wäre für alle Klone/das Team sichtbar). Er gehört in eine **lokale, gitignorete** Datei — immer `.agency-os/secrets.env` (dafür eine Gitignore-Regel `.agency-os/secrets.env`, da nur `.agency-os/state.md` einzeln ignoriert ist). Das Script liest deshalb local-first (Umgebungsvariable, dann `.agency-os/secrets.env`); die committete, geteilte `{context}/secrets.env` wird nur als letzter Ausweg und nur **innerhalb Cowork** genutzt, mit Warnung — auf einem persönlichen Rechner wird ein geteilter Token so nie still konfiguriert. Geteilte Org-Keys (z.B. `ELEVENLABS_API_KEY`) bleiben dagegen in der committeten `{context}/secrets.env`.

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
