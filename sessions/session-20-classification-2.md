# Session 20 — Classification II: Decision Trees, Overfitting, Tuning

**Week 10 · Session 20 · Module B · 90 min · CLO-2**

## 1. Learning objectives

By the end of this session, students can:
- Explain how a decision tree makes predictions and why it's interpretable.
- Fit and visualize a `DecisionTreeClassifier` with scikit-learn.
- Diagnose overfitting: train score ≫ test score.
- Reduce overfitting with `max_depth` / `min_samples_leaf` and reasonable default settings.
- Do a simple manual hyperparameter sweep and read the results.

## 2. Key concepts

- **Decision trees = nested if-then rules** learned from data (splits that best separate classes).
- **Interpretability is the tree's superpower** — you can print and read the rules.
- **Overfitting:** the tree memorizes training noise; the fix is *limiting its freedom* (depth, leaf size).
- **Train vs. test gap** is the overfitting thermometer.
- **Hyperparameters** are model settings chosen *before* fitting (`max_depth`), unlike the learned parameters.
- Trees handle numeric and categorical features natively and need no scaling — a nice contrast with k-NN.

## 3. Detailed lecture notes

**Why trees?** k-NN and logistic regression are black boxes compared with this:
a decision tree is literally a list of `if feature > value` questions —
"if bill_length > 43 and flipper > 205 → Gentoo". You can *read* the whole model
and explain every prediction. That interpretability is why trees and their
cousins (random forests, XGBoost — beyond this course) dominate tabular
industry work: stakeholders want reasons, and trees give them.

**How a tree is built.** Greedily: at each node, pick the feature and split
value that best separates the classes (scikit-learn uses Gini impurity — "how
mixed is this node?"; less mixing = better split). Split, repeat, until leaves
are pure or a stopping rule fires. Teach this by *drawing* a tiny tree on
penguins by hand (bill length > 43? → split) before fitting one in code. The
picture makes `plot_tree` output meaningful.

**The overfitting trap.** A tree with no limits will split until every training
point is isolated — 100% training accuracy, terrible generalization. That's the
canonical overfitting story, and trees demonstrate it more dramatically than
any other model. The diagnostic is the **train–test gap**: train R²/accuracy ≈
1.0 while test ≈ 0.8 means memorization. Always report *both* scores. Also
mention: the deeper the tree, the more variance (small data changes → very
different trees); shallow trees are stable but may underfit (high bias).

**The fix: regularize the tree.** Restrict its freedom *before* fitting —
these settings are **hyperparameters**:
- `max_depth` — how many nested questions (5 is a sensible default; 2–3 for small data).
- `min_samples_leaf` — minimum examples per leaf (e.g., 5–10) prevents leaves with a single lucky row.
- `min_samples_split` — minimum rows required to attempt a split.
Teach the *effect*, not the tuning theory: smaller freedom → smaller train-test
gap → usually better test performance. The art is balancing bias (too simple:
both scores low) vs. variance (too complex: big gap). The "sweet spot" is where
test performance peaks — the sweep below finds it.

**Manual hyperparameter sweep.** The honest way to choose: loop over candidate
values, record train and test scores, plot them, pick the value where test peaks
before the gap widens. scikit-learn's `GridSearchCV` automates this (Session 22),
but doing it by hand *once* builds the intuition that automation hides. Emphasize:
tune on train (via validation), evaluate *once* on test — peeking at test during
tuning leaks information.

**Validation concept (preview).** To tune without touching test, split train
into train/validation (or use cross-validation, Session 22). For today, a
train/validation/test trio or a simple 80/20 with a fixed seed is enough — the
principle is what matters: *test is evaluated exactly once, at the end.*

## 4. Important terminology

- **Decision tree** — nested if-then rules learned from data.
- **Node / leaf** — a decision point / a terminal prediction.
- **Gini impurity** — node "mixedness" used to choose splits.
- **Overfitting** — memorizing training noise; train ≫ test.
- **Underfitting** — too simple to capture the pattern; both scores low.
- **Bias–variance trade-off** — simplicity (bias) vs. complexity (variance).
- **Hyperparameter** — setting chosen before fitting (`max_depth`, `min_samples_leaf`, `k` in k-NN).
- **`max_depth`** — max number of nested splits.
- **`min_samples_leaf`** — minimum rows per leaf (regularizer).
- **Train–test gap** — the overfitting thermometer.
- **Sweep** — trying candidate hyperparameter values and comparing scores.

## 5. Python examples

```python
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score

iris = sns.load_dataset("iris")
X = iris[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
y = iris["species"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                    random_state=42, stratify=y)

# --- The overfitting demonstration: unlimited tree ---
unlimited = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
print("UNLIMITED  train:", round(accuracy_score(y_train, unlimited.predict(X_train)), 3),
      "| test:", round(accuracy_score(y_test, unlimited.predict(X_test)), 3))
# train ~1.00, test ~0.93 -> memorization

# --- Regularized tree ---
tree = DecisionTreeClassifier(max_depth=4, min_samples_leaf=4, random_state=42)
tree.fit(X_train, y_train)
print("REGULARIZED train:", round(accuracy_score(y_train, tree.predict(X_train)), 3),
      "| test:", round(accuracy_score(y_test, tree.predict(X_test)), 3))

# --- Visualize the readable rules ---
plt.figure(figsize=(14, 7))
plot_tree(tree, feature_names=X.columns, class_names=y.unique(), filled=True, fontsize=9)
plt.show()

# --- Manual sweep ---
depths = range(1, 11)
train_scores, test_scores = [], []
for d in depths:
    m = DecisionTreeClassifier(max_depth=d, random_state=42).fit(X_train, y_train)
    train_scores.append(accuracy_score(y_train, m.predict(X_train)))
    test_scores.append(accuracy_score(y_test, m.predict(X_test)))

plt.plot(depths, train_scores, "o-", label="train")
plt.plot(depths, test_scores, "o-", label="test")
plt.xlabel("max_depth"); plt.ylabel("accuracy")
plt.legend(); plt.title("The overfitting curve")
plt.show()
```

## 6. Beginner example

```python
from sklearn.tree import DecisionTreeClassifier

# Rules from two tiny features
X = [[1.5, 1], [1.7, 1], [1.9, 2], [2.0, 2]]
y = ["no", "no", "yes", "yes"]

t = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X, y)
print(t.predict([[1.6, 1]]))   # 'no'
print(t.predict([[1.95, 2]]))  # 'yes'
```

The model is a small set of if-then rules — readable, explainable, done.

## 7. Practical Data Science example

```python
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Titanic-style survival modeling on the seaborn titanic dataset
titanic = sns.load_dataset("titanic").dropna(subset=["survived", "age", "fare", "pclass"])

X = titanic[["pclass", "age", "fare"]]
y = titanic["survived"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                    random_state=42, stratify=y)

# Baseline: predict the majority class (did NOT survive)
baseline_acc = max(y_train.mean(), 1 - y_train.mean())
print("Baseline accuracy: %.3f" % baseline_acc)

# Model (regularized from the start)
model = DecisionTreeClassifier(max_depth=4, min_samples_leaf=5, random_state=42)
model.fit(X_train, y_train)
acc = accuracy_score(y_test, model.predict(X_test))
print("Tree test accuracy: %.3f" % acc)

# Which feature did the tree lean on most?
print(pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False))
```

## 8. In-class activity (50 min)

In `notebooks/week-10/session-20-classification-2.ipynb`:

1. **Draw a tree by hand (10 min):** for `penguins`, propose a two-question
   decision rule separating Gentoo from the others using the Session 14
   pairplot; then fit `max_depth=2` and compare with `plot_tree`.
2. **The overfitting curve (20 min):** run the depth sweep 1–10 on penguins;
   mark where the train-test gap starts widening; pick your `max_depth`.
3. **Read the rules (10 min):** with `max_depth=3, min_samples_leaf=5`, read the
   tree out loud: "if ..., and ..., then species is ...".
4. **Regularize (10 min):** compare `min_samples_leaf` in {1, 5, 15}; record
   train/test accuracy in a small table.

## 9. Lab exercise

**Lab 6 is due today** (`labs/lab-06/`): classification — k-NN + logistic
regression + one tree, confusion matrices, k/depth sweeps, checkpoint questions.
Push before deadline.

## 10. Common mistakes

- Reporting only test accuracy without the train score → can't see the gap → can't see overfitting.
- Tuning on the test set (peeking) → test no longer honest. Tune on train/validation; test once.
- Choosing `max_depth` by trial while watching test scores — same leak, subtler.
- An unlimited tree "because trees are cool" → classic memorization.
- Believing deeper is always better.
- Forgetting `random_state` → trees differ run to run (they're data-dependent greedy).
- Ignoring `feature_importances_` when asked "which feature matters?"

## 11. Short assessment questions

1. What is the overfitting symptom in terms of train vs. test scores?
2. Name two hyperparameters that limit a tree's complexity.
3. What does `plot_tree` show you that accuracy can't?
4. Why does an unlimited tree achieve ~100% training accuracy?
5. What is the danger of evaluating hyperparameters on the test set?
6. True/False: decision trees need feature scaling like k-NN. (False — trees split per feature, scale doesn't matter.)

## 12. CLO mapping

CLO-2: decision trees complete the "basic classification techniques" set, and
overfitting + hyperparameters are the core *analysis* skill of CLO-2 ("apply
appropriate tools and techniques to solve data-driven problems" — choosing
regularization IS the appropriate-tool skill). Feeds Assignment 2 and Session 22's pipelines.

## 13. Suggested homework

- Commit the activity notebook.
- Practice: rerun the penguins tree with 2 features vs. 4 features; does the tree exploit more features, and does test accuracy change?
- Read: scikit-learn docs — "Decision Trees" page (the tips/classification example).
- Preview: `from sklearn.cluster import KMeans` — Session 21 drops the labels and asks the model to find groups on its own (unsupervised learning).