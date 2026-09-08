# Lab 19 — Classification I: k-NN & Logistic Regression

**Session:** Week 10 · Session 19 · 90 min
**CLO:** CLO-2
**Difficulty:** Intermediate

## Learning objectives

By the end of this lab you can:

1. Train and evaluate k-NN and logistic regression classifiers.
2. Read a confusion matrix and compute accuracy/precision/recall.
3. Explain the effect of `k` and of feature scaling on k-NN.
4. Compare two classifiers on the same split, honestly.

## Problem statement

A marine lab needs an automatic species ID from two measurements:
`bill_length_mm` and `flipper_length_mm`. Two candidate models (k-NN and
logistic regression) must be compared **on the same train/test split**,
with the same random state, and the winner reported with evidence — not
vibes.

## Dataset requirements

Seaborn built-in `penguins`, `dropna()` (333 rows). Target: `species`
(3 classes). Features: `bill_length_mm`, `flipper_length_mm`.

## Step-by-step tasks

1. **Prep:** dropna, define `X` (2 features) and `y` (species). Split
   test_size=0.3, random_state=42, `stratify=y` — comment on why
   stratify matters with 3 classes.
2. **Scale:** fit `StandardScaler` on **train only**; transform train and
   test. Print the mean/std of the scaled train features (should be ≈0/1).
   Comment: why must the scaler learn from train only?
3. **k-NN:** `KNeighborsClassifier(n_neighbors=5)`; fit, predict, print
   `accuracy_score`. Then try `k` in [1, 3, 5, 11, 21] and print a small
   table of test accuracy per k. Which k wins?
4. **Logistic regression:** `LogisticRegression(max_iter=1000)`; fit,
   predict, print accuracy.
5. **Confusion matrix:** `confusion_matrix(y_test, pred)` for the *better*
   model; print it with `pd.DataFrame(cm, index=y_test classes,
   columns=y_test classes)`. Which pair of species gets confused most?
6. **Per-class report:** `classification_report(y_test, pred)` — report
   precision, recall, and f1 for each species. Which class is hardest to
   get right?
7. **Verdict (markdown):** which model wins, by how much, and would you
   trust the difference? (Consider that a 1–2 point accuracy gap on 100
   test rows is not decisive.)

## Starter code

```python
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             classification_report)

penguins = sns.load_dataset("penguins").dropna()
X = penguins[["bill_length_mm", "flipper_length_mm"]]
y = penguins["species"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# your code here: k-NN sweep, logistic regression, matrix, report, verdict
```

## Expected output

- Split: 233 train / 100 test rows.
- Scaled train features: mean ≈ 0, std ≈ 1.
- k-NN: accuracy ≈ 0.94–0.98 at k=5; the sweep shows k=1 overfits
  slightly, larger k slightly worse.
- Logistic regression accuracy ≈ 0.95–0.99.
- Confusion matrix mostly diagonal; Chinstrap↔Adelie are the most confused
  pair.
- `classification_report`: Chinstrap typically has the lowest recall.
- A written verdict naming the winner and its margin.

## Questions

1. Why does `stratify=y` matter with 3 classes and 344 rows?
2. Why must `StandardScaler` be fit on train only? What leaks if you fit
   on all data?
3. What happens to k-NN if features are unscaled and one has a much larger
   range?
4. Accuracy vs recall: which would you watch if missing a penguin species
   were costly? Why?
5. Two models differ by 1 accuracy point on 100 test rows — why be
   cautious about declaring a winner?

## Challenge task

Repeat the k-NN sweep **without** scaling and print the same table. Then
answer: how much does scaling change k-NN accuracy here, and why does it
matter less for logistic regression? (Hint: think about what each algorithm
computes — distances vs. weighted sums.)

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Prep + stratified split | 3 | 233/100 + comment |
| Scaling on train only | 4 | mean≈0/std≈1, no leakage |
| k-NN sweep table | 4 | best k identified |
| Logistic regression + accuracy | 3 | max_iter noted |
| Confusion matrix read | 3 | confused pair named |
| classification_report read | 3 | hardest class named |
| Written verdict | 3 | winner + margin + caution |
| Answers to questions | 3 | Q2, Q3, Q4 correct |
| Challenge: unscaled comparison | 4 | table + explanation |
| **Total** | **30** | |