"""Render a video from an EDL.

Implements the HEURISTICS render pipeline in the correct order:

  1. Per-segment extract with color grade + 30ms audio fades baked in
  2. Lossless -c copy concat into base.mp4
  3. If overlays or subtitles: single filter graph that overlays animations
     (with PTS shift so frame 0 lands at the overlay window start)
     and applies `subtitles` filter LAST → final.mp4

Optionally builds a master SRT from the per-source transcripts + EDL
output-timeline offsets, applies the proven force_style (2-word
UPPERCASE chunks, Helvetica 18 Bold, MarginV=35).

Usage:
    python helpers/render.py <edl.json> -o final.mp4
    python helpers/render.py <edl.json> -o preview.mp4 --preview
    python helpers/render.py <edl.json> -o final.mp4 --build-subtitles
    python helpers/render.py <edl.json> -o final.mp4 --no-subtitles
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

from ffmpeg_utils import run as ffrun

try:
    from grade import get_preset, auto_grade_for_clip, lut_filter  # same directory
except Exception:
    def get_preset(name: str) -> str:
        return ""

    def auto_grade_for_clip(video, start=0.0, duration=None, verbose=False):  # type: ignore
        return "eq=contrast=1.03:saturation=0.98", {}

    def lut_filter(lut_path) -> str:  # type: ignore
        return f"lut3d='{lut_path}'"


# -------- Subtitle style (bold-overlay, proven at 1920×1080 and 1080×1920) --
#
# MarginV is NOT taste — it is a platform safe-zone rule.
# TikTok / IG Reels / Shorts UI (caption, username, music, right-rail actions)
# covers roughly the bottom ~25–30% of a 1080×1920 frame. Captions placed near
# the bottom edge get clipped or obscured by the UI. libass auto-scales the
# render canvas relative to PlayResY=288, so MarginV=90 lands the caption
# baseline roughly 30% up from the bottom on any aspect — clear of the UI on
# every major vertical-video platform. Do not drop this below ~75 without a
# specific reason.
def _color_to_ass(value: str | None) -> str:
    """Accept an ASS &H.. value as-is, a #RRGGBB hex (-> &H00BBGGRR), or None -> white."""
    if not value:
        return "&H00FFFFFF"
    v = value.strip()
    if v.lower().startswith("&h"):
        return v
    m = re.search(r"#?([0-9a-fA-F]{6})\b", v)
    if not m:
        return "&H00FFFFFF"
    rr, gg, bb = m.group(1)[0:2], m.group(1)[2:4], m.group(1)[4:6]
    return f"&H00{bb}{gg}{rr}".upper()


def build_sub_style(color: str | None = None, font: str | None = None) -> str:
    """Build the libass force_style from optional CI values. MarginV/Bold/Outline are
    the proven safe-zone defaults (do not lower MarginV below ~75). Colour accepts hex
    or ASS; font falls back to a widely available family when none is given.

    MarginL/MarginR enforce a caption max width: without them long cues run almost to
    the frame edge. Values are in libass' default 384x288 script space (same space as
    MarginV=90), so 46 ≈ 12% per side ≈ 130px on a 1080-wide frame — inside the safe
    zone. libass then wraps cues that exceed the remaining width instead of overflowing."""
    return (
        f"FontName={font or 'Helvetica'},FontSize=18,Bold=1,"
        f"PrimaryColour={_color_to_ass(color)},OutlineColour=&H00000000,BackColour=&H00000000,"
        "BorderStyle=1,Outline=2,Shadow=0,"
        "Alignment=2,MarginV=90,MarginL=46,MarginR=46"
    )


# Default style (white, Helvetica) — used when no CI caption colour/font is passed.
SUB_FORCE_STYLE = build_sub_style()

# -------- Helpers ------------------------------------------------------------


def run(cmd: list[str], quiet: bool = False) -> None:
    if not quiet:
        print(f"  $ {' '.join(str(c) for c in cmd[:6])}{' …' if len(cmd) > 6 else ''}")
    ffrun(cmd)


def resolve_grade_filter(grade_field: str | None, edit_dir: Path) -> str:
    """The EDL's 'grade' field can be a preset name, a .cube LUT, a raw ffmpeg
    filter, or 'auto'.

    Recognized forms:
      - "auto"                  -> sentinel "__AUTO__" (resolved per-segment)
      - "lut:/path/look.cube"   -> lut3d filter (path relative to edit_dir)
      - "<preset_name>"         -> the preset's filter chain
      - "<raw ffmpeg filter>"   -> used verbatim

    Returns the filter string to embed into the per-segment -vf chain.
    """
    if not grade_field:
        return ""
    if grade_field == "auto":
        return "__AUTO__"
    if grade_field.startswith("lut:"):
        lut_path = Path(grade_field[len("lut:"):].strip())
        if not lut_path.is_absolute():
            lut_path = edit_dir / lut_path
        return lut_filter(lut_path)
    # Preset names are short identifiers, filter strings contain '=' or ','.
    if re.fullmatch(r"[a-zA-Z0-9_\-]+", grade_field):
        try:
            return get_preset(grade_field)
        except KeyError:
            print(f"warning: unknown preset '{grade_field}', using as raw filter")
            return grade_field
    return grade_field


def resolve_path(maybe_path: str, base: Path) -> Path:
    """Resolve a path that may be absolute or relative to `base`."""
    p = Path(maybe_path)
    if p.is_absolute():
        return p
    return (base / p).resolve()


# -------- HDR → SDR tone mapping (HLG / PQ sources) --------------------------
#
# iPhone defaults to HLG HDR in Rec.2020 (and many mirrorless cameras ship PQ).
# If the source is HDR and we only downconvert bit depth (yuv420p10le → yuv420p)
# without tone-mapping, the output is 8-bit but still carries HLG/PQ transfer
# metadata. Players that honor the metadata (screen recorders, most social
# upload re-encodes) interpret 8-bit values in an HDR container and the result
# looks oversaturated / blown out. QuickTime on macOS can hide this locally —
# screen recording and uploaded renders cannot.
#
# Fix: detect HDR via color_transfer and prepend a zscale+tonemap chain to the
# vf graph so the output is clean Rec.709 SDR.

HDR_TRANSFERS = {"smpte2084", "arib-std-b67"}  # PQ (HDR10) and HLG

TONEMAP_CHAIN = (
    "zscale=t=linear:npl=100,"
    "format=gbrpf32le,"
    "zscale=p=bt709,"
    "tonemap=tonemap=hable:desat=0,"
    "zscale=t=bt709:m=bt709:r=tv,"
    "format=yuv420p"
)


# Probes are cached per source path: extract_segment runs once per EDL range,
# but HDR/orientation/frame rate are properties of the source file, not the cut.
_STREAM_CACHE: dict[str, dict] = {}


def probe_stream(video: Path) -> dict:
    """Cached JSON probe of the first video stream.

    JSON on purpose, never `-of csv=p=0`: ffprobe 8 appends a trailing separator
    to CSV rows ("3840,2160,"), which made the old width/height parse raise and
    silently fall back to landscape. Every portrait render came out scaled by
    width (1920x3414 instead of 1080x1920).
    """
    key = str(video)
    if key in _STREAM_CACHE:
        return _STREAM_CACHE[key]
    data: dict = {}
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-print_format", "json", "-show_streams", str(video)],
            capture_output=True, text=True, check=True,
        )
        streams = json.loads(out.stdout).get("streams") or []
        data = streams[0] if streams else {}
    except Exception as exc:
        print(f"warning: ffprobe failed for {video.name}: {exc}")
    _STREAM_CACHE[key] = data
    return data


def is_hdr_source(video: Path) -> bool:
    """Return True if the source uses a PQ or HLG transfer function."""
    return str(probe_stream(video).get("color_transfer") or "") in HDR_TRANSFERS


def display_size(video: Path) -> tuple[int, int]:
    """Frame size as it is DISPLAYED, i.e. after rotation. (0, 0) if unknown.

    Phones store landscape pixels plus a rotation flag; ffmpeg autorotates on
    decode, so the filter graph sees the swapped size and the scale filter has
    to be chosen for that, not for the stored size.
    """
    stream = probe_stream(video)
    try:
        w, h = int(stream["width"]), int(stream["height"])
    except (KeyError, TypeError, ValueError):
        return 0, 0
    rot = 0
    for side in stream.get("side_data_list") or []:
        if "rotation" in side:
            try:
                rot = int(float(side["rotation"]))
            except (TypeError, ValueError):
                rot = 0
            break
    else:
        try:
            rot = int(float((stream.get("tags") or {}).get("rotate") or 0))
        except (TypeError, ValueError):
            rot = 0
    if rot % 180 != 0:
        w, h = h, w
    return w, h


def is_portrait_source(video: Path) -> bool:
    """Return True if the displayed frame is taller than wide."""
    w, h = display_size(video)
    if not w or not h:
        # Loud on purpose: a silent landscape default is exactly what produced
        # 1920x3414 renders from portrait phone clips.
        print(f"warning: no frame size for {video.name}, treating it as landscape")
        return False
    return h > w


def source_frame_rate(video: Path) -> str | None:
    """Source frame rate as the exact ffmpeg rational ("30000/1001"), or None.

    Returned verbatim so 29.97 stays 30000/1001 instead of being rounded.
    r_frame_rate first (the nominal rate), avg_frame_rate only as a fallback: the
    average is a measured value and yields unusable rationals like 128000/4267.
    Both are sanity-checked, which also rejects the bogus high r_frame_rate some
    variable-frame-rate screen recordings report.
    """
    stream = probe_stream(video)
    for key in ("r_frame_rate", "avg_frame_rate"):
        raw = str(stream.get(key) or "")
        try:
            num, den = raw.split("/")
            fps = float(num) / float(den)
        except (ValueError, ZeroDivisionError):
            continue
        if 1.0 < fps <= 120.0:
            return raw
    return None


# -------- Per-segment extraction (Rule 2 + Rule 3) --------------------------


def media_is_valid(path: Path) -> bool:
    """True if ffprobe reads a positive duration, i.e. the file has a moov atom and
    is not a truncated/partial render. Used to skip already-rendered segments and to
    reject corrupt leftovers from an interrupted run."""
    if not path.exists() or path.stat().st_size == 0:
        return False
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(path)],
            capture_output=True, text=True, timeout=30,
        )
    except Exception:
        return False
    if out.returncode != 0:
        return False
    try:
        return float(out.stdout.strip() or 0) > 0
    except ValueError:
        return False


def extract_segment(
    source: Path,
    seg_start: float,
    duration: float,
    grade_filter: str,
    out_path: Path,
    preview: bool = False,
    draft: bool = False,
    fps: str = "24",
) -> None:
    """Extract a cut range as its own MP4 with grade + 30ms audio fades baked in.

    `-ss` before `-i` for fast accurate seeking. Scale to 1080p from 4K.
    Portrait sources (height > width) are scaled by height to preserve orientation.

    Quality ladder:
      - final (default): 1080p libx264 fast CRF 20
      - preview:         1080p libx264 medium CRF 22 (evaluable for QC)
      - draft:           720p libx264 ultrafast CRF 28 (cut-point check only)
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)

    portrait = is_portrait_source(source)
    if draft:
        scale = "scale=-2:1280" if portrait else "scale=1280:-2"
    else:
        scale = "scale=-2:1920" if portrait else "scale=1920:-2"

    vf_parts: list[str] = []
    if is_hdr_source(source):
        vf_parts.append(TONEMAP_CHAIN)
    vf_parts.append(scale)
    if grade_filter:
        vf_parts.append(grade_filter)
    vf = ",".join(vf_parts)

    # 30ms audio fades at both edges (Rule 3) — prevent pops
    fade_out_start = max(0.0, duration - 0.03)
    af = f"afade=t=in:st=0:d=0.03,afade=t=out:st={fade_out_start:.3f}:d=0.03"

    if draft:
        preset, crf = "ultrafast", "28"
    elif preview:
        preset, crf = "medium", "22"
    else:
        preset, crf = "fast", "20"

    # Atomic: render to a .part.mp4, rename on success. An interrupted ffmpeg then
    # never leaves a corrupt seg_NN.mp4 (moov atom not found) that a resume would trust.
    tmp_path = out_path.with_suffix(".part.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{seg_start:.3f}",
        "-i", str(source),
        "-t", f"{duration:.3f}",
        "-vf", vf,
        "-af", af,
        "-c:v", "libx264", "-preset", preset, "-crf", crf,
        # Every segment is forced to ONE frame rate so the concat is seamless;
        # the value comes from the source, not from a hardcoded 24.
        "-pix_fmt", "yuv420p", "-r", fps,
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(tmp_path),
    ]
    ffrun(cmd)
    tmp_path.replace(out_path)


def extract_all_segments(
    edl: dict,
    edit_dir: Path,
    preview: bool,
    draft: bool = False,
    budget_deadline: float | None = None,
    fps_override: str | None = None,
) -> tuple[list[Path], bool]:
    """Extract every EDL range into edit_dir/clips_graded/seg_NN.mp4.
    Returns (ordered segment paths, complete?).

    Idempotent + resumable: a segment that already exists and is a valid media file
    is skipped, so re-running the same command continues where an interrupted run
    stopped. If `budget_deadline` (epoch seconds) is given, the loop stops after the
    segment that crosses it and returns complete=False; the caller re-runs to resume.

    If the EDL `grade` is "auto", analyze each segment range with
    `auto_grade_for_clip` and apply a per-segment subtle correction.
    Otherwise, apply the same preset/raw filter to every segment.
    """
    resolved = resolve_grade_filter(edl.get("grade"), edit_dir)
    is_auto = resolved == "__AUTO__"
    clips_dir = edit_dir / (
        "clips_draft" if draft else ("clips_preview" if preview else "clips_graded")
    )
    clips_dir.mkdir(parents=True, exist_ok=True)

    ranges = edl["ranges"]
    sources = edl["sources"]

    # One frame rate for all segments (concat requirement). Prefer the explicit
    # override, else the first source's rate, else the old 24 as last resort.
    fps = fps_override
    if not fps:
        for name in (r["source"] for r in ranges):
            fps = source_frame_rate(resolve_path(sources[name], edit_dir))
            if fps:
                break
    if not fps:
        fps = "24"
        print("  (no source frame rate readable, falling back to 24 fps)")
    else:
        print(f"  (frame rate: {fps})")

    seg_paths: list[Path] = []
    print(f"extracting {len(ranges)} segment(s) → {clips_dir.name}/")
    if is_auto:
        print("  (auto-grade per segment: analyzing each range)")
    for i, r in enumerate(ranges):
        src_name = r["source"]
        out_path = clips_dir / f"seg_{i:02d}_{src_name}.mp4"

        # Skip if already rendered and valid (resume after an interrupted run).
        if media_is_valid(out_path):
            print(f"  [{i:02d}] {src_name}  cached, skip")
            seg_paths.append(out_path)
            continue

        src_path = resolve_path(sources[src_name], edit_dir)
        start = float(r["start"])
        end = float(r["end"])
        duration = end - start

        if is_auto:
            seg_filter, _stats = auto_grade_for_clip(src_path, start=start, duration=duration, verbose=False)
        else:
            seg_filter = resolved

        note = r.get("beat") or r.get("note") or ""
        print(f"  [{i:02d}] {src_name}  {start:7.2f}-{end:7.2f}  ({duration:5.2f}s)  {note}")
        if is_auto:
            print(f"        grade: {seg_filter or '(none)'}")
        extract_segment(src_path, start, duration, seg_filter, out_path,
                        preview=preview, draft=draft, fps=fps)
        seg_paths.append(out_path)

        if budget_deadline is not None and time.time() >= budget_deadline:
            return seg_paths, (i == len(ranges) - 1)

    return seg_paths, True


# -------- Lossless concat ----------------------------------------------------


def concat_segments(segment_paths: list[Path], out_path: Path, edit_dir: Path) -> None:
    """Lossless concat via the concat demuxer. No re-encode."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    concat_list = edit_dir / "_concat.txt"
    concat_list.write_text("".join(f"file '{p.resolve()}'\n" for p in segment_paths))

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        "-movflags", "+faststart",
        str(out_path),
    ]
    print(f"concat → {out_path.name}")
    ffrun(cmd)
    try:
        concat_list.unlink(missing_ok=True)
    except OSError:
        pass  # Cowork mount may forbid unlink (EPERM); leftover is gitignored cache, harmless


# -------- Master SRT (Rule 5) ------------------------------------------------


PUNCT_BREAK = set(".,!?;:")


def _srt_timestamp(seconds: float) -> str:
    total_ms = int(round(seconds * 1000))
    h, rem = divmod(total_ms, 3600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _words_in_range(transcript: dict, t_start: float, t_end: float) -> list[dict]:
    out: list[dict] = []
    for w in transcript.get("words", []):
        if w.get("type") != "word":
            continue
        ws = w.get("start")
        we = w.get("end")
        if ws is None or we is None:
            continue
        if we <= t_start or ws >= t_end:
            continue
        out.append(w)
    return out


def build_master_srt(edl: dict, edit_dir: Path, out_path: Path) -> None:
    """Build an output-timeline SRT from per-source transcripts.

    - 2-word chunks (break on any punctuation in between)
    - UPPERCASE text
    - Output times computed as word.start - segment_start + segment_offset
    """
    transcripts_dir = edit_dir / "transcripts"
    sources = edl["sources"]

    entries: list[tuple[float, float, str]] = []
    seg_offset = 0.0

    for r in edl["ranges"]:
        src_name = r["source"]
        seg_start = float(r["start"])
        seg_end = float(r["end"])
        seg_duration = seg_end - seg_start

        tr_path = transcripts_dir / f"{src_name}.json"
        if not tr_path.exists():
            print(f"  no transcript for {src_name}, skipping captions for this segment")
            seg_offset += seg_duration
            continue

        transcript = json.loads(tr_path.read_text())
        words_in_seg = _words_in_range(transcript, seg_start, seg_end)

        # Group into 2-word chunks, break on punctuation
        chunks: list[list[dict]] = []
        current: list[dict] = []
        for w in words_in_seg:
            text = (w.get("text") or "").strip()
            if not text:
                continue
            current.append(w)
            # Break if the current text ends in punctuation or we hit 2 words
            ends_in_punct = bool(text) and text[-1] in PUNCT_BREAK
            if len(current) >= 2 or ends_in_punct:
                chunks.append(current)
                current = []
        if current:
            chunks.append(current)

        for chunk in chunks:
            local_start = max(seg_start, chunk[0].get("start", seg_start))
            local_end = min(seg_end, chunk[-1].get("end", seg_end))
            out_start = max(0.0, local_start - seg_start) + seg_offset
            out_end = max(0.0, local_end - seg_start) + seg_offset
            if out_end < out_start:
                out_end = out_start
            text = " ".join((w.get("text") or "").strip() for w in chunk)
            text = re.sub(r"\s+", " ", text).strip()
            # Strip trailing punctuation for cleaner uppercase look
            text = text.rstrip(",;:")
            text = text.upper()
            entries.append((out_start, out_end, text))

        seg_offset += seg_duration

    # Sort, then give each cue a minimum on-screen time WITHOUT ever overlapping
    # the next one. Extending a short cue toward the next cue is fine, but it must
    # never run past the next cue's start: overlapping cues make libass stack them
    # and a caption appears to "jump" upward. Touching (end == next start) is safe.
    entries.sort(key=lambda e: e[0])
    MIN_CUE = 0.3
    fixed: list[tuple[float, float, str]] = []
    for i, (a, b, t) in enumerate(entries):
        end = max(b, a + MIN_CUE)
        if i + 1 < len(entries):
            end = min(end, entries[i + 1][0])  # never overlap the next cue
        if end < a:
            end = a
        fixed.append((a, end, t))
    entries = fixed

    lines: list[str] = []
    for i, (a, b, t) in enumerate(entries, start=1):
        lines.append(str(i))
        lines.append(f"{_srt_timestamp(a)} --> {_srt_timestamp(b)}")
        lines.append(t)
        lines.append("")
    out_path.write_text("\n".join(lines))
    print(f"master SRT → {out_path.name} ({len(entries)} cues)")


# -------- Loudness normalization (social-ready audio) -----------------------


# Social-media standard: -14 LUFS integrated, -1 dBTP peak, LRA 11 LU.
# Matches YouTube / Instagram / TikTok / X / LinkedIn normalization targets.
LOUDNORM_I = -14.0
LOUDNORM_TP = -1.0
LOUDNORM_LRA = 11.0


def measure_loudness(video_path: Path) -> dict[str, str] | None:
    """Run ffmpeg loudnorm first pass and parse the JSON measurement.

    Returns a dict with measured_i, measured_tp, measured_lra, measured_thresh,
    target_offset, or None if measurement failed.
    """
    filter_str = (
        f"loudnorm=I={LOUDNORM_I}:TP={LOUDNORM_TP}:LRA={LOUDNORM_LRA}:print_format=json"
    )
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-nostats",
        "-i", str(video_path),
        "-af", filter_str,
        "-vn", "-f", "null", "-",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    # loudnorm prints the JSON to stderr at the end of the run
    stderr = proc.stderr

    # Find the JSON block — loudnorm output contains a `{ ... }` block
    start = stderr.rfind("{")
    end = stderr.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        data = json.loads(stderr[start : end + 1])
    except json.JSONDecodeError:
        return None
    needed = {"input_i", "input_tp", "input_lra", "input_thresh", "target_offset"}
    if not needed.issubset(data.keys()):
        return None
    return data


def apply_loudnorm_two_pass(
    input_path: Path,
    output_path: Path,
    preview: bool = False,
) -> bool:
    """Run two-pass loudnorm on input_path, write normalized copy to output_path.

    Returns True on success, False if measurement failed (caller should fall
    back to copying the input unchanged).

    In preview mode, skips the measurement pass and uses a one-pass approximation
    for speed. Final mode always does the proper two-pass.
    """
    if preview:
        # One-pass approximation — faster, slightly less accurate.
        filter_str = f"loudnorm=I={LOUDNORM_I}:TP={LOUDNORM_TP}:LRA={LOUDNORM_LRA}"
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-nostats",
            "-i", str(input_path),
            "-c:v", "copy",
            "-af", filter_str,
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart",
            str(output_path),
        ]
        print(f"  loudnorm (1-pass preview) → {output_path.name}")
        ffrun(cmd)
        return True

    # Full two-pass
    print(f"  loudnorm pass 1: measuring {input_path.name}")
    measurement = measure_loudness(input_path)
    if measurement is None:
        print("  loudnorm measurement failed — falling back to 1-pass")
        return apply_loudnorm_two_pass(input_path, output_path, preview=True)

    print(f"    measured: I={measurement['input_i']} LUFS  "
          f"TP={measurement['input_tp']}  LRA={measurement['input_lra']}")

    filter_str = (
        f"loudnorm=I={LOUDNORM_I}:TP={LOUDNORM_TP}:LRA={LOUDNORM_LRA}"
        f":measured_I={measurement['input_i']}"
        f":measured_TP={measurement['input_tp']}"
        f":measured_LRA={measurement['input_lra']}"
        f":measured_thresh={measurement['input_thresh']}"
        f":offset={measurement['target_offset']}"
        f":linear=true"
    )
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-nostats",
        "-i", str(input_path),
        "-c:v", "copy",
        "-af", filter_str,
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(output_path),
    ]
    print(f"  loudnorm pass 2: normalizing → {output_path.name}")
    ffrun(cmd)
    return True


# -------- Final compositing (Rule 1 + Rule 4) -------------------------------


def build_final_composite(
    base_path: Path,
    overlays: list[dict],
    subtitles_path: Path | None,
    out_path: Path,
    edit_dir: Path,
    force_style: str = SUB_FORCE_STYLE,
    fonts_dir: Path | None = None,
) -> None:
    """Final pass: base → overlays (PTS-shifted) → subtitles LAST → out.

    If there are no overlays and no subtitles, just copy base to out.
    """
    has_overlays = bool(overlays)
    has_subs = subtitles_path is not None and subtitles_path.exists()

    if not has_overlays and not has_subs:
        # Nothing to do — just rename/copy base to final name
        run(["ffmpeg", "-y", "-i", str(base_path), "-c", "copy", str(out_path)], quiet=True)
        return

    inputs: list[str] = ["-i", str(base_path)]
    for ov in overlays:
        ov_path = resolve_path(ov["file"], edit_dir)
        inputs += ["-i", str(ov_path)]

    filter_parts: list[str] = []
    # PTS-shift every overlay so its frame 0 lands at start_in_output
    for idx, ov in enumerate(overlays, start=1):
        t = float(ov["start_in_output"])
        filter_parts.append(f"[{idx}:v]setpts=PTS-STARTPTS+{t}/TB[a{idx}]")

    # Chain overlays on top of base
    current = "[0:v]"
    for idx, ov in enumerate(overlays, start=1):
        t = float(ov["start_in_output"])
        dur = float(ov["duration"])
        end = t + dur
        next_label = f"[v{idx}]"
        filter_parts.append(
            f"{current}[a{idx}]overlay=enable='between(t,{t:.3f},{end:.3f})'{next_label}"
        )
        current = next_label

    # Subtitles LAST — Rule 1
    if has_subs:
        # Escape for the `subtitles` filter inside a filter_complex string.
        # Backslash first, then the chars libavfilter treats specially.
        subs_abs = str(subtitles_path.resolve())
        for ch in ("\\", ":", "'", "[", "]", ","):
            subs_abs = subs_abs.replace(ch, "\\" + ch)
        filter_parts.append(
            # An .ass carries its own styles (and \pos overrides); force_style would
            # overwrite font size, margins and alignment, so only style plain SRT.
            f"{current}subtitles='{subs_abs}'"
            + (f":force_style='{force_style}'" if subtitles_path.suffix.lower() not in (".ass", ".ssa") else "")
            + (f":fontsdir='{fonts_dir.resolve()}'" if fonts_dir else "")
            + "[outv]"
        )
        out_label = "[outv]"
    else:
        # Rename the last overlay output to [outv] for consistency
        if has_overlays:
            filter_parts.append(f"{current}null[outv]")
            out_label = "[outv]"
        else:
            out_label = "[0:v]"

    filter_complex = ";".join(filter_parts)

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", out_label,
        "-map", "0:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-movflags", "+faststart",
        str(out_path),
    ]
    print(f"compositing → {out_path.name}")
    print(f"  overlays: {len(overlays)}, subtitles: {'yes' if has_subs else 'no'}")
    ffrun(cmd)


# -------- Main ---------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description="Render a video from an EDL")
    ap.add_argument("edl", type=Path, help="Path to edl.json")
    ap.add_argument("-o", "--output", type=Path, required=True, help="Output video path")
    ap.add_argument(
        "--preview",
        action="store_true",
        help="Preview mode: 1080p, medium, CRF 22 — evaluable for QC, faster than final.",
    )
    ap.add_argument(
        "--draft",
        action="store_true",
        help="Draft mode: 720p, ultrafast, CRF 28 — cut-point verification only.",
    )
    ap.add_argument(
        "--fps",
        help="Force an output frame rate (e.g. 25 or 30000/1001). Default: the source's rate",
    )
    p.add_argument(
        "--fonts-dir",
        type=Path,
        help="Directory holding the caption font file (for .ass with a brand font)",
    )
    p.add_argument(
        "--build-subtitles",
        action="store_true",
        help="Build master.srt from transcripts + EDL offsets before compositing",
    )
    ap.add_argument(
        "--no-subtitles",
        action="store_true",
        help="Skip subtitles even if the EDL references one",
    )
    ap.add_argument(
        "--no-loudnorm",
        action="store_true",
        help="Skip audio loudness normalization. Default is on (-14 LUFS, -1 dBTP, LRA 11).",
    )
    ap.add_argument(
        "--budget-seconds",
        type=float,
        default=None,
        help="Stop segment extraction after this many seconds and exit (resumable: "
             "re-run the same command to continue). Useful where a single call is "
             "time-limited; omit for a one-shot run.",
    )
    ap.add_argument(
        "--caption-color",
        default=None,
        help="Subtitle colour as hex (#FED760) or ASS (&H0060D7FE), from the brand CI. Default white.",
    )
    ap.add_argument(
        "--caption-font",
        default=None,
        help="Subtitle font name (libass) from the brand CI. Default Helvetica.",
    )
    args = ap.parse_args()

    edl_path = args.edl.resolve()
    if not edl_path.exists():
        sys.exit(f"edl not found: {edl_path}")

    edl = json.loads(edl_path.read_text())
    edit_dir = edl_path.parent
    out_path = args.output.resolve()

    # 1. Extract per-segment (auto-grade per range if EDL grade is "auto").
    #    Idempotent + resumable; honours an optional time budget.
    budget_deadline = (time.time() + args.budget_seconds) if args.budget_seconds else None
    segment_paths, complete = extract_all_segments(
        edl, edit_dir, preview=args.preview, draft=args.draft,
        budget_deadline=budget_deadline, fps_override=args.fps,
    )
    if not complete:
        print(f"\n[budget] {len(segment_paths)} Segment(e) fertig, weitere offen. "
              f"Denselben Befehl erneut aufrufen - er macht beim naechsten Segment weiter.")
        return

    # 2. Concat → base
    if args.draft:
        base_name = "base_draft.mp4"
    elif args.preview:
        base_name = "base_preview.mp4"
    else:
        base_name = "base.mp4"
    base_path = edit_dir / base_name
    concat_segments(segment_paths, base_path, edit_dir)

    # 3. Subtitles: build if requested, resolve final path
    subs_path: Path | None = None
    if not args.no_subtitles:
        if args.build_subtitles:
            subs_path = edit_dir / "master.srt"
            build_master_srt(edl, edit_dir, subs_path)
        elif edl.get("subtitles"):
            subs_path = resolve_path(edl["subtitles"], edit_dir)
            if not subs_path.exists():
                print(f"warning: subtitles path in EDL does not exist: {subs_path}")
                subs_path = None

    # 4. Composite (overlays + subtitles LAST) → intermediate (pre-loudnorm) path
    overlays = edl.get("overlays") or []
    sub_style = build_sub_style(args.caption_color, args.caption_font)  # CI colour/font -> libass
    # libass resolves fonts by family name through fontconfig. A brand font that is
    # only a file in the brain (not installed system-wide) is found via fontsdir.
    fonts_dir = args.fonts_dir if args.fonts_dir and args.fonts_dir.is_dir() else None
    # Write the final output atomically: build it under .part.mp4, rename last — an
    # interrupted composite/loudnorm never leaves a corrupt {slug}.mp4 behind.
    final_tmp = out_path.with_suffix(".part.mp4")
    if args.no_loudnorm:
        build_final_composite(base_path, overlays, subs_path, final_tmp, edit_dir,
                              force_style=sub_style, fonts_dir=fonts_dir)
    else:
        # Composite to a temp file, then run loudnorm → final (atomic) output
        tmp_composite = out_path.with_suffix(".prenorm.mp4")
        build_final_composite(base_path, overlays, subs_path, tmp_composite, edit_dir,
                              force_style=sub_style, fonts_dir=fonts_dir)
        print("loudness normalization → social-ready (-14 LUFS / -1 dBTP / LRA 11)")
        apply_loudnorm_two_pass(tmp_composite, final_tmp, preview=args.draft)
        try:
            tmp_composite.unlink(missing_ok=True)
        except OSError:
            pass  # Cowork mount may forbid unlink (EPERM); leftover is gitignored cache, harmless
    final_tmp.replace(out_path)
    print(f"done → {out_path.name}")

    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"\ndone: {out_path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
