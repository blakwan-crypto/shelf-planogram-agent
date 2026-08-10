---
workflow: faceless-explainer
flow: automation
status: complete
storyboard: yes
message: "This retail shelf agent turns one shelf photo into an explainable work order through perception, reasoning, action, and trace logging."
destination: youtube
aspect: 1920x1080
language: en
audience: "ITAI 1378 instructor and technical reviewer"
length: 120s
angle: "how-to-process with story-explainer"
narration: yes
---

## Intent

A two-minute project demonstration that feels like a live walkthrough: open with the store problem, show the shelf image entering the system, explain the ScannerAgent, AnalystAgent, TaskAgent, and Orchestrator, then land on the saved work order and trace. Include the evaluation lesson that the agent found and fixed the hidden `max_det=300` truncation bug. The tone is clear, human, and technically honest rather than promotional.

## Assets

None. This is a faceless explainer; visuals are invented as diagrams, data panels, terminal-style readouts, and agent-message flows.

## Customizations

- Hybrid narrative + architecture walkthrough + live processing demo.
- Show perception → reasoning → action → graceful failure / trace logging.
- Include real project proof points: six sample images completed, ten robustness scenarios passed, and shelf2 detections improving from 300 to 909 after the fix.

## Notes

- YouTube landscape output: 1920×1080.
- Use offline Kokoro narration; no HeyGen credentials or paid services.
- Do not claim brand-level SKU identification; the system detects generic product locations and reasons about facings.
- Avoid presenting the sample shelves as a perfect accuracy benchmark; the evaluation report documents their limitations.
