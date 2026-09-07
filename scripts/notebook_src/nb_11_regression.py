# Content for notebook 11: Regression.
CELLS = [
    ("md", """# 11 — Regression

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-2 — Apply basic machine learning techniques.

Regression predicts a **number** from features. Its superpower is
**interpretability**: the model is a weighted sum you can read — "each extra
study hour adds ~6 points, all else equal." This notebook covers fitting,
reading coefficients, and the three evaluation metrics.

---
"""),("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Explain a linear model: `y = intercept + slope1*x1 + slope2*x2 + ...`.
2. Fit linear regression with scikit-learn.
3. Interpret coefficients and the intercept (with their limits).
4. Evaluate with MAE, RMSE, and R² — and say what each means.
5. Check residuals and decide whether the model is trustworthy.

---
"""),("md", """## Theory: the linear model in words

A linear model says: *the target is a weighted sum of the features, plus
noise*. Two parts to read:

- **Intercept** — the prediction when all features are 0.
- **Coefficient** — "one more unit of this feature changes the prediction by
  this much, all else equal" (*ceteris paribus*).

Fitting finds the coefficients that minimize the sum of squared errors
(ordinary least squares). Why squared? Big errors get punished
disproportionately, and the math is clean.

---
"""),("code", """import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

%matplotlib inline

# Reproducible dataset: score = 40 + 6*hours + noise
np.random.seed(7)
n = 300
df = pd.DataFrame({"hours": np.random.uniform(1, 10, n)})
df["score"] = 40 + 6 * df["hours"] + np.random.normal(0, 5, n)

X = df[["hours"]]
y = df["score"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression().fit(X_train, y_train)
y_pred = model.predict(X_test)

print("intercept:", round(model.intercept_, 2))
print("coefficient (hours):", round(model.coef_[0], 2))
"""),
    ("md", """## Metrics: three lenses on the same model

- **MAE** — average absolute error. Same units as the target. "Off by ~4
  points on average." Easy to explain to non-technical people.
- **RMSE** — root mean squared error. Same units, but penalizes big errors
  more. RMSE >= MAE always; a big gap means a few large misses.
- **R²** — share of variance explained vs. the "predict-the-mean" baseline.
  0 = no better than the mean, 1 = perfect, negative = worse than the mean.

Report at least two metrics — never just one.

---
"""),("code", """mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"MAE : {mae:.2f} (average error in score points)")
print(f"RMSE: {rmse:.2f} (big errors penalized)")
print(f"R²  : {r2:.3f} (share of variance explained)")

# Baseline for context
baseline_rmse = np.sqrt(mean_squared_error(y_test, [y_train.mean()] * len(y_test)))
print(f"baseline RMSE: {baseline_rmse:.2f} -> R² compares the model to this")
"""),
    ("md", """## The honesty check: residuals

Residual = actual − predicted. Two plots catch what no number can:

- **Predicted vs actual**: points near the diagonal = good fit.
- **Residuals vs predicted**: a random cloud around 0 = good; a funnel
  (spread grows) or a curve = the model is missing structure.

---
"""),("code", """fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].scatter(y_test, y_pred, alpha=0.6)
axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--")
axes[0].set(xlabel="Actual", ylabel="Predicted", title="Predicted vs actual")

residuals = y_test - y_pred
axes[1].scatter(y_pred, residuals, alpha=0.6)
axes[1].axhline(0, color="r", linestyle="--")
axes[1].set(xlabel="Predicted", ylabel="Residual", title="Residuals")

plt.tight_layout()
plt.show()

# Read: residuals scatter randomly around 0 with no funnel or curve -> linear
# assumption holds for this dataset.
"""),
    ("md", """## Beginner example: two points define a line

---
"""),("code", """from sklearn.linear_model import LinearRegression

X = [[1], [5]]
y = [10, 30]

m = LinearRegression().fit(X, y)
print("slope:", m.coef_[0], "| intercept:", m.intercept_)
print("predict at x=3:", m.predict([[3]]))

# Expected output:
#   slope: 5.0 | intercept: 5.0
#   predict at x=3: [20.]
"""),
    ("md", """## Intermediate example: real data, real caveats

Predict tips from bill size. Note what the coefficients mean — and what they
don't. (The intercept at a $0 bill is an extrapolation; there are no $0
bills in the data.)

---
"""),("code", """tips = sns.load_dataset("tips")

X = tips[["total_bill"]]
y = tips["tip"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression().fit(X_train, y_train)
y_pred = model.predict(X_test)

print(f"coefficient: {model.coef_[0]:.3f} -> each $1 bill adds ~${model.coef_[0]:.3f} tip")
print(f"intercept: {model.intercept_:.3f} -> a $0 bill would 'predict' a ${model.intercept_:.2f} tip (extrapolation!)")
print(f"MAE: ${mean_absolute_error(y_test, y_pred):.2f} | R²: {r2_score(y_test, y_pred):.2f}")

sns.scatterplot(data=tips, x="total_bill", y="tip", alpha=0.5)
xs = np.linspace(tips["total_bill"].min(), tips["total_bill"].max(), 100)
plt.plot(xs, model.intercept_ + model.coef_[0] * xs, "r-", label="regression line")
plt.legend()
plt.show()
"""),
    ("md", """## Exercises

---
"""),
    ("md", """### Exercise 1 — Interpret

Print the intercept and coefficient for a regression of `body_mass_g` on
`flipper_length_mm` (penguins, drop missing). Write a sentence: "a penguin
with a 1 mm longer flipper weighs about ___ g more, all else equal." (It
should be roughly 49 g.)"""),
    ("code", """import seaborn as sns
penguins = sns.load_dataset("penguins").dropna()

# your code here
"""),
    ("code", """# Solution
from sklearn.linear_model import LinearRegression

X = penguins[["flipper_length_mm"]]
y = penguins["body_mass_g"]
m = LinearRegression().fit(X, y)
print("intercept:", round(m.intercept_, 1))
print("slope:", round(m.coef_[0], 1), "g per mm")
"""),
    ("md", """### Exercise 2 — Metrics

For the penguins model above, compute MAE, RMSE, and R² on a held-out test
set. Which metric would you quote to a non-technical audience?"""),
    ("code", """# your code here
"""),
    ("code", """# Solution
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
m = LinearRegression().fit(Xtr, ytr)
p = m.predict(Xte)
print("MAE:", round(mean_absolute_error(yte, p), 1), "grams")
print("RMSE:", round(np.sqrt(mean_squared_error(yte, p)), 1))
print("R²:", round(r2_score(yte, p), 3))
"""),
    ("md", """### Exercise 3 — Two features

Add `bill_length_mm` as a second feature. Does R² improve? (Usually yes —
more relevant signal.) Report both R² values."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

for cols in [["flipper_length_mm"], ["flipper_length_mm", "bill_length_mm"]]:
    Xtr, Xte, ytr, yte = train_test_split(penguins[cols], y, test_size=0.2, random_state=42)
    m = LinearRegression().fit(Xtr, ytr)
    print(cols, "-> R²:", round(r2_score(yte, m.predict(Xte)), 3))
"""),
    ("md", """## Challenge exercise

Predict `body_mass_g` from **all** numeric penguin measurements. Then:

1. Report MAE, RMSE, R², and the baseline RMSE.
2. Print the coefficients with their feature names — which feature dominates?
3. Plot residuals vs predicted. Does the cloud look random, funnel-shaped,
   or curved? Write your reading in markdown."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
features = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm"]
X = penguins[features]
y = penguins["body_mass_g"]

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
m = LinearRegression().fit(Xtr, ytr)
p = m.predict(Xte)

print("MAE:", round(mean_absolute_error(yte, p), 1))
print("RMSE:", round(np.sqrt(mean_squared_error(yte, p)), 1))
print("R²:", round(r2_score(yte, p), 3))
print(pd.Series(m.coef_, index=features).round(2).sort_values(ascending=False))

fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(p, yte - p, alpha=0.6)
ax.axhline(0, color="r", linestyle="--")
ax.set(xlabel="Predicted body mass", ylabel="Residual", title="Residuals")
plt.show()
"""),
    ("md", """## Recap

- Linear model = intercept + weighted features; read it like a sentence.
- MAE (average error, units), RMSE (penalizes big errors), R² (vs. mean baseline).
- Check predicted-vs-actual and residuals — the numbers can lie.
- Coefficients are associations, "all else equal" — not proof of cause.
- Intercepts can be meaningless extrapolations outside the data range.

---
"""),
    ("md", """## Questions

1. Write the linear model formula in words for two features.
2. What does a coefficient of 3.5 on `hours` mean?
3. Which metric would you quote to a manager, and why?
4. R² = 0.7 — what does that mean in one sentence?
5. What pattern in a residual plot suggests a non-linear relationship?
6. Why is the intercept sometimes meaningless?

---
**Next:** notebook 12 — Classification.
"""),
]