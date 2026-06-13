#!/usr/bin/env python3
"""
Carousel-Builder Render Script (Marcus Vieghofer / Lean Agency)

Wandelt eine Carousel-HTML-Datei in eine mobile-first preview.html und — mit
--final — in einzelne PNG-Slides (1080x1350) plus ein gesamthaftes PDF.

Usage (immer aus dem Projekt-Root aufrufen):
  python3 skills/carousel/resources/render.py <input.html> <output_dir> [--final]
                                              [--handle "@markusvieghofer_com"]
                                              [--brand "LEAN AGENCY"]

Voraussetzungen fuer --final (einmalig):
  pip install playwright pillow --break-system-packages
  python3 -m playwright install chromium

Verhalten:
  - Schreibt IMMER zuerst eine preview.html (kein Chromium noetig) -> Iterations-Modus.
  - Nur mit --final zusaetzlich: pro Slide ein PNG (1080x1350) + ein PDF.

Pfad-Konventionen:
  - Bild-Assets im Slide-HTML referenzieren als
      ../../../../01-context/positionierung/brand-assets/{file}
    und werden relativ zum CWD (Projekt-Root) aufgeloest und base64-eingebettet.
  - preview-template.html liegt neben diesem Script.
"""

import sys
import os
import re
import base64
from pathlib import Path


def usage():
    print('Usage: python3 render.py <input.html> <output_dir> [--final] '
          '[--handle "@x"] [--brand "Name"]')
    sys.exit(1)


def write_preview(input_html, output_dir, slide_ids, handle, brand):
    """
    Schreibt eine mobile-first preview.html (Instagram-Mobile-View-Mockup).

    Architektur (Template-driven):
      - preview-template.html (neben diesem Script) ist ein statisches IG-Mockup
        mit Platzhaltern {{CAROUSEL_STYLES}}, {{SLIDES}}, {{CAPTION}}, {{TOTAL}},
        {{HANDLE}}, {{BRAND}}.
      - Diese Funktion extrahiert Slide-CSS + <section class="slide"> aus dem
        Carousel-HTML, bettet alle Brand-Asset-Bilder als base64 ein und
        injiziert beides ins Template. Caption aus caption.md wird formatiert.

    base64-Pflicht:
      Unter file:// blockiert Chrome je nach OS lokale Bilder aus relativen
      Pfaden. Die preview.html muss self-contained sein.
    """
    # ---- 1. Carousel-HTML laden + Brand-Assets in base64 ----
    carousel_html = input_html.read_text(encoding="utf-8")

    # Matching: beliebig viele "../"-Prefixe + 01-context/positionierung/brand-assets/{file}
    asset_re = re.compile(
        r"(?:\.\./)*01-context/positionierung/brand-assets/([^\'\")\s]+)"
    )
    brand_dir = (Path.cwd() / "01-context" / "positionierung" / "brand-assets").resolve()
    mime_map = {
        ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml",
    }

    def to_data_uri(match):
        rel = match.group(1)
        asset_path = brand_dir / rel
        if not asset_path.exists():
            print(f"  WARNUNG: Brand-Asset nicht gefunden: {rel}")
            return match.group(0)
        ext = asset_path.suffix.lower()
        mime = mime_map.get(ext, "application/octet-stream")
        b64 = base64.b64encode(asset_path.read_bytes()).decode("ascii")
        return f"data:{mime};base64,{b64}"

    carousel_html = asset_re.sub(to_data_uri, carousel_html)

    # ---- 2. Slide-CSS und Slide-Sections extrahieren ----
    style_match = re.search(r"<style>(.*?)</style>", carousel_html, re.DOTALL)
    carousel_styles = style_match.group(1).strip() if style_match else ""

    slide_pattern = re.compile(
        r'<section[^>]*class="slide[^"]*"[^>]*>.*?</section>',
        re.DOTALL,
    )
    slide_html_blocks = slide_pattern.findall(carousel_html)
    slides_html = "\n\n".join(slide_html_blocks)

    # ---- 3. Caption aus caption.md formatieren ----
    caption_path = output_dir / "caption.md"
    caption_html = ""
    if caption_path.exists():
        ct = caption_path.read_text(encoding="utf-8")
        lines = [l for l in ct.split("\n") if not l.strip().startswith("# ")]
        raw = "\n".join(lines).strip()
        blocks = [b.strip() for b in raw.split("\n\n") if b.strip()]
        out = []
        first_text_block = True
        for b in blocks:
            if all(w.startswith("#") for w in b.split() if w):
                hashtags_html = " ".join(
                    f'<span class="hashtag">{w}</span>'
                    for w in b.split() if w.startswith("#")
                )
                out.append(f'<div class="ig-hashtags">{hashtags_html}</div>')
            else:
                inner = b.replace("\n", "<br>")
                if first_text_block:
                    inner = f'<span class="ig-cap-handle">{handle}</span>' + inner
                    first_text_block = False
                out.append(f'<div class="ig-cap-block">{inner}</div>')
        caption_html = "\n".join(out)

    # ---- 4. preview-template.html laden + Platzhalter substituieren ----
    template_path = Path(__file__).resolve().parent / "preview-template.html"
    if not template_path.exists():
        raise FileNotFoundError(f"preview-template.html nicht gefunden: {template_path}")

    preview_tpl = template_path.read_text(encoding="utf-8")
    preview_html = (preview_tpl
        .replace("<!-- {{CAROUSEL_STYLES}} -->", f"<style>\n{carousel_styles}\n</style>")
        .replace("<!-- {{SLIDES}} -->", slides_html)
        .replace("<!-- {{CAPTION}} -->", caption_html)
        .replace("{{TOTAL}}", str(len(slide_ids)))
        .replace("{{HANDLE}}", handle)
        .replace("{{BRAND}}", brand)
    )

    # ---- 5. preview.html schreiben ----
    preview_path = output_dir / "preview.html"
    preview_path.write_text(preview_html, encoding="utf-8")
    print(f"Preview geschrieben: {preview_path.name}")


def main():
    # Args parsen: --final ist Flag, --handle/--brand nehmen einen Wert, Rest positional.
    args = sys.argv[1:]
    handle = "@markusvieghofer_com"
    brand = "LEAN AGENCY"
    pos = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--final":
            i += 1
        elif a == "--handle":
            handle = args[i + 1] if i + 1 < len(args) else handle
            i += 2
        elif a == "--brand":
            brand = args[i + 1] if i + 1 < len(args) else brand
            i += 2
        elif a.startswith("--"):
            i += 1
        else:
            pos.append(a)
            i += 1

    if len(pos) < 2:
        usage()

    input_html = Path(pos[0]).resolve()
    output_dir = Path(pos[1]).resolve()

    if not input_html.exists():
        print(f"FEHLER: HTML-Datei nicht gefunden: {input_html}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    html_text = input_html.read_text(encoding='utf-8')
    slide_ids = re.findall(r'<section[^>]*class="slide[^"]*"[^>]*id="(slide-\d+)"', html_text)
    if not slide_ids:
        slide_count = len(re.findall(r'<section[^>]*class="slide', html_text))
        slide_ids = [f"slide-{i+1}" for i in range(slide_count)]

    if not slide_ids:
        print("FEHLER: Keine .slide-Sektionen im HTML gefunden.")
        sys.exit(1)

    print(f"Gefunden: {len(slide_ids)} Slides")

    # preview.html IMMER schreiben (Iterations-Modus, kein Chromium noetig).
    write_preview(input_html, output_dir, slide_ids, handle, brand)

    if "--final" not in sys.argv:
        print("Preview geschrieben (preview-only). PNGs + PDF erst mit --final am Schluss.")
        return

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("FEHLER: Playwright nicht installiert.")
        print("Setup: pip install playwright pillow --break-system-packages")
        print("       python3 -m playwright install chromium")
        sys.exit(1)

    try:
        from PIL import Image
    except ImportError:
        print("FEHLER: Pillow nicht installiert.")
        print("Setup: pip install pillow --break-system-packages")
        sys.exit(1)

    file_url = f"file://{input_html}"
    png_paths = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1080, "height": 1350},
            device_scale_factor=2
        )
        page = context.new_page()
        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(1500)

        for idx, slide_id in enumerate(slide_ids, start=1):
            png_path = output_dir / f"slide-{idx:02d}.png"
            element = page.query_selector(f"#{slide_id}")
            if element is None:
                print(f"WARNUNG: #{slide_id} nicht gefunden, ueberspringe.")
                continue
            element.screenshot(path=str(png_path), omit_background=False)
            png_paths.append(png_path)
            print(f"  [{idx:02d}/{len(slide_ids)}] {png_path.name}")

        browser.close()

    if not png_paths:
        print("FEHLER: Keine Slides gerendert.")
        sys.exit(1)

    pdf_path = output_dir / "full-carousel.pdf"
    images = [Image.open(p_path).convert("RGB") for p_path in png_paths]
    if images:
        first, *rest = images
        first.save(pdf_path, save_all=True, append_images=rest, resolution=150)
        print(f"PDF erstellt: {pdf_path.name} ({len(images)} Seiten)")

    print(f"\nFertig. Output in: {output_dir}")
    print(f"  PNGs: {len(png_paths)}")
    print(f"  PDF:  {pdf_path.name}")
    print(f"  Preview: preview.html (mobile-first IG-Slider)")


if __name__ == "__main__":
    main()
