"""Stage 6 — Orchestrator + trace logger.

The conductor of the orchestra: it owns the run_id, hands each message
from one agent to the next using the Envelope contract, and logs every
single hand-off to results/traces/<run_id>.jsonl.

Run it:
    python -m agents.orchestrator --images data/sample
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from agents.analyst_agent import AnalystAgent
from agents.contracts import Envelope, PreprocessResult, RejectedInput, new_run_id
from agents.scanner_agent import ScannerAgent
from agents.task_agent import TaskAgent
from tools.preprocess import preprocess


class Orchestrator:
    name = "Orchestrator"

    def __init__(self, out_dir: str = "results",
                 planogram_path: str = "data/planogram.json"):
        self.run_id = new_run_id()
        self.out_dir = Path(out_dir)
        self.planogram_path = planogram_path
        self.trace_path = self.out_dir / "traces" / f"{self.run_id}.jsonl"
        self.trace_path.parent.mkdir(parents=True, exist_ok=True)

        self.scanner = ScannerAgent()
        self.analyst = AnalystAgent(planogram_path)
        self.task_agent = TaskAgent(out_dir)

    # ---- Stage 6 core: every message between agents goes through here ----
    def route(self, sender: str, recipient: str, message) -> None:
        """Log one agent-to-agent hand-off as an Envelope (JSONL trace)."""
        envelope = Envelope(
            sender=sender,
            recipient=recipient,
            message_type=type(message).__name__,
            payload=message.to_dict(),
            confidence=getattr(message, "mean_confidence", 1.0),
            run_id=self.run_id,
        )
        with open(self.trace_path, "a") as f:
            f.write(json.dumps(envelope.to_dict()) + "\n")

    # ---- The full pipeline for ONE image ----
    def process_image(self, image_path: Path) -> dict:
        started = time.time()

        # Stage 1+2: ingestion & preprocessing (or graceful rejection)
        prepped = preprocess(image_path)
        self.route(self.name, "ScannerAgent", prepped)
        if isinstance(prepped, RejectedInput):
            print(f"  ✗ {image_path.name}: rejected ({prepped.reason})")
            return {"image": image_path.name, "status": "rejected",
                    "reason": prepped.reason}
        assert isinstance(prepped, PreprocessResult)

        # Stage 3: perception
        scan = self.scanner.scan(prepped)
        self.route("ScannerAgent", "AnalystAgent", scan)

        # Stage 4: reasoning
        report = self.analyst.analyze(scan)
        self.route("AnalystAgent", "TaskAgent", report)

        # Stage 5: action
        order = self.task_agent.act(scan, report, self.planogram_path)
        self.route("TaskAgent", self.name, order)

        elapsed = time.time() - started
        print(f"  ✓ {image_path.name}: {len(scan.detections)} products, "
              f"{len(order.tasks)} task(s), {elapsed:.1f}s")
        return {"image": image_path.name,
                "status": "ok",
                "detections": len(scan.detections),
                "mean_confidence": scan.mean_confidence,
                "summary": report.summary,
                "tasks": len(order.tasks),
                "seconds": round(elapsed, 2)}

    # ---- A whole batch ----
    def run(self, images_dir: str) -> dict:
        images = sorted(
            p for p in Path(images_dir).iterdir()
            if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
        )
        print(f"Run {self.run_id}: {len(images)} image(s) in {images_dir}")

        results = [self.process_image(p) for p in images]

        ok = [r for r in results if r["status"] == "ok"]
        metrics = {
            "run_id": self.run_id,
            "images_total": len(results),
            "images_ok": len(ok),
            "images_rejected": len(results) - len(ok),
            "task_success_rate": round(len(ok) / len(results), 3) if results else 0,
            "avg_seconds_per_image": (
                round(sum(r["seconds"] for r in ok) / len(ok), 2) if ok else 0
            ),
            "per_image": results,
        }
        metrics_path = self.out_dir / "metrics.json"
        metrics_path.write_text(json.dumps(metrics, indent=2))
        print(f"Trace:   {self.trace_path}")
        print(f"Metrics: {metrics_path}")
        return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Shelf planogram compliance agent")
    parser.add_argument("--images", default="data/sample",
                        help="folder of shelf images to inspect")
    parser.add_argument("--planogram", default="data/planogram.json",
                        help="planogram definition file")
    parser.add_argument("--out", default="results",
                        help="where to write results/")
    args = parser.parse_args()

    orch = Orchestrator(out_dir=args.out, planogram_path=args.planogram)
    orch.run(args.images)


if __name__ == "__main__":
    main()
