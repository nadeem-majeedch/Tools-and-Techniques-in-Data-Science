# Lab 13 — Matplotlib: Figures That Communicate

**Session:** Week 7 · Session 13 · 90 min
**CLO:** CLO-1
**Difficulty:** Intermediate

## Learning objectives

By the end of this lab you can:

1. Build figures with the `figure`/`axes` model.
2. Create line, scatter, bar, and histogram plots.
3. Label axes, titles, legends, and grids; use colors deliberately.
4. Save figures with `savefig` at print quality.

## Problem statement

A client wants "one picture that explains our sales week." You will produce
a **2×2 dashboard figure**: (a) daily revenue line, (b) revenue by day-of-
week bar, (c) bill-vs-tip scatter, (d) tip histogram. Every subplot needs
proper labels; the whole figure must save to
`datasets/sales-dashboard.png` at 150 dpi.

## Dataset requirements

Seaborn built-in `tips` (244 rows). Use `tips["total_bill"]` as a proxy for
"bill" and `tips["tip"]` for "tip". "Day" is `tips["day"]`.

## Step-by-step tasks

1. **Figure/axes:** `fig, axes = plt.subplots(2, 2, figsize=(12, 8))`.
   Explain in a comment what `axes` is (a 2×2 ndarray of Axes).
2. **Line:** on `axes[0, 0]`, plot mean `total_bill` per day (groupby +
   mean), as a line with markers. Title "Mean bill by day".
3. **Bar:** on `axes[0, 1]`, bar chart of total `tip` per day, colored by
   day, y-label "Total tip ($)".
4. **Scatter:** on `axes[1, 0]`, `total_bill` vs `tip` with `alpha=0.5`,
   axis labels, and a title "Bill vs tip".
5. **Histogram:** on `axes[1, 1]`, `tip` with 15 bins, edgecolor white,
   title "Tip distribution".
6. **Polish:** one shared suptitle "Tips — one week", `tight_layout()`, and
   a legend where it adds information.
7. **Save:** `fig.savefig("datasets/sales-dashboard.png", dpi=150,
   bbox_inches="tight")` — then load it back with `matplotlib.image.imread`
   and print its shape to prove it exists.

## Starter code

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

Path("datasets").mkdir(exist_ok=True)

tips = sns.load_dataset("tips")

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
# axes is a 2x2 array of Axes objects; index with [row, col]

# --- axes[0, 0]: mean bill per day (line) ---
# your code here

# --- axes[0, 1]: total tip per day (bar) ---
# your code here

# --- axes[1, 0]: bill vs tip (scatter) ---
# your code here

# --- axes[1, 1]: tip histogram ---
# your code here

fig.suptitle("Tips — one week", fontsize=16)
fig.tight_layout()
fig.savefig("datasets/sales-dashboard.png", dpi=150, bbox_inches="tight")
```

## Expected output

- A 2×2 figure, every subplot titled and axis-labeled.
- The scatter shows the known positive bill–tip relationship; the
  histogram is right-skewed (most tips 2–4 $).
- `datasets/sales-dashboard.png` exists; `imread(...).shape` prints e.g.
  `(1050, 1400, 3)` (exact numbers vary with dpi/size).
- No overlapping labels after `tight_layout()`.

## Questions

1. What is the difference between a `Figure` and an `Axes`?
2. Why `alpha=0.5` on the scatter? What problem does it solve with 244
   points?
3. Why use `tight_layout()` before saving?
4. `dpi=150` — what does it change about the saved file?
5. When would a bar chart mislead vs. a histogram?

## Challenge task

Add a **third dimension** to the scatter without seaborn: color points by
`smoker` using a loop over `for smoker, color in [("Yes", "red"),
("No", "blue")]`, plotting each subset separately with its own label and a
legend. Save as `datasets/scatter-smoker.png`. Comment on whether the
groups separate visually.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| 2×2 subplot structure | 3 | figure/axes used correctly |
| Line + bar subplots | 4 | correct data, labels, titles |
| Scatter + histogram | 4 | alpha, bins, labels |
| Polish (suptitle, tight_layout) | 2 | visible in output |
| savefig + imread proof | 3 | file exists, shape printed |
| Answers to questions | 2 | Q1, Q3 correct |
| Challenge: smoker-colored scatter | 4 | legend, saved, comment |
| **Total** | **22** | |