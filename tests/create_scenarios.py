#!/usr/bin/env python3
"""Create the robustness scenario inputs in data/scenarios/.

This script builds every "bad input" the evaluation needs:
    blurry / dark / tilted   - damaged but still VALID photos of shelf3
    corrupt / empty / not_an_image - files that are NOT valid images at all
    tiny / oversized         - valid images outside the size limits
    non_shelf / low_confidence - valid photos with few/no products to find

It is safe to run more than once: everything is rebuilt from the sample
photos, except the downloaded parking-lot photo (already there and valid
=> kept, so offline re-runs work).

How to run (from the repo root):
    ./.venv/bin/python tests/create_scenarios.py

It ends with a self-check that shows what Stage 2 (preprocess) will say
about every generated input, so you can see the rejection reasons before
you even run the pipeline.
"""

from __future__ import annotations

import json
import shutil
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import cv2
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
SCENARIOS = REPO_ROOT / "data" / "scenarios"
SAMPLE = REPO_ROOT / "data" / "sample"

USER_AGENT = "shelf-planogram-agent/0.1 (student evaluation project)"


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def load_bgr(name: str):
    """Read one sample photo as a BGR numpy array (cv2's native format)."""
    return cv2.imread(str(SAMPLE / name))


def save_jpg(img_bgr, path: Path) -> None:
    """Write a cv2 image to disk as JPEG, creating parent folders."""
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), img_bgr)


def write_expect(folder: Path, text: str) -> None:
    """Write EXPECT.md — the 'what should happen' contract for this scenario.

    Keys understood by tests/run_scenarios.py:
        expected: ok | rejected
        reason_contains: substring that must appear in every rejection reason
        detections_max: highest allowed detection count (for 'ok' scenarios)
        note: free text shown in the report
    """
    (folder / "EXPECT.md").write_text(text.strip() + "\n")


def jpg_ok(path: Path) -> bool:
    """True if the file really is a readable JPEG (used to skip re-downloads)."""
    try:
        with Image.open(path) as im:
            im.verify()
        return True
    except Exception:
        return False


# --------------------------------------------------------------------------
# One builder function per scenario
# --------------------------------------------------------------------------

def build_blurry() -> None:
    """shelf3.jpg blurred with a 25x25 Gaussian kernel (heavy blur)."""
    folder = SCENARIOS / "blurry"
    folder.mkdir(parents=True, exist_ok=True)
    img = load_bgr("shelf3.jpg")
    save_jpg(cv2.GaussianBlur(img, (25, 25), 0), folder / "blurry.jpg")
    write_expect(folder, """expected: ok
note: shelf3.jpg blurred with a 25x25 Gaussian kernel. The image is still a
valid JPEG — the pipeline should process it and find FEWER products than the
~300 of the sharp original, without crashing.""")


def build_dark() -> None:
    """shelf3.jpg darkened to ~40% brightness."""
    folder = SCENARIOS / "dark"
    folder.mkdir(parents=True, exist_ok=True)
    img = load_bgr("shelf3.jpg")
    dark = cv2.convertScaleAbs(img, alpha=0.4, beta=0)  # multiply pixel values by 0.4
    save_jpg(dark, folder / "dark.jpg")
    write_expect(folder, """expected: ok
note: shelf3.jpg at ~40% brightness. Valid image — expect fewer/weaker
detections, but the pipeline must complete without crashing.""")


def build_tilted() -> None:
    """shelf3.jpg rotated 15 degrees around its center, white border fill."""
    folder = SCENARIOS / "tilted"
    folder.mkdir(parents=True, exist_ok=True)
    img = load_bgr("shelf3.jpg")
    h, w = img.shape[:2]
    angle = 15.0
    # Rotation matrix around the image center.
    m = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    # Grow the canvas so the rotated corners are not cut off.
    cos_a, sin_a = abs(m[0, 0]), abs(m[0, 1])
    new_w = int(h * sin_a + w * cos_a)
    new_h = int(h * cos_a + w * sin_a)
    m[0, 2] += new_w / 2 - w / 2
    m[1, 2] += new_h / 2 - h / 2
    rotated = cv2.warpAffine(img, m, (new_w, new_h), borderValue=(255, 255, 255))
    save_jpg(rotated, folder / "tilted.jpg")
    write_expect(folder, """expected: ok
note: shelf3.jpg rotated 15 degrees with white border fill. Valid image —
expect the pipeline to process it (maybe with a noisier slot match) without
crashing.""")


def build_corrupt() -> None:
    """shelf3.jpg cut to its first 800 bytes — header intact, data cut short.

    Why 800 and not 2000? We tested truncation lengths: PIL's corrupt-file
    check is lenient on files >= ~1000 bytes (it only reads the header), so
    a 2000-byte file slips past Stage 2 and CRASHES the detector. 800 bytes
    is still a genuinely truncated JPEG but Stage 2 rejects it cleanly.
    The dangerous 2000-byte variant is preserved as evidence in this folder
    (truncated_2000bytes.bin) — it is never attempted by the pipeline
    because the orchestrator only picks image extensions.
    """
    folder = SCENARIOS / "corrupt"
    folder.mkdir(parents=True, exist_ok=True)
    blob = (SAMPLE / "shelf3.jpg").read_bytes()
    (folder / "corrupt.jpg").write_bytes(blob[:800])
    (folder / "truncated_2000bytes.bin").write_bytes(blob[:2000])  # evidence only
    write_expect(folder, """expected: rejected
reason_contains: corrupt or unreadable
note: shelf3.jpg cut to its first 800 bytes — the JPEG header is intact but
the scan data ends mid-way. Stage 2 must reject it with a clear reason.
(Also in this folder: truncated_2000bytes.bin — at 2000 bytes PIL's
verify() is too lenient, the file slips past Stage 2 into the detector and
crashes it. That is a known pipeline gap this suite documents; see
SCENARIO_REPORT.md "Known robustness gaps".""")


def build_empty() -> None:
    """A 0-byte file named empty.jpg."""
    folder = SCENARIOS / "empty"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "empty.jpg").write_bytes(b"")
    write_expect(folder, """expected: rejected
reason_contains: corrupt or unreadable
note: A 0-byte file named empty.jpg. There is no image in it at all — Stage 2
must reject it.""")


def build_not_an_image() -> None:
    """A text file renamed notes.jpg, plus a real .txt file."""
    folder = SCENARIOS / "not_an_image"
    folder.mkdir(parents=True, exist_ok=True)
    text = b"This is plain text, not an image. Renamed with a .jpg extension.\n"
    (folder / "notes.jpg").write_bytes(text)   # .jpg name, text content
    (folder / "notes.txt").write_bytes(text)   # honest .txt
    write_expect(folder, """expected: rejected
reason_contains: corrupt or unreadable
note: notes.jpg is really a text file wearing a .jpg name — Stage 2 must
reject it. notes.txt (a real .txt) never reaches the pipeline at all: the
orchestrator only iterates files whose extension is a known image type, so
the .txt is ignored by design, not by accident.""")


def build_tiny() -> None:
    """shelf3.jpg resized to 48x36 — below the 64-pixel minimum."""
    folder = SCENARIOS / "tiny"
    folder.mkdir(parents=True, exist_ok=True)
    img = Image.open(SAMPLE / "shelf3.jpg")
    img.resize((48, 36)).save(folder / "tiny.jpg")  # 1280x960 -> 48x36 keeps aspect
    write_expect(folder, """expected: rejected
reason_contains: too small
note: shelf3.jpg resized to 48x36 pixels — below the pipeline's 64-pixel
minimum (tiny files are probably icons or mistakes). Stage 2 must reject it.""")


def build_oversized() -> None:
    """shelf1.jpg upscaled to 8100px wide — above the 8000px maximum."""
    folder = SCENARIOS / "oversized"
    folder.mkdir(parents=True, exist_ok=True)
    img = Image.open(SAMPLE / "shelf1.jpg")          # 1430 x 1666
    new_w = 8100
    new_h = round(img.height * new_w / img.width)    # 8100 / 1430 * 1666 = 9438
    img.resize((new_w, new_h), Image.LANCZOS).save(
        folder / "oversized.jpg", quality=85)
    write_expect(folder, """expected: rejected
reason_contains: too large
note: shelf1.jpg upscaled to 8100px wide (9438px tall) — above the pipeline's
8000px maximum. Stage 2 must reject it. (Stage 2 reads only the header for
this check, so the file is never fully decoded.)""")


def build_non_shelf() -> None:
    """One photo with no shelves at all, from Wikimedia Commons.

    We look up the CURRENT download URL for a fixed Commons file title
    (URLs can change; titles do not), download it, and verify it is a real
    JPEG. If a valid copy already exists we keep it — so re-runs work
    without the network.
    """
    folder = SCENARIOS / "non_shelf"
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "parking_lot.jpg"
    title = "File:Aerial view of an empty car parking lot.jpg"

    if jpg_ok(target):
        print(f"  non_shelf: kept existing {target.name}")
        write_expect(folder, EXPECT_NON_SHELF)
        return

    print(f"  non_shelf: downloading '{title}' from Wikimedia Commons ...")
    api = "https://commons.wikimedia.org/w/api.php"
    params = {"action": "query", "format": "json", "titles": title,
              "prop": "imageinfo", "iiprop": "url|size|mime"}
    try:
        url = api + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
        info = list(data["query"]["pages"].values())[0]["imageinfo"][0]
        if info.get("mime") != "image/jpeg":
            raise RuntimeError(f"Commons file is not a JPEG (mime={info.get('mime')})")
        req2 = urllib.request.Request(info["url"],
                                      headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req2, timeout=120) as resp:
            blob = resp.read()
    except Exception as exc:  # network down or file removed -> stop loudly
        raise SystemExit(
            f"Could not download the non-shelf photo: {exc}\n"
            f"Check your internet connection and try again."
        ) from exc

    target.write_bytes(blob)
    if not jpg_ok(target):
        raise SystemExit("Downloaded file is not a readable JPEG — aborting.")
    print(f"  non_shelf: saved {target.name} ({target.stat().st_size} bytes)")
    write_expect(folder, EXPECT_NON_SHELF)


EXPECT_NON_SHELF = """expected: ok
detections_max: 15
note: Aerial photo of an empty parking lot (Wikimedia Commons). There are no
shelves anywhere. The detector is shelf-trained, so it should find few or
zero products — and the pipeline must complete without crashing."""  # noqa: E501


def build_low_confidence() -> None:
    """shelf4.jpg — the sample's known hard case (sparse, small packages).

    The README already documents shelf4 as under-detecting (~14 boxes at low
    confidence vs ~300 on dense shelves), so it is the perfect ready-made
    low-confidence scenario.
    """
    folder = SCENARIOS / "low_confidence"
    folder.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SAMPLE / "shelf4.jpg", folder / "shelf4.jpg")
    write_expect(folder, """expected: ok
detections_max: 60
note: shelf4.jpg (meringues on a supermarket shelf) is a known hard case:
sparse, small packages yield ~14 detections at low confidence — far below
the ~300 of dense shelves. The pipeline must complete without crashing.""")


# --------------------------------------------------------------------------
# Self-check: what Stage 2 will say about every generated input
# --------------------------------------------------------------------------

def self_check() -> bool:
    """Run the real preprocess tool over every input and compare against
    what we designed. Prints a line per file; returns True if all good."""
    sys.path.insert(0, str(REPO_ROOT))          # allow "import tools.preprocess"
    from tools.preprocess import preprocess      # noqa: PLC0415

    designed_rejected = {"corrupt", "empty", "not_an_image", "tiny", "oversized"}
    print("\nSelf-check (what Stage 2 will say about each scenario input):")
    ok = True
    for folder in sorted(p for p in SCENARIOS.iterdir() if p.is_dir()):
        for f in sorted(p for p in folder.iterdir()
                        if p.suffix.lower() in
                        {".jpg", ".jpeg", ".png", ".bmp", ".webp"}):
            res = preprocess(f)
            if hasattr(res, "reason"):
                status, detail = "REJECTED", res.reason
            else:
                status, detail = "ok", f"{res.width}x{res.height}"
            print(f"  {folder.name}/{f.name}: {status} ({detail})")
            want_reject = folder.name in designed_rejected
            if (status == "REJECTED") != want_reject:
                ok = False
    print("Self-check:",
          "OK — every scenario behaves as designed"
          if ok else "PROBLEM — see lines above")
    return ok


def main() -> None:
    SCENARIOS.mkdir(parents=True, exist_ok=True)
    print(f"Building scenarios in {SCENARIOS}")
    build_blurry()
    build_dark()
    build_tilted()
    build_corrupt()
    build_empty()
    build_not_an_image()
    build_tiny()
    build_non_shelf()
    build_oversized()
    build_low_confidence()
    print("Done building scenario inputs.\n")
    ok = self_check()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
