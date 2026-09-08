# Lab 14 — Seaborn: Statistical Plots

**Session:** Week 7 · Session 14 · 90 min
**CLO:** CLO-1
**Difficulty:** Intermediate

## Learning objectives

By the end of this lab you can:

1. Use `relplot`, `catplot`, and `displot` with `kind` and `hue`.
2. Read boxplots, violin plots, heatmaps, and pairplots.
3. Choose the right plot for a three-variable question.
4. Interpret what a plot shows — and what it hides.

## Problem statement

The marketing team asks three questions about the tips data: (1) does the
bill–tip relationship differ between lunch and dinner? (2) which day has
the highest tips *accounting for bill size*? (3) which variables correlate
most with `tip`? Your deliverable is **three plots, each answering exactly
one question**, plus one sentence of interpretation each.

## Dataset requirements

Seaborn built-in `tips` (244 rows). Optional: `penguins` for the challenge.

## Step-by-step tasks

1. **Q1 — relationship by meal:** `sns.relplot(data=tips, x="total_bill",
   y="tip", hue="time", style="smoker", alpha=0.6)`. Interpret: does the
   slope look different for lunch vs. dinner?
2. **Q2 — tip proportion by day:** first add
   `tips["tip_pct"] = tips["tip"] / tips["total_bill"] * 100`. Plot
   `sns.boxplot(data=tips, x="day", y="tip_pct")`. Which day's *median*
   is highest? Why is `tip_pct` fairer than raw `tip` for this question?
3. **Q3 — correlations:** build the numeric subset (`total_bill`, `tip`,
   `size`) and plot `sns.heatmap(df.corr(), annot=True, cmap="coolwarm")`.
   Which single variable correlates most with `tip`? Report the number.
4. **Add a categorical:** `sns.catplot(data=tips, x="day", y="tip",
   hue="smoker", kind="bar", ci=None)` — read it: is the smoker gap
   consistent across days? (Write one sentence.)
5. **Pairplot for EDA:** `sns.pairplot(tips[["total_bill", "tip",
   "size"]], diag_kind="kde")` — name one pair with the clearest
   relationship and one with the weakest.
6. **Style pass:** set `sns.set_theme(style="whitegrid")` at the top, and
   add titles via `plt.title` on the two single-axes plots.

## Starter code

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")

tips = sns.load_dataset("tips")
tips["tip_pct"] = tips["tip"] / tips["total_bill"] * 100

# Q1: relplot with hue="time", style="smoker"
# your code here

# Q2: boxplot of tip_pct by day
# your code here

# Q3: correlation heatmap with annotations
# your code here

# Q4: catplot bar, hue="smoker"
# your code here

# Q5: pairplot
# your code here
```

## Expected output

- Q1: a relplot with both `time` and `smoker` encoded; points overlap a
  lot but the positive trend is visible in both meals.
- Q2: a boxplot; Thursday's median `tip_pct` is highest (≈ 27%),
  Sunday's lowest (≈ 18%) — the *opposite* of the raw-tip ranking, which is
  the point.
- Q3: heatmap with numbers; `total_bill` correlates with `tip` at ≈ 0.68.
- Q4: a bar plot showing smokers tip slightly less per meal on most days.
- Q5: pairplot with 3×3 grid; `total_bill`–`tip` clearest, `size` pairs
  weakest (mostly discrete).

## Questions

1. Why use `tip_pct` instead of raw `tip` when comparing days?
2. What does `hue` add to a plot that color alone cannot?
3. A heatmap shows correlation 0.68 between bill and tip. Does that mean
   bill *causes* tip? Explain.
4. What is the difference between a boxplot and a violin plot?
5. When is a pairplot a bad idea (think: dataset size)?

## Challenge task

Repeat Q2 with **penguins**: build `sns.boxplot(data=penguins,
x="species", y="body_mass_g", hue="sex")`. Then add `dodge=False` and note
how the interpretation changes. Finally, write one sentence: which plot
would you show a non-technical manager, and why?

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Q1 relplot correct + interpretation | 4 | hue+style, sentence |
| Q2 boxplot + tip_pct rationale | 4 | correct day, reasoning |
| Q3 heatmap + correlation report | 3 | 0.68 stated |
| Q4 catplot + reading | 3 | sentence on smoker gap |
| Q5 pairplot pairs named | 3 | strongest + weakest |
| Style pass | 2 | theme + titles |
| Answers to questions | 3 | Q1, Q3, Q4 correct |
| Challenge: penguins boxplot | 4 | hue, dodge note, sentence |
| **Total** | **26** | |