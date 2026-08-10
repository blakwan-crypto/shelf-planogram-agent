# Sample Data

## Contents

| File | Source | Notes |
|---|---|---|
| shelf1.jpg | SKU-110K repo teaser figure (github.com/eg4000/SKU110K_CVPR19) | Dense shelf, ~300 products |
| shelf2.jpg | SKU-110K repo qualitative figure | Dense shelf |
| shelf3.jpg | Wikimedia Commons — "Faced products on a supermarket shelf" | Real-world photo, angled perspective |
| shelf4.jpg | Wikimedia Commons — "Meringues on a supermarket shelf" | Sparse / small packages — known hard case |
| shelf5.jpg | Wikimedia Commons — "Veganz Berlin vegan products shelf" | Medium density |
| shelf6.jpg | Wikimedia Commons — "Private label products in Swedish Hemköp store" | Wide shot, low detection count — known hard case |

Wikimedia images are used under their respective Commons licenses (see each file's
description page on commons.wikimedia.org). SKU-110K figures are from the public
dataset repository (CVPR 2019, EG 4000).

## Test manifest

The full 20-scenario evaluation manifest lives in `notebooks/02_evaluation.ipynb`.
These 6 images seed the sample set so the pipeline runs out of the box.

## planogram.json

Default generic planogram: 4 rows × 8 slots, row bands as fractions of image
height, `expected_facings` per slot. Tune bands/facings per real shelf layout —
see `docs/architecture.md` for how the AnalystAgent consumes it.
