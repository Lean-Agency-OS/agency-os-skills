---
name: brand-ci
version: 1.0.0
description: >
  Legt die Brand-CI an oder aktualisiert sie: schreibt `ci.md` (YAML-Frontmatter) mit Farben, Fonts,
  Logo, Handle, Brand-Name und Asset-Ordner in den Brand-Kontext. Die `ci.md` ist die gemeinsame
  Quelle für `/carousel` und `/video-studio`. Geführtes Interview, schreibt erst nach Bestätigung.
  Triggern bei: "CI einrichten", "Brand-CI anlegen", "ci.md erstellen", "Corporate Identity festlegen",
  "Farben und Fonts festlegen", "Markenfarben hinterlegen", "CI aktualisieren", "/brand-ci".
---

# Brand-CI

Schreibt die **Brand-CI** als `ci.md` (YAML-Frontmatter) in den Brand-Ordner. Die Datei ist die
**eine Quelle** für Farben, Fonts, Logo, Handle, Brand-Name und Asset-Ordner und wird von `/carousel`
(Layout-CI) und `/video-studio` (Untertitel, Overlays, Logo) gelesen. Ton/Stimme gehören NICHT hierher,
die liegen in `voice-profile.md` (`/brand-voice`).

## Pfade & Fundament

Keine hartkodierten Pfade. Den `context`-Ordner über `.agency-os/architecture.md` auflösen
(`agency-os-start` pflegt die Map), sonst per Muster `*context*`. Ziel: `{context}/brands/{brand}/ci.md`.

- **Brand bestimmen:** Gibt es schon Ordner unter `{context}/brands/`? Dann den passenden nehmen bzw. fragen, welche Brand. Neue Brand → Slug (kebab-case) + Name erfragen, Ordner `{context}/brands/{brand}/` anlegen.
- **Existiert die `ci.md` schon:** laden, aktuellen Stand zeigen, im **Update-Modus** nur das Genannte ändern (Rest unverändert). Sonst **Anlege-Modus**.

### Schema (`ci.md`)

Vollständiges Schema + ausgefülltes Beispiel: [`references/ci.example.md`](references/ci.example.md) (kanonische
Vorlage, nach diesem Schema schreiben). Frontmatter-Felder in Kürze:

- `brand` (Slug, = Ordnername), `name` (Anzeigename), `handle` (`@…`), `status` (`active`)
- `colors`: `accent`, `bg_light`, `bg_cinema`, `subtitle` (Hex)
- `fonts`: `display` (+ `display_weight`), `mono`, `subtitle` (+ optional `subtitle_path`)
- `assets_dir` (relativ ab Projekt-Root), `logo` (Dateiname im `assets_dir`)
- darunter optionale Prosa-Notizen (Bildsprache, Do/Don'ts)

## Workflow

### 1. Kontext scannen (vor dem Interview)

Erst schauen, was schon da ist, statt blind zu fragen. Den Brand-Ordner + Umgebung scannen und Werte ableiten:

- **Bestehende `ci.md`** → Update-Modus, alle Felder vorbelegen.
- **Brand-Assets-Ordner** (z.B. `{context}/brands/{brand}/brand-assets/` o.ä.): vorhanden? → `assets_dir` vorschlagen; Logo-/Bilddatei finden → `logo` vorschlagen.
- **Bestehende Layout-Templates** (`{marketing}/content/carousels/00-templates/*.html`): `:root`-Werte (Akzent/Hintergründe) + Fonts auslesen → `colors`/`fonts` vorschlagen.
- **`voice-profile.md`, Positionierungs-/Brand-Notizen** im Kontext: Hinweise auf Name, Handle, Farben, Fonts.
- **Account/Projekt:** Brand-Name + Handle ableitbar (z.B. aus vorhandenen Profilen)?

Die gefundenen Werte als **Vorschläge** ins Interview übernehmen. Was nicht gefunden wird, normal erfragen.

### 2. Interview (Stop-Punkt, gruppiert)

Pro Gruppe die **gescannten Vorschläge zeigen** und bestätigen/anpassen lassen - nur fehlende Werte aktiv
erfragen. Der User darf auch alles auf einmal liefern. Gruppen nacheinander:

1. **Identität:** Brand-Name + Social-Handle. (Slug daraus ableiten, kurz bestätigen.)
2. **Farben:** Akzent, heller Hintergrund, dunkler Hintergrund, Untertitel-Farbe (Hex). Unbekannt → vorschlagen/leer lassen.
3. **Fonts:** Display-Font (+ Weight), Mono-Font, Untertitel-Font (+ optional Pfad).
4. **Assets:** Asset-Ordner (`assets_dir`, relativ ab Projekt-Root) + Logo-Dateiname.

**Minimal valide:** Name + Handle + Akzentfarbe reichen für eine erste `ci.md`. Der Rest darf leer bleiben
und kann später ergänzt werden. Fehlende Pflicht-Optik → der jeweilige Skill nutzt seine Platzhalter.

### 3. Vorschau + Bestätigung (Stop-Punkt)

Die fertige `ci.md` (Frontmatter + optionale Notizen) im Chat zeigen. Abschlussfrage:
*"Passt das? 'go' zum Speichern, sonst sag, was anders soll."* Ohne explizites "go" → nicht schreiben.

### 4. Schreiben

Nach "go" `{context}/brands/{brand}/ci.md` schreiben (Anlege-Modus) bzw. die geänderten Frontmatter-Felder
aktualisieren (Update-Modus, übrige Felder + Prosa unverändert lassen). Ordner ggf. anlegen.

### 5. Abschluss

Pfad ausgeben. Hinweis: `/carousel` und `/video-studio` nutzen die `ci.md` ab jetzt automatisch. Falls
ein `assets_dir` gesetzt wurde, das aber noch nicht existiert: kurz erwähnen, dass dort Logo/Fotos abgelegt werden sollten.

## Output

Schreibt (nach "go") `{context}/brands/{brand}/ci.md` (YAML-Frontmatter + optionale Prosa-Notizen). Im Update-Modus nur die geänderten Felder, Rest unverändert. `/carousel` und `/video-studio` lesen die Datei ab dann automatisch.

## Verwandte Skills

- Schreibt nur die `ci.md` (Optik/Identität). Stimme/Ton → `/brand-voice` (`voice-profile.md`), Zielgruppe → `/icp` (`icp.md`).
- Erstellt keine Layout-Templates und keine Assets - nur die CI-Daten.

## Hard-Stops

- Kein explizites "go" → nicht schreiben.
- Brand unklar (mehrere Ordner, keine Wahl getroffen) → erst klären, nicht raten.
