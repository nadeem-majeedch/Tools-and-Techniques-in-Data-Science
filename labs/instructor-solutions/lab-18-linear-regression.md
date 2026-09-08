# Lab 18 — Solution: Linear Regression

**Session:** W9 S18 · **CLO:** CLO-2

## Complete solution

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
    return (round(r2_score(y_train, model.predict(X_train)), 3),
            round(r2_score(y_test, model.predict(X_test)), 3),
            round(mean_absolute_error(y_test, model.predict(X_test)), 1))

f1 = ["flipper_length_mm"]
f2 = f1 + ["bill_length_mm"]
f3 = f2 + ["bill_depth_mm"]
for feats in (f1, f2, f3):
    print(feats, "->", evaluate(feats))

# linearity check
sns.regplot(data=penguins, x="flipper_length_mm", y="body_mass_g")
plt.title("Flipper length vs body mass")

# residuals for the best (3-feature) model
X = penguins[f3]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=7)
model = LinearRegression().fit(X_train, y_train)
resid = y_test - model.predict(X_test)
print("residual mean:", round(resid.mean(), 1),
      "std:", round(resid.std(), 1))

# coefficient sentence
print("flipper coef:", round(model.coef_[0], 1))   # ~+50 g per mm
```

## Expected output

- f1: train R² ≈ 0.79, test R² ≈ 0.76, MAE ≈ 281.
- f2: test R² ≈ 0.78, MAE ≈ 279 (small gain).
- f3: test R² ≈ 0.78, MAE ≈ 280 (no real gain — depth adds nothing).
- Train–test gaps small (≤ 0.03) → no strong overfitting.
- Residual mean ≈ 0, std ≈ 260 g.
- Flipper coefficient ≈ 48–52 g per mm.

## Model answers

1. **R² = 0.76** — 76% of the variance in body mass is explained by the
   model's features (on that set); 24% is left to noise/unmodeled factors.
2. **Test R² for selection** — train R² rewards complexity (it always
   rises when you add features); test R² shows whether the added feature
   generalizes to unseen data.
3. **Train up / test down** — overfitting: the extra feature fits noise
   in the training data that isn't present in the test set.
4. **Residual mean ≈ 0** — indicates no *systematic* bias (errors cancel),
   but it says nothing about magnitude (std), linearity, or whether a
   different model would do better.
5. **No causation** — correlation/regression on observational data can't
   rule out confounders (species, age, sex drive both flipper length and
   mass).

## Challenge solution

```python
dummies = pd.get_dummies(penguins[["species"]], drop_first=True)
X4 = pd.concat([penguins[f3], dummies], axis=1)
print("with species:", evaluate(list(X4.columns)))
# Species dummies add real signal (test R² ≈ 0.82-0.85): species captures
# group differences the measurements alone compress into one slope.
```