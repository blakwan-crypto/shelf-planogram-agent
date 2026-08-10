"""Stage 4 — AnalystAgent (Reasoning).

Analogy: the manager who compares the clipboard list against the
planogram (the map of what SHOULD be on each shelf) and marks each
slot: correct / low_facing / out_of_stock / misplaced.

The rules are deliberately simple and inspectable — you can point at
any verdict and say exactly why it was made.
"""

from __future__ import annotations

import json
from pathlib import Path

from agents.contracts import ComplianceReport, ShelfScan, SlotStatus


class AnalystAgent:
    name = "AnalystAgent"

    def __init__(self, planogram_path: str = "data/planogram.json"):
        with open(planogram_path) as f:
            self.planogram = json.load(f)

    def analyze(self, scan: ShelfScan) -> ComplianceReport:
        """Compare one ShelfScan against the planogram."""
        slots: list[SlotStatus] = []
        assigned: set[int] = set()   # detection indexes placed in a slot

        for row in self.planogram["rows"]:
            # Row band as a vertical fraction of the image (0.0–1.0),
            # so the same planogram works on any photo size.
            y_min = row["y_min"] * scan.image_height
            y_max = row["y_max"] * scan.image_height
            n_slots = len(row["slots"])
            slot_width = scan.image_width / n_slots

            for slot_index, slot in enumerate(row["slots"]):
                x_min = slot_index * slot_width
                x_max = x_min + slot_width

                # Count detections whose center falls inside this slot.
                actual = 0
                for i, det in enumerate(scan.detections):
                    if (x_min <= det.center_x < x_max
                            and y_min <= det.center_y < y_max):
                        actual += 1
                        assigned.add(i)

                expected = slot["expected_facings"]
                if actual == 0:
                    status = "out_of_stock"
                elif actual < expected:
                    status = "low_facing"
                else:
                    status = "correct"

                slots.append(SlotStatus(
                    slot_id=slot["slot_id"],
                    row_id=row["row_id"],
                    expected_facings=expected,
                    actual_facings=actual,
                    status=status,
                ))

        # A product sitting where NO slot is defined = misplaced.
        misplaced = len(scan.detections) - len(assigned)

        summary: dict[str, int] = {
            "correct": 0, "low_facing": 0, "out_of_stock": 0,
        }
        for s in slots:
            summary[s.status] = summary.get(s.status, 0) + 1
        summary["misplaced"] = misplaced

        return ComplianceReport(
            image_path=scan.image_path,
            slots=slots,
            misplaced_count=misplaced,
            summary=summary,
        )
