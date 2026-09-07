# Session 14 — Seaborn: Statistical Visualization

**Week 7 · Session 14 · Module A · 90 min · CLO-1**

## 1. Learning objectives

By the end of this session, students can:
- Explain what Seaborn adds on top of Matplotlib: statistical defaults and data-frame-native API.
- Create `scatterplot`, `relplot`, `histplot`, `boxplot`, `barplot`, `countplot`, `heatmap`, and `pairplot`.
- Use `hue`, `col`, and `style` to encode extra variables in one figure.
- Interpret a boxplot and a correlation heatmap correctly.
- Move between the "wide" (Pandas/Matplotlib) and "long" (Seaborn) mental models.

## 2. Key concepts

- Seaborn speaks **data-frame-native**: `sns.histplot(data=df, x="tip")` — no manual extraction.
- **`hue`** adds a categorical third dimension by color in one line.
- Statistical plot types: boxplot (distribution by category), heatmap (correlations), pairplot (all scatter pairs).
- `relplot`/`catplot` are "faceting" super-functions: many small panels, one spec.
- Seaborn is built on Matplotlib — all Session 13 customization still applies (`ax.set_title`, `savefig`).
- Read plots for insight, not just decoration — every figure needs a written takeaway.

## 3. Detailed lecture notes

**Why Seaborn?** Matplotlib gives you the canvas; Seaborn gives you *statistical
thinking*: it computes aggregates (mean tip by day with error bars), handles
grouping via `hue`, and looks good by default. Its API matches how data actually
lives: long-form DataFrames with named columns — `data=df, x="col"` — so you stop
writing `df["col"]` extraction boilerplate. It's also the fastest path to the
charts EDA actually uses (boxplots, heatmaps, pairplots).

**The `hue` superpower.** One extra argument encodes a categorical variable by
color: `sns.scatterplot(data=tips, x="total_bill", y="tip", hue="day")` — three
variables, one figure. This is the *same* question-answering power you'd get
from looping subplots, without the loop. `col=` splits into separate panels;
`style=` changes markers. Show the same figure with `hue` vs. `col` so students
feel the difference (color = overlay; col = faceting).

**Distribution plots.** `histplot` (histogram; add `kde=True` for a smooth
curve), `kdeplot` (density alone — useful to overlay two groups),
`boxplot` (median, quartiles, whiskers, outliers — the workhorse for comparing
groups: `sns.boxplot(data=tips, x="day", y="tip")`), `violinplot` (box + density
— mention, don't dwell). Interpretation drill: read a boxplot out loud — median
line, box = middle 50%, whiskers, dots = outliers.

**Relationships at scale.** `sns.heatmap(df.corr(), annot=True, cmap="coolwarm")`
— the correlation matrix: -1..1, color-coded. Interpretation: strong positive
(diagonal red), strong negative (blue), near zero (white). Caveat: correlation ≠
causation, and numeric-only columns (drop/select non-numeric first).
`sns.pairplot(df, hue="species")` — every numeric pair as a scatter, distributions
on the diagonal: the single best "first look" at a small dataset. On `penguins`,
pairplot *reveals the species clusters* in one command — a memorable demo of why
EDA exists.

**Counts and bars.** `countplot` = `value_counts` as a chart;
`barplot` = aggregated statistic with error bars (mean ± CI by default — the
"aggfunc" behavior surprises people used to raw bars); `pointplot` for trends
across categories. When in doubt about what a bar's height means, check the docs.

**Tidiness.** Seaborn wants long-form data (Session 10). Wide tables need
`melt` first. This is the payoff of the reshaping lesson.

## 4. Important terminology

- **Data-frame-native API** — `data=df, x=..., y=...` argument style.
- **`hue`** — color-encode a third variable.
- **Faceting** — multiple panels per category (`col=`, `row=`).
- **Boxplot** — median, quartiles (box), whiskers, outliers (dots).
- **`pairplot`** — matrix of scatter plots + diagonal distributions.
- **Correlation matrix / `df.corr()`** — pairwise Pearson correlations.
- **Heatmap** — color grid of values (`annot=True` prints the numbers).
- **KDE** — smooth density estimate over a histogram.
- **`relplot` / `catplot`** — faceting wrappers for relational/categorical plots.
- **Long-form data** — tidy layout Seaborn expects.

## 5. Python examples

```python
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

tips = sns.load_dataset("tips")
penguins = sns.load_dataset("penguins")

# --- hue: three variables, one figure ---
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="day")
plt.title("Tip vs bill, colored by day")
plt.show()

# --- distribution by category ---
sns.boxplot(data=tips, x="day", y="tip")
plt.title("Tip distribution by day")
plt.show()

# --- counts ---
sns.countplot(data=tips, x="day", hue="sex")
plt.show()

# --- correlation heatmap ---
sns.heatmap(tips[["total_bill", "tip", "size"]].corr(),
            annot=True, cmap="coolwarm")
plt.title("Correlations in tips")
plt.show()

# --- pairplot: the first look ---
sns.pairplot(penguins, hue="species")
plt.show()          # 4x4 grid: distributions + all pairwise scatters
```

## 6. Beginner example

```python
import seaborn as sns

tips = sns.load_dataset("tips")
sns.histplot(data=tips, x="tip", kde=True)
```

One line, real insight (most tips are small; a long right tail). That's the
whole value proposition.

## 7. Practical Data Science example

```python
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

penguins = sns.load_dataset("penguins").dropna()

# Question: "Can we tell penguin species apart from measurements?"
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Panel 1: boxplot comparison
sns.boxplot(data=penguins, x="species", y="bill_length_mm", ax=axes[0])
axes[0].set_title("Bill length by species")

# Panel 2: scatter with hue — do two measurements separate the species?
sns.scatterplot(data=penguins, x="bill_length_mm", y="flipper_length_mm",
                hue="species", ax=axes[1])
axes[1].set_title("Measurements by species")

fig.tight_layout()
fig.savefig("charts/penguins-eda.png", dpi=150, bbox_inches="tight")

# Written takeaway (markdown cell):
# "Gentoo penguins have clearly longer bills and flippers — a scatter of
#  bill vs flipper length nearly separates the three species, which is
#  exactly what a classification model (Session 19) can exploit."
```

## 8. In-class activity (50 min)

In `notebooks/week-07/session-14-seaborn.ipynb`:

1. **hue drill (15 min):** recreate the scatter with `hue="day"`, then with
   `col="day"` — write which you prefer and why.
2. **Boxplot reading (10 min):** `sns.boxplot(data=tips, x="day", y="total_bill")`;
   describe the median, spread, and outliers of one day out loud.
3. **Heatmap (10 min):** compute `tips[["total_bill","tip","size"]].corr()`,
   heatmap it with `annot=True`; write the strongest correlation as a sentence.
4. **pairplot (15 min):** run `sns.pairplot(penguins.dropna(), hue="species")`;
   identify the two measurements that best separate species — this will matter
   in the ML module.

## 9. Lab exercise

**Lab 4 is due today** (`labs/lab-04/`): visualization — four chart types,
customized and saved, plus checkpoint questions on what the charts show.
Commit and push.

## 10. Common mistakes

- Passing a DataFrame where Seaborn expects columns and vice versa — always `data=df, x="col"`.
- Forgetting `hue` exists and writing manual group loops instead.
- Heatmapping a DataFrame with non-numeric columns → error; select numeric columns first.
- Reading `barplot` heights as raw values — they're *means with error bars* by default.
- `plt.show()` missing → faceting figures don't render inline.
- Pairplot on a 50-column frame → 2,500 tiny panels; keep it for small frames.
- Interpreting correlation > 0 as causation (the classic error — Session 15 reinforces this).

## 11. Short assessment questions

1. What does `hue="day"` do in `sns.scatterplot`?
2. Which plot type is best for comparing the *distribution* of tips across days? (Boxplot.)
3. In a heatmap of `df.corr()`, what does a value of -0.8 mean?
4. What does `sns.pairplot(df, hue="class")` produce?
5. Why does Seaborn need long-form data?
6. True/False: `sns.barplot` by default shows the mean with an error bar, not the raw values. (True.)

## 12. CLO mapping

CLO-1: Seaborn is the "visualize and explore" tool of CLO-1; these plots are the
vocabulary of the EDA case study (Session 15) and the final project. Reading
plots for real structure (species separation) is a preview of CLO-2's modeling.

## 13. Suggested homework

- Commit the activity notebook and any saved charts.
- Practice: redo the penguins exploration with `hue="sex"` instead of species; what new pattern appears?
- Read: Seaborn's tutorial intro (seaborn.pydata.org/tutorial.html) — sections on relational and categorical plots.
- Prepare: bring your own small dataset (from homework in Session 1) to Session 15 — you'll run a full EDA on it.