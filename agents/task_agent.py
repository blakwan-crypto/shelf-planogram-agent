"""Stage 5 — TaskAgent (Action).

Analogy: the supervisor who turns the manager's report into a work
order for the restocking crew: a to-do list, an annotated photo, and
saved files — never just console prints.
"""

from __future__ import annotations

import json
from pathlib import Path

import cv2

from agents.contracts import ComplianceReport, ShelfScan, WorkOrder

# Colors (BGR) per slot status for the annotated image.
STATUS_COLORS = {
    "correct": (46, 160, 67),        # green
    "low_facing": (0, 165, 255),     # orange
    "out_of_stock": (60, 60, 220),   # red
}


class TaskAgent:
    name = "TaskAgent"

    def __init__(self, out_dir: str = "results"):
        self.out_dir = Path(out_dir)
        # Create output folders up front so a fresh --out directory works.
        (self.out_dir / "images").mkdir(parents=True, exist_ok=True)
        (self.out_dir / "tasks").mkdir(parents=True, exist_ok=True)

    def act(self, scan: ShelfScan, report: ComplianceReport,
            planogram_path: str = "data/planogram.json") -> WorkOrder:
        stem = Path(scan.image_path).stem

        # 1. Build the task list from anything that isn't "correct".
        tasks = []
        for slot in report.slots:
            if slot.status == "out_of_stock":
                tasks.append({
                    "slot_id": slot.slot_id, "action": "restock",
                    "detail": f"slot empty — expected {slot.expected_facings} facings",
                })
            elif slot.status == "low_facing":
                tasks.append({
                    "slot_id": slot.slot_id, "action": "fill",
                    "detail": f"{slot.actual_facings}/{slot.expected_facings} facings present",
                })
        if report.misplaced_count:
            tasks.append({
                "slot_id": "(none)", "action": "investigate",
                "detail": f"{report.misplaced_count} product(s) found outside any planogram slot",
            })

        # 2. Draw the annotated image: gray boxes = detections,
        #    colored boxes = slot verdicts.
        annotated_path = self.out_dir / "images" / f"{stem}_annotated.jpg"
        self._draw(scan, report, planogram_path, annotated_path)

        # 3. Save the machine-readable report + work order.
        report_path = self.out_dir / "tasks" / f"{stem}_report.json"
        report_path.write_text(json.dumps(report.to_dict(), indent=2))

        order = WorkOrder(
            image_path=scan.image_path,
            tasks=tasks,
            annotated_image=str(annotated_path),
            report_json=str(report_path),
        )
        order_path = self.out_dir / "tasks" / f"{stem}_workorder.json"
        order_path.write_text(json.dumps(order.to_dict(), indent=2))

        return order

    def _draw(self, scan: ShelfScan, report: ComplianceReport,
              planogram_path: str, out_path: Path) -> None:
        img = cv2.imread(scan.image_path)
        if img is None:                      # should never happen post-preprocess
            return
        h, w = img.shape[:2]

        for det in scan.detections:
            cv2.rectangle(img, (int(det.x1), int(det.y1)),
                          (int(det.x2), int(det.y2)), (160, 160, 160), 1)

        with open(planogram_path) as f:
            planogram = json.load(f)
        status_by_slot = {s.slot_id: s for s in report.slots}

        for row in planogram["rows"]:
            y_min = int(row["y_min"] * h)
            y_max = int(row["y_max"] * h)
            n_slots = len(row["slots"])
            slot_w = w / n_slots
            for i, slot in enumerate(row["slots"]):
                verdict = status_by_slot[slot["slot_id"]].status
                color = STATUS_COLORS[verdict]
                x_min = int(i * slot_w)
                x_max = int((i + 1) * slot_w)
                cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color, 2)
                cv2.putText(img, f"{slot['slot_id']}: {verdict}",
                            (x_min + 4, y_min + 18),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(out_path), img)
