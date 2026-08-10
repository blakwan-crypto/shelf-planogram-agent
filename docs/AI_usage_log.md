# AI Usage Log

Course policy: document how AI tools were used while building this project.
Most recent entries first.

## Summary & Attribution

AI pair-programming agents (pi coding agent; Claude Code for the demo video)
were used throughout this project, and every session is logged below. Rough
attribution: the AI drafted most of the code and the video; the project idea,
architecture, scope decisions, test-scenario choices, and all verification and
evaluation judgments were mine. Every AI-produced bug fix was reproduced by
hand before being accepted, and I have reviewed every file well enough to
explain it.

## 2026-08-03 — Final polish: README, notebooks, repo hygiene (pi coding agent)

**Tool:** pi coding agent (LLM pair-programmer), local terminal.

**What the AI did:**

- Final README pass: verified every command and number in it against a real
  fresh run of the pipeline.
- Cleaned up repo hygiene: made sure generated outputs, model weights, and
  working files were gitignored so the submitted repo only contains source,
  docs, sample data, and curated results.
- Updated the three notebooks (exploration, evaluation, demo) to match the
  final pipeline behavior.

**What I did myself:**

- Decided what the final README should claim and checked every claim against
  real output before allowing it in.
- Ran the fresh-clone test myself: cloned the repo into a new folder, followed
  my own README start to finish, confirmed it works.

**What I learned:**

- "Works on my machine" ≠ "works from a fresh clone" — generated files
  committed to git make a repo look broken even when it isn't.
- A README is a contract: if a stranger can't follow it in 10 minutes, the
  project isn't done.

## 2026-08-02 — Demo video production (Claude Code + HyperFrames)

**Tool:** Claude Code (LLM agent) driving HyperFrames, a code-based video
framework, plus a TTS narration tool.

**What the AI did:**

- Built the narrated explainer video end-to-end: storyboard, animated scenes
  of the problem/pipeline/results/limitations, synthetic voiceover, captions,
  and the final render.
- Produced supporting assets (scene text, capture scripts) under
  `videos/shelf-planogram-agent-demo/`.

**What I did myself:**

- Wrote the creative brief: audience (instructor), tone (honest, including
  limitations), and which results to show.
- Reviewed every scene for factual accuracy against the real pipeline output
  and rejected/revised scenes that overstated results.
- Made the call to include the failure cases in the video, not just wins.

**What I learned:**

- Video generation agents are fast at production but will happily narrate
  claims that aren't true — every number on screen has to be checked against
  the real metrics.
- Showing a failure case on purpose made the demo more credible, not less.

## 2026-08-02 — Evaluation round: verify every flag, fix max_det bug (pi coding agent)

**Tool:** pi coding agent, local terminal.

**What the AI did:**

- Ran the evaluation: all 6 sample images through the pipeline, compared
  agent flags against the actual photos, and wrote `results/eval_report.md`.
- Found and fixed a real bug: the detector's `max_det` cap silently truncated
  dense shelves (shelf2 reported 300 products; the true count was 909).
- Built the staged out-of-stock test (blacking out one slot in a photo) to
  probe whether the reasoning stage detects OOS in the right direction.

**What I did myself:**

- Human-verified all 25 agent flags against the actual shelf photos — the AI
  proposed the verdicts, I confirmed each one by eye.
- Decided which failures were honest limitations to document (unusual
  packaging, color-cast photos, perspective foreshortening) vs. bugs to fix.

**What I learned:**

- A detector can be "working" and still silently wrong — the `max_det`
  default looked fine until we counted.
- Evaluation isn't a victory lap: the most valuable output of this round was
  the documented failure list.

## 2026-08-02 — Robustness suite + parallel code review (pi coding agent, parallel review agents)

**Tool:** pi coding agent, including multiple review agents run in parallel
against the codebase.

**What the AI did:**

- Built `tests/run_scenarios.py` and the 11-scenario robustness suite
  (blurry, dark, corrupt, empty, oversized, tiny, tilted, non-shelf,
  not-an-image, low-confidence, staged OOS).
- The parallel review agents found two real bugs I had missed: an IndexError
  in the detector on empty detection sets, and a missing mkdir in the
  TaskAgent when output folders don't exist yet.
- Tuned per-image planograms where camera angle made the default 4x8 grid a
  bad fit.

**What I did myself:**

- Chose the scenario list — I wanted the "unhappy paths" tested, not just
  clean inputs.
- Reproduced both reported bugs myself before accepting the fixes, and
  confirmed the suite passed 10/10 after them (later 11/11 once the staged
  OOS scenario got its machine-readable expectation line).

**What I learned:**

- Parallel AI review is genuinely useful for bug-hunting, but every finding
  still has to be reproduced by hand before you trust it.
- Graceful rejection (corrupt file → clean error, not a crash) is a feature
  you have to design and test for, not something you get for free.

## 2026-08-02 — Project scaffolding + feasibility test (pi coding agent)

**Tool:** pi coding agent (LLM pair-programmer), running locally in my terminal.

**What the AI did:**

- Ran a feasibility test: compared off-the-shelf YOLOv8 (COCO classes) vs. a
  SKU-110K-trained YOLO11 on 3 shelf photos. Finding: generic YOLOv8 is useless
  on shelf photos (0 detections); the SKU-110K model detects ~300 products/photo.
  This decided the project was viable.
- Scaffolded this repository: message contracts, three agents, orchestrator,
  planogram format, docs, and this log.
- Ran the pipeline end-to-end on the 6 sample images and verified outputs.

**What I did myself:**
- Chose the project idea (retail shelf planogram) and designed the architecture
  through 4 diagram versions.
- Made the go/no-go decision after the feasibility test.
- (Ongoing) Reviewing every generated file so I can explain each line.

**What I learned:**
- Pre-trained generic detectors (COCO) fail on dense retail shelves; a
  domain-specific model (SKU-110K) is essential.
- The SKU-110K model detects product *locations*, not brand identity — this
  shaped the honest scope of slot-compliance vs. brand-level compliance.
- Message envelopes between agents make the system traceable and the
  reasoning inspectable.
