# Lab 17 — Introduction to Machine Learning

**Session:** Week 9 · Session 17 · 90 min
**CLO:** CLO-2
**Difficulty:** Intermediate

## Learning objectives

By the end of this lab you can:

1. Frame a problem as supervised regression or classification.
2. Split data with `train_test_split` and explain why.
3. Fit and evaluate a first scikit-learn model (the 4-step API).
4. Compute a baseline and judge a model against it.

## Problem statement

The tips data returns, but now as a **prediction** problem: "given a
party's total bill and size, how much will they tip?" You must build the
full Module B skeleton — split, fit, predict, evaluate — and answer the
honest question: is the model actually better than just predicting the
average tip?

## Dataset requirements

Seaborn built-in `tips` (244 rows). Use `total_bill` + `size` as features,
`tip` as target.

## Step-by-step tasks

1. **Frame:** write one markdown line: is this supervised or unsupervised?
   Regression or classification? Why?
2. **Features/target:** `X = tips[["total_bill", "size"]]`, `y = tips["tip"]`.
   Comment on why `X` is 2-D and `y` 1-D.
3. **Split:** `train_test_split(X, y, test_size=0.2, random_state=42)`.
   Print the four shapes and verify
   `len(X_train) == 0.8 * len(tips)`.
4. **Model:** `LinearRegression()`; fit on train; predict on test.
5. **Evaluate:** `mean_absolute_error(y_test, pred)` and
   `np.sqrt(mean_squared_error(y_test, pred))`. Print both rounded.
6. **Baseline:** predict the mean of `y_train` for every test row; compute
   its MAE. Report both MAEs side by side and the % improvement.
7. **Coefficients:** `pd.Series(model.coef_, index=X.columns)` — which
   feature matters more per unit? Explain what the `size` coefficient means
   in plain words.

## Starter code

```python
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

tips = sns.load_dataset("tips")

X = tips[["total_bill", "size"]]
y = tips["tip"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

print("train:", X_train.shape, "test:", X_test.shape)

# your code here: fit, predict, evaluate, baseline, coefficients
```

## Expected output

- `train: (195, 2) test: (49, 2)`.
- Model MAE ≈ 0.67–0.70; RMSE ≈ 0.90–0.95 (approx — record yours).
- Baseline MAE ≈ 1.03–1.08; the model is ~33–38% better than baseline.
- Coefficients: `total_bill` ≈ 0.09, `size` ≈ 0.19 — every extra person
  adds roughly $0.19 in tip (holding bill constant).
- A markdown line answering task 1.

## Questions

1. Why do we fit on `X_train` but evaluate on `X_test`?
2. What is `random_state=42` doing, and what happens if you remove it?
3. MAE vs RMSE: when is the difference between them informative?
4. Why is "predict the mean" called the *baseline* and not just "a simple
   model"?
5. A test MAE of $0.68 — good or bad? What do you need to know to judge?

## Challenge task

Change the feature set to **only** `total_bill` and re-run the whole
pipeline. Compare the two models' MAEs and their improvement over
baseline. Write one sentence: is `size` worth keeping? (Later labs will
formalize this with pipelines and cross-validation.)

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Problem framing (supervised/regression + why) | 3 | markdown, correct |
| Split + shapes verified | 3 | 195/49, proportion check |
| Fit/predict/evaluate | 4 | correct API, metrics |
| Baseline + improvement % | 4 | both MAEs + math |
| Coefficients interpreted | 3 | size ≈ 0.19 explained |
| Answers to questions | 3 | Q1, Q2, Q5 correct |
| Challenge: one-feature comparison | 4 | MAE comparison + verdict |
| **Total** | **24** | |