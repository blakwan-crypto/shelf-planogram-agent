"""Stage 3 — ScannerAgent (Perception).

Analogy: the employee who walks the aisle with a clipboard and writes
down every product they see. They don't judge anything — they just
report what's there, as a structured ShelfScan.
"""

from __future__ import annotations

from agents.contracts import PreprocessResult, ShelfScan
from tools.detector import ProductDetector


class ScannerAgent:
    name = "ScannerAgent"

    def __init__(self, detector: ProductDetector | None = None):
        self.detector = detector or ProductDetector()

    def scan(self, prepped: PreprocessResult) -> ShelfScan:
        """Detect all products in a preprocessed image."""
        detections = self.detector.detect(prepped.image_path)
        mean_conf = (
            sum(d.confidence for d in detections) / len(detections)
            if detections else 0.0
        )
        return ShelfScan(
            image_path=prepped.image_path,
            image_width=prepped.width,
            image_height=prepped.height,
            detections=detections,
            mean_confidence=round(mean_conf, 4),
        )
