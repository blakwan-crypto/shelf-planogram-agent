# Planogram Tuning — data/planograms/

This document explains what a planogram file is, how the tuned planograms in
`data/planograms/` were chosen for each sample photo, what changed versus the
default grid, and what the known limits are.

> Read this with a photo in one hand and the matching `data/planograms/*.json`
> in the other — every number in the JSON traces back to something visible in
> the photo or in the detection data.

---

## 1. What is a planogram? (plain English)

A planogram is the store's official map of a shelf: *which shelf, how many
products should be there, and where*. The AnalystAgent compares that map
against what the computer *sees* in a photo (the list of detected product
boxes) and marks each map slot:

| Verdict | Meaning |
|---|---|
| `correct` | the slot holds about what the planogram says it should |
| `low_facing` | the slot has some product, but fewer than expected |
| `out_of_stock` | the slot is completely empty |
| `misplaced` | a product was detected where no slot exists at all |

## 2. The file format

One JSON file per photo. Top level:

```json
{
  "name": "shelf3",
  "description": "…why this planogram was built this way…",
  "rows": [ … ]
}
```

Each **row** = one shelf band in the photo:

```json
{
  "row_id": "r2",
  "y_min": 0.28,   // top edge of the shelf, as a fraction of photo height
  "y_max": 0.50,   // bottom edge of the shelf (0.0 = very top, 1.0 = very bottom)
  "slots": [ … ]
}
```

Each **slot** = one spot on that shelf. Slots split the row into equal widths
left → right (like a clipboard with fixed columns):

```json
{ "slot_id": "r2_s1", "expected_facings": 6 }
```

`expected_facings` = how many products a *full* slot should show. The
AnalystAgent counts the detected products whose center lands inside a slot:
0 → out_of_stock, fewer than expected → low_facing, expected or more → correct.

**Key rule to remember:** `y_min`/`y_max` are fractions (0–1) of the image
height, so the same planogram style works on any photo size.

## 3. How the tuned planograms were chosen

I could not rely on the default 4×8 grid (4 rows over the full image height,
8 slots, expected 5 everywhere) because real photos contain **floor, ceiling,
wall, and signage** — the grid happily turned those into fake "empty slots".

Method (same for every photo):

1. **Find the shelf bands.** Product boxes that sit on the same shelf line up
   at the bottom (they rest on the shelf). I clustered those bottom edges to
   find where the real shelves are, and excluded anything that is not a shelf
   (floor, ceiling, wall, gap).
2. **Pick slot counts** from the product groupings in each row (6–8 slots for
   busy rows, fewer for sparse rows).
3. **Set `expected_facings`** to what a full slot of that width actually holds
   in the photo (the typical count seen per slot), instead of a flat 5.

### Per image

**shelf1.jpg (1430×1666)** — a tall, densely packed display whose products sit
on many narrow levels. The top half splits into 5 levels (rows 1–5, 8 slots
each, expected 5–6 — that is the real density). The lower shelves are sparser
in the photo, so rows 6–7 use 6 wider slots with expected 2.

**shelf2.jpg (1385×1405)** — three shelf levels (the shelf boards are visible
at ~36% and ~68% of the height). 8 slots per row. Expected facings follow the
photo: 8 on the top shelf, 5 on the middle (its right half is genuinely
lighter), 10 on the dense bottom shelf.

**shelf3.jpg (1280×960)** — four rows. The top row stops at 27% (there is an
empty gap below it). Rows 2–3 cover the dense middle. The **bottom row is the
fix**: it ends at 99% (not 100%) and uses **5 wider slots instead of 8**, so
the photo's bottom-right corner — which is plain floor, not shelf — no longer
becomes an out_of_stock slot. This is the exact bogus flag the default grid
produced (`r4_s8`).

**shelf4.jpg (1280×853)** — this photo shows only a handful of *large*
products on two levels (the top of the frame and the middle band are empty
wall). Two rows, 3 wide slots each; a full slot of that width holds about
2 large products.

**shelf5.jpg (1280×853)** — four rows matching the visible product levels.
The photo's left edge is plain wall, so the leftmost slot of each row
inevitably reads out_of_stock (slots always split the full width — see
limitations). Stocked rows use 6 slots (4 on the thin bottom row), expected
2–3 per slot.

**shelf6.jpg (1280×960)** — the detector found only 7 products, all in the
top half of the frame; the rest of the photo is background/other aisles.
Rows only cover the three visible product levels (0–11%, 12–36%, 37–51%)
with 2 wide slots each, so the empty bottom half is **not turned into slots
at all** — the default grid flagged 26 fake out-of-stock slots there.

## 4. Before / after (verified with real pipeline runs)

All six were verified end-to-end with the real pipeline
(`agents.orchestrator`, output under `results/planogram_check/<name>/`).
"Before" = the default `data/planogram.json` (4×8 grid, expected 5).

| Photo | Before (correct / low / out_of_stock) | After (correct / low / out_of_stock) |
|---|---|---|
| shelf1 | 16 / 16 / 0 | **50 / 2 / 0** |
| shelf2 | 27 / 5 / 0 | **21 / 3 / 0** |
| shelf3 | 25 / 6 / **1** (bogus floor slot) | **22 / 7 / 0** |
| shelf4 | 0 / 11 / **21** | **5 / 1 / 0** |
| shelf5 | 3 / 20 / 9 | **11 / 5 / 4** |
| shelf6 | 0 / 6 / **26** | **3 / 0 / 3** |

Highlights:

- **shelf3**: the bogus bottom-right "out_of_stock" (which was floor) is gone.
- **shelf4** and **shelf6**: 47 fake out-of-stock flags eliminated (21 → 0
  and 26 → 3). The remaining 3 on shelf6 are the right-hand half of the photo,
  where nothing was detectable.
- **shelf1**: 16 low_facing flags (mostly from the default grid's mismatch
  between 4 wide rows and ~10 real levels) dropped to 2.
- **shelf5**: the remaining 4 out-of-stock slots are all on the photo's left
  wall strip — see limitation 2 below.

## 5. Known limitations (read before judging a verdict)

1. **Camera tilt shifts the bands (documented eval failure case).** The rows
   are horizontal bands. If a photo is taken at an angle, products on one
   shelf no longer sit inside one band, and the AnalystAgent reports
   phantom out_of_stock/low_facing slots or "misplaced" products. Tuned
   planograms assume a reasonably level photo.
2. **Slots always split the full row width.** If a photo shows a shelf that is
   only partly stocked (e.g. shelf5, where the left ~25% of the frame is
   wall), the leftmost slot still exists and reads out_of_stock. The planogram
   cannot shrink a row's sides — only the number of (equal-width) slots.
3. **The detector caps at 300 boxes per photo.** On very dense photos
   (shelf1, shelf2, shelf3) the busiest shelves use up the budget, so lower
   shelves can look "light" even when the store is full. `expected_facings`
   for those rows reflects what the detector actually sees.
4. **Signs vs. products.** The detector labels everything "object". A hanging
   sign near the top of a photo can land in a slot and count as a "facing"
   (shelf6's top row). It is harmless for the demo but worth knowing.

## 6. Re-running the verification

```bash
# make a one-image folder (symlink is fine)
mkdir -p data/planograms/tmp_shelf3
ln -s ../../sample/shelf3.jpg data/planograms/tmp_shelf3/shelf3.jpg

# run the pipeline against that photo's tuned planogram
./.venv/bin/python -m agents.orchestrator \
  --images data/planograms/tmp_shelf3 \
  --planogram data/planograms/shelf3.json \
  --out results/planogram_check/shelf3
```

The report lands in `results/planogram_check/shelf3/tasks/shelf3_report.json`
and the annotated photo in `results/planogram_check/shelf3/images/`.
