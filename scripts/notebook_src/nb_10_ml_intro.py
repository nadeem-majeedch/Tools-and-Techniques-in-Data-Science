# Content for notebook 10: Introduction to Machine Learning.
CELLS = [
    ("md", """# 10 — Introduction to Machine Learning

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-2 — Apply basic machine learning techniques.

Machine learning inverts programming: instead of writing rules that produce
answers, you provide *examples* (data + answers) and the algorithm *finds*
the rules. This notebook establishes the vocabulary and the one uniform
workflow used by every model in the rest of the course.

---
"""),("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Distinguish supervised vs. unsupervised learning and regression vs. classification.
2. Explain the train/test split and why it exists.
3. Train and evaluate a first scikit-learn model.
4. Compute a baseline and judge a model against it.
5. Use `random_state` to make results reproducible.

---
"""),("md", """## Theory: the learning problem

Two questions decide everything:

1. Do the examples have **labels** (known answers)?
   - Yes → **supervised** learning (predict the label).
   - No → **unsupervised** learning (find structure — clustering).
2. What kind of answer do we want?
   - A number → **regression** (price, score, tip).
   - A category → **classification** (spam/not, species).

| | Supervised | Unsupervised |
|---|---|---|
| Has answers | yes | no |
| Goal | predict | find groups |
| Course models | regression, classification | k-means |

**Why a train/test split?** A model that aces its training data may simply
have *memorized* it. The only honest test is data it never saw. Split into
train (80%) and test (20%), fit on train, score on test. If test is much
worse than train, the model memorized (overfitting).

---
"""),("code", """import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Generate a small, reproducible dataset: score ~ hours (with noise)
np.random.seed(42)
n = 200
hours = np.random.uniform(1, 10, n)
score = 40 + 6 * hours + np.random.normal(0, 5, n)

df = pd.DataFrame({"hours": hours, "score": score})
print(df.head(3))
"""),
    ("md", """## The scikit-learn uniform API

Every model in scikit-learn works the same four steps:

1. **Choose** — `model = LinearRegression()`
2. **Fit** — `model.fit(X_train, y_train)` (learn from training data)
3. **Predict** — `model.predict(X_test)` (apply to unseen data)
4. **Evaluate** — compare predictions to the true `y_test`

`X` is the feature matrix (2-D), `y` the target (1-D). Learn this shape once;
sessions 11–13 only change the model and the metric.

---
"""),("code", """X = df[["hours"]]          # feature(s): always 2-D for sklearn
y = df["score"]            # target: 1-D

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42,
)

model = LinearRegression()
model.fit(X_train, y_train)                    # 2. fit
y_pred = model.predict(X_test)                 # 3. predict

rmse = np.sqrt(mean_squared_error(y_test, y_pred))   # 4. evaluate
print("test RMSE:", round(rmse, 2))
"""),
    ("md", """## The baseline: what "good" means

Before celebrating any score, beat the **baseline** — the trivial prediction:
for regression, always predict the mean of the training target. A model that
cannot beat the baseline adds nothing.

---
"""),("code", """baseline_pred = np.full_like(y_test, y_train.mean())
baseline_rmse = np.sqrt(mean_squared_error(y_test, baseline_pred))

print("baseline RMSE (predict the mean):", round(baseline_rmse, 2))
print("model RMSE:", round(rmse, 2))
print("improvement: {:.0%} lower error".format(1 - rmse / baseline_rmse))
"""),
    ("md", """## Beginner example: a classifier in six lines

The exact same workflow, with a different model and metric.

---
"""),("code", """from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Tiny labeled dataset: (feature1, feature2) -> "small" or "big"
X = [[1, 0], [2, 0], [1, 1], [5, 4], [6, 4], [5, 5]]
y = ["small", "small", "small", "big", "big", "big"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

print("predictions:", list(pred))
print("accuracy:", round(accuracy_score(y_test, pred), 2))
"""),
    ("md", """## Intermediate example: can we predict tips?

Everything together on a real dataset. The steps never change: split → fit →
predict → evaluate → compare to baseline.

---
"""),("code", """import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

tips = sns.load_dataset("tips").dropna()
X = tips[["total_bill", "size"]]
y = tips["tip"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression().fit(X_train, y_train)
pred = model.predict(X_test)

mae = mean_absolute_error(y_test, pred)
base = mean_absolute_error(y_test, [y_train.mean()] * len(y_test))
print(f"model MAE: ${mae:.2f}  | baseline MAE: ${base:.2f}")

# Coefficients: which feature matters more?
print(pd.Series(model.coef_, index=X.columns).round(3))
"""),
    ("md", """## Exercises

---
"""),
    ("md", """### Exercise 1 — Vocabulary

Classify each problem: supervised/unsupervised + regression/classification.
(Answer in your head or in a markdown cell: house price → supervised
regression; spam filter → supervised classification; customer segments →
unsupervised clustering; churn prediction → supervised classification.)"""),
    ("code", """# Add your answers in a markdown cell, e.g.:
#   house price       -> supervised, regression
#   spam filter       -> supervised, classification
#   customer segments -> unsupervised, clustering
#   churn prediction  -> supervised, classification
print("answers recorded in markdown")
"""),
    ("md", """### Exercise 2 — Seed experiment

Run `train_test_split` on the tips data with `random_state` values 0, 1, 42
and note the (slightly) different test MAEs. What does this tell you about
single-split estimates?"""),
    ("code", """# your code here
"""),
    ("code", """# Solution
from sklearn.metrics import mean_absolute_error

for seed in [0, 1, 42]:
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=seed)
    m = LinearRegression().fit(Xtr, ytr)
    print(seed, "-> MAE:", round(mean_absolute_error(yte, m.predict(Xte)), 3))
"""),
    ("md", """### Exercise 3 — First classifier

Train a `KNeighborsClassifier` on the iris dataset (seaborn or
`sklearn.datasets.load_iris`) and report test accuracy."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
import seaborn as sns

iris = sns.load_dataset("iris")
X = iris.drop(columns="species"); y = iris["species"]

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
knn = KNeighborsClassifier(n_neighbors=5).fit(Xtr, ytr)
print("iris kNN accuracy:", round(accuracy_score(yte, knn.predict(Xte)), 3))
"""),
    ("md", """## Challenge exercise

On the tips data, predict `tip` using **only** `total_bill` (one feature),
and compare against the two-feature model (`total_bill` + `size`) from the
intermediate example. Report both MAEs and both baseline comparisons. Which
model wins, and why might the difference be small?"""),
    ("code", """# your code here
"""),
    ("code", """# Solution
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

for cols in [["total_bill"], ["total_bill", "size"]]:
    X = tips[cols]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    m = LinearRegression().fit(Xtr, ytr)
    mae = mean_absolute_error(yte, m.predict(Xte))
    print(cols, "-> MAE:", round(mae, 3))
"""),
    ("md", """## Recap

- Supervised (has labels) vs unsupervised (finds structure).
- Regression (number) vs classification (category).
- The four-step API: choose → fit → predict → evaluate.
- Train/test split = honest evaluation on unseen data.
- Beat the baseline (mean / most-common class) before trusting a model.
- `random_state` everywhere → reproducible results.

---
"""),
    ("md", """## Questions

1. What is the difference between supervised and unsupervised learning?
2. Regression predicts a ___; classification predicts a ___.
3. Why must we evaluate on data the model has never seen?
4. What does `random_state=42` do?
5. What is a baseline and why compute one?
6. Name the four steps of the scikit-learn pattern.

---
**Next:** notebook 11 — Regression.
"""),
]