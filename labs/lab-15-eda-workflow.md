# Lab 15 — EDA Workflow: One Full Analysis

**Session:** Week 8 · Session 15 · 90 min
**CLO:** CLO-1
**Difficulty:** Intermediate

## Learning objectives

By the end of this lab you can:

1. Run a complete EDA: shape → quality → univariate → bivariate → insights.
2. Decide which columns need cleaning and justify it.
3. Produce a written insight per finding (not just code output).
4. Structure an EDA as a reproducible notebook.

## Problem statement

The biology lab hands you the penguins dataset with no instructions: "tell
us what is interesting." You must deliver a **structured EDA notebook**
with five numbered sections and exactly three written insights at the end —
each insight backed by a number and a plot. This is the pattern you will
repeat for the final project.

## Dataset requirements

Seaborn built-in `penguins` (344 rows, 7 columns, known missing values).

## Step-by-step tasks

1. **Section 1 — Overview:** print `shape`, `info()`, `describe()`,
   `head()`. One sentence: what is this dataset?
2. **Section 2 — Quality:** count missing values per column; state which
   column is worst and why you will `dropna()` for the rest of the EDA
   (note the row loss: 344 → 333).
3. **Section 3 — Univariate:** for each numeric column, print `mean`,
   `median`, `std`; plot histograms for `bill_length_mm` and
   `body_mass_g` (2 subplots). Note any bimodality — why might it exist?
4. **Section 4 — Bivariate:**
   - `sns.boxplot(x="species", y="body_mass_g")` — which species is
     heaviest? Report median values.
   - `sns.scatterplot(x="bill_length_mm", y="bill_depth_mm",
     hue="species")` — do species separate on these two? Which pair
     separates best?
   - `sns.heatmap(df.select_dtypes("number").corr(), annot=True)` — the
     two strongest correlations, with values.
5. **Section 5 — Insights:** exactly three bullet points, each with the
   pattern *claim → evidence (number) → plot reference*. Example:
   "Gentoo penguins are the heaviest — median body mass 5,000+ g vs under
   4,000 g for the others — boxplot in Section 4."

## Starter code

```python
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")

penguins = sns.load_dataset("penguins")

# Section 1 — Overview
# your code here

# Section 2 — Quality
# your code here

# Section 3 — Univariate
# your code here

# Section 4 — Bivariate
# your code here

# Section 5 — Insights (write these as a markdown cell, not code)
```

## Expected output

- Section 1: `(344, 7)`, dtypes listed, `describe()` printed.
- Section 2: `body_mass_g` and `sex` missing 2 each; `bill_*` and
  `flipper_length_mm` missing 1–2; total loss to `dropna()`: 344 → 333.
- Section 3: histograms show two peaks (species mixture) — this is the
  bimodality note.
- Section 4: Gentoo clearly heaviest; Chinstrap and Adelie overlap on
  mass; bill length vs depth separates all three species well.
- Section 5: three claim→evidence→plot bullets.

## Questions

1. What does `select_dtypes("number")` return, and why is it needed before
   `.corr()`?
2. Why does `describe()` hide missing values instead of showing them?
3. What is bimodality, and what does it hint at in this dataset?
4. Correlation between `bill_length_mm` and `body_mass_g` is ~0.59 — what
   does that number *not* tell you?
5. Order the EDA stages and say why quality checks come before plots.

## Challenge task

Re-run the bivariate analysis **by island** instead of by species
(`hue="island"` on the scatter, boxplot on island). Write a 4th insight
about islands vs. species (hint: island and species are almost the same
partition — check `pd.crosstab(penguins["island"], penguins["species"])`
to see why).

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Overview section | 3 | shape/info/describe/head |
| Quality section + dropna decision | 4 | missing counts + reasoning |
| Univariate stats + histograms | 4 | bimodality noted |
| Bivariate: box, scatter, heatmap | 6 | correct readings, values |
| Three insights (claim+evidence+plot) | 6 | all three grounded |
| Answers to questions | 3 | Q1, Q4, Q5 correct |
| Challenge: island analysis + crosstab | 4 | insight + crosstab |
| **Total** | **30** | |