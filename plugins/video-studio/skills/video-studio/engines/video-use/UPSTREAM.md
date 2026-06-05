# Upstream

video-use wurde gevendort aus:
**https://github.com/browser-use/video-use** (branch `main`, HEAD `cf12ac3`, Stand 2026-06-05).

Das eingebettete `.git` wurde entfernt - video-use ist jetzt Teil dieses Repos und wird hier mitgepflegt.

## Manuell mit Upstream vergleichen / Fixes holen
```bash
git clone https://github.com/browser-use/video-use /tmp/vu-upstream
diff -ru /tmp/vu-upstream video-use --exclude .git --exclude .venv --exclude __pycache__
```
