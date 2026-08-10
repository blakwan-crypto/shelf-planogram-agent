---
format: 1920x1080
duration: 120s
message: "This retail shelf agent turns one shelf photo into an explainable work order through perception, reasoning, action, and trace logging."
arc: story-explainer with how-to-process
audience: ITAI 1378 instructor and technical reviewer
mode: collaborative
music: none
---

## Video direction

- **Palette system:** Code Editorial — warm cream ground and tile surfaces, ink typography, one coral voltage moment per frame, and warm navy only for terminal / trace surfaces. EB Garamond carries the display thesis; Inter carries explanation; JetBrains Mono carries stage labels, code, and message metadata.
- **Motion grammar:** smooth long-tail settles; every reveal is paced to the narration and arrives when its phrase is spoken. Use sequential reveals in the back half of each frame, then deliberate holds. No default bounce, no lazy breathing, and no slow back-half camera drift.
- **Rhythm:** the hook and problem are quick recognitions; the pipeline and agent frames are the explanatory build; the evaluation frame is the peak; the limits frame is a quiet credibility breather; the close holds still on the thesis.
- **Caption-safe layout:** keep all load-bearing copy and diagrams in the upper 83% of the canvas so the caption band remains clear.
- **Negative list:** no fake browser chrome, no invented model-accuracy claims, no brand-recognition implication, no purple/blue AI gradients, no slideshow front-load-then-freeze, and no screensaver-style independent floating motion.

## Frame 1 — A photo is not a work order

- scene: A store shelf sketch fractures into a question, then resolves into the agent's promise.
- voiceover: "A shelf photo shows what is there. It does not tell staff what to do. This agent closes that gap."
- duration: 6.677s
- poster: 5s
- transition_in: cut
- status: animated
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Question → answer pairing
- beat: Recognition and curiosity
- blueprint: kinetic-type-beats (Adapt)
- focal: the phrase “photo → work order”
- roles: warm paper field = background · coral spike = supporting accent · thesis type = foreground subject

Adapt: keep the centered type relay and held final beat; replace a product tagline with the practical shelf-audit gap.

Scene 1 (0.0–1.6s): warm cream field with a small coral spike in the upper-left; only “A shelf photo…” enters as a per-word staggered reveal (`dynamic-content-sequencing`) in a rule-of-thirds layout.
Scene 2 (1.6–4.3s): the phrase “does not tell staff what to do” assembles in the centered upper field via kinetic beat-slam (`kinetic-beat-slam`), with one coral underline drawing beneath “do” (`css-marker-patterns`).
Scene 3 (4.3–6.7s): “This agent closes that gap” scale-swaps into a compact work-order arrow lockup (`scale-swap-transition`) and holds still in the upper two-thirds; the caption band stays empty.

narrativeRole: Open on the viewer's practical problem, then land the value proposition before introducing implementation details.
keyMessage: The system converts visual shelf evidence into an actionable work order.

## Frame 2 — The manual audit problem

- scene: A shelf photo, a planogram grid, and a handwritten checklist orbit a tired store worker before collapsing into one clean input.
- voiceover: "The old audit is three disconnected things: a photo, a planogram, and a person trying to reconcile them by eye."
- duration: 8.085s
- poster: 6s
- transition_in: crossfade
- status: animated
- src: compositions/frames/02-problem.html
- type: pain_point
- persuasion: Concretization and accumulation
- beat: Friction and recognition
- blueprint: overwhelm-surround (Adapt)
- focal: three disconnected audit surfaces closing around “by eye”
- roles: cream paper = background · photo tile / planogram tile / checklist = midground · “by eye” question = foreground subject

Adapt: keep the accumulation and clutter-shove-to-question shape; replace generic software windows and avatar morph with shelf evidence, a planogram, and a manual checklist.

Scene 1 (0.0–2.0s): a small invented shelf tile, planogram grid, and checklist assemble in a layered 60/40 composition through staggered scale-in (`spring-pop-entrance`), one object per spoken noun.
Scene 2 (2.0–4.4s): the three surfaces multiply into a dense but readable audit cluster; labels “photo”, “planogram”, and “checklist” scatter as density markers (`center-outward-expansion`) around the upper-middle stage.
Scene 3 (4.4–6.4s): the surfaces shove toward the edges while “by eye” builds in the opened center with a word-by-word reveal (`dynamic-content-sequencing`), then the question holds.
Scene 4 (6.4–8.1s): a single coral line draws between the three surfaces and resolves the phrase “reconcile them” (`svg-path-draw`); hold the causal picture.

narrativeRole: Make the operational friction tangible without claiming an unsupported time or accuracy statistic.
keyMessage: The agent exists to connect evidence, expected layout, and action in one inspectable flow.

## Frame 3 — One image, six stages

- scene: A single shelf-image tile feeds a six-stage horizontal pipeline: validate, detect, align, reason, act, trace.
- voiceover: "Point the system at a folder of shelf images. Six stages take over: validate, detect, align, reason, act, and trace."
- duration: 8.704s
- poster: 8s
- transition_in: push-slide RIGHT
- status: animated
- src: compositions/frames/03-pipeline.html
- type: product_intro
- persuasion: Progressive disclosure
- beat: Orientation and focus
- blueprint: constellation-hub (Adapt)
- focal: the six-stage pipeline hub
- roles: shelf image tile = foreground source · stage nodes = supporting midground · connector lines and warm navy trace node = background structure

Adapt: keep the hub-and-satellite structure; use the Orchestrator as the center and the six pipeline stages as labeled satellites rather than logos.

Scene 1 (0.0–1.9s): a shelf-image tile lands left of center; “one folder of images” types on above it (`discrete-text-sequence`) in an asymmetric 60/40 layout.
Scene 2 (1.9–4.4s): validate, detect, align, reason, act, and trace nodes spring-pop one by one around the image and central Orchestrator (`spring-pop-entrance`); connector lines draw from source to hub (`svg-path-draw`).
Scene 3 (4.4–6.8s): the six nodes settle into a clear horizontal process strip; “six stages” counts up beside the hub (`counting-dynamic-scale`) while the camera stays locked.
Scene 4 (6.8–8.7s): the trace node switches to warm navy and a small JSONL receipt appears; the full pipeline holds as a readable map.

narrativeRole: Name the protagonist and give the viewer a stable map before the close-up walkthrough.
keyMessage: The project is a layered pipeline, not a single opaque prediction.

## Frame 4 — Perception: ScannerAgent

- scene: An invented shelf image receives product-location boxes; ScannerAgent sends a ShelfScan envelope to the next station.
- voiceover: "First, preprocessing rejects bad inputs. Then ScannerAgent uses a SKU-110K-trained YOLO model to find product locations — not brand names."
- duration: 12.309s
- poster: 8s
- transition_in: crossfade
- status: animated
- src: compositions/frames/04-perception.html
- type: feature_showcase
- persuasion: Demonstration and scope boundary
- beat: Comprehension
- blueprint: agent-progress-theater (Adapt)
- focal: ScannerAgent’s working state and ShelfScan receipt
- roles: validation status = foreground subject · invented shelf image and detection boxes = midground · warm cream grid = background

Adapt: keep the working-state theater and receipt cascade; replace a generic checklist with a validation status, product-location boxes, and a typed ShelfScan envelope.

Scene 1 (0.0–2.5s): a validation panel appears in the upper-left with “valid image 1280×960”; a thin coral scan arc draws on (`svg-path-draw`) while the shelf schematic remains dim.
Scene 2 (2.5–5.7s): as the narration names product locations, detection boxes appear in two staggered rows across the shelf schematic (`spring-pop-entrance`); the status changes from “scanning” to “found products” (`discrete-text-sequence`).
Scene 3 (5.7–9.0s): the ScannerAgent label docks to the top-left and a warm-navy ShelfScan envelope expands beside it (`anchored-layout-expand`); the model boundary “locations, not brands” highlights once (`css-marker-patterns`).
Scene 4 (9.0–12.3s): the receipt card holds with boxes and message metadata still; the working spinner stops exactly as the envelope lands.

narrativeRole: Demonstrate perception while making the model's honest scope explicit.
keyMessage: The detector supplies visual evidence about where products are, while validation provides graceful failure before inference.

## Frame 5 — Reasoning: AnalystAgent

- scene: Detection dots snap into planogram rows and slots; a rules panel changes slot states to correct, low facing, and out of stock.
- voiceover: "AnalystAgent maps those detections into planogram slots. Inspectable rules turn counts into correct, low-facing, out-of-stock, or misplaced."
- duration: 10.325s
- poster: 9s
- transition_in: push-slide RIGHT
- status: animated
- src: compositions/frames/05-reasoning.html
- type: feature_showcase
- persuasion: Progressive disclosure and rule reveal
- beat: Aha and confidence
- blueprint: panel-edit-live-sync (Adapt)
- focal: detections syncing into planogram slot verdicts
- roles: detection surface = foreground left · rule panel = foreground right · connector arrows and slot bands = supporting structure

Adapt: keep the live-sync couple; replace an editor control with the AnalystAgent’s detection count and the planogram rule panel, showing evidence and verdict changing together.

Scene 1 (0.0–2.1s): a shelf surface and an empty slot grid establish side by side in a split-screen layout; “map detections into slots” appears as the upper kicker.
Scene 2 (2.1–4.6s): product boxes align into row bands while the matching slot counter increments in the right panel (`control-target-sync`); the two surfaces remain co-visible.
Scene 3 (4.6–7.6s): rule rows reveal in sequence — correct, low-facing, out-of-stock, misplaced — with a highlight following the spoken category (`dynamic-content-sequencing`).
Scene 4 (7.6–10.3s): the final slot verdicts lock into a clean three-row report; the rule panel holds still so the reviewer can read the causal mapping.

narrativeRole: Show the reasoning layer as a visible transformation from raw detections to understandable slot verdicts.
keyMessage: The agent reasons with rules that a reviewer can inspect rather than hiding the decision inside an LLM.

## Frame 6 — Action and trace: TaskAgent

- scene: An Envelope message becomes a prioritized work-order list while a JSONL trace scrolls beside it.
- voiceover: "TaskAgent turns the report into a prioritized work order, saves photo evidence, and writes the hand-off to a JSONL trace."
- duration: 9.003s
- poster: 7s
- transition_in: crossfade
- status: animated
- src: compositions/frames/06-action-trace.html
- type: feature_showcase
- persuasion: Causal chain
- beat: Momentum and payoff
- blueprint: transcript-scroll-artifact-reveal (Adapt)
- focal: the JSONL hand-off becoming a work order
- roles: JSONL trace = foreground evidence surface · envelope rows = supporting midground · work-order card = payoff foreground

Adapt: keep the evidence traversal and artifact reveal; use the project’s Orchestrator → ScannerAgent → AnalystAgent → TaskAgent messages as the long surface.

Scene 1 (0.0–2.1s): a warm-navy trace surface establishes with one message row, then three more envelope lines cascade beneath it (`waterfall-entry`) in a full-width upper-83% strip.
Scene 2 (2.1–4.5s): the trace content scrolls upward through the frame (`3d-page-scroll` flat variant), revealing sender, recipient, message type, and confidence metadata in reading order.
Scene 3 (4.5–6.6s): the final TaskAgent hand-off receives a coral selection marker; a work-order card expands from the selected line (`anchored-layout-expand`) as the only hinge.
Scene 4 (6.6–9.0s): the work order holds beside the last trace line, with “photo evidence + machine-readable task” as the calm payoff.

narrativeRole: Complete the operational loop and prove that communication is defined, routed, and recorded.
keyMessage: The output is useful to staff and auditable to reviewers.

## Frame 7 — Evaluation found the hidden bug

- scene: Three proof counters assemble: 6/6 images, 10/10 scenarios, then a before-and-after detector cap showing 300 → 909.
- voiceover: "The system completed six sample images and ten robustness scenarios with zero crashes. Evaluation also found a hidden detector cap: shelf2 jumped from 300 to 909 detections after the fix, and its false flags disappeared."
- duration: 17.579s
- poster: 10s
- transition_in: push-slide RIGHT
- status: animated
- src: compositions/frames/07-proof.html
- type: social_proof
- persuasion: Demonstration and before/after contrast
- beat: Surprise and conviction
- blueprint: dataviz-countup (Adapt)
- focal: the 300 → 909 detector-cap correction
- roles: proof counters = foreground data instruments · before/after detector panels = midground · editorial grid = background

Adapt: keep the count-up and before/after data instruments; use only measured project values and let the detector-cap fix carry the peak.

Scene 1 (0.0–3.9s): “6 / 6 images” counts up beside a simple completion ring (`counting-dynamic-scale` + `stat-bars-and-fills`) in a centered upper-third lockup.
Scene 2 (3.9–7.8s): “10 / 10 scenarios” arrives as a second instrument with a short bar fill; the first proof shifts to a supporting rail.
Scene 3 (7.8–12.7s): a warm-navy before/after panel reveals “max_det 300” first, then “909 detections” counts up on the right (`counting-dynamic-scale`); a coral correction line draws between them.
Scene 4 (12.7–17.6s): “false flags disappeared” resolves as a quiet proof card beneath the comparison; the numbers hold still for reading.

narrativeRole: Make evaluation the proof beat and show that testing improved the system rather than merely decorating the README.
keyMessage: The project has reproducible pipeline evidence and an evaluation-driven bug fix.

## Frame 8 — Honest limits

- scene: Two balanced panels contrast what the baseline can claim with what it cannot yet claim.
- voiceover: "It is not brand recognition. Perspective, unusual packaging, and color casts still cause misses. And the current photos do not contain real stockouts, so true positive precision still needs staged data."
- duration: 14.677s
- poster: 5s
- transition_in: crossfade
- status: animated
- src: compositions/frames/08-limits.html
- type: benefit_highlight
- persuasion: Boundary-setting contrast
- beat: Unease and trust
- blueprint: comparison-split (Adapt)
- focal: the honest capability boundary
- roles: “can claim” card = foreground left · “not yet” card = foreground right · warm paper and hairline rule = background structure

Adapt: keep the balanced two-card comparison; use capability and limitation cards instead of paired product features, with no tilt or hype.

Scene 1 (0.0–2.0s): the title “honest limits” slides down into the upper center (`gsap-effects`) over a quiet cream field.
Scene 2 (2.0–5.0s): the left card arrives from the left with “generic product locations + rules-first reasoning”; the right card arrives from the right with “not brand recognition” (`split-tilt-cards` adapted to a flat editorial entry).
Scene 3 (5.0–7.5s): two small badges land — “demonstrated” and “future work” (`spring-pop-entrance`) — while perspective, packaging, and color-cast labels reveal below.
Scene 4 (7.5–9.0s): both cards hold in symmetry; the caption band remains clear.

narrativeRole: Protect credibility by clearly separating demonstrated capability from future work.
keyMessage: Honest scope and documented failure cases are part of the deliverable.

## Frame 9 — From pixels to a task

- scene: The shelf-image icon, agent nodes, work order, and trace lock into a final editorial statement with the GitHub repository name.
- voiceover: "That is the whole idea: pixels in, explainable action out, with the reasoning left behind. The repository is public, reproducible, and ready to inspect."
- duration: 11.008s
- poster: 6s
- transition_in: crossfade
- status: animated
- src: compositions/frames/09-close.html
- type: cta
- persuasion: Distillation and callback
- beat: Resolution and resolve
- blueprint: titlecard-reveal (Adapt)
- focal: “pixels in → explainable action out”
- roles: shelf glyph and trace mark = supporting foreground accents · thesis line = foreground subject · public repository label = mono chrome

Adapt: keep the restrained title-card landing; replace a brand logo with the project’s public, inspectable thesis and repository label.

Scene 1 (0.0–2.0s): the shelf glyph, agent-node mark, and trace mark sit faintly on warm cream; only the coral spike appears.
Scene 2 (2.0–5.0s): “pixels in” and “explainable action out” slide-up crossfade into the center (`discrete-text-sequence`), with a single coral arrow drawing between them.
Scene 3 (5.0–8.0s): “reasoning left behind” appears beneath in JetBrains Mono and the repository name types on as technical chrome (`dynamic-content-sequencing`).
Scene 4 (8.0–11.0s): the complete thesis holds static to the final frame; no additional motion is added.

narrativeRole: Callback to the opening gap and land the project's actual submission value: inspectable, reproducible work.
keyMessage: The project turns computer vision into a traceable retail action, not just a bounding-box demo.
