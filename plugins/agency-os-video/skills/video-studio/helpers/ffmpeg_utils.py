"""Shared subprocess wrapper that surfaces stderr instead of swallowing it.

Every helper shells out to ffmpeg/ffprobe constantly. The old pattern
(`subprocess.run(cmd, check=True, stderr=DEVNULL/PIPE)` with no handling)
hid ffmpeg's actual error behind a bare Python traceback, which makes
failures opaque for an operator or an LLM driving this skill.

`run()` always captures stdout+stderr as text. On a non-zero exit it raises
RuntimeError containing the command and the tail of stderr, so the real
ffmpeg error is visible. Pass `check=False` when a non-zero exit is an
expected, recoverable outcome (e.g. probing optional audio).
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def run(
    cmd: list,
    *,
    check: bool = True,
    tail: int = 30,
) -> subprocess.CompletedProcess:
    """Run a command, capturing stdout/stderr as text.

    Raises RuntimeError with the stderr tail on failure (unless check=False).
    Returns the CompletedProcess so callers can read .stdout / .stderr.
    """
    cmd = [str(c) for c in cmd]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if check and proc.returncode != 0:
        err = (proc.stderr or "").strip().splitlines()
        tail_txt = "\n".join(err[-tail:]) if err else "(no stderr)"
        head = " ".join(cmd[:8]) + (" …" if len(cmd) > 8 else "")
        raise RuntimeError(f"command failed (exit {proc.returncode}): {head}\n{tail_txt}")
    return proc


def probe(cmd: list) -> str:
    """Run an ffprobe-style command and return stdout (stripped). Raises on failure."""
    return run(cmd).stdout.strip()
