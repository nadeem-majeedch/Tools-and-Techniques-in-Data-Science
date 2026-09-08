# Session 22 — Pipelines & Cross-Validation

**Week 11 · Session 22 · Module B · 90 min · CLO-2**

## 1. Learning objectives

By the end of this session, students can:
- Explain the problem pipelines solve: preprocessing steps must not leak test information.
- Build a `Pipeline` that chains scaler + model, and use it like a normal model.
- Explain k-fold cross-validation and why it beats a single split.
- Run `cross_val_score` and interpret mean ± spread.
- Choose the right model by comparing *cross-validated* scores, not one lucky split.
- Apply the full Module B workflow: pipeline + CV + baseline comparison.

## 2. Key concepts

- **Data leakage:** fitting a scaler (or any step) on the *whole* dataset lets test information sneak into training → inflated scores.
- **Pipeline** = named preprocessing + model steps fitted *inside* each fold; one object, one `fit`/`predict`.
- **Cross-validation** = k train/validation rounds, every row validated exactly once.
- **`cross_val_score`** — honest, stable performance estimate; report mean ± std.
- **Model selection = compare CV scores**, not single-split accuracy.
- Pipelines make your workflow **reproducible** — a single object that encodes "scale then model" (and a direct link to CLO-3's reproducibility theme).

## 3. Detailed lecture notes

**Why pipelines?** Revisit Session 19's k-NN lesson: features must be scaled.
Where do you fit the scaler? If you fit `StandardScaler` on *all* data before
splitting, the scaler has seen the test set — its mean/std carry test
information into training. That's **data leakage**: your test score is
optimistically biased, and the model won't perform that well on truly new data.
The correct order: fit scaler on train **only**, transform test with that
fitted scaler. Doing this by hand invites bugs. The `Pipeline` object encodes
the whole sequence once and guarantees the right behavior inside every split.
This is not an advanced topic — it's the difference between a correct and an
incorrect experiment.

**How a pipeline works.** `Pipeline([("scaler", StandardScaler()),
("knn", KNeighborsClassifier(n_neighbors=5))])` — a list of named steps.
`pipe.fit(X_train, y_train)` runs: fit scaler on train, transform train, fit
model; `pipe.predict(X_test)` runs: transform test with the *already-fitted*
scaler, then predict. One object, used exactly like a model. Because the steps
are fitted inside `fit`, cross-validation (below) re-fits the scaler on each
fold's training portion — leakage impossible by construction. Preprocessing is
now part of the model, which is also the reproducible way to document "this is
exactly how predictions are made."

**Why cross-validation?** A single 80/20 split gives *one* estimate that
depends on luck: shuffle differently, and the score wobbles (Session 17's seed
experiment showed this). **k-fold CV** splits the training data into k parts;
each part becomes a validation set once while the model trains on the other
k−1; average the k scores. Every row is validated exactly once. You get a mean
(honest performance) and a spread (stability — big spread = your estimate is
fragile). k=5 is the default and fine here. Explain the loop with a diagram:
fold 1: train on folds 2–5, validate on 1; fold 2: train on 1,3,4,5, validate
on 2; …

**The honest workflow (Module B in one recipe):**
1. Split data **once** into train/test (stratified for classification), and lock test away.
2. Build a pipeline (scaler + model).
3. `cross_val_score(pipe, X_train, y_train, cv=5)` → mean ± std.
4. Compare models *by their CV means* (k-NN vs. logistic vs. tree, tuned hyperparameters).
5. Fit the winning pipeline on all of train; evaluate **once** on test.
6. Report train, CV, and test numbers together.
Emphasize the one-test-evaluation rule (Session 20's lesson) now backed by CV —
tune with CV on train; test is the final, single check.

**Choosing the right model.** With CV scores in hand, "which model is best?" has
an evidence-based answer: the one with the highest mean (or best trade-off of
mean vs. stability) — not the one that flashed 0.99 on a lucky split. Also
consider interpretability (tree > k-NN > deep models) when scores are close.
This decision procedure — baseline, CV comparison, final test — is the
backbone of Labs 21–22 and the project's modeling section.

## 4. Important terminology

- **Pipeline** — chained preprocessing + model steps, fitted together.
- **Data leakage** — test information reaching the model during training.
- **Cross-validation (CV)** — k train/validate rounds over the training data.
- **Fold** — one of the k validation partitions.
- **`cross_val_score`** — CV accuracy/R² per fold; report mean ± std.
- **`StandardScaler`** — z-score transform (mean 0, std 1).
- **Grid/parameter search** — (mentioned) trying hyperparameter combinations; `GridSearchCV` automates it with CV.
- **Model selection** — choosing among models by CV scores.
- **Locked test set** — test evaluated once, at the end.
- **`make_pipeline`** — shortcut for pipelines without naming steps.

## 5. Python examples

```python
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

iris = sns.load_dataset("iris")
X = iris.drop(columns="species")
y = iris["species"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                    random_state=42, stratify=y)

# --- Pipeline: scale, then classify ---
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(n_neighbors=5)),
])
pipe.fit(X_train, y_train)
print("Pipeline test accuracy:", round(pipe.score(X_test, y_test), 3))

# --- Cross-validation on the TRAINING portion ---
scores = cross_val_score(pipe, X_train, y_train, cv=5)
print("CV accuracy: mean %.3f ± %.3f" % (scores.mean(), scores.std()))

# --- Compare models with CV ---
models = {
    "kNN":        Pipeline([("s", StandardScaler()), ("m", KNeighborsClassifier(n_neighbors=5))]),
    "Logistic":   Pipeline([("s", StandardScaler()), ("m", LogisticRegression(max_iter=1000))]),
    "Tree(d=3)":  DecisionTreeClassifier(max_depth=3, random_state=42),
}
for name, m in models.items():
    cv = cross_val_score(m, X_train, y_train, cv=5)
    print(f"{name:10s} CV mean {cv.mean():.3f} ± {cv.std():.3f}")

# --- Final: fit winner on full train, evaluate ONCE on test ---
winner = models["Logistic"].fit(X_train, y_train)
print("Final test accuracy:", round(winner.score(X_test, y_test), 3))
```

## 6. Beginner example

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

pipe = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))
# fit once, and the scaler + model travel together forever
```

One line, and the "scale before predict" bug class disappears.

## 7. Practical Data Science example

```python
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

# Titanic survival, full Module B recipe
titanic = sns.load_dataset("titanic").dropna(subset=["survived", "age", "fare", "pclass"])
X = titanic[["pclass", "age", "fare"]]
y = titanic["survived"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                    random_state=42, stratify=y)

logreg = Pipeline([("scaler", StandardScaler()),
                   ("model", LogisticRegression(max_iter=1000))])
tree   = DecisionTreeClassifier(max_depth=4, min_samples_leaf=5, random_state=42)

for name, m in [("LogReg", logreg), ("Tree", tree)]:
    cv = cross_val_score(m, X_train, y_train, cv=5)
    print(f"{name}: CV {cv.mean():.3f} ± {cv.std():.3f}")

# Winner -> fit on train, evaluate once on test
logreg.fit(X_train, y_train)
print(classification_report(y_test, logreg.predict(X_test)))
```

## 8. In-class activity (50 min)

In `notebooks/week-11/session-22-pipelines-cv.ipynb`:

1. **Leakage demo (15 min):** fit a scaler on *all* data, then split, then train
   k-NN — compare test accuracy vs. the pipeline version. Usually the leaked
   version looks better; discuss why that's a lie.
2. **CV vs. single split (15 min):** run `cross_val_score` 5 times on the iris
   pipeline and a single 80/20 split 5 times (different seeds). Which estimate
   is more stable? Write your observation.
3. **Model comparison (20 min):** build the three-model CV table on penguins
   (scaled features); pick a winner; fit on full train; report the single test
   score. Write one paragraph justifying your choice (score + interpretability).

## 9. Lab exercise

**Lab 22 is due today** (`labs/lab-22-pipelines-and-cross-validation.md`):
pipelines & cross-validation — scaler→model pipelines with CV comparison.
Push.

## 10. Common mistakes

- Fitting the scaler on all data before splitting → leakage → inflated, dishonest scores.
- Forgetting preprocessing inside CV (scaling outside the folds leaks again — pipelines prevent it).
- Tuning on the test set instead of CV on train.
- Reporting CV mean without the spread (± std matters).
- Comparing models on *different* splits — compare on the same CV folds.
- Using `predict` on a scaler (it's `transform`) — pipelines remove this whole bug class.
- Treating one CV run as gospel — randomness still exists; report and repeat with different seeds if skeptical.

## 11. Short assessment questions

1. What is data leakage, in one sentence?
2. Why does a pipeline prevent leakage during cross-validation?
3. Describe 5-fold CV in two sentences.
4. What do `scores.mean()` and `scores.std()` tell you about a model?
5. How many times may the test set be used, and why?
6. Which is more trustworthy for model choice: one 80/20 split accuracy or a 5-fold CV mean? Why?

## 12. CLO mapping

CLO-2: pipelines + CV are the "appropriate data science tools" for honest model
selection — the culminating skill of Module B and the backbone of the final
project's modeling section. Reproducible pipelines also hand off
directly to CLO-3's reproducibility requirement (Sessions 24, 30).

## 13. Suggested homework

- Commit the activity notebook.
- Start the **project proposal draft** (due Session 26): your modeling plan (regression or classification with CV and baseline comparison) goes into it.
- Read: scikit-learn docs — "Pipelines and composite estimators" (the intro).
- Preview: the **final project kickoff (Session 23)** — bring two candidate questions and datasets; you'll pick one and write the proposal.