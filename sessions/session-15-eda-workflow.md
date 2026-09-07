# Session 15 — The EDA Workflow

**Week 8 · Session 15 · Module A · 90 min · CLO-1**

## 1. Learning objectives

By the end of this session, students can:
- Explain what EDA is and why it precedes modeling.
- Run a systematic EDA: shape/quality check → univariate summaries → relationships → written findings.
- Compute and interpret summary statistics (`describe`, grouped stats) and correlations.
- Turn every finding into a written, non-obvious insight with chart or table evidence.
- Structure an EDA notebook that a colleague can follow.

## 2. Key concepts

- **EDA = asking questions of the data before modeling**, guided by summaries and plots.
- The **EDA loop:** look → question → analyze → question again. The analysis *generates* the next question.
- **Univariate first, bivariate second:** each variable alone, then pairs/triples.
- **Every insight needs evidence:** a number *and* a chart *and* a sentence.
- **Correlation describes association, not causation** — the most abused concept in the field.
- EDA is where cleaning mistakes and data quirks surface — it validates Sessions 9–12.

## 3. Detailed lecture notes

**Why EDA?** You don't model data you haven't met. EDA is the conversation with
the dataset: what's here, what's weird, what's interesting? It catches problems
(models trained on dirty data silently fail), generates hypotheses (which
features matter?), and shapes the modeling plan (Sessions 17–22). The worst
professional failure mode is skipping EDA and shipping a model that "worked"
on nonsense. EDA is also the majority of the final project's first half.

**The workflow — a repeatable recipe.** Teach it as a fixed sequence so students
never stare at a blank notebook:
1. **Orientation:** `df.info()`, `df.shape`, `df.head()`, `df.dtypes` — what's the table, and is it what you expected?
2. **Quality:** `isna().sum()`, `duplicated().sum()` — any cleaning debt from Sessions 9–10?
3. **Univariate:** `describe()` for numerics; `value_counts()` for categories; histograms/boxplots for shape; check for outliers and implausible values (negative prices? 200-year-old students?).
4. **Bivariate:** scatter/correlation for numeric pairs; `groupby` means and boxplots across categories; heatmap of `corr()`.
5. **Synthesis:** write 3–5 findings as sentences, each backed by a chart or number. Findings should be *non-obvious* ("weekend bills are higher" beats "bills vary").

**Summary statistics — what to read.** `describe()` gives count, mean, std, min,
quartiles, max. Read it for: scale (mean vs median — skew), spread (std, IQR),
implausible extremes. The mean vs. median gap is the first clue of skewness;
the histogram confirms. `groupby` summaries turn categories into comparisons.
Correlation: Pearson's r ranges -1..1; |r| > 0.7 strong, 0.3–0.7 moderate, below
weak — *for linear relationships only*. Always pair correlation with a scatter
(Anscombe's quartet from Session 13 — nonlinear patterns hide from r).

**The written insight.** EDA is judged by what you *conclude*, not how many
charts you made. The format: "**Finding:** weekend tips average 18% vs. 15% on
weekdays. **Evidence:** boxplot by day, mean table. **Implication:** consider a
weekend/day feature in modeling." This finding→evidence→implication trio is the
grading rubric for the EDA component of labs and the project.

**Correlation vs. causation.** One rule repeated loudly: ice cream sales and
drowning deaths correlate because both rise in summer — the *third variable*
explains both. An EDA finding is a *hypothesis*, not proof; experiments or
careful causal methods (beyond this course) establish cause. This discipline
matters doubly in the AI era (Session 30: models can find spurious patterns at
scale).

## 4. Important terminology

- **EDA** — Exploratory Data Analysis: summarizing and visualizing before modeling.
- **Univariate / bivariate** — one variable / two variables at a time.
- **`describe()`** — count, mean, std, min, quartiles, max of numeric columns.
- **Outlier** — a value far outside the typical range (needs scrutiny, not deletion).
- **Correlation (Pearson r)** — linear association strength/direction, -1..1.
- **Skew** — asymmetric distribution; mean pulled toward the long tail.
- **Quartiles / IQR** — 25/50/75th percentiles; IQR = Q3 − Q1 (boxplot anatomy).
- **Hypothesis** — a candidate explanation to test later.
- **Spurious correlation** — association driven by a third variable or chance.
- **Finding → evidence → implication** — the structure of every EDA conclusion.

## 5. Python examples

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

tips = sns.load_dataset("tips")

# --- 1. Orientation & quality ---
print(tips.info())
print(tips.isna().sum(), tips.duplicated().sum())

# --- 2. Univariate ---
print(tips.describe().round(2))
print(tips["day"].value_counts())

# --- 3. Bivariate ---
print(tips.groupby("day")["total_bill"].mean().round(2))
print(tips[["total_bill", "tip", "size"]].corr().round(2))

fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=tips, x="day", y="total_bill", ax=ax)
ax.set_title("Bill size by day")
plt.show()
```

## 6. Beginner example

```python
import pandas as pd

scores = pd.Series([45, 62, 70, 75, 82, 88, 95, 99])
print(scores.describe())
# count 8.00 | mean 77.0 | std 17.3 | min 45 | 25% 68 | 50% 78.5 | 75% 89.5 | max 99
```

One command, the whole shape of a variable. Everything else in EDA is asking
this question repeatedly, one variable at a time.

## 7. Practical Data Science example

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

penguins = sns.load_dataset("penguins").dropna()

# Full mini-EDA following the recipe
print(penguins.shape, penguins["species"].value_counts().to_dict())

# Finding 1: bill length differs strongly by species
print(penguins.groupby("species")["bill_length_mm"].mean().round(1))
sns.boxplot(data=penguins, x="species", y="bill_length_mm")
plt.title("Finding 1: Gentoo bills are clearly longer")
plt.show()

# Finding 2: bill length and flipper length move together (r ~ 0.65)
print(round(penguins[["bill_length_mm", "flipper_length_mm"]].corr().iloc[0, 1], 2))
sns.scatterplot(data=penguins, x="bill_length_mm", y="flipper_length_mm", hue="species")
plt.title("Finding 2: larger penguins have longer bills and flippers")
plt.show()

# Synthesis (markdown cell):
# "Finding 1: Gentoo penguins average ~47 mm bills vs ~39 mm for the others.
#  Finding 2: bill and flipper length correlate (r≈0.65) and together
#  separate the species — a promising feature pair for Session 19's model."
```

## 8. In-class activity (50 min)

The **EDA case study** — each student runs the recipe on **their own dataset**
(brought per Session 1's homework; fallback: `tips` or `penguins`) in
`notebooks/week-08/session-15-eda-workflow.ipynb`:

1. **Recipe pass (25 min):** orientation → quality → univariate (describe +
   one histogram) → bivariate (one groupby comparison + one scatter or heatmap).
2. **Three findings (15 min):** write three finding→evidence→implication
   sentences in markdown, each citing a printed number and a chart.
3. **Peer check (10 min):** swap notebooks with a partner; partner must be able
   to state your main finding from reading your markdown alone.

## 9. Lab exercise

**Assignment 1 is due today** (`../assignments/assignment-01`): Pandas cleaning +
manipulation on the provided dataset — clean, reshape, analyze, and answer
questions with evidence. Push to your repo. (No new lab this session; the case
study above is the graded-by-participation work.)

## 10. Common mistakes

- Jumping to `corr()` before checking for missing values and outliers → misleading numbers.
- Reading `describe()` without looking at histograms → missing skew and bimodality.
- Listing 20 charts with zero written findings → an EDA is judged by conclusions.
- Claiming causation from correlation (e.g., "tips cause larger bills").
- Fixating on one interesting chart and skipping the rest of the data.
- Treating outliers as errors — investigate *why* before deciding.
- Not stating units and context in findings ("average is higher" — than what?).

## 11. Short assessment questions

1. What are the five steps of the EDA recipe (in order)?
2. What does `describe()` show, and what is one thing it *can't* show? (Distribution shape.)
3. r = 0.9 between X and Y. Can you conclude X causes Y? Why not?
4. Why is the mean vs. median gap a clue about skew?
5. Write a finding sentence about a dataset in this course using the finding→evidence→implication structure.
6. When in the workflow do you check for missing values, and why there?

## 12. CLO mapping

CLO-1: EDA is the capstone of Module A — "explore datasets" with the full
toolchain (acquisition, cleaning, manipulation, visualization). The findings
discipline directly transfers to Assignment 1's questions and the final
project's exploration section.

## 13. Suggested homework

- Polish the case-study notebook; commit it.
- Read: *The Art of Data Science* chapter on EDA (Peng & Matsui) — the "explore" chapter.
- Practice: run the recipe on a dataset you haven't seen before (e.g., `planets` from seaborn); write two findings.
- Prepare: review Sessions 1–15 — the **midterm (Session 16)** covers CLO-1 end-to-end (written + practical notebook task).