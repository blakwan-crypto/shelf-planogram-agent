"""Stage 2 — Preprocessing.

Job: turn "a file on disk" into "an image the detector can safely read",
or reject it with a clear reason. Nothing here should ever crash the
pipeline — bad inputs become RejectedInput messages instead.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, UnidentifiedImageError

from agents.contracts import PreprocessResult, RejectedInput

# Only these extensions are even attempted.
ALLOWED_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# Sanity bounds: tiny images are probably thumbnails/icons, huge ones
# are probably mistakes. Both get rejected with a reason.
MIN_SIDE = 64
MAX_SIDE = 8000


def preprocess(image_path: str | Path) -> PreprocessResult | RejectedInput:
    """Validate one image file.

    Returns PreprocessResult if usable, RejectedInput (with reason) if not.
    Never raises — the whole point is graceful failure.
    """
    path = Path(image_path)

    if not path.exists():
        return RejectedInput(str(path), "file does not exist")

    if path.suffix.lower() not in ALLOWED_SUFFIXES:
        return RejectedInput(str(path), f"unsupported file type '{path.suffix}'")

    try:
        # Image.open + verify() catches truncated/corrupt files.
        with Image.open(path) as img:
            img.verify()
        # verify() leaves the file unusable, so reopen to read size.
        with Image.open(path) as img:
            width, height = img.size
    except (UnidentifiedImageError, OSError) as exc:
        return RejectedInput(str(path), f"corrupt or unreadable image ({exc})")

    if width < MIN_SIDE or height < MIN_SIDE:
        return RejectedInput(str(path), f"too small ({width}x{height})")
    if width > MAX_SIDE or height > MAX_SIDE:
        return RejectedInput(str(path), f"too large ({width}x{height})")

    return PreprocessResult(str(path), width, height)
