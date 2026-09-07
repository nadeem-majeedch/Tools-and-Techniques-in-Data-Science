# Session 17 — Introduction to Machine Learning

**Week 9 · Session 17 · Module B · 90 min · CLO-2**

## 1. Learning objectives

By the end of this session, students can:
- Explain the difference between traditional programming and machine learning.
- Distinguish supervised (labeled) vs. unsupervised (unlabeled) learning, and regression vs. classification.
- Describe the train/test split and why it exists.
- Train and evaluate a first scikit-learn model end-to-end.
- Identify when a machine learning approach is (and isn't) appropriate.

## 2. Key concepts

- **ML inverts programming:** instead of rules → answers, you give *examples* → rules.
- **Supervised:** data has answers (labels) — you learn the mapping features → label.
- **Unsupervised:** no labels — you find structure (groups, patterns).
- **Regression** predicts a number; **classification** predicts a category.
- **Generalization** — the model must work on *new* data, not just memorized training data.
- **train/test split** simulates "new data" honestly; scikit-learn's uniform API makes every model interchangeable.
- A **baseline** (predict the mean / most common class) must be beaten — otherwise the model is noise.

## 3. Detailed lecture notes

**Why machine learning, why now?** Weeks 1–8 answered "what *is* in this data?"
via EDA. Machine learning answers "what *can we predict* from this data?"
Traditional programming: you write the rule (`if bill > 40: tip = high`).
Machine learning: you provide thousands of (bill, size, day, tip) examples and
the algorithm *finds* the rule. That inversion — data in, rules out — is the
entire idea, and it's why the phrase "learning from data" is literal.

**The learning problem shapes.** Two questions decide everything:
1. Do the examples have **labels** (known answers)?
   - Yes → **supervised** learning.
   - No → **unsupervised** learning (find structure: clusters).
2. What kind of answer do we want?
   - A number (price, score, tip) → **regression**.
   - A category (spam/not, species, churn) → **classification**.
Give the 2×2 with examples from their world: predict GPA (supervised,
regression), detect fraud (supervised, classification), segment customers
(unsupervised, clustering — Session 21).

**Why train/test?** A model that aces its training data may simply have
*memorized* it (overfitting — the theme of Session 20). The only honest test is
data the model never saw. The **train/test split** (typically 80/20) holds out a
slice: fit on train, score on test. If test performance is much worse than train,
the model memorized. This discipline — never judge a model on its training data
— is the first law of applied ML. Randomness in the split: `random_state=42`
makes the split reproducible (the seed habit from Session 6 pays off).

**The scikit-learn API — one uniform pattern.** Every model in scikit-learn
works the same four-step way, which is why the library is the standard:
```python
model = LinearRegression()      # 1. choose a model
model.fit(X_train, y_train)     # 2. learn from training data
y_pred = model.predict(X_test)  # 3. predict on unseen data
score(model)                    # 4. evaluate
```
`X` = feature matrix (2-D), `y` = target (1-D). This uniform API means Sessions
18–22 are all variations of one pattern with different models and metrics.

**The baseline discipline.** Before any model, compute the trivial prediction:
for regression, always predict the mean; for classification, always predict the
most common class. A model that can't beat its baseline adds nothing. This habit
keeps beginners honest and is a rubric item on Assignment 2.

**When NOT to use ML.** If the rule is simple and stable, write the rule. If you
need an explanation a regulator must audit, prefer interpretable models. If the
data is tiny or the question is answered by a `groupby`, don't build a model.
And always: the model is only as good as the data — garbage in, garbage out
(Session 9's lesson, now with consequences).

## 4. Important terminology

- **Machine learning** — algorithms that improve at a task from data/examples.
- **Feature (X)** — input variable(s) used for prediction.
- **Target / label (y)** — the answer we want to predict.
- **Supervised / unsupervised** — with/without labels.
- **Regression / classification** — predict a number / predict a category.
- **Train/test split** — held-out data for honest evaluation.
- **Generalization** — performing well on unseen data.
- **Overfitting** — memorizing training data; test performance drops (Session 20).
- **Baseline** — naive prediction to beat (mean / most common class).
- **`fit` / `predict`** — learn / apply a scikit-learn model.
- **`random_state`** — seed for reproducible splits and models.

## 5. Python examples

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

np.random.seed(42)
df = pd.DataFrame({
    "hours": np.random.uniform(1, 10, 200),
})
df["score"] = 40 + 6 * df["hours"] + np.random.normal(0, 5, 200)  # linear + noise

X = df[["hours"]]
y = df["score"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Test RMSE:", round(np.sqrt(mean_squared_error(y_test, y_pred)), 2))

# Baseline: always predict the training mean
baseline_pred = np.full_like(y_test, y_train.mean())
print("Baseline RMSE:", round(np.sqrt(mean_squared_error(y_test, baseline_pred)), 2))
```

## 6. Beginner example

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 3 features, 2 classes — tiny, but the full pattern
X = [[1, 0], [2, 0], [1, 1], [5, 4], [6, 4], [5, 5]]
y = ["small", "small", "small", "big", "big", "big"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
print("Accuracy:", accuracy_score(y_test, knn.predict(X_test)))
```

Six lines: choose → fit → predict → score. Every model this module is this shape.

## 7. Practical Data Science example

```python
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Question: can bill size + party size predict the tip?
tips = sns.load_dataset("tips")
X = tips[["total_bill", "size"]]
y = tips["tip"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression().fit(X_train, y_train)
pred = model.predict(X_test)

print("MAE: we're off by $", round(mean_absolute_error(y_test, pred), 2), "on average")
print("Baseline MAE: $", round(mean_absolute_error(y_test, [y_train.mean()] * len(y_test)), 2))

# Model coefficients: which feature matters more?
print(pd.Series(model.coef_, index=X.columns))
```

## 8. In-class activity (50 min)

In `notebooks/week-09/session-17-intro-to-ml.ipynb`:

1. **Concept mapping (10 min):** for 6 given problems (churn prediction, product
   recommendation, house price, spam filter, customer segments, GPA), classify
   each: supervised/unsupervised + regression/classification. Class votes.
2. **First model (25 min):** reproduce the tips regression above; change the
   seed and re-split — does the MAE change? (Yes — hence `random_state`.) Plot
   predicted vs. actual tips as a scatter.
3. **Baseline check (15 min):** compute the baseline MAE; write one markdown
   sentence: is the model better than guessing the mean, and by how much?

## 9. Lab exercise

**Lab 5** (due Session 18): `labs/lab-05/` — linear regression & evaluation:
split, fit, predict, compare with baseline, checkpoint questions. Starter:
`labs/lab-05/lab-05-starter.ipynb`.

## 10. Common mistakes

- Evaluating on the *training* set → inflated scores and false confidence.
- Forgetting `random_state` → non-reproducible results across runs.
- Passing `y` as a DataFrame with wrong shape → cryptic errors; keep it 1-D (`df["col"]`, not `df[["col"]]`).
- Skipping the baseline → calling a useless model "good" because the score is above zero.
- Forgetting to drop NaN before training (sklearn refuses silently or errors confusingly).
- Expecting a model to magically fix bad data — the model inherits every cleaning mistake.
- Confusing `fit` (learn) with `predict` (apply).

## 11. Short assessment questions

1. What is the difference between supervised and unsupervised learning?
2. Regression predicts a ___; classification predicts a ___.
3. Why must we evaluate a model on data it has never seen?
4. What does `random_state=42` do in `train_test_split`?
5. What is a baseline, and why compute one?
6. Name the four steps of the scikit-learn pattern in order.

## 12. CLO mapping

CLO-2: this session defines the entire Module B learning problem (tools +
basic ML techniques). The fit/predict/evaluate pattern and baseline discipline
are reused in every later session and in Assignment 2 and the project's
modeling component.

## 13. Suggested homework

- Finish Lab 5 and push before Session 18.
- Read: scikit-learn "An introduction to machine learning" (sklearn.org — Getting Started page, first half).
- Practice: re-run the tips example with only `total_bill` as the feature; how does MAE change? (Fewer features, simpler model — usually slightly worse, but more interpretable.)
- Preview: `model.intercept_` and `model.coef_` from your fit — Session 18 explains what they mean and how to read a regression line.