# Lab 18 — Linear Regression & Evaluation

**Session:** Week 9 · Session 18 · 90 min
**CLO:** CLO-2
**Difficulty:** Intermediate

## Learning objectives

By the end of this lab you can:

1. Fit single- and multiple-feature linear regression models.
2. Interpret R², MAE, RMSE, and coefficients honestly.
3. Spot overfitting symptoms (train ≫ test performance).
4. Judge whether a relationship is truly linear.

## Problem statement

The penguins team wants a mass predictor. You will fit regression models
with 1, 2, and 3 features, report R² and MAE on a held-out test set for
each, and — critically — **explain the numbers**: which feature earns its
place, and whether adding features is actually helping or just fitting
noise.

## Dataset requirements

Seaborn built-in `penguins`, `dropna()` (333 rows). Target:
`body_mass_g`. Features to try: `flipper_length_mm`, `bill_length_mm`,
`bill_depth_mm`.

## Step-by-step tasks

1. **Prep:** `penguins = sns.load_dataset("penguins").dropna()`; build
   feature lists `f1 = ["flipper_length_mm"]`, `f2 = f1 +
   ["bill_length_mm"]`, `f3 = f2 + ["bill_depth_mm"]`.
2. **Helper function** `evaluate(features)` that splits (test_size=0.25,
   random_state=7), fits, and returns `(R² test, MAE test, R² train)`.
   Call it for all three feature sets and print a small comparison table
   (feature set → R² train, R² test, MAE test).
3. **Reading the table:**
   - Which single feature explains the most variance? (Compare R² test.)
   - Does adding `bill_depth_mm` improve test R²? By how much?
   - Is there any sign of overfitting (train R² much higher than test)?
4. **Linearity check:** scatter `flipper_length_mm` vs `body_mass_g` with a
   regression line (`sns.regplot`). Is the relationship plausibly linear?
   Name one place where points bend away from the line.
5. **Residual sanity check:** compute
   `residuals = y_test - model.predict(X_test)` for the best model and
   print `residuals.mean()` (should be near 0) and `residuals.std()`.
6. **Plain-language summary** (markdown): "A 1 mm longer flipper is
   associated with ≈ ___ g more mass, holding other features constant" —
   fill the blank from the best model's coefficient on
   `flipper_length_mm` (times 1 mm).

## Starter code

```python
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

penguins = sns.load_dataset("penguins").dropna()
y = penguins["body_mass_g"]

def evaluate(features):
    X = penguins[features]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=7)
    model = LinearRegression().fit(X_train, y_train)
    return (
        round(r2_score(y_train, model.predict(X_train)), 3),
        round(r2_score(y_test, model.predict(X_test)), 3),
        round(mean_absolute_error(y_test, model.predict(X_test)), 1),
    )

for features in (["flipper_length_mm"],
                 ["flipper_length_mm", "bill_length_mm"],
                 ["flipper_length_mm", "bill_length_mm", "bill_depth_mm"]):
    print(features, "->", evaluate(features))
# your code here for tasks 4-6
```

## Expected output

- Table: flipper-only ≈ R² test 0.75–0.77, MAE ≈ 275–300 g; adding
  bill_length_mm pushes R² to ≈ 0.76–0.79; adding bill_depth_mm changes
  little (≈ +0.00–0.01). Train vs test R² gap small (no strong
  overfitting).
- `regplot` shows a clear positive, roughly linear trend with more scatter
  at the heavy end.
- Residuals: mean ≈ 0 (within ±10 g), std ≈ 250–300 g.
- The "1 mm longer flipper ≈ +48–52 g" sentence with the actual number.

## Questions

1. What does R² = 0.76 mean in plain words?
2. Why compare **test** R² and not train R² when choosing features?
3. If adding a feature raises train R² but lowers test R², what is
   happening?
4. Residual mean ≈ 0 — is that a sign of a good model? What does it *not*
   prove?
5. Why can't you conclude "longer flippers *cause* more mass" from this
   regression?

## Challenge task

Add `species` as a **categorical** feature by encoding it yourself with
`pd.get_dummies(penguins[["species"]], drop_first=True)` and concatenating
with the numeric features. Re-run `evaluate` on the 4–5 feature set. Does
species add real test-set value? Write one sentence explaining the result.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Prep + helper function | 4 | correct split/seed/returns |
| Comparison table printed | 3 | three feature sets |
| Table reading (R² gains, overfitting) | 4 | numbers cited |
| regplot + linearity comment | 3 | trend + bend noted |
| Residual mean/std | 3 | near-zero mean |
| Coefficient sentence | 3 | number filled in |
| Answers to questions | 3 | Q2, Q4, Q5 correct |
| Challenge: dummies for species | 4 | encoded + verdict |
| **Total** | **27** | |