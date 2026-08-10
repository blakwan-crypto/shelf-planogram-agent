# Model Weights

Weights are **not** committed to this repo (assignment rule: no large binary files in git).

## Required: SKU-110K product detector (YOLO11n)

Download `sku110k-yolo11-n640.pt` (~16 MB) from Hugging Face:

```
https://huggingface.co/chistopat/sku110k-yolo11-object-detector/resolve/main/weights/sku110k-yolo11-n640.pt
```

Place it at `models/sku110k-yolo11-n640.pt` (the default path used by `tools/detector.py`).

**What it does:** finds *where* products are on a shelf (bounding boxes), labeled generically as `object`. It does **not** identify brands — brand identity is an optional stretch goal.

**Published test metrics (SKU-110K test set, 2,935 images):** precision 0.896 · recall 0.838 · mAP@0.5 0.906 · mAP@0.5:0.95 0.550.

A larger, slightly more accurate variant (`sku110k-yolo11-s640.pt`, mAP@0.5 0.927) is available from the same repo if the nano model proves too weak.

License/provenance: see the model card at https://huggingface.co/chistopat/sku110k-yolo11-object-detector — trained on SKU-110K (EG 4000, CVPR 2019).
