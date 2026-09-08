# Session 18 — Linear Regression

**Week 9 · Session 18 · Module B · 90 min · CLO-2**

## 1. Learning objectives

By the end of this session, students can:
- Explain a linear model: `y = b0 + b1·x1 + b2·x2 + ...` in plain words.
- Fit a linear regression with scikit-learn on numeric features.
- Interpret coefficients (direction, magnitude, units) and the intercept.
- Evaluate with MAE, MSE/RMSE, and R², and explain what each means.
- Recognize when linearity is a bad assumption (scatter check first).

## 2. Key concepts

- **Linear model = weighted sum of features + intercept**; the coefficients are the "learned rules".
- **Fitting** = finding coefficients that minimize the error (ordinary least squares).
- **Error metrics:** MAE (average absolute error, interpretable units), MSE/RMSE (penalize big errors), R² (share of variance explained, 0–1).
- **R²** is a *relative* score: 0 = no better than the mean, 1 = perfect fit; negative R² = worse than the mean.
- **Coefficient reading:** "one more unit of X is associated with `b` units of y, all else equal".
- Plot **predicted vs. actual** and **residuals** — the model's failures are visible there.

## 3. Detailed lecture notes

**Why linear regression first?** It is the oldest, simplest, most interpretable
model — and the foundation for understanding every other one. A linear model
says: *the target is a weighted sum of the features, plus noise*. Its strength is
not raw accuracy but **readability**: you can open the model and explain exactly
how each feature moves the prediction. Regulators, doctors, and managers ask
"why?" — linear models answer best.

**The equation, in words first.** `score = 40 + 6 × hours`. The **intercept**
(40) is the prediction when all features are 0; the **coefficient** (6) says each
extra study hour adds ~6 points *on average, all else equal*. For multiple
features the sentence becomes "holding other features fixed…". Warning: "all
else equal" is a ceteris paribus claim — with correlated features, coefficients
get shaky (multicollinearity — mention, don't dive in).

**How the model "learns".** Ordinary least squares picks coefficients that
minimize the sum of squared errors (residuals). Show the intuition: try a flat
line, then tilt it — the sum of squared vertical gaps shrinks; calculus finds
the minimum. No need for the closed-form derivation; the picture is enough.
Why *squared* errors? Big errors get punished disproportionately, and the math
is clean. That's also why RMSE is in the target's units.

**Metrics — three lenses.**
- **MAE:** average absolute error. "Our tip predictions are off by $1.40 on average." Units = target units; easiest to explain to non-technical people.
- **MSE/RMSE:** square errors, take the root → same units as MAE but penalizes large misses more. RMSE ≥ MAE always; a big gap means your model has a few large errors (outliers).
- **R²:** 1 − (model error ÷ "predict-the-mean" error). R² = 0.6 means the model explains 60% of the variance the mean baseline leaves unexplained. R² can go negative when the model is *worse* than the mean — which is information, not a bug.
Which metric to report? MAE/RMSE for business meaning, R² for model quality. Report at least two; never just one.

**Residual plots — the honesty check.** Residual = actual − predicted. Plot
residuals vs. predicted: random cloud around 0 = good; a funnel (spread growing)
= variance isn't constant; a curve = the relationship isn't linear (add
features, try non-linear models). Always scatter `y_test` vs `y_pred` first: a
straight-ish diagonal = the model captures the pattern; a bent cloud = missing
structure. These two plots catch what no single number can.

**Assumptions — keep it practical.** Linear regression assumes a roughly
*linear* relationship and no wild outliers. The workflow: scatter features vs.
target *before* fitting (Session 13's skill). If the relationship is clearly
curved (e.g., tips vs. bill looks linear-ish, but age vs. income is not), linear
regression will mislead. Log-transform or try other models — Sessions 19–20
offer alternatives. For this course: check the plot, note the limitation.

## 4. Important terminology

- **Coefficient (slope, weight)** — effect of one feature on the target, all else equal.
- **Intercept** — predicted target when all features are 0.
- **Residual** — actual minus predicted value.
- **Ordinary least squares (OLS)** — fitting by minimizing squared residuals.
- **MAE** — mean absolute error (same units as target).
- **MSE / RMSE** — mean squared error; RMSE = root, back in target units, penalizes big errors.
- **R²** — share of target variance explained vs. the mean baseline.
- **Fit** — the act of learning coefficients from training data.
- **Predicted vs. actual plot** — visual model check.
- **Linearity assumption** — the relationship is (roughly) additive/straight.
- **Ceteris paribus** — "all else equal" (how to read a coefficient).

## 5. Python examples

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

np.random.seed(7)
df = pd.DataFrame({"hours": np.random.uniform(1, 10, 300)})
df["score"] = 40 + 6 * df["hours"] + np.random.normal(0, 5, 300)

X = df[["hours"]]
y = df["score"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression().fit(X_train, y_train)
y_pred = model.predict(X_test)

print("Intercept:", round(model.intercept_, 2))          # ~40
print("Coefficient:", round(model.coef_[0], 2))          # ~6
print("MAE:", round(mean_absolute_error(y_test, y_pred), 2))
print("RMSE:", round(np.sqrt(mean_squared_error(y_test, y_pred)), 2))
print("R²:", round(r2_score(y_test, y_pred), 3))

# Model check: predicted vs actual + residuals
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].scatter(y_test, y_pred, alpha=0.6)
axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--")
axes[0].set(xlabel="Actual", ylabel="Predicted", title="Predicted vs actual")
residuals = y_test - y_pred
axes[1].scatter(y_pred, residuals, alpha=0.6)
axes[1].axhline(0, color="r", linestyle="--")
axes[1].set(xlabel="Predicted", ylabel="Residual", title="Residuals")
plt.tight_layout()
```

## 6. Beginner example

```python
from sklearn.linear_model import LinearRegression

# Two points define a line — the simplest possible fit
X = [[1], [5]]
y = [10, 30]
m = LinearRegression().fit(X, y)
print(m.coef_[0], m.intercept_)     # slope 5, intercept 5
print(m.predict([[3]]))             # 20 — the point on the line
```

With two points the model is a straight line through them; with 300 points it
becomes the best-fitting line through the cloud.

## 7. Practical Data Science example

```python
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# Question: predict tip from bill size — but check linearity first
tips = sns.load_dataset("tips")

X = tips[["total_bill"]]
y = tips["tip"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression().fit(X_train, y_train)
y_pred = model.predict(X_test)

print("Coefficient:", round(model.coef_[0], 3), "— each $1 bill → +$0.09 tip")
print("Intercept:", round(model.intercept_, 3), "— ~0.92 base tip")
print(f"MAE: ${mean_absolute_error(y_test, y_pred):.2f} | R²: {r2_score(y_test, y_pred):.2f}")

# Compare with baseline
baseline = np.full_like(y_test, y_train.mean())
print("Baseline R² would be 0 by definition; model explains",
      round((1 - ((y_test - y_pred) ** 2).sum() / ((y_test - y_train.mean()) ** 2).sum()) * 100), "% of variance")
```

## 8. In-class activity (50 min)

In `notebooks/week-09/session-18-linear-regression.ipynb`:

1. **Interpret first (15 min):** print intercept + coefficient for the tips
   model; write in markdown: "For every extra dollar on the bill, the model
   predicts ___ more tip. At a $0 bill it predicts ___." Is the intercept
   meaningful here? (Not really — no $0 bills; note that.)
2. **Metrics (15 min):** compute MAE, RMSE, R²; write which metric you'd tell a
   restaurant manager and why.
3. **Residuals (20 min):** make the predicted-vs-actual and residual plots;
   check: funnel shape? curve? Write one sentence about what the residuals say.
   Then re-fit with both `total_bill` and `size` and compare R².

## 9. Lab exercise

**Lab 18 is due today** (`labs/lab-18-linear-regression.md`): linear regression
— fit, evaluate with MAE/RMSE/R², compare vs. baseline, residual check. Push.

## 10. Common mistakes

- Interpreting the intercept when feature=0 is outside the data range (e.g., $0 bills) — it's an extrapolation.
- Saying "hours *cause* +6 points" — regression shows *association*, all else equal; causation needs experiments.
- Reporting R² = 0.95 on training data — always report *test* R².
- Ignoring the residual plot and trusting R² alone.
- Using categorical features without encoding (Sessions 19–20 fix this).
- Forgetting that RMSE is in target units — reporting "RMSE = 2.3" without "$" or "%" is meaningless.
- Fitting on data with NaN or non-numeric columns → errors or silent garbage.

## 11. Short assessment questions

1. Write the linear model formula in words for two features.
2. What does a coefficient of 3.5 on `hours` mean?
3. Which metric should you quote to a non-technical manager, and why?
4. R² = 0.7 — what does that mean in one sentence?
5. What pattern in a residual plot tells you the relationship isn't linear?
6. Why is the intercept sometimes meaningless? (Feature=0 is out of data range.)

## 12. CLO mapping

CLO-2: linear regression is the first "basic machine learning technique" applied
to a data-driven problem — the fit/evaluate/interpet pattern is repeated for
every model in Module B and graded in Labs 17–22, the final exam, and the project.

## 13. Suggested homework

- Commit the activity notebook.
- Practice: run the same workflow on `penguins` predicting `body_mass_g` from `flipper_length_mm`; report all three metrics.
- Read: scikit-learn docs — `LinearRegression` page and the `mean_squared_error`/`r2_score` pages (10 minutes).
- Preview: `from sklearn.neighbors import KNeighborsClassifier` + the iris dataset — Session 19 moves from numbers to categories (classification).