# Lab 30 — Ethics & Responsible AI

**Session:** Week 15 · Session 30 · 90 min
**CLO:** CLO-3
**Difficulty:** Advanced

## Learning objectives

By the end of this lab you can:

1. Audit a model for differential outcomes across groups.
2. Document data provenance and privacy decisions.
3. Apply the course AI-use disclosure policy to your own work.
4. Write a short responsible-AI section for the project report.

## Problem statement

The course's AI-use policy (see `assessment-plan.md`) requires disclosure
and verification. This lab makes it concrete: (1) run a **bias audit** on a
real model, (2) write the **data sheet** for your project dataset, (3)
draft your **AI disclosure** for the final report. A model that treats
groups differently is not automatically "wrong" — the skill is detecting
it and *reporting* it.

## Dataset requirements

Seaborn built-in `tips` (244 rows) for the audit; your own project dataset
for the data sheet.

## Step-by-step tasks

1. **Audit setup:** predict `tip` from `total_bill` with a
   `LinearRegression` (split, random_state=42). Then compute **mean
   absolute error by group**: `sex`, `smoker`, and `day` — for each group,
   MAE over the test rows in that group.
2. **Read the audit:** report the MAE spread (max group MAE − min group
   MAE) for each of the three groupings. Which grouping shows the largest
   gap? Write one sentence on whether you consider that a fairness problem
   here (small sample, descriptive task).
3. **Systematic check:** for the `sex` grouping, print a table of
   `mean_abs_error`, `n_test_rows` per group. Comment: can you trust a
   MAE computed on 3 test rows? (This is the sample-size trap.)
4. **Data sheet** (markdown) for your project dataset — one line each:
   - source and license,
   - who collected it and for what purpose,
   - what it does *not* contain (privacy: no personal identifiers?),
   - known limitations (missingness, bias in sampling, staleness).
5. **AI disclosure** (markdown): for your project work so far, list which
   steps used AI assistance (code generation, debugging, writing, analysis)
   and for each: what you verified yourself. Follow the disclosure template
   from `assessment-plan.md`.
6. **Privacy decision:** one paragraph: does your project handle personal
   data? If yes, what is your minimization plan (aggregates only,
   deletion after grading, local models)? If no, say so explicitly and
   justify.

## Starter code

```python
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

tips = sns.load_dataset("tips")
X = tips[["total_bill"]]
y = tips["tip"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
model = LinearRegression().fit(X_train, y_train)
test = X_test.copy()
test["tip"] = y_test
test["pred"] = model.predict(X_test)
test["abs_err"] = (test["tip"] - test["pred"]).abs()

for group in ["sex", "smoker", "day"]:
    table = test.groupby(group)["abs_err"].agg(["mean", "count"]).round(3)
    print("---", group)
    print(table)
```

## Expected output

- Three group MAE tables (sex: M/F; smoker: yes/no; day: 4 values) with
  `mean` and `count`.
- A stated spread per grouping and the largest gap identified.
- The sample-size comment: day groups have ~10–19 test rows, fine; but if
  any group had ≤ 3 rows, its MAE would be meaningless — state the rule.
- A 4-line data sheet, a disclosure table with ≥ 3 AI-use rows (each with a
  verification note), and a privacy paragraph.

## Questions

1. A model has MAE 0.60 for males and 0.80 for females. Is that proof of
   bias? What else do you need to check before claiming it?
2. Why does a small test group make its error metric unreliable?
3. What belongs in a data sheet that `df.describe()` cannot tell you?
4. Under the course policy, is it acceptable to use AI to fix a bug?
   What must you record?
5. "We only use public data, so privacy is not an issue." Why is this
   statement incomplete?

## Challenge task

Audit a **classifier** for label imbalance: train a `KNeighborsClassifier`
to predict `smoker` from `total_bill` and `tip`, and report accuracy **per
class** (use `classification_report`). Since non-smokers outnumber smokers,
check whether the model just predicts the majority class (compare with a
"predict always 'No'" baseline). Write two sentences: what the audit shows
and one thing you would do next (e.g., class weighting, different metric).

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Audit setup + 3 group tables | 5 | correct MAE by group |
| Gap analysis + fairness sentence | 4 | largest gap identified |
| Sample-size trap comment | 3 | rule stated |
| Data sheet (4 lines) | 4 | source/license/limits |
| AI disclosure (≥3 rows, verified) | 5 | template followed |
| Privacy paragraph | 3 | decision + justification |
| Answers to questions | 4 | Q1, Q2, Q5 correct |
| Challenge: classifier imbalance audit | 5 | per-class + baseline + next step |
| **Total** | **33** | |