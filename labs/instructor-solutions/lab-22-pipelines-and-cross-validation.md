# Lab 22 — Solution: Pipelines & Cross-Validation

**Session:** W11 S22 · **CLO:** CLO-2

## Complete solution

```python
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

penguins = sns.load_dataset("penguins").dropna()
X = penguins[["bill_length_mm", "bill_depth_mm",
              "flipper_length_mm", "body_mass_g"]]
y = penguins["species"]

# hold out FIRST — the test set must never influence CV/model choice
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

for kind in ["knn", "logreg", "tree"]:
    pipe = make_model(kind)
    scores = cross_val_score(pipe, X_train, y_train, cv=5)
    print(kind, "->", round(scores.mean(), 3), "+/-", round(scores.std(), 3))

# winner: logistic regression (or k-NN — whichever is best on your run)
best = make_model("logreg").fit(X_train, y_train)
test_acc = accuracy_score(y_test, best.predict(X_test))
print("winner test acc:", round(test_acc, 3))
```

## Expected output

- Split: 266 train / 67 test.
- CV (approx): knn 0.975 ± 0.02, logreg 0.985 ± 0.01, tree 0.955 ± 0.02.
- Winner: logistic regression (margin ~1 point over k-NN — small).
- Test acc ≈ 0.97, close to the CV mean.
- Leakage explanation: the scaler is fit *inside each CV fold* on that
  fold's training portion only; the pipeline guarantees this because
  scaling is a step in the estimator that CV refits per fold.

## Model answers

1. **Hold out first** — the test set must stay untouched until the very
   end; any use of it (even for choosing a model) leaks information and
   inflates the final score.
2. **cross_val_score(cv=5)** — splits train into 5 folds; for each fold:
   fit on the other 4, score on the held-out fold; returns 5 scores (one
   per fold).
3. **Mean ± std** — the mean estimates expected performance across data
   partitions; the std shows stability. Two models with equal means but
   different stds aren't equally trustworthy.
4. **Scaler on all data (leakage)** — the scaler's mean/std would
   incorporate test-fold statistics; the scaled train features would carry
   test information, flattering validation scores.
5. **CV 0.97 / test 0.88** — (1) small test set → noisy estimate; (2)
   distribution shift between train and test (different data source or
   time); (3) luck in the single test split.

## Challenge solution

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold

pipe_rf = Pipeline([("scale", StandardScaler()),
                    ("clf", RandomForestClassifier(n_estimators=100,
                                                   random_state=42))])
scores_rf = cross_val_score(pipe_rf, X_train, y_train, cv=5)
print("rf:", round(scores_rf.mean(), 3), "+/-", round(scores_rf.std(), 3))

kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(make_model("logreg"), X_train, y_train, cv=kf)
print("per-fold:", [round(s, 3) for s in scores])
# The fold spread (e.g., 0.96-1.00) shows how much the estimate wobbles
# depending on which rows are held out — the std, not just the mean.
```