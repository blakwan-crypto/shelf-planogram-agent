"""Stage 3 tool — the product detector.

Wraps a YOLO11 model trained on SKU-110K (a dataset of dense retail
shelf photos). It finds WHERE products are (bounding boxes), not WHAT
brand they are — every box comes back labeled "object".

Weights are NOT committed to git (see models/README.md); download from:
https://huggingface.co/chistopat/sku110k-yolo11-object-detector
"""

from __future__ import annotations

from pathlib import Path

from agents.contracts import Detection

DEFAULT_WEIGHTS = "models/sku110k-yolo11-n640.pt"


class ProductDetector:
    """Load once, then call .detect(path) for each image."""

    def __init__(self, weights: str = DEFAULT_WEIGHTS,
                 confidence: float = 0.25, device: str | None = None):
        if not Path(weights).exists():
            raise FileNotFoundError(
                f"Model weights not found at {weights}.\n"
                "Download them first — see models/README.md for the link."
            )
        # Imported here so the import cost only hits when we actually detect.
        from ultralytics import YOLO

        self.model = YOLO(weights)
        self.confidence = confidence
        # "mps" = Apple Silicon GPU. Falls back to CPU automatically.
        self.device = device or "mps"

    def detect(self, image_path: str) -> list[Detection]:
        """Run the model on one image, return plain Detection objects."""
        results = self.model.predict(
            image_path, conf=self.confidence, device=self.device,
            max_det=1000,  # default 300 truncates dense shelves (>300 products)
            verbose=False,
        )
        # Ultralytics returns an empty list when the image can't be decoded
        # (e.g. a truncated JPEG that slipped past Stage 2). Treat it as
        # "nothing detected" instead of crashing with IndexError.
        if not results:
            return []
        result = results[0]

        detections = []
        for box in result.boxes:
            x1, y1, x2, y2 = (float(v) for v in box.xyxy[0])
            detections.append(Detection(
                x1=x1, y1=y1, x2=x2, y2=y2,
                confidence=float(box.conf),
                label=result.names[int(box.cls)],
            ))
        return detections
