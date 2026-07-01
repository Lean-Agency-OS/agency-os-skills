---
name: agency-os-update
version: 1.0.0
description: Prüft, ob die installierten Agency-OS-Plugins aktuell sind (installiert vs. neuester Stand im Marketplace) und nennt die genauen Update-Schritte je nach Umgebung (Claude Code oder Cowork). Verwende wenn der User "sind meine Plugins aktuell", "gibt es Updates", "check for updates", "neuste Version", "bin ich auf dem neuesten Stand", "Plugin-Update", "update verfügbar", "welche Version habe ich" sagt oder ähnlich nach Aktualität/Updates der Skills/Plugins fragt.
allowed-tools: Bash(claude plugin list) Bash(claude plugin marketplace update *) Bash(bash scripts/update-check.sh) Bash(curl *)
---

# Agency-OS-Update-Check

Beantwortet **"Sind meine Plugins aktuell?"** und sagt konkret, was zu tun ist. Wichtig vor allem in **Cowork**: dort gibt es keine Update-Benachrichtigungen, aktualisiert wird manuell.

## Prinzip

Zwei Fakten holen, dann vergleichen:
- **Installiert** = was gerade läuft.
- **Latest** = der neueste Stand im Marketplace-Repo (`main`), maschinenlesbar in `.claude-plugin/versions.json`.

Nicht die Umgebung raten - die **Fähigkeit zur Laufzeit ermitteln** (gleiche Leitlinie wie in `docs/cowork-improvements.md`). Der Helper macht das: Claude Code vs. Cowork wird per Probe unterschieden (gibt es die nutzbare `claude`-CLI?).

## Ablauf

1. **Fakten holen** (still): aus dem Skill-Verzeichnis
   ```bash
   bash scripts/update-check.sh
   ```
   Ausgabe: `ENV` (`code` oder `cowork`), `INSTALLIERT` und `LATEST` (`versions.json` von `main`, öffentliche raw-URL, kein Token nötig). Das Script vergleicht bewusst **nicht** - das machst du.

2. **Vergleichen und berichten.** Tabelle in einfacher Sprache:

   | Plugin | Installiert | Neueste | Status |
   |--------|-------------|---------|--------|
   | agency-os-core | 3.7.0 | 3.8.0 | Update verfügbar |
   | agency-os-video | 2.3.2 | 2.3.2 | aktuell |

   - Alles aktuell -> klar sagen: "Alle Plugins sind auf dem neuesten Stand."
   - Rückstände -> nur die betroffenen Plugins hervorheben.

3. **Update-Schritte nennen** (nur wenn etwas veraltet ist) - **passend zur `ENV`:**

   ### ENV = code (Claude Code)
   Installiert wird über die Settings/CLI. Beide Stufen sind nötig, Stufe 1 allein reicht **nicht**:
   ```bash
   # 1. Marketplace-Cache auf den neuesten Repo-Stand bringen
   claude plugin marketplace update agency-os
   # 2. Die veralteten Plugins anheben (nur die betroffenen auflisten)
   claude plugin update agency-os-core@agency-os --scope project
   ```
   Danach **Claude Code neu starten**. `--scope project` = Template-/Brain-Install (Plugins in `.claude/settings.json` des Brains); bei globaler Installation `--scope user`.

   ### ENV = cowork
   Kein CLI-Update. Aktualisiert wird über den **Button/Dialog, mit dem der Marketplace eingetragen wurde** (das Agency-OS-Repo). Schritte:
   1. Den Connector-/Marketplace-Dialog öffnen, in dem das Agency-OS-Repo (`Lean-Agency-OS/agency-os-skills`) eingetragen ist.
   2. Das Repo **neu laden / erneut hinzufügen** (der Button, über den du es ursprünglich eingetragen hast) - das zieht den neuesten Stand.
   3. Danach die Session/Chat **neu laden**, damit die neuen Skill-Versionen greifen.

4. **Sonderfall Cowork ohne lesbare Installations-Versionen.** Zeigt `INSTALLIERT` an, dass in der Sandbox nur der eigene Skill-Ordner gemountet ist (kein exakter Diff möglich): **nicht** so tun, als wäre der Vergleich vollständig. Stattdessen die **LATEST-Liste** zeigen und den Cowork-Button-Weg (oben) zum Aktualisieren nennen - so ist der User trotzdem sicher auf dem neuesten Stand.

## Regeln

- **Nur lesen/prüfen.** Dieser Skill installiert oder aktualisiert **nichts** selbst - er berichtet und nennt die Schritte. Das eigentliche Update macht der User bewusst (CLI bzw. Button), Neustart/Reload nötig.
- Ein Update greift nur, wenn die Plugin-`version` im Repo hochgezählt wurde - sonst bleibt der Client auf dem Cache-Stand.
- Klartext-Feedback am Ende: entweder "alles aktuell" oder eine kurze Liste "diese Plugins updaten: …" plus der zur `ENV` passende Weg.
