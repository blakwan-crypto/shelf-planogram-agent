"""Message contracts — the shared language every agent speaks.

Think of these as the standardized forms in a company: nobody hands
a coworker a sticky note, they fill in the official form so the next
person (and the trace logger) always knows what they're looking at.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any


def new_run_id() -> str:
    """Unique ID for one batch run, e.g. 'run_20260802-081530-a1b2'."""
    stamp = time.strftime("%Y%m%d-%H%M%S")
    return f"run_{stamp}-{uuid.uuid4().hex[:4]}"


@dataclass
class Envelope:
    """The wrapper around EVERY message passed between agents.

    The orchestrator logs one of these per hand-off, which is what the
    assignment's Stage 6 (Logging / Traceability) requires.
    """
    sender: str
    recipient: str
    message_type: str          # e.g. "ShelfScan", "ComplianceReport"
    payload: dict[str, Any]    # the actual content (one of the types below)
    confidence: float = 1.0
    run_id: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PreprocessResult:
    """Stage 2 output: an image that is safe for the detector to read."""
    image_path: str
    width: int
    height: int
    ok: bool = True

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RejectedInput:
    """Stage 2 output when an image is corrupt/unreadable.

    We record WHY and keep going — the batch must never crash.
    """
    image_path: str
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Detection:
    """One product found on the shelf (a bounding box + confidence)."""
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float
    label: str = "object"   # the SKU-110K model only knows generic "object"

    @property
    def center_x(self) -> float:
        return (self.x1 + self.x2) / 2

    @property
    def center_y(self) -> float:
        return (self.y1 + self.y2) / 2

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ShelfScan:
    """Stage 3 output: everything the ScannerAgent saw in one image."""
    image_path: str
    image_width: int
    image_height: int
    detections: list[Detection]
    mean_confidence: float

    def to_dict(self) -> dict:
        d = asdict(self)
        return d


@dataclass
class SlotStatus:
    """How one planogram slot compares to reality."""
    slot_id: str
    row_id: str
    expected_facings: int
    actual_facings: int
    # one of: correct | low_facing | out_of_stock | misplaced
    status: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ComplianceReport:
    """Stage 4 output: the AnalystAgent's verdict for one image."""
    image_path: str
    slots: list[SlotStatus]
    misplaced_count: int
    summary: dict[str, int]   # {"correct": n, "low_facing": n, ...}

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class WorkOrder:
    """Stage 5 output: the human-actionable restocking task list."""
    image_path: str
    tasks: list[dict]         # [{"slot_id", "action", "detail"}, ...]
    annotated_image: str      # path to the saved annotated image
    report_json: str          # path to the saved compliance report

    def to_dict(self) -> dict:
        return asdict(self)
