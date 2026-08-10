# Evaluation Report — Component & System Level

Date: 2026-08-02 · Run after planogram tuning + `max_det` fix.
Method: every agent flag was verified by a human (with AI assistance) against the annotated photos — see `results/eval*/images/`.

## 1. Component level — detection

| Image | Detections (before fix) | Detections (after `max_det=1000`) | Note |
|---|---|---|---|
| shelf1 | 300 (capped) | **342** | was being truncated |
| shelf2 | 300 (capped) | **909** (!) | severe truncation — composite figure with 6 dense panels |
| shelf3 | 298 | 298 | never capped; dense real photo |
| shelf4 | 14 | 14 | under-detection: huge transparent bags |
| shelf5 | 60 | 60 | angled photo, foreshortened right side |
| shelf6 | 7 | 7 | under-detection: yellow color cast + photo-print boxes |

**Finding F1 (fixed):** ultralytics defaults to `max_det=300` — dense shelves were silently truncated, which produced false `low_facing` flags. Fixed in `tools/detector.py`; shelf2 tripled its detections and its 3 false flags disappeared.

**Finding F2 (documented, not fixed):** the detector is weak on unusual packaging (shelf4's oversized clear bags: 14 boxes on a full shelf) and odd color casts (shelf6: 7 boxes). These are our two honest model-level failure cases. A larger model variant (`sku110k-yolo11-s640`) is available as a mitigation.

## 2. Component level — slot verdicts (flag verification)

All 25 flags across the 6 sample images were checked against the photos:

| Image | Flags | Genuine problems | Root cause of false alarms |
|---|---|---|---|
| shelf1 | 2 | 0 | detector cap (fixed) + composite figure |
| shelf2 | 3 → 0 after fix | 0 | detector cap (fixed) |
| shelf3 | 7 | 0 | perspective foreshortening at shelf edges; expected_facings calibrated from observed density (circular) |
| shelf4 | 1 | 0 | under-detection of large transparent bags |
| shelf5 | 9 | 0* | *4 left-column `out_of_stock` flags are technically correct but unactionable — the planogram column covers a window/wall, not shelf. Rest: perspective under-detection |
| shelf6 | 3 | 0 | severe under-detection (7 boxes on a full shelf) |

**Honest conclusion:** the sample set contains **no real out-of-stock situations**, so true-positive precision cannot be measured from these photos alone. This motivated the staged test below — and future work: real staged photos with known gaps.

**Data-quality finding:** shelf1/shelf2 are *composite figures from the SKU-110K paper* (multiple photos + labels stitched together), not single photographs. They remain useful for detection smoke-tests but are excluded from slot-verdict scoring. Real photos should replace them in the final eval set.

## 3. Staged out-of-stock test (synthetic)

Blacked out one slot of shelf3 (row 2, slot 3) to simulate a genuine gap.

- **Result:** the slot's count dropped from ≥6 (correct) to 4/6 → flagged `low_facing`. Direction correct, magnitude weak — the dark rectangle still yields some detections (shelf rails/edges), and neighboring slot counts shifted.
- **Conclusion:** synthetic blackouts are a blunt instrument; the agent *is* sensitive to stock removal, but clean true-positive measurement needs real staged photos. Documented as a limitation + next step.

## 4. System level

| Metric | Value |
|---|---|
| Pipeline completion (sample set) | 6/6 images, 0 crashes |
| Robustness scenarios (`tests/run_scenarios.py`) | 11/11 pass, 0 crashes |
| Latency | 0.6–1.7 s/image (Apple Silicon MPS) |
| Trace completeness | every run logs all 4 envelope hand-offs per image |
| Rejection correctness | 5/5 bad inputs rejected with clear reasons (corrupt, empty, tiny, oversized, text-as-jpg) |

## 5. Fixes applied as a result of evaluation

1. `max_det` 300→1000 in detector (finding F1)
2. Detector no longer crashes on undecodable images (IndexError guard)
3. TaskAgent creates output folders on any `--out` path
4. Per-image tuned planograms in `data/planograms/` (removes floor/wall false flags)

## 6. Known limitations (carried into README)

- Detection ≠ identification: no brand-level "wrong product" verdicts
- Perspective at shelf edges under-detects → some false `low_facing` on fully stocked shelves
- No true-positive OOS measurement yet — needs real staged photos
- Composite paper figures excluded from verdict scoring
