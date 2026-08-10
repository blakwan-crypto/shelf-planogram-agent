# SCRIPT — shelf-planogram-agent-demo

**Voice:** Kokoro local default
**Voice settings:** natural tutorial pace · English
**Voice direction:** Clear, grounded, technically honest; sound like a student confidently explaining a working project to a reviewer.

---

## Line 1 — Hook (Frame 1)

**Time:** 0.0 – 9.0s
**Delivery:** Start with a practical question, then land the promise.

    A shelf photo shows what is there. It does not tell staff what to do. This agent closes that gap.

## Line 2 — The manual audit problem (Frame 2)

**Time:** 9.0 – 21.0s
**Delivery:** Recognize the friction without overselling it.

    The old audit is three disconnected things: a photo, a planogram, and a person trying to reconcile them by eye.

## Line 3 — One image, six stages (Frame 3)

**Time:** 21.0 – 37.0s
**Delivery:** Orient the viewer with a clean, measured list.

    Point the system at a folder of shelf images. Six stages take over: validate, detect, align, reason, act, and trace.

## Line 4 — Perception: ScannerAgent (Frame 4)

**Time:** 37.0 – 52.0s
**Delivery:** Explain the model's job and its boundary.

    First, preprocessing rejects bad inputs. Then ScannerAgent uses a SKU-110K-trained YOLO model to find product locations — not brand names.

## Line 5 — Reasoning: AnalystAgent (Frame 5)

**Time:** 52.0 – 69.0s
**Delivery:** Make the rules feel inspectable, not magical.

    AnalystAgent maps those detections into planogram slots. Inspectable rules turn counts into correct, low-facing, out-of-stock, or misplaced.

## Line 6 — Action and trace: TaskAgent (Frame 6)

**Time:** 69.0 – 82.0s
**Delivery:** Accelerate slightly into the operational payoff.

    TaskAgent turns the report into a prioritized work order, saves photo evidence, and writes the hand-off to a JSONL trace.

## Line 7 — Evaluation found the hidden bug (Frame 7)

**Time:** 82.0 – 100.0s
**Delivery:** Emphasize the before-and-after discovery.

    The system completed six sample images and ten robustness scenarios with zero crashes. Evaluation also found a hidden detector cap: shelf2 jumped from 300 to 909 detections after the fix, and its false flags disappeared.

## Line 8 — Honest limits (Frame 8)

**Time:** 100.0 – 109.0s
**Delivery:** Slow down and be candid.

    It is not brand recognition. Perspective, unusual packaging, and color casts still cause misses. And the current photos do not contain real stockouts, so true positive precision still needs staged data.

## Line 9 — From pixels to a task (Frame 9)

**Time:** 109.0 – 120.0s
**Delivery:** Return to the opening idea and finish with calm confidence.

    That is the whole idea: pixels in, explainable action out, with the reasoning left behind. The repository is public, reproducible, and ready to inspect.
