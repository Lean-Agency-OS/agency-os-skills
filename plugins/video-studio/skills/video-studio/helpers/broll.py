"""Brand-driven B-roll tool.

Takes a JSON spec, builds a static overlay PNG (background layer + text block)
with PIL, and composites it with ffmpeg onto a trimmed, (by default) muted
footage clip.

Defaults (font, colors, scrim/box/vignette) come from a brand config
`<brand>/broll.json`. Every value can be overridden per clip in the spec.

Paths are resolved explicitly, not guessed from the script location:
  --root         base for resolving relative paths in the spec (source,
                 output, font). Default: current working directory.
  --brand-config direct path to the brand's broll.json. If omitted it is
                 derived as <brands-dir>/<brand>/broll.json.
  --brands-dir   base directory that holds <brand>/broll.json. Default:
                 <root>/01-context/brands.

Usage:
    uv run python helpers/broll.py path/to/broll.json
    uv run python helpers/broll.py spec.json --out other.mp4 --root /repo
    uv run python helpers/broll.py spec.json --brand-config /path/brand/broll.json

Spec fields (see broll.example.json):
    source      path to footage (relative to --root or absolute)
    start       seconds, in-point in the footage             (default 0)
    duration    seconds, b-roll length                        (default 7)
    mute        true -> no audio                              (default true)
    brand       brand folder name under --brands-dir          (default "default")
    output      target MP4 (default: <spec-dir>/preview.mp4)
    resolution  [w, h]                                        (default [1080,1920])
    fps                                                       (default 24)
    fade_in     overlay fade-in seconds                       (default 0 = instant)
    fade_out    overlay fade-out seconds at the end           (default 0 = hard cut)
    background  { mode, + overrides of the brand defaults }
                mode: "scrim" | "box" | "vignette" | list of those
    text        { font?, weight?, align?, block_position?, stroke?,
                  stroke_color?, max_width?,
                  elements: [ {text,size,color?,gap_after?,line_gap?} ] }
                align: center|left|right ; block_position: center|top|bottom
                max_width: fraction of frame width at which text wraps
                  (box mode default 0.8 -> box stays indented; off otherwise)
    Box-mode defaults (all overridable): white opaque box (box_color #fff,
    box_alpha 1.0), black text (box_text_color), no stroke, auto-wrap on
    box_max_width. box_style: "block" (one rectangle around the whole block)
    or "lines" (a background per line, fits the line width; box_line_pad_x/y
    control the padding).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ffmpeg_utils import run


# ---- helpers --------------------------------------------------------------
def parse_color(s, alpha=None):
    """'#rgb' / '#rrggbb' / '#rrggbbaa' -> (r,g,b,a). alpha (0..1) overrides."""
    if not isinstance(s, str):
        raise ValueError(f"color must be a string, got {type(s).__name__}: {s!r}")
    raw = s
    s = s.lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) not in (6, 8) or any(c not in "0123456789abcdefABCDEF" for c in s):
        raise ValueError(f"invalid hex color: {raw!r} (expected #rgb, #rrggbb or #rrggbbaa)")
    r, g, b = int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)
    a = int(s[6:8], 16) if len(s) >= 8 else 255
    if alpha is not None:
        a = max(0, min(255, round(alpha * 255)))
    return (r, g, b, a)


def make_path_resolver(root: Path):
    """Return a resolver that maps relative paths against `root`, leaving absolutes alone."""
    def resolve(p) -> Path:
        p = Path(p)
        return p if p.is_absolute() else (root / p)
    return resolve


def load_font(path, size, weight, width=100):
    if not Path(path).exists():
        sys.exit(f"ERROR: font not found: {path}")
    f = ImageFont.truetype(str(path), size)
    try:
        axes = f.get_variation_axes() or []
        if axes:
            vals = []
            for ax in axes:
                name = ax.get("name", "")
                if isinstance(name, bytes):
                    name = name.decode("latin-1", "ignore")
                n = name.lower()
                if "weight" in n or "wght" in n:
                    vals.append(weight)
                elif "width" in n or "wdth" in n:
                    vals.append(width)
                else:
                    vals.append(ax.get("default", 0))
            f.set_variation_by_axes(vals)
    except Exception as e:  # static font or no axes -> ignore
        print(f"  (font has no variation axes: {e})")
    return f


def line_h(font):
    a, d = font.getmetrics()
    return a + d


def deep_merge(base, override):
    out = dict(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


# ---- overlay --------------------------------------------------------------
def build_vignette(w, h, color, strength, inner):
    """Radial alpha gradient: clear center, dark edges."""
    yy, xx = np.mgrid[0:h, 0:w].astype("float32")
    dx = (xx - w / 2) / (w / 2)
    dy = (yy - h / 2) / (h / 2)
    d = np.sqrt(dx * dx + dy * dy) / np.sqrt(2.0)
    falloff = np.clip((d - inner) / max(1e-6, 1.0 - inner), 0.0, 1.0)
    alpha = (falloff ** 2) * strength * 255.0
    layer = np.zeros((h, w, 4), dtype="uint8")
    layer[..., 0], layer[..., 1], layer[..., 2] = color[0], color[1], color[2]
    layer[..., 3] = alpha.astype("uint8")
    return Image.fromarray(layer, "RGBA")


def wrap_text(s, font, max_px):
    """Greedy word-wrap to a maximum pixel width."""
    words = s.split()
    if not words:
        return [s]
    lines, cur = [], words[0]
    for word in words[1:]:
        if font.getlength(cur + " " + word) <= max_px:
            cur += " " + word
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def build_overlay(spec, brand, out_png, resolve):
    w, h = spec.get("resolution", [1080, 1920])
    bg = deep_merge(brand["background"], spec.get("background", {}))
    modes = bg.get("mode", "scrim")
    modes = [modes] if isinstance(modes, str) else list(modes)

    text = spec.get("text", {})
    font_path = text.get("font")
    if font_path:
        font_path = resolve(font_path)
    else:
        font_path = Path(brand["_dir"]) / brand["font"]
    weight = text.get("weight", brand.get("weight", 800))
    width = text.get("width", brand.get("width", 100))
    align = text.get("align", "center")
    block_position = text.get("block_position", "center")
    margin = text.get("block_margin", 160)

    is_box = "box" in modes
    # Box mode: black text on a (white) box, no stroke, auto-wrap so the box
    # stays narrow/indented. Other modes: brand text color + stroke for
    # readability directly over footage.
    default_text_color = bg["box_text_color"] if is_box else brand["palette"]["text"]
    stroke_w = text.get("stroke", 0 if is_box else brand["stroke"]["width"])
    stroke_color = parse_color(text.get("stroke_color", brand["stroke"]["color"]))
    max_w_frac = text.get("max_width", bg.get("box_max_width") if is_box else None)
    max_text_px = (max_w_frac * w - 2 * bg["box_padding"]) if max_w_frac else None

    # --- measure text layout (with optional word-wrap) ---
    elements = text.get("elements", [])
    if not elements:
        sys.exit("ERROR: spec.text.elements is empty - nothing to render")
    laid = []
    for el in elements:
        size = el.get("size", 72)
        font = load_font(font_path, size, weight, width)
        color = parse_color(el.get("color", default_text_color))
        gap = el.get("gap_after", 24)
        line_gap = el.get("line_gap", int(size * 0.12))
        lines = wrap_text(el["text"], font, max_text_px) if max_text_px else [el["text"]]
        for i, ln in enumerate(lines):
            last = i == len(lines) - 1
            laid.append({
                "text": ln, "font": font, "tw": font.getlength(ln), "color": color,
                "lh": line_h(font), "gap": gap if last else line_gap,
            })

    total = sum(e["lh"] for e in laid) + sum(e["gap"] for e in laid)
    if block_position == "top":
        y0 = margin
    elif block_position == "bottom":
        y0 = h - margin - total
    else:
        y0 = (h - total) / 2

    # x per line
    for e in laid:
        if align == "left":
            e["x"] = margin
        elif align == "right":
            e["x"] = w - margin - e["tw"]
        else:
            e["x"] = (w - e["tw"]) / 2

    # --- build layers (bottom -> top) ---
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    if "vignette" in modes:
        vig = build_vignette(
            w, h,
            parse_color(bg["vignette_color"]),
            float(bg["vignette_strength"]),
            float(bg["vignette_inner"]),
        )
        img = Image.alpha_composite(img, vig)

    draw = ImageDraw.Draw(img)

    if "scrim" in modes:
        draw.rectangle(
            [0, 0, w, h],
            fill=parse_color(bg["scrim_color"], alpha=float(bg["scrim_alpha"])),
        )

    if "box" in modes and laid:
        box_fill = parse_color(bg["box_color"], alpha=float(bg["box_alpha"]))
        if bg.get("box_style", "block") == "lines":
            # One background per line, fits the line width.
            px, py = bg["box_line_pad_x"], bg["box_line_pad_y"]
            yl = y0
            for e in laid:
                x0, x1 = e["x"] - px, e["x"] + e["tw"] + px
                yy0, yy1 = yl - py, yl + e["lh"] + py
                r = min(bg["box_radius"], (yy1 - yy0) / 2, (x1 - x0) / 2)
                draw.rounded_rectangle([x0, yy0, x1, yy1], radius=r, fill=box_fill)
                yl += e["lh"] + e["gap"]
        else:
            pad = bg["box_padding"]
            bx0 = min(e["x"] for e in laid) - pad
            bx1 = max(e["x"] + e["tw"] for e in laid) + pad
            by0 = y0 - pad
            by1 = y0 + total + pad
            radius = min(bg["box_radius"], (by1 - by0) / 2, (bx1 - bx0) / 2)
            draw.rounded_rectangle([bx0, by0, bx1, by1], radius=radius, fill=box_fill)

    # --- text ---
    y = y0
    for e in laid:
        draw.text(
            (e["x"], y), e["text"], font=e["font"], fill=e["color"],
            stroke_width=stroke_w, stroke_fill=stroke_color,
        )
        y += e["lh"] + e["gap"]

    out_png.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_png)
    print(f"overlay -> {out_png}  modes={modes} block={int(total)}px")
    return (w, h)


# ---- composite ------------------------------------------------------------
def composite(spec, overlay_png, res, out_mp4, resolve):
    w, h = res
    source = resolve(spec["source"])
    if not source.exists():
        sys.exit(f"ERROR: source footage not found: {source}")
    start = float(spec.get("start", 0.0))
    dur = float(spec.get("duration", 7.0))
    # No animation by default (b-roll is fully present immediately and stays
    # until the hard cut). Enable fades via fade_in / fade_out.
    fade_in = float(spec.get("fade_in", 0.0))
    fade_out = float(spec.get("fade_out", 0.0))
    fps = int(spec.get("fps", 24))
    mute = spec.get("mute", True)

    out_mp4.parent.mkdir(parents=True, exist_ok=True)

    ov_fades = ""
    if fade_in > 0:
        ov_fades += f"fade=t=in:st=0:d={fade_in:.2f}:alpha=1,"
    if fade_out > 0:
        ov_fades += f"fade=t=out:st={max(0.0, dur - fade_out):.2f}:d={fade_out:.2f}:alpha=1,"
    fg = (
        f"[0:v]scale={w}:{h}:force_original_aspect_ratio=increase,"
        f"crop={w}:{h},setsar=1,fps={fps},setpts=PTS-STARTPTS[base];"
        f"[1:v]format=rgba,{ov_fades}setpts=PTS-STARTPTS[ov];"
        f"[base][ov]overlay=0:0:eof_action=pass[outv]"
    )

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-nostats",
        "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", str(source),
        "-loop", "1", "-t", f"{dur:.3f}", "-i", str(overlay_png),
        "-filter_complex", fg,
        "-map", "[outv]",
    ]
    if mute:
        cmd += ["-an"]
    else:
        cmd += ["-map", "0:a?", "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += [
        "-t", f"{dur:.3f}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        str(out_mp4),
    ]
    print(f"compositing -> {out_mp4}  (start={start}s dur={dur}s mute={mute})")
    run(cmd)


def grab_verify(out_mp4, dur):
    verify = out_mp4.parent / "verify" / "broll_mid.png"
    verify.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-y", "-hide_banner", "-nostats",
        "-ss", f"{dur / 2:.3f}", "-i", str(out_mp4),
        "-frames:v", "1", str(verify),
    ])
    print(f"verify frame -> {verify}")
    return verify


# ---- main -----------------------------------------------------------------
def load_brand(brand_config: Path):
    if not brand_config.exists():
        sys.exit(f"ERROR: brand config not found: {brand_config}")
    brand = json.loads(brand_config.read_text(encoding="utf-8"))
    brand["_dir"] = str(brand_config.parent)
    return brand


def main():
    ap = argparse.ArgumentParser(description="Brand-driven B-roll generator")
    ap.add_argument("spec", help="Path to the broll.json spec")
    ap.add_argument("--out", help="Override the output MP4 path")
    ap.add_argument(
        "--root", type=Path, default=None,
        help="Base for resolving relative spec paths (default: current working directory)",
    )
    ap.add_argument(
        "--brand-config", type=Path, default=None,
        help="Direct path to the brand's broll.json (overrides --brands-dir derivation)",
    )
    ap.add_argument(
        "--brands-dir", type=Path, default=None,
        help="Base dir holding <brand>/broll.json (default: <root>/01-context/brands)",
    )
    args = ap.parse_args()

    root = (args.root or Path.cwd()).resolve()
    resolve = make_path_resolver(root)

    spec_path = Path(args.spec).resolve()
    if not spec_path.exists():
        sys.exit(f"ERROR: spec not found: {spec_path}")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    brand_name = spec.get("brand", "default")
    if args.brand_config:
        brand_config = args.brand_config.resolve()
    else:
        brands_dir = (args.brands_dir or (root / "01-context" / "brands")).resolve()
        brand_config = brands_dir / brand_name / "broll.json"
    brand = load_brand(brand_config)

    out_mp4 = Path(args.out).resolve() if args.out else (
        resolve(spec["output"]).resolve() if spec.get("output")
        else spec_path.parent / "preview.mp4"
    )
    # Unique per spec -> no collision on parallel renders.
    overlay_png = spec_path.parent / f"{spec_path.stem}.overlay.png"

    res = build_overlay(spec, brand, overlay_png, resolve)
    composite(spec, overlay_png, res, out_mp4, resolve)
    grab_verify(out_mp4, float(spec.get("duration", 7.0)))
    print(f"\ndone: {out_mp4}")


if __name__ == "__main__":
    main()
