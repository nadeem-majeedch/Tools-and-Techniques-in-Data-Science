# Session 19 — Classification I: k-NN and Logistic Regression

**Week 10 · Session 19 · Module B · 90 min · CLO-2**

## 1. Learning objectives

By the end of this session, students can:
- Explain classification and the difference from regression.
- Fit and evaluate k-NN and logistic regression with scikit-learn.
- Read a confusion matrix and compute accuracy, precision, recall, and F1.
- Choose the right metric when classes are imbalanced.
- Split classification data with `stratify` to keep class proportions.

## 2. Key concepts

- **Classification predicts a category** — the output is a class (or class probabilities).
- **k-NN:** predict by majority vote of the k nearest training examples — no training phase, instance-based.
- **Logistic regression:** despite the name, a *classifier* — it models the probability of a class.
- **Confusion matrix:** TN/FP/FN/TP — the four outcomes that define every metric.
- **Accuracy can lie:** with 95% non-spam, a "always say non-spam" model is 95% accurate. Precision/recall tell the real story.
- **`stratify=y`** keeps rare classes present in both train and test.

## 3. Detailed lecture notes

**Why classification?** Many decisions are categorical: spam or not, fraud or
not, churn or stay, penguin species. Regression's line doesn't fit — you need a
*decision boundary* in feature space. This session covers two very different
classifiers: one dead-simple (k-NN) and one that builds on regression ideas
(logistic regression). Their contrast teaches the general principle: different
models, same scikit-learn pattern.

**k-NN — the "look at your neighbors" model.** A new point is classified by the
majority class among its k nearest training examples (Euclidean distance).
k=3, five nearest... intuition: similar examples tend to share labels. Two
consequences to teach: (1) there is **no real training** — fitting just stores
the data, predictions are computed on the fly (fast to train, slow to predict on
big data); (2) **scale matters** — a feature measured in millions dominates
distance; features must be scaled (Session 21's `StandardScaler`, previewed
here). Choosing k: small k = sensitive to noise (overfit); large k = smoother,
blurrier boundaries (underfit). Demo with iris: plot two features, color by
species, see the regions.

**Logistic regression — probabilities, not lines.** Despite the name it's a
classifier. Instead of predicting 0/1 directly, it models *probability*:
`p(class) = 1 / (1 + e^-(b0 + b1·x1 + ...))` — the sigmoid squashes any number
into (0, 1). Predict class 1 when p ≥ 0.5. Why useful? (a) You get a calibrated
probability ("65% chance this email is spam") — often more actionable than a
hard label; (b) coefficients are readable like linear regression (positive
coefficient → higher class probability); (c) it's fast and works well on clean,
moderate-sized data. `predict_proba()` returns the probabilities — show it,
since it's the killer feature of this model. (Skip the gradient-descent math;
the sigmoid picture suffices.)

**The confusion matrix — where all metrics live.** For a binary problem there
are four outcomes:
- **TP** — predicted spam, actually spam (correct hit).
- **TN** — predicted not-spam, actually not-spam.
- **FP** — predicted spam, actually not (false alarm; Type I error).
- **FN** — predicted not-spam, actually spam (missed; Type II error).
Metrics as ratios: **accuracy** = (TP+TN)/all; **precision** = TP/(TP+FP) — of
all *predicted* spam, how many were right?; **recall** = TP/(TP+FN) — of all
*actual* spam, how many did we catch?; **F1** = harmonic mean of precision and
recall. Which matters? It depends on the cost of each error: for spam, missing
real spam (FN) is tolerable, so recall isn't critical; for cancer screening,
missing a case (FN) is catastrophic — maximize recall; for fraud alerts,
annoying customers with false alarms (FP) is costly — precision matters. Teach
the trade-off story; the formulas follow from it.

**Why accuracy isn't enough.** 95% non-spam data → "always predict non-spam"
gets 95% accuracy and zero value. Always compare against the **baseline**
(Session 17): most-common-class accuracy. Any classifier worth using must beat
it. Also report the confusion matrix, not just one number.

**Stratified splits.** `train_test_split(..., stratify=y)` preserves class
proportions in both halves. Without it, a rare class can vanish entirely from
the test set by chance — then the confusion matrix lies. Make it a default habit
for classification.

## 4. Important terminology

- **Class / label** — the category to predict.
- **Decision boundary** — the region boundary between predicted classes in feature space.
- **k-NN** — k-nearest neighbors; majority vote of k nearest examples.
- **Logistic regression / sigmoid** — probabilistic classifier; `1/(1+e^-z)` squeezes scores into (0,1).
- **`predict_proba`** — class probabilities output.
- **Confusion matrix** — TN/FP/FN/TP counts.
- **Precision** — TP/(TP+FP); **recall** — TP/(TP+FN); **F1** — their harmonic mean.
- **Accuracy** — (TP+TN)/all; unreliable on imbalanced data.
- **Class imbalance** — very unequal class frequencies.
- **`stratify`** — preserve class proportions in the split.
- **Feature scaling** — standardizing features so distances are fair (full treatment Session 21).

## 5. Python examples

```python
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

iris = sns.load_dataset("iris")
X = iris[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
y = iris["species"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

# --- k-NN ---
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
print("k-NN accuracy:", round(accuracy_score(y_test, knn.predict(X_test)), 3))

# --- Logistic regression (multinomial by default for 3 classes) ---
logreg = LogisticRegression(max_iter=1000)
logreg.fit(X_train, y_train)
pred = logreg.predict(X_test)
print("LogReg accuracy:", round(accuracy_score(y_test, pred), 3))

print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred))

# Probabilities: how confident is the model?
print(logreg.predict_proba(X_test[:3]).round(2))
print(logreg.classes_)
```

## 6. Beginner example

```python
from sklearn.neighbors import KNeighborsClassifier

# Two features, two classes: tall vs short
X = [[1.5], [1.6], [1.8], [1.9]]
y = ["short", "short", "tall", "tall"]

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)
print(knn.predict([[1.7]]))   # 'tall' — 2 of 3 nearest neighbors are tall
```

k-NN is just this: look at the closest examples, take a vote.

## 7. Practical Data Science example

```python
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score

# Question: can we predict penguin species from bill + flipper measurements?
penguins = sns.load_dataset("penguins").dropna()

X = penguins[["bill_length_mm", "flipper_length_mm"]]
y = penguins["species"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
pred = model.predict(X_test)

print(confusion_matrix(y_test, pred))
# For a multi-class problem, precision/recall are computed per class;
# classification_report shows all three:
from sklearn.metrics import classification_report
print(classification_report(y_test, pred))

# Confidence matters: which predictions were uncertain?
proba = model.predict_proba(X_test)
uncertain = (proba.max(axis=1) < 0.7).sum()
print("Predictions with <70% confidence:", uncertain)
```

## 8. In-class activity (50 min)

In `notebooks/week-10/session-19-classification-1.ipynb`:

1. **k-NN exploration (20 min):** on iris, try `k` = 1, 3, 5, 20; record accuracy
   on train and test. Watch: k=1 nails training but wobbles on test; large k
   smooths. Write the trend you observe.
2. **Confusion matrix reading (15 min):** print the matrix for the penguins
   model; identify which species pair is most confused and hypothesize why
   (look at the EDA pairplot from Session 14).
3. **Metric choice (15 min):** invent a scenario (fraud detection vs. cancer
   screening); pick the metric to optimize and justify in two sentences.

## 9. Lab exercise

**Lab 6** (due Session 20): `labs/lab-06/` — classification: k-NN and logistic
regression on a labeled dataset, confusion matrix + classification report,
k-tuning exercise, checkpoint questions.

## 10. Common mistakes

- Reporting accuracy alone on imbalanced data (95% "always no" problem).
- Not using `stratify` → rare classes missing from test.
- Forgetting to scale features for k-NN → distance dominated by big-number features.
- Confusing precision and recall — anchor with the story (precision = how many flagged are real; recall = how many real were flagged).
- Reading the confusion matrix backwards (rows are actual, columns are predicted in sklearn — verify with labels).
- Calling logistic regression "regression" in reports — it's a classifier.
- `max_iter` warnings on logistic regression — bump `max_iter=1000` or scale features.

## 11. Short assessment questions

1. How does k-NN decide the class of a new point?
2. What does `predict_proba` return that `predict` doesn't?
3. Write the four cells of a confusion matrix and define precision and recall in words.
4. In cancer screening, which error (FP or FN) is worse, and which metric should you maximize?
5. Why does k=1 often overfit?
6. What does `stratify=y` do in `train_test_split`?

## 12. CLO mapping

CLO-2: classification with k-NN and logistic regression is the second "basic
machine learning technique" — plus the evaluation toolkit (confusion matrix,
precision/recall) used by every later classifier, Assignment 2, and the project.

## 13. Suggested homework

- Finish Lab 6 and push before Session 20.
- Practice: swap k-NN and logistic regression on the penguins model; which wins and by how much? Why might that be?
- Read: scikit-learn docs — "Metrics and scoring: quantifying the quality of predictions" (skim precision/recall/F1 sections).
- Preview: `from sklearn.tree import DecisionTreeClassifier; plot_tree(...)` — Session 20 covers decision trees, overfitting, and hyperparameter tuning.