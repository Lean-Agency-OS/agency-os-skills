#!/usr/bin/env python3
"""Build styled ASS captions from a word-level transcript.

Companion to make_srt.py: where the SRT path hands a flat cue list to libass and
styles it with one global force_style, this builds the ASS itself. That buys a
real drop shadow (second dialogue layer, blurred), an exact baseline anchor and
cost-based chunking, none of which force_style can express.

Style values are brand data, not code: they come from the brand CI (ci.md, key
`captions:`) and fall back to the reference values below, which were measured on
a 1080x1920 frame. Every length is a reference pixel at REF_W and is scaled to
the target resolution, so the same CI works for any output size.

Chunking: at most MAX_WORDS words and MAX_DUR seconds per cue, never a single
word when it can be avoided, hard break at sentence ends, cues that would end on
a filler word are penalized.

Timing: by default every cue starts at its first word's transcript timestamp.
With --audio the start is pulled to the audible onset of that word instead,
measured on the level envelope of the given media file, plus SWITCH_DELAY. The
previous cue ends exactly where the next one starts, so there is no gap and no
minimum hold time. Measured values (tested on a real reel, do not change
casually): SWITCH_DELAY 50 ms, ONSET_DB 10 dB, HOLD_GAP 0.7 s, and a 80 ms
median lead that compensates transcript stamps landing late.

Usage:
    python helpers/make_ass.py <transcript.json> <out.ass> --width 1080 --height 1920 \\
        --font-path <font.ttf> --font-name <FamilyName> [--ci <ci.md>] [--audio <media>]

Burn in with ffmpeg, without force_style (the file carries its own styles):
    ffmpeg -i in.mp4 -vf "subtitles=out.ass:fontsdir=<dir with the ttf>" out.mp4
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from PIL import ImageFont
except ImportError:
    sys.exit("Pillow is not installed. Install the engine deps: pip install pillow")

try:
    from ci_read import resolve as ci_resolve  # same directory
except Exception:  # pragma: no cover - ci_read is optional for a bare run
    ci_resolve = None

# -------- Reference style (1080 wide); every value can be overridden by the CI --
REF_W = 1080.0
DEFAULT_STYLE = {
    "size": 105,
    "outline": 1,
    "max_width": 1080 - 2 * 70,  # safe zone, tighter than the raw frame width
    "baseline": 1093,            # bottom edge anchor of the text line
    "shadow_dy": 7,
    "shadow_blur": 15,
    "shadow_alpha": 200,         # 0..255 opacity, ASS wants 255 - value
    "shadow_border": 2,          # extra border on the shadow layer
}

# -------- Chunking ------------------------------------------------------------
DEFAULT_MAX_WORDS = 3
DEFAULT_MAX_DUR = 1.0            # seconds per cue, 0 disables the duration split
HOLD_GAP = 0.7                   # a cue holds until the next one if the gap is smaller
TAIL = 0.12                      # otherwise it ends this long after its last word
LAST_TAIL = 0.30                 # tail of the final cue
COST_SINGLE_WORD = 12.0
COST_FILLER_END = 3.0
BONUS_SENTENCE_END = 2.0

# German stop words: cues should not end on them. Override via CI `captions.filler`.
DEFAULT_FILLER = {
    "der", "die", "das", "und", "im", "in", "mit", "ist", "hat", "ein", "eine",
    "einen", "einem", "einer", "den", "dem", "des", "zu", "zur", "zum", "von",
    "vom", "auf", "an", "am", "als", "wie", "so", "auch", "noch", "nur", "aber",
    "oder", "dass", "wenn", "weil", "du", "dir", "dich", "ich", "es", "sie",
    "wir", "man", "sich", "mal", "ja", "schon", "dann", "da", "was", "bei",
}
SENT_END = re.compile(r"[.!?]+[\"')\]]*$")

# -------- Audible onset (only used with --audio) ------------------------------
ONSET_BACK = 0.30                # how far ahead of the transcript stamp we may look
ONSET_DB = 10.0                  # rise over the local minimum that counts as speech
DEFAULT_LEAD = 0.08              # no clear onset (continuous speech): pull back by the median
DEFAULT_SWITCH_DELAY = 0.05      # switch slightly after the audible word start


def norm(word: str) -> str:
    """Lowercase, strip everything that is not a letter or digit."""
    return re.sub(r"[^\w]", "", word.lower(), flags=re.UNICODE)


# -------- Brand spellings -----------------------------------------------------


def parse_replacements(spec: str | None) -> list[dict]:
    """Parse the CI string into replacement rules.

    Format:  <source> => <cue> | <cue> ;  <source> => <cue>
    The source is matched against consecutive words with punctuation removed, so
    it matches whether the transcript delivers one token or several. A target of
    several cues splits the matched time span evenly, which keeps a long brand
    term on two readable lines instead of one overlong one.
    """
    rules: list[dict] = []
    for raw in (spec or "").split(";"):
        if "=>" not in raw:
            continue
        src, dst = raw.split("=>", 1)
        parts = [p.strip() for p in dst.split("|") if p.strip()]
        if norm(src) and parts:
            rules.append({"key": norm(src), "parts": parts})
    return rules


def apply_replacements(words: list[dict], rules: list[dict], max_span: int = 6) -> list[dict]:
    """Replace brand terms, keeping the timing of the words they replace."""
    if not rules:
        return words
    out: list[dict] = []
    i = 0
    while i < len(words):
        hit = None
        for span in range(1, min(max_span, len(words) - i) + 1):
            joined = "".join(norm(w["text"]) for w in words[i:i + span])
            for rule in rules:
                if joined == rule["key"]:
                    hit = (span, rule)
                    break
            if hit:
                break
        if not hit:
            out.append(words[i])
            i += 1
            continue
        span, rule = hit
        first, last = words[i], words[i + span - 1]
        start, end = float(first["start"]), float(last["end"])
        # keep trailing punctuation of the original (", " or "." after the term)
        trailing = re.sub(r"^.*?(\W*)$", r"\1", last["text"].strip())
        parts = list(rule["parts"])
        step = (end - start) / len(parts)
        for k, text in enumerate(parts):
            if k == len(parts) - 1:
                text += trailing
            out.append(dict(first, text=text,
                            start=start + k * step, end=start + (k + 1) * step))
        i += span
    return out


# -------- Chunking ------------------------------------------------------------


def chunk_sentence(words: list[dict], font, maxw: float, max_words: int,
                   max_dur: float, filler: set[str]) -> list[list[dict]]:
    """Split one sentence into cues with a minimal-cost dynamic program."""
    n = len(words)
    INF = float("inf")
    best = [INF] * (n + 1)
    back = [0] * (n + 1)
    best[0] = 0.0
    for i in range(1, n + 1):
        for ln in range(1, max_words + 1):
            j = i - ln
            if j < 0 or best[j] == INF:
                continue
            piece = words[j:i]
            text = " ".join(w["text"].strip() for w in piece)
            bb = font.getbbox(text)
            if bb[2] - bb[0] > maxw and ln > 1:
                continue  # a single word is always allowed, else the sentence collapses into one line
            if max_dur and ln > 1 and float(piece[-1]["end"]) - float(piece[0]["start"]) > max_dur:
                continue  # standing too long: split
            cost = (max_words - ln) ** 2 * 1.0  # prefer full cues
            if ln == 1:
                cost += COST_SINGLE_WORD
            if i < n and norm(piece[-1]["text"]) in filler:
                cost += COST_FILLER_END
            if i == n:
                cost -= BONUS_SENTENCE_END
            if best[j] + cost < best[i]:
                best[i] = best[j] + cost
                back[i] = j
    out, i = [], n
    while i > 0:
        j = back[i]
        out.append(words[j:i])
        i = j
    return out[::-1]


# -------- Audible onset -------------------------------------------------------


def load_envelope(media: Path):
    """Level curve in dB on a 10 ms grid, taken from the media file's audio."""
    import subprocess
    try:
        import numpy as np
    except ImportError:
        sys.exit("numpy is not installed but --audio needs it. Install the engine deps.")
    try:
        raw = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(media), "-vn", "-ac", "1", "-ar", "16000",
             "-f", "s16le", "-"],
            capture_output=True, check=True).stdout
    except FileNotFoundError:
        sys.exit("ffmpeg not found but --audio needs it.")
    except subprocess.CalledProcessError as exc:
        sys.exit(f"ffmpeg could not read the audio of {media}: {exc.stderr.decode()[:200]}")
    samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    hop, win = 160, 320
    n = max(0, (len(samples) - win) // hop)
    if n < 3:
        sys.exit(f"audio track of {media} is too short to measure")
    frames = np.lib.stride_tricks.sliding_window_view(samples, win)[::hop][:n]
    return 20 * np.log10(np.sqrt((frames ** 2).mean(axis=1)) + 1e-9)


def acoustic_onset(db, stamp: float, lower: float) -> float:
    """First audible sound before the transcript stamp: local minimum, then the
    first frame ONSET_DB above it."""
    lo = int(max(lower, stamp - ONSET_BACK) * 100)
    hi = int(stamp * 100) + 5
    if hi - lo < 3 or hi > len(db):
        return max(lower, stamp - DEFAULT_LEAD)
    seg = db[lo:hi]
    j = int(seg.argmin())
    for k in range(j, len(seg)):
        if seg[k] > seg[j] + ONSET_DB:
            return min(stamp, (lo + k) / 100)
    return max(lower, stamp - DEFAULT_LEAD)


# -------- ASS -----------------------------------------------------------------


def ts(t: float) -> str:
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def ass_escape(text: str) -> str:
    """Neutralize the characters libass reads as markup."""
    return (text.replace("\\", "∖").replace("{", "(").replace("}", ")")
                .replace("\n", " ").replace("\r", " "))


def load_words(transcript: Path) -> list[dict]:
    try:
        data = json.loads(transcript.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"transcript not found: {transcript}")
    except json.JSONDecodeError as exc:
        sys.exit(f"transcript is not valid JSON ({transcript}): {exc}")
    words = [w for w in data.get("words", [])
             if w.get("type") == "word" and str(w.get("text", "")).strip()]
    if not words:
        sys.exit(f"transcript has no word timestamps: {transcript}\n"
                 "Re-transcribe with word timestamps (Scribe, or whisper word mode).")
    missing = [w for w in words if w.get("start") is None or w.get("end") is None]
    if missing:
        sys.exit(f"{len(missing)} words in {transcript} have no start/end time")
    return words


def build(transcript: Path, out_path: Path, vw: int, vh: int, font_name: str,
          font_path: Path, style: dict, max_words: int, max_dur: float,
          filler: set[str], rules: list[dict], audio: Path | None,
          switch_delay: float) -> tuple[int, int, int, int]:
    scale = vw / REF_W
    size = round(style["size"] * scale)
    outline = max(1, round(style["outline"] * scale))
    maxw = style["max_width"] * scale
    sh_dy = style["shadow_dy"] * scale
    sh_blur = style["shadow_blur"] * scale
    sh_border = outline + round(style["shadow_border"] * scale)
    sh_alpha = f"&H{255 - int(style['shadow_alpha']):02X}&"

    try:
        font = ImageFont.truetype(str(font_path), size)
    except OSError:
        sys.exit(f"font file could not be opened: {font_path}\n"
                 "Set fonts.subtitle_path in the brand ci.md to a .ttf/.otf file.")
    _, descent = font.getmetrics()
    # \an2 anchors the bottom edge of the line, so the baseline moves down by the descent
    y_bottom = style.get("baseline_px") or round(style["baseline"] * scale + descent)
    cx = round(vw / 2)

    words = apply_replacements(load_words(transcript), rules)

    sentences, cur = [], []
    for w in words:
        cur.append(w)
        if SENT_END.search(str(w["text"]).strip()):
            sentences.append(cur)
            cur = []
    if cur:
        sentences.append(cur)

    chunks: list[list[dict]] = []
    for sentence in sentences:
        chunks += chunk_sentence(sentence, font, maxw, max_words, max_dur, filler)

    starts = [float(ch[0]["start"]) for ch in chunks]
    if audio:
        db = load_envelope(audio)
        for i in range(len(chunks)):
            lower = starts[i - 1] + 0.01 if i else 0.0  # keep the order, no minimum hold
            starts[i] = max(lower, acoustic_onset(db, starts[i], lower) + switch_delay)

    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {vw}
PlayResY: {vh}
WrapStyle: 2
ScaledBorderAndShadow: no
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Main,{font_name},{size},{style['color_ass']},{style['color_ass']},&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,{outline},0,2,0,0,0,1
Style: Shade,{font_name},{size},&H00000000,&H00000000,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,{sh_border},0,2,0,0,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    lines = []
    for i, ch in enumerate(chunks):
        start = starts[i]
        own_end = float(ch[-1]["end"])
        if i + 1 < len(chunks):
            nxt = starts[i + 1]
            end = nxt if (nxt - own_end) < HOLD_GAP else own_end + TAIL
        else:
            end = own_end + LAST_TAIL
        text = ass_escape(" ".join(str(w["text"]).strip() for w in ch))
        lines.append(f"Dialogue: 0,{ts(start)},{ts(end)},Shade,,0,0,0,,"
                     f"{{\\pos({cx},{y_bottom + round(sh_dy)})\\blur{sh_blur:.1f}\\alpha{sh_alpha}}}{text}")
        lines.append(f"Dialogue: 1,{ts(start)},{ts(end)},Main,,0,0,0,,"
                     f"{{\\pos({cx},{y_bottom})}}{text}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(head + "\n".join(lines) + "\n", encoding="utf-8")
    singles = sum(1 for c in chunks if len(c) == 1)
    return len(chunks), size, y_bottom, singles


def style_from_ci(ci_path: Path | None) -> tuple[dict, str | None, str | None, str | None]:
    """Merge the brand CI over the reference style. Returns style, font name,
    font path and the replacement spec; every piece may be None."""
    style = dict(DEFAULT_STYLE)
    style["color_ass"] = "&H00FFFFFF"
    if not ci_path:
        return style, None, None, None
    if not ci_path.exists():
        sys.exit(f"ci not found: {ci_path}")
    if ci_resolve is None:
        sys.exit("ci_read.py is missing next to make_ass.py, cannot read the CI")
    values = ci_resolve(ci_path.read_text(encoding="utf-8"))
    style["color_ass"] = values.get("caption_color_ass") or style["color_ass"]
    captions = values.get("captions") or {}
    for key in ("size", "outline", "max_width", "baseline", "shadow_dy",
                "shadow_blur", "shadow_alpha", "shadow_border"):
        if captions.get(key) not in (None, ""):
            style[key] = float(captions[key])
    if captions.get("baseline_px"):
        style["baseline_px"] = int(float(captions["baseline_px"]))
    filler = captions.get("filler")
    if filler:
        style["filler"] = {norm(w) for w in re.split(r"[,\s]+", filler) if w.strip()}
    return style, values.get("caption_font"), values.get("caption_font_path"), captions.get("replacements")


def main() -> None:
    ap = argparse.ArgumentParser(description="Build styled ASS captions from a word-level transcript")
    ap.add_argument("transcript", type=Path, help="Scribe/whisper JSON with word timestamps")
    ap.add_argument("out", type=Path, help="Output .ass path")
    ap.add_argument("--width", type=int, required=True, help="Target video width in px")
    ap.add_argument("--height", type=int, required=True, help="Target video height in px")
    ap.add_argument("--ci", type=Path, help="Brand ci.md: caption colour, font, style, spellings")
    ap.add_argument("--font-path", type=Path, help="TTF/OTF file (overrides fonts.subtitle_path)")
    ap.add_argument("--font-name", help="Family name as libass resolves it (overrides fonts.subtitle)")
    ap.add_argument("--baseline", type=int, help="Bottom edge of the text in TARGET px (overrides the CI)")
    ap.add_argument("--audio", type=Path, help="Measure cue starts on this media file's audio instead of the transcript stamps")
    ap.add_argument("--switch-delay", type=float, default=DEFAULT_SWITCH_DELAY, help="Delay after the audible onset (only with --audio)")
    ap.add_argument("--max-words", type=int, default=DEFAULT_MAX_WORDS, help="Words per cue")
    ap.add_argument("--max-dur", type=float, default=DEFAULT_MAX_DUR, help="Seconds per cue, 0 disables")
    args = ap.parse_args()

    style, ci_font, ci_font_path, replacements = style_from_ci(args.ci)
    font_name = args.font_name or ci_font
    font_path = args.font_path or (Path(ci_font_path) if ci_font_path else None)
    if not font_path:
        sys.exit("no font file: pass --font-path or set fonts.subtitle_path in the brand ci.md")
    if not font_name:
        font_name = Path(font_path).stem
    if args.baseline:
        style["baseline_px"] = args.baseline

    filler = style.pop("filler", DEFAULT_FILLER)
    count, size, y_bottom, singles = build(
        args.transcript, args.out, args.width, args.height, font_name, font_path,
        style, args.max_words, args.max_dur, filler, parse_replacements(replacements),
        args.audio, args.switch_delay,
    )
    timing = "audio onset" if args.audio else "transcript stamps"
    print(f"{count} cues, font {size}px, bottom edge y={y_bottom}, "
          f"single-word cues: {singles}, timing: {timing}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
