# Architecture — Retail Shelf Planogram Compliance Agent

Tier 3 multi-agent system. Three agents with distinct roles communicate
**only** through defined message envelopes; the orchestrator routes and
logs every hand-off.

## Pipeline (all 6 mandatory stages)

```
                 ┌────────────────────────────────────────────────┐
                 │  STAGE 6 — ORCHESTRATOR + TRACE LOGGER         │
                 │  owns run_id · routes every handoff · logs     │
                 │  input→perception→decision→action to JSONL     │
                 └───────┬────────┬────────┬────────┬─────────────┘
                         ▼        ▼        ▼        ▼
┌──────────┐   ┌──────────┐   ┌───────────┐   ┌────────────┐   ┌──────────┐
│ STAGE 1  │──▶│ STAGE 2  │──▶│ STAGE 3   │──▶│ STAGE 4    │──▶│ STAGE 5  │
│ Ingest   │   │ Preprocess│  │ Scanner   │   │ Analyst    │   │ Task     │
│ batch    │   │ validate │   │ Agent     │   │ Agent      │   │ Agent    │
│ folder   │   │ + reject │   │ YOLO11 /  │   │ planogram  │   │ annotate │
│          │   │  bad ones│   │ SKU-110K  │   │ rules      │   │ + work   │
└──────────┘   └────┬─────┘   └───────────┘   └────────────┘   │ order    │
                    ▼                                           └────┬─────┘
             RejectedInput                                          ▼
             (trace saved,                                  results/images/
              batch continues)                               results/tasks/
                                                              results/traces/
```

## Message contract

Every hand-off is an `Envelope` (see `agents/contracts.py`):

`run_id · sender · recipient · message_type · timestamp · confidence · payload`

Payload types flow in a fixed chain:

`PreprocessResult → ShelfScan → ComplianceReport → WorkOrder`
(with `RejectedInput` as the graceful-failure branch after Stage 2)

## Agent roles

| Agent | Stage | Input → Output | Logic |
|---|---|---|---|
| ScannerAgent | 3 Perception | PreprocessResult → ShelfScan | YOLO11n trained on SKU-110K; boxes + confidence, generic `object` label |
| AnalystAgent | 4 Reasoning | ShelfScan → ComplianceReport | Rule-based: map detection centers into planogram slots; verdict per slot: `correct` / `low_facing` / `out_of_stock`; detections outside all slots = `misplaced` |
| TaskAgent | 5 Action | ComplianceReport → WorkOrder | Builds restock task list, draws annotated image (slot colors by verdict), writes JSON report + work order to results/ |
| Orchestrator | 6 Logging | — | run_id, routes every message as an Envelope, appends each to `results/traces/<run_id>.jsonl` |

## Why rules instead of an LLM (for now)

The assignment allows rule-based reasoning and warns that a working rule
loop beats a broken LLM orchestration. Every verdict here is inspectable:
slot verdict = f(expected_facings, actual_facings). An LLM/VLM layer
(e.g., brand identification, OCR of shelf labels) is a documented stretch
goal behind the "implementation guardrail": only after the baseline is stable.

## Known limitations (honest list)

- The detector finds products, not brands → "misplaced" means "outside any
  slot", not "wrong product in slot".
- Slot bands are fractions of image height; camera tilt shifts them
  (mitigation: per-shelf planogram tuning; documented in eval failure cases).
- Sparse/unusual packaging (shelf4, shelf6) under-detects — tracked as
  failure cases in the evaluation.
