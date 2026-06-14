---
# Brand-CI — eine Quelle für carousel + video-studio.
# Liegt im Brain unter {context}/brands/{brand}/ci.md (z.B. 01-context/brands/your-brand/ci.md).
# Werte im Frontmatter sind maschinenlesbar (Modell liest sie, gibt sie an render.py/ffmpeg weiter).
# Ton/Stimme NICHT hier, sondern in voice-profile.md (gleicher Brand-Ordner).
# Platzhalter unten durch die eigenen Brand-Werte ersetzen.
brand: your-brand
name: BRAND
handle: "@yourhandle"
status: active            # nur aktive Brands werden genutzt
colors:
  accent: "#E85F33"       # Akzentfarbe (carousel --coral, video Overlays)
  bg_light: "#F2EBDD"     # Light-Edition Hintergrund (carousel --cream)
  bg_cinema: "#0F0F0E"    # Cinema-Edition Hintergrund / Vordergrund Light (carousel --black)
  subtitle: "#FED760"     # Untertitel-Füllfarbe (video-studio --caption-color)
fonts:
  display: "Open Sans"    # Headlines (carousel --font-display)
  display_weight: 800
  mono: "JetBrains Mono"  # Mono/Topbar (carousel --font-mono)
  subtitle: "Helvetica"   # Untertitel-Font (video-studio)
  subtitle_path: "/System/Library/Fonts/Helvetica.ttc"   # optional, für ffmpeg/PIL
assets_dir: "01-context/brands/your-brand/brand-assets"  # relativ ab Projekt-Root; carousel --assets-dir
logo: "logo.png"          # Dateiname im assets_dir
---

# CI Notizen (optional, Prosa)

Hier dürfen freie Brand-Notizen stehen (Bildsprache, Do/Don'ts). Die maschinellen Werte
stehen ausschließlich im Frontmatter oben. Ton und Stimme leben in `voice-profile.md`.

## Wie die Skills das lesen

- **carousel:** Modell liest das Frontmatter, schreibt `colors`/`fonts` in den `:root`-Block von
  `carousel.html` und übergibt `--handle {handle}`, `--brand {name}`, `--assets-dir {assets_dir}` an `render.py`.
  Die Layout-Templates liegen unter `{marketing}/carousels/00-templates/*.html` (mehrere möglich), nicht im
  Plugin; sie werden beim ersten Lauf aus dem Skill-Seed dorthin generiert (CI eingebacken) und sind danach
  frei anpass-/erweiterbar.
- **video-studio:** Modell liest das Frontmatter und übergibt z.B. `--caption-color {colors.subtitle}`,
  Fonts/Logo an die ffmpeg/PIL-Helfer.

Fehlt eine Zeile, gilt der neutrale Platzhalter-Default des jeweiligen Skills.
