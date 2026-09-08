# Lab 17 — Solution: Intro to ML

**Session:** W9 S17 · **CLO:** CLO-2

## Complete solution

```python
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

tips = sns.load_dataset("tips")

# Task 1 (markdown): supervised — rows have a known answer (tip).
# Regression — the answer is a continuous number, not a category.

X = tips[["total_bill", "size"]]   # 2-D: rows x features
y = tips["tip"]                    # 1-D: one value per row

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
print("train:", X_train.shape, "test:", X_test.shape)   # (195, 2) (49, 2)
print("proportion check:", round(len(X_train) / len(tips), 2))  # 0.8

model = LinearRegression()
model.fit(X_train, y_train)
pred = model.predict(X_test)

mae = mean_absolute_error(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))
print("model MAE:", round(mae, 3), "RMSE:", round(rmse, 3))

baseline_pred = np.full_like(y_test, y_train.mean())
base_mae = mean_absolute_error(y_test, baseline_pred)
print("baseline MAE:", round(base_mae, 3))
print("improvement: {:.0%}".format(1 - mae / base_mae))

coefs = pd.Series(model.coef_, index=X.columns).round(3)
print(coefs)                        # total_bill ~0.09, size ~0.19
```

## Expected output

- Model MAE ≈ 0.68, RMSE ≈ 0.91; baseline MAE ≈ 1.04; improvement ≈ 35%.
- Coefficients: total_bill ≈ 0.09, size ≈ 0.19 — an extra person adds
  ~$0.19 of tip with bill held constant.

## Model answers

1. **Fit train, evaluate test** — the test set simulates unseen future
   data; fitting on it (or tuning on it) leaks information and flatters
   the score.
2. **random_state=42** — fixes the random split so reruns give identical
   results; without it every run draws a different test set and the score
   jitters.
3. **MAE vs RMSE** — both measure error in target units; RMSE punishes
   large errors (squared), so when RMSE ≫ MAE, big mistakes dominate.
4. **Baseline = "simple"** — the mean prediction is the cheapest model
   that uses the target's own distribution; a model must beat it to prove
   it learned *any* signal.
5. **Judging $0.68** — you need context: the baseline (≈$1.04), the
   target's spread (tips range 1–10), and the business cost of an error.
   Absolute goodness doesn't exist without a comparison.

## Challenge solution

```python
for cols in [["total_bill"], ["total_bill", "size"]]:
    X1 = tips[cols]
    Xtr, Xte, ytr, yte = train_test_split(X1, y, test_size=0.2,
                                          random_state=42)
    m = LinearRegression().fit(Xtr, ytr)
    print(cols, "MAE:", round(mean_absolute_error(yte, m.predict(Xte)), 3))
# one-feature ≈ 0.70; two-feature ≈ 0.68 — size adds a little. Verdict:
# keep it (small but consistent gain, free to include).
```