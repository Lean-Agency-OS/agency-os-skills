"""Export an EDL as a timeline for DaVinci Resolve / Adobe Premiere.

Reads edl.json and writes a timeline that references the ORIGINAL source
files with each cut's in/out and timeline position. This is the cut, not the
finish: grade and ffmpeg overlays are intentionally NOT exported so the editor
can colour and add graphics natively.

Formats (--format):
  fcpxml  (default)  DaVinci Resolve and modern Premiere. Supports embedded
                     captions (--captions) and an explicit timeline raster
                     (--width/--height, e.g. 1080x1920 for a vertical reel).
  premiere           Final Cut Pro 7 XML (xmeml v4) for older Adobe Premiere.
                     Captions are NOT embeddable in this format; import the
                     SRT separately for captions.
  both               Write both files.

Captions (--captions, fcpxml only) are read from <edit>/transcripts/<src>.json
(word-level Scribe output) using the same 2-word UPPERCASE chunking as the
burn-in pipeline, and embedded as a subtitle track. --caption-color sets the
default fill (hex, default FFFFFF); final styling is done in the NLE.

Timeline raster: by default the sequence uses the first source's pixel
dimensions. Pass --width/--height to force a raster (e.g. 1080x1920). Each
source asset keeps its own native format, so a vertical timeline conforms a
landscape/rotated source cleanly.

Path remap (--remap 'FROM=TO', repeatable): media refs point at the source
path on disk. When the EDL was built in a sandbox whose paths differ from the
user's machine (e.g. Cowork), rewrite the media URLs so the NLE finds the
footage. Probing still uses the real on-disk path.

Integer frame rates only (24/25/30/50/60); times are frame-aligned at --fps.

Usage:
    python helpers/export_nle.py <edl.json>
    python helpers/export_nle.py <edl.json> --width 1080 --height 1920 --captions
    python helpers/export_nle.py <edl.json> --format both -o timeline.fcpxml
    python helpers/export_nle.py <edl.json> \
        --remap '/sessions/x/mnt/Proj=/Users/me/Documents/Proj'
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

from ffmpeg_utils import probe

PUNCT_BREAK = ".?!,:;"


def tc(seconds: float, fps: int) -> str:
    """Frame-aligned FCPXML rational time, e.g. 2.0s @24 -> '48/24s'."""
    frames = int(round(seconds * fps))
    return "0s" if frames == 0 else f"{frames}/{fps}s"


def xa(s: str) -> str:
    """Escape a string for use inside an XML attribute or text node."""
    return (
        str(s).replace("&", "&amp;").replace("<", "&lt;")
        .replace(">", "&gt;").replace('"', "&quot;")
    )


def hex_to_rgba(h: str) -> str:
    """'#FED760' -> '1.000 0.843 0.376 1' (FCPXML fontColor)."""
    h = h.lstrip("#")
    if len(h) != 6:
        return "1 1 1 1"
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return f"{r:.3f} {g:.3f} {b:.3f} 1"


def file_uri(path_str: str) -> str:
    """Absolute POSIX path -> percent-encoded file:// URI."""
    return "file://" + quote(path_str)


def apply_remap(path_str: str, remaps: list[tuple[str, str]]) -> str:
    """Rewrite a leading path prefix per the first matching --remap rule."""
    for frm, to in remaps:
        if path_str.startswith(frm):
            return to + path_str[len(frm):]
    return path_str


def probe_source(path: Path) -> tuple[float, int, int]:
    """Return (duration_seconds, width, height) for a source via ffprobe."""
    out = probe([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "format=duration:stream=width,height",
        "-of", "json", str(path),
    ])
    data = json.loads(out)
    dur = float(data.get("format", {}).get("duration", 0.0) or 0.0)
    stream = (data.get("streams") or [{}])[0]
    w = int(stream.get("width") or 1920)
    h = int(stream.get("height") or 1080)
    return dur, w, h


def resolve_source(maybe_path: str, base: Path) -> Path:
    p = Path(maybe_path)
    return p if p.is_absolute() else (base / maybe_path).resolve()


def load_transcript(edit_dir: Path, src_name: str) -> dict | None:
    p = edit_dir / "transcripts" / f"{src_name}.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def caption_chunks(transcript: dict, t0: float, t1: float) -> list[tuple[float, float, str]]:
    """2-word UPPERCASE chunks (break on punctuation) within [t0, t1)."""
    ws = [
        w for w in transcript.get("words", [])
        if w.get("type") == "word" and w.get("start") is not None
        and w.get("end") is not None and not (w["end"] <= t0 or w["start"] >= t1)
    ]
    chunks: list[list[dict]] = []
    cur: list[dict] = []
    for w in ws:
        tx = (w.get("text") or "").strip()
        if not tx:
            continue
        cur.append(w)
        if len(cur) >= 2 or tx[-1] in PUNCT_BREAK:
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    out: list[tuple[float, float, str]] = []
    for ch in chunks:
        ls = max(t0, ch[0].get("start", t0))
        le = min(t1, ch[-1].get("end", t1))
        txt = " ".join((w.get("text") or "").strip() for w in ch)
        txt = re.sub(r"\s+", " ", txt).strip().rstrip(",;:").upper()
        if txt:
            out.append((ls, le, txt))
    return out


def gather_assets(edl: dict, edit_dir: Path) -> dict:
    """One probed asset per unique source."""
    assets: dict[str, dict] = {}
    for i, (name, rel) in enumerate(edl["sources"].items(), start=1):
        path = resolve_source(rel, edit_dir)
        if not path.exists():
            sys.exit(f"source not found: {path}")
        dur, w, h = probe_source(path)
        assets[name] = {"idx": i, "path": path, "dur": dur, "w": w, "h": h}
    return assets


def build_fcpxml(edl: dict, edit_dir: Path, fps: int, project_name: str,
                 seq_wh: tuple[int, int] | None, captions: bool,
                 caption_color: str, remaps: list[tuple[str, str]]) -> str:
    ranges = edl["ranges"]
    if not ranges:
        sys.exit("EDL has no ranges to export")
    assets = gather_assets(edl, edit_dir)

    # Sequence raster: explicit override, else first range's source dims.
    if seq_wh:
        seq_w, seq_h = seq_wh
    else:
        a0 = assets[ranges[0]["source"]]
        seq_w, seq_h = a0["w"], a0["h"]

    cap_rgba = hex_to_rgba(caption_color)
    transcripts = {
        n: (load_transcript(edit_dir, n) if captions else None) for n in assets
    }

    # Build spine; accumulate timeline offset in frames (no rounding drift).
    spine: list[str] = []
    offset_frames = 0
    ts_id = 0
    for r in ranges:
        a = assets[r["source"]]
        start = float(r["start"])
        end = float(r["end"])
        seg = max(1, int(round((end - start) * fps)))
        cover = int(round(start * fps)) + seg
        a["dur_frames"] = max(a.get("dur_frames", 0),
                              max(int(round(a["dur"] * fps)), cover))

        caps_xml = ""
        tr = transcripts.get(r["source"])
        if captions and tr:
            cap_lines = []
            for ls, le, txt in caption_chunks(tr, start, end):
                cs = int(round((ls - start) * fps))
                cd = max(1, int(round((le - ls) * fps)))
                ts_id += 1
                cap_lines.append(
                    f'            <caption lane="1" offset="{cs}/{fps}s" '
                    f'name="cap{ts_id}" start="0s" duration="{cd}/{fps}s" '
                    f'role="iTT?.de-DE">\n'
                    f'              <text placement="bottom">'
                    f'<text-style ref="ts{ts_id}">{xa(txt)}</text-style></text>\n'
                    f'              <text-style-def id="ts{ts_id}">'
                    f'<text-style font="Helvetica" fontSize="62" bold="1" '
                    f'fontColor="{cap_rgba}" strokeColor="0 0 0 1" '
                    f'strokeWidth="6"/></text-style-def>\n'
                    f'            </caption>'
                )
            if cap_lines:
                caps_xml = "\n" + "\n".join(cap_lines)

        name = r.get("beat") or r.get("quote") or a["path"].stem
        spine.append(
            f'          <asset-clip ref="af{a["idx"]}" '
            f'offset="{offset_frames}/{fps}s" name="{xa(str(name)[:60])}" '
            f'start="{tc(start, fps)}" duration="{seg}/{fps}s" '
            f'tcFormat="NDF">{caps_xml}\n          </asset-clip>'
        )
        offset_frames += seg

    total = f"{offset_frames}/{fps}s"

    # Resources: one sequence format + one native format & asset per source.
    fmt_lines = [
        f'    <format id="rseq" name="FFVideoFormat{seq_h}p{fps}" '
        f'frameDuration="1/{fps}s" width="{seq_w}" height="{seq_h}" '
        f'colorSpace="1-1-1 (Rec. 709)"/>'
    ]
    asset_lines: list[str] = []
    for name, a in assets.items():
        disp = apply_remap(str(a["path"]), remaps)
        uri = file_uri(disp)
        fmt_lines.append(
            f'    <format id="ff{a["idx"]}" name="FFSource{a["idx"]}" '
            f'frameDuration="1/{fps}s" width="{a["w"]}" height="{a["h"]}" '
            f'colorSpace="1-1-1 (Rec. 709)"/>'
        )
        asset_lines.append(
            f'    <asset id="af{a["idx"]}" name="{xa(name)}" start="0s" '
            f'hasVideo="1" hasAudio="1" audioSources="1" audioChannels="2" '
            f'format="ff{a["idx"]}" duration="{a.get("dur_frames", 0)}/{fps}s">\n'
            f'      <media-rep kind="original-media" src="{xa(uri)}"/>\n'
            f'    </asset>'
        )

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE fcpxml>\n'
        '<fcpxml version="1.10">\n'
        '  <resources>\n'
        + "\n".join(fmt_lines) + "\n"
        + "\n".join(asset_lines) + "\n"
        '  </resources>\n'
        '  <library>\n'
        '    <event name="agency-os-video">\n'
        f'      <project name="{xa(project_name)}">\n'
        f'        <sequence format="rseq" tcStart="0s" tcFormat="NDF" duration="{total}">\n'
        '          <spine>\n'
        + "\n".join(spine) + "\n"
        '          </spine>\n'
        '        </sequence>\n'
        '      </project>\n'
        '    </event>\n'
        '  </library>\n'
        '</fcpxml>\n'
    )


def build_fcp7_xml(edl: dict, edit_dir: Path, fps: int, project_name: str,
                   seq_wh: tuple[int, int] | None,
                   remaps: list[tuple[str, str]]) -> str:
    """Final Cut Pro 7 xmeml (Premiere). Cut only; captions via SRT."""
    ranges = edl["ranges"]
    if not ranges:
        sys.exit("EDL has no ranges to export")
    assets = gather_assets(edl, edit_dir)
    for a in assets.values():
        a["frames"] = int(round(a["dur"] * fps))
    if seq_wh:
        seq_w, seq_h = seq_wh
    else:
        a0 = assets[ranges[0]["source"]]
        seq_w, seq_h = a0["w"], a0["h"]

    seen: set[str] = set()
    v: list[str] = []
    aud: list[str] = []
    tl = 0
    for n, r in enumerate(ranges, 1):
        a = assets[r["source"]]
        sin = int(round(float(r["start"]) * fps))
        seg = max(1, int(round(float(r["end"]) * fps)) - sin)
        sout = sin + seg
        ts, te = tl, tl + seg
        tl = te
        fid = f'file-{a["idx"]}'
        if r["source"] not in seen:
            seen.add(r["source"])
            disp = apply_remap(str(a["path"]), remaps)
            fileref = (
                f'<file id="{fid}">\n'
                f'            <name>{xa(a["path"].name)}</name>\n'
                f'            <pathurl>{xa(file_uri(disp))}</pathurl>\n'
                f'            <rate><timebase>{fps}</timebase><ntsc>FALSE</ntsc></rate>\n'
                f'            <duration>{a["frames"]}</duration>\n'
                f'            <media>\n'
                f'              <video><samplecharacteristics><rate><timebase>{fps}</timebase>'
                f'<ntsc>FALSE</ntsc></rate><width>{a["w"]}</width><height>{a["h"]}</height>'
                f'</samplecharacteristics></video>\n'
                f'              <audio><samplecharacteristics><depth>16</depth>'
                f'<samplerate>48000</samplerate></samplecharacteristics>'
                f'<channelcount>2</channelcount></audio>\n'
                f'            </media>\n'
                f'          </file>'
            )
        else:
            fileref = f'<file id="{fid}"/>'
        nm = xa((r.get("quote") or r.get("beat") or a["path"].stem)[:40])
        link = (
            f'<link><linkclipref>v{n}</linkclipref><mediatype>video</mediatype>'
            f'<trackindex>1</trackindex><clipindex>{n}</clipindex></link>'
            f'<link><linkclipref>a{n}</linkclipref><mediatype>audio</mediatype>'
            f'<trackindex>1</trackindex><clipindex>{n}</clipindex></link>'
        )
        v.append(
            f'        <clipitem id="v{n}">\n'
            f'          <name>{nm}</name><enabled>TRUE</enabled><duration>{a["frames"]}</duration>\n'
            f'          <rate><timebase>{fps}</timebase><ntsc>FALSE</ntsc></rate>\n'
            f'          <start>{ts}</start><end>{te}</end><in>{sin}</in><out>{sout}</out>\n'
            f'          {fileref}\n          {link}\n        </clipitem>'
        )
        aud.append(
            f'        <clipitem id="a{n}">\n'
            f'          <name>{nm}</name><enabled>TRUE</enabled><duration>{a["frames"]}</duration>\n'
            f'          <rate><timebase>{fps}</timebase><ntsc>FALSE</ntsc></rate>\n'
            f'          <start>{ts}</start><end>{te}</end><in>{sin}</in><out>{sout}</out>\n'
            f'          <file id="{fid}"/>'
            f'<sourcetrack><mediatype>audio</mediatype><trackindex>1</trackindex></sourcetrack>\n'
            f'          {link}\n        </clipitem>'
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE xmeml>\n'
        '<xmeml version="4">\n'
        f'  <sequence id="{xa(project_name).replace(" ", "-").lower()}">\n'
        f'    <name>{xa(project_name)}</name>\n'
        f'    <duration>{tl}</duration>\n'
        f'    <rate><timebase>{fps}</timebase><ntsc>FALSE</ntsc></rate>\n'
        '    <media>\n'
        '      <video>\n'
        f'        <format><samplecharacteristics><rate><timebase>{fps}</timebase>'
        f'<ntsc>FALSE</ntsc></rate><width>{seq_w}</width><height>{seq_h}</height>'
        '<pixelaspectratio>square</pixelaspectratio></samplecharacteristics></format>\n'
        '        <track>\n'
        + "\n".join(v) + "\n"
        '        </track>\n'
        '      </video>\n'
        '      <audio>\n'
        '        <format><samplecharacteristics><depth>16</depth>'
        '<samplerate>48000</samplerate></samplecharacteristics></format>\n'
        '        <track>\n'
        + "\n".join(aud) + "\n"
        '        </track>\n'
        '      </audio>\n'
        '    </media>\n'
        '  </sequence>\n'
        '</xmeml>\n'
    )


def parse_remaps(items: list[str]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for it in items or []:
        if "=" not in it:
            sys.exit(f"--remap expects FROM=TO, got: {it}")
        frm, to = it.split("=", 1)
        out.append((frm, to))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Export an EDL as FCPXML / FCP7 XML")
    ap.add_argument("edl", type=Path, help="Path to edl.json")
    ap.add_argument("-o", "--output", type=Path, default=None,
                    help="Output path (default: <edit>/final.fcpxml resp. _premiere.xml)")
    ap.add_argument("--fps", type=int, default=24,
                    help="Project frame rate (24/25/30/50/60). Default 24.")
    ap.add_argument("--name", type=str, default=None, help="Project name in the NLE")
    ap.add_argument("--format", choices=["fcpxml", "premiere", "both"],
                    default="fcpxml", help="Output format. Default fcpxml.")
    ap.add_argument("--width", type=int, default=None, help="Timeline width override")
    ap.add_argument("--height", type=int, default=None, help="Timeline height override")
    ap.add_argument("--captions", action="store_true",
                    help="Embed captions from <edit>/transcripts/<src>.json (fcpxml only)")
    ap.add_argument("--caption-color", type=str, default="FFFFFF",
                    help="Caption fill hex (default FFFFFF)")
    ap.add_argument("--remap", action="append", default=[],
                    help="Rewrite media path prefix: FROM=TO (repeatable)")
    args = ap.parse_args()

    edl_path = args.edl.resolve()
    if not edl_path.exists():
        sys.exit(f"edl not found: {edl_path}")
    edl = json.loads(edl_path.read_text())
    edit_dir = edl_path.parent
    name = args.name or edit_dir.name
    remaps = parse_remaps(args.remap)
    seq_wh = (args.width, args.height) if (args.width and args.height) else None

    if args.width and not args.height or args.height and not args.width:
        sys.exit("--width and --height must be given together")

    wrote = []
    if args.format in ("fcpxml", "both"):
        out = args.output if (args.output and args.format == "fcpxml") else None
        if out is None:
            stem = (args.output.stem if args.output else "final")
            out = edit_dir / f"{stem}.fcpxml"
        xml = build_fcpxml(edl, edit_dir, args.fps, name, seq_wh,
                           args.captions, args.caption_color, remaps)
        out.resolve().write_text(xml, encoding="utf-8")
        wrote.append(out.resolve())
        print(f"FCPXML -> {out}  ({len(edl['ranges'])} clips @ {args.fps}fps"
              f"{', captions' if args.captions else ''})")
        print("Import in Resolve: File > Import > Timeline > Import XML.")

    if args.format in ("premiere", "both"):
        if args.output and args.format == "premiere":
            out = args.output
        else:
            stem = (args.output.stem if args.output else "final")
            out = edit_dir / f"{stem}_premiere.xml"
        xml = build_fcp7_xml(edl, edit_dir, args.fps, name, seq_wh, remaps)
        out.resolve().write_text(xml, encoding="utf-8")
        wrote.append(out.resolve())
        print(f"FCP7 XML -> {out}  ({len(edl['ranges'])} clips @ {args.fps}fps)")
        print("Import in Premiere: File > Import. Captions: import the SRT separately.")


if __name__ == "__main__":
    main()
