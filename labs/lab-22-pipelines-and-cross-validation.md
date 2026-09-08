# Lab 22 — Pipelines & Cross-Validation

**Session:** Week 11 · Session 22 · 90 min
**CLO:** CLO-2
**Difficulty:** Intermediate

## Learning objectives

By the end of this lab you can:

1. Build a `Pipeline` that scales + models in one object.
2. Use `cross_val_score` and explain what it estimates.
3. Compare models fairly with CV instead of one lucky split.
4. Spot the difference between CV score and final test score.

## Problem statement

Until now every comparison used a single split — a one-roll-of-the-dice
estimate. This lab replaces that with 5-fold cross-validation, packaged in
a pipeline so scaling can never leak across folds. You will compare three
models (k-NN, logistic regression, decision tree) on penguins **with CV**,
then confirm the winner once on a held-out test set.

## Dataset requirements

Seaborn built-in `penguins`, `dropna()`. Features: all 4 numeric body
measurements. Target: `species`.

## Step-by-step tasks

1. **Prep:** dropna; hold out a test set FIRST:
   `X_train, X_test, y_train, y_test = train_test_split(X, y,
   test_size=0.2, random_state=42, stratify=y)`. Comment: why hold out
   before any fitting or CV?
2. **Pipeline factory** `make_model(kind)` returning a `Pipeline`:
   `[("scale", StandardScaler()), ("clf", <model>)]` for:
   - k-NN (k=5),
   - logistic regression (max_iter=1000),
   - decision tree (max_depth=4, random_state=42).
3. **CV comparison:** for each pipeline, run
   `cross_val_score(pipeline, X_train, y_train, cv=5)` and print
   `mean ± std` of the 5 scores. Build a small table.
4. **Winner:** pick the best mean CV score (tie-break by lower std, then
   simpler model). State the winner and margin in a sentence.
5. **Final check:** fit the winner on all of `X_train` and score on
   `X_test`. Compare with the CV estimate — they should be close (within a
   few points). Comment on any gap.
6. **Leakage note:** explain in one sentence how the pipeline prevents
   scaling leakage during CV (scaler is fit inside each fold).

## Starter code

```python
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

penguins = sns.load_dataset("penguins").dropna()
X = penguins[["bill_length_mm", "bill_depth_mm",
              "flipper_length_mm", "body_mass_g"]]
y = penguins["species"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

def make_model(kind):
    if kind == "knn":
        clf = KNeighborsClassifier(n_neighbors=5)
    elif kind == "logreg":
        clf = LogisticRegression(max_iter=1000)
    else:
        clf = DecisionTreeClassifier(max_depth=4, random_state=42)
    return Pipeline([("scale", StandardScaler()), ("clf", clf)])

# your code here: CV loop, table, winner, final test score
```

## Expected output

- Train/test split: 266 train / 67 test.
- CV table (approx, ±): k-NN 0.96–0.98, logistic 0.97–0.99, tree
  (depth 4) 0.95–0.97 — means + stds printed.
- Winner stated with margin (usually logistic regression or k-NN).
- Final test accuracy close to the CV mean (e.g., CV 0.97, test 0.97).
- A correct one-sentence leakage explanation.

## Questions

1. Why hold out the test set before doing anything else?
2. What exactly does `cross_val_score(..., cv=5)` compute, step by step?
3. Why is `mean ± std` a better comparison than a single split accuracy?
4. What would happen if the scaler were fit on `X_train + X_test` inside
   the pipeline?
5. CV score 0.97 but test score 0.88 — what are two possible explanations?

## Challenge task

Add a **4th model** — `RandomForestClassifier(n_estimators=100,
random_state=42)` — to the comparison. Then, for the winner, print the
per-fold scores themselves (set `cv=KFold(5, shuffle=True,
random_state=42)` and print each fold's score) instead of only the mean.
Write one sentence about what the spread across folds tells you.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Test set held out first | 3 | comment explains why |
| Pipeline factory (3 models) | 4 | scale inside pipeline |
| CV comparison table | 5 | mean ± std per model |
| Winner + margin sentence | 3 | correct pick |
| Final test check + gap comment | 4 | close to CV |
| Leakage explanation | 3 | correct mechanism |
| Answers to questions | 3 | Q2, Q4, Q5 correct |
| Challenge: random forest + per-fold scores | 5 | both done + sentence |
| **Total** | **30** | |