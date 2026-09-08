# Lab 14 — Solution: Seaborn

**Session:** W7 S14 · **CLO:** CLO-1

## Complete solution

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")

tips = sns.load_dataset("tips")
tips["tip_pct"] = tips["tip"] / tips["total_bill"] * 100

# Q1
sns.relplot(data=tips, x="total_bill", y="tip",
            hue="time", style="smoker", alpha=0.6)
plt.title("Bill vs tip by meal time and smoker status")

# Q2
plt.figure()
sns.boxplot(data=tips, x="day", y="tip_pct")
plt.title("Tip % by day")

# Q3
plt.figure(figsize=(6, 5))
sns.heatmap(tips[["total_bill", "tip", "size"]].corr(),
            annot=True, cmap="coolwarm")
plt.title("Correlations")

# Q4
sns.catplot(data=tips, x="day", y="tip", hue="smoker",
            kind="bar", ci=None)
plt.title("Mean tip by day and smoker status")

# Q5
sns.pairplot(tips[["total_bill", "tip", "size"]], diag_kind="kde")
```

## Expected output

- Q2: Thursday's median tip% highest (~27%), Sunday lowest (~18%) — the
  raw-tip ranking is reversed, which is the lesson.
- Q3: `total_bill`–`tip` ≈ 0.68; `size`–`tip` ≈ 0.49; `size`–`total_bill`
  ≈ 0.60.
- Q4: smokers tip slightly less per meal on most days; small gaps.
- Q5: bill–tip strongest; size pairs show discrete stripes (few distinct
  values).

## Model answers

1. **tip_pct not tip** — raw tip correlates with bill size, so bigger
  bills dominate; tip% controls for bill size and answers "who tips
  generously," which is the fair comparison across days.
2. **hue** — encodes a third variable by color AND automatically produces a
  legend, so the reader can split the data visually without extra code.
3. **Correlation ≠ causation** — 0.68 means linear association, not that
  bill causes tip; a lurking variable (party size, meal) could drive both.
4. **Boxplot vs violin** — boxplot shows quartiles/outliers compactly
  (robust, few numbers); violin shows the full distribution shape (peaks,
  multimodality) at the cost of density-estimation complexity.
5. **Pairplot limits** — it makes n×(n−1)/2 scatterplots: with many
  features it becomes unreadable and slow; use it only for small feature
  sets (≤ ~6).

## Challenge solution

```python
penguins = sns.load_dataset("penguins")
sns.boxplot(data=penguins, x="species", y="body_mass_g", hue="sex")
plt.title("Body mass by species and sex (default dodge)")

plt.figure()
sns.boxplot(data=penguins, x="species", y="body_mass_g",
            hue="sex", dodge=False)
plt.title("Same, dodge=False (hue as color only)")
# dodge=False overlaps the sex boxes within each species — comparison is
# harder; default dodge is clearer for side-by-side groups.
```

For a non-technical manager, the dodged boxplot: it needs no statistics
vocabulary and directly answers "which group weighs what."