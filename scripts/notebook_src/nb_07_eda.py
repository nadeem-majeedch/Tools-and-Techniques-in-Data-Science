# Content for notebook 07: EDA.
CELLS = [
    ("md", """# 07 — Exploratory Data Analysis (EDA)

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-1 — Explore datasets.

EDA is the *conversation with your data* before modeling: what's here, what's
weird, what's interesting? It catches problems, generates hypotheses, and
decides the modeling plan. This notebook teaches one repeatable recipe.

---
"""),
    ("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Run a systematic EDA: orientation → quality → univariate → bivariate → synthesis.
2. Read summary statistics and detect skew, outliers, and implausible values.
3. Interpret correlations — including their limits.
4. Turn findings into **finding → evidence → implication** statements.
5. Structure an EDA notebook a colleague can follow.

---
"""),
    ("md", """## Theory: the EDA recipe

1. **Orientation** — `info()`, `shape`, `head()`, `dtypes`: what is this table?
2. **Quality** — `isna().sum()`, `duplicated().sum()`: any cleaning debt?
3. **Univariate** — `describe()`, `value_counts()`, histograms: each variable alone.
4. **Bivariate** — `groupby`, scatter, `corr()`, boxplots: pairs of variables.
5. **Synthesis** — 3–5 written findings, each with evidence.

The analysis *generates* the next question — EDA is a loop, not a checklist.
And remember Session 15's law: **correlation is not causation**.

---
"""),("code", """import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

%matplotlib inline

penguins = sns.load_dataset("penguins")
print("Loaded penguins:", penguins.shape)
"""),
    ("md", """## Step 1–2: Orientation and quality

---
"""),("code", """print(penguins.info())
print()
print("Missing values per column:")
print(penguins.isna().sum())
print()
print("Duplicate rows:", penguins.duplicated().sum())
"""),
    ("md", """## Step 3: Univariate analysis

`describe()` gives count, mean, std, min, quartiles, max. Read it for:
**scale** (mean vs median → skew), **spread** (std, IQR), and **implausible
extremes** (negative prices? impossible heights?).

---
"""),("code", """print(penguins.describe().round(2))
print()
print(penguins["species"].value_counts())
print()
print(penguins["island"].value_counts())

# A histogram reveals the shape describe() cannot show
fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(data=penguins.dropna(), x="body_mass_g", bins=25, kde=True)
ax.set_title("Distribution of penguin body mass")
plt.show()
"""),
    ("md", """## Step 4: Bivariate analysis

Two questions dominate: *do categories differ?* (groupby + boxplot) and *do
variables move together?* (correlation + scatter).

---
"""),("code", """clean = penguins.dropna()

# Categories differ? Body mass by species
print(clean.groupby("species")["body_mass_g"].mean().round(0))
sns.boxplot(data=clean, x="species", y="body_mass_g")
plt.title("Body mass by species")
plt.show()

# Variables move together? Correlation heatmap
corr = clean[["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlations among penguin measurements")
plt.show()
"""),
    ("md", """## Correlation: what it can and cannot tell you

Pearson's r runs from -1 (perfect negative) to +1 (perfect positive); near 0
means no *linear* relationship. Rules of thumb: |r| > 0.7 strong, 0.3–0.7
moderate, below weak. Two limits to state out loud:

1. Correlation only sees *linear* patterns (Anscombe's quartet — four very
   different datasets with identical r).
2. Correlation ≠ causation: a third variable may drive both (ice cream sales
   and drownings both rise in summer).

---
"""),("code", """r = clean["bill_length_mm"].corr(clean["body_mass_g"])
print("corr(bill_length, body_mass) =", round(r, 2))

# Always pair the number with a scatter
sns.scatterplot(data=clean, x="bill_length_mm", y="body_mass_g", hue="species")
plt.title("Bill length vs body mass — the correlation in context")
plt.show()
"""),
    ("md", """## Beginner example: one variable, the full treatment

The recipe for a *single* column — every EDA is this, repeated.

---
"""),("code", """col = clean["flipper_length_mm"]

print(col.describe().round(1))
print("Skew check — mean vs median:", round(col.mean(), 1), "vs", col.median())

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
sns.histplot(col, kde=True, ax=axes[0])
sns.boxplot(x=col, ax=axes[1])
plt.tight_layout()
plt.show()
"""),
    ("md", """## Intermediate example: full EDA on a new dataset

Run the whole recipe on the `tips` dataset, then write the synthesis. This is
the exact structure expected in the course's EDA case study.

---
"""),("code", """tips = sns.load_dataset("tips")

# 1-2. Orientation & quality
print(tips.info())
print("missing:", tips.isna().sum().sum(), "| duplicates:", tips.duplicated().sum())

# 3. Univariate
print(tips.describe().round(2))
print(tips["day"].value_counts())

# 4. Bivariate
print(tips.groupby("day")["total_bill"].mean().round(2))
print(tips[["total_bill", "tip", "size"]].corr().round(2))

sns.boxplot(data=tips, x="day", y="total_bill")
plt.title("Bill size by day")
plt.show()
"""),
    ("md", """## The synthesis: finding → evidence → implication

An EDA is judged by its conclusions, not its chart count. The format:

> **Finding:** weekend bills average ~$21 vs ~$17 on weekdays.
> **Evidence:** boxplot above; groupby means.
> **Implication:** a day-of-week feature is worth testing in a model (notebook 11).

Write 3–5 of these. Each must cite a printed number and a chart. (Fill in
your own findings for the exercises below.)

---
"""),("code", """# A model finding, written as markdown in a real notebook:
# "Finding: bill size and tip correlate strongly (r = 0.68), but the
#  relationship is noisier for small bills.
#  Evidence: heatmap value 0.68 + the scatter above.
#  Implication: total_bill will be the strongest feature in a tip predictor."
"""),
    ("md", """## Exercises

---
"""),
    ("md", """### Exercise 1 — Quality check

On `penguins`: how many rows have missing values in **any** column? Which
single column has the most missing values?"""),
    ("code", """# your code here
"""),
    ("code", """# Solution
print("rows with any missing:", penguins.isna().any(axis=1).sum())
print(penguins.isna().sum().sort_values(ascending=False).head(1))
# Expected output:
#   rows with any missing: 11
#   sex    11
#   dtype: int64
"""),
    ("md", """### Exercise 2 — Univariate reading

Run `describe()` on `penguins["body_mass_g"]` (drop missing first). Is the
distribution skewed? How do you know?"""),
    ("code", """# your code here
"""),
    ("code", """# Solution
s = penguins["body_mass_g"].dropna()
print(s.describe().round(0))
print("mean:", round(s.mean(), 0), "median:", s.median(),
      "-> mean slightly above median, mild right skew")
"""),
    ("md", """### Exercise 3 — Bivariate

Compute the correlation between `bill_depth_mm` and `body_mass_g`; is it
strong? What does its sign mean? (Answer: r ≈ -0.47 — a moderate negative:
deeper bills tend to come with lighter bodies.)"""),
    ("code", """# your code here
"""),
    ("code", """# Solution
r = clean["bill_depth_mm"].corr(clean["body_mass_g"])
print("corr =", round(r, 2))
"""),
    ("md", """## Challenge exercise

Run the full EDA recipe on `sns.load_dataset("planets")` (exoplanet
discoveries — columns like `method`, `year`, `orbital_period`, `mass`):

1. Orientation + quality (note: this dataset is much messier than penguins).
2. Univariate: distribution of `year` (a histogram); `value_counts()` of `method`.
3. Bivariate: does `mass` differ by `method`? (groupby + boxplot).
4. Synthesis: write **two** finding → evidence → implication statements."""),
    ("code", """import seaborn as sns
planets = sns.load_dataset("planets")

# your code here
"""),
    ("md", """## Recap

- EDA recipe: orientation → quality → univariate → bivariate → synthesis.
- `describe()` + histograms for single variables; `groupby`/boxplot/corr for pairs.
- Correlation: linear only, and never causation.
- Findings need the trio: **finding → evidence → implication**.
- The analysis generates the next question — iterate.

---
"""),
    ("md", """## Questions

1. What are the five steps of the EDA recipe?
2. What does `describe()` show, and what can't it show?
3. r = 0.9 between X and Y. Can you conclude X causes Y? Why not?
4. Why is the mean vs median gap a skew clue?
5. Write a finding about `tips` in finding → evidence → implication form.
6. When in the recipe do you check missing values, and why there?

---
**Next:** notebook 08 — Git/GitHub workflow.
"""),
]