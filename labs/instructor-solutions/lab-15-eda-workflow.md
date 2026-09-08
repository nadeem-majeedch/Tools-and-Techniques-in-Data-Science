# Lab 15 — Solution: EDA Workflow

**Session:** W8 S15 · **CLO:** CLO-1

## Complete solution

```python
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")
penguins = sns.load_dataset("penguins")

# S1 overview
print(penguins.shape)            # (344, 7)
print(penguins.info())
print(penguins.describe())
print(penguins.head())

# S2 quality
print(penguins.isna().sum())
# species 0, island 0, bill_length 2, bill_depth 2, flipper 2,
# body_mass 2, sex 11
clean = penguins.dropna()
print("after dropna:", clean.shape)   # (333, 7)

# S3 univariate
for col in ["bill_length_mm", "body_mass_g"]:
    print(col, "mean", clean[col].mean().round(1),
          "median", clean[col].median().round(1),
          "std", clean[col].std().round(1))
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
clean["bill_length_mm"].hist(ax=axes[0], bins=25, edgecolor="white")
axes[0].set_title("Bill length")
clean["body_mass_g"].hist(ax=axes[1], bins=25, edgecolor="white")
axes[1].set_title("Body mass")
# both histograms are bimodal (two peaks) — the data mixes ~3 species.

# S4 bivariate
sns.boxplot(data=clean, x="species", y="body_mass_g")
plt.title("Body mass by species")
print(clean.groupby("species")["body_mass_g"].median())

sns.scatterplot(data=clean, x="bill_length_mm", y="bill_depth_mm",
                hue="species")
plt.title("Bill length vs depth by species")

plt.figure(figsize=(7, 6))
sns.heatmap(clean.select_dtypes("number").corr(), annot=True, cmap="coolwarm")
```

## Expected output

- Gentoo median mass ≈ 5050 g vs Adelie ≈ 3700 g, Chinstrap ≈ 3700 g.
- bill length vs depth separates all three species cleanly (three blobs);
  mass alone separates Gentoo only.
- Correlations: flipper–mass ≈ 0.87, bill_length–mass ≈ 0.59,
  bill_length–bill_depth ≈ −0.24.

## Sample insight bullets (Section 5)

- **Gentoo penguins are the heaviest** — median body mass ≈ 5,050 g vs
  ≈ 3,700 g for both other species (boxplot, Section 4).
- **Bill shape separates all three species** — bill length vs. depth forms
  three non-overlapping clusters (scatter, Section 4).
- **Flipper length is the single best mass proxy** — correlation ≈ 0.87,
  the strongest in the heatmap (Section 4).

## Model answers

1. **select_dtypes("number")** — `.corr()` computes pairwise Pearson
   correlation, which needs numeric columns; calling it on the whole frame
   would choke on the object columns (species, island, sex) or silently
   drop them.
2. **describe() hides missing** — it summarizes the *present* values; nulls
   are excluded by design, so a 90%-missing column can still show a
   plausible mean — which is why `isna().sum()` is a separate, mandatory
   step.
3. **Bimodality** — two peaks in one distribution; it hints that the
   sample is a mixture (here: multiple species with different sizes).
4. **Correlation 0.59** — it quantifies linear co-movement only; it says
   nothing about causation, nonlinear relationships, or which species drive
   the trend (Simpson's-paradox territory).
5. **Order** — shape → quality → univariate → bivariate → insights;
   quality first because plots and stats are meaningless on dirty data
   (and missingness itself is a finding).

## Challenge solution

```python
sns.scatterplot(data=clean, x="bill_length_mm", y="bill_depth_mm",
                hue="island")
print(pd.crosstab(clean["island"], clean["species"]))
# island × species is nearly one-to-one (Dream has Adelie+Chinstrap,
# Biscoe has Adelie+Gentoo, Torgersen only Adelie) — so "island" mostly
# repeats the species pattern.
```