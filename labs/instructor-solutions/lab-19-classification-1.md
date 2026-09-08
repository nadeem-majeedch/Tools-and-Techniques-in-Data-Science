# Lab 19 — Solution: Classification I

**Session:** W10 S19 · **CLO:** CLO-2

## Complete solution

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
# stratify keeps each species's share in train and test (Adelie ~44%,
# Chinstrap ~20%, Gentoo ~36% in both), so rare classes aren't lost.

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)
print("scaled mean/std:", X_train_s.mean().round(4),
      X_train_s.std().round(4))            # ~0 / ~1

# k-NN sweep
for k in [1, 3, 5, 11, 21]:
    knn = KNeighborsClassifier(n_neighbors=k).fit(X_train_s, y_train)
    print("k =", k, "acc:", round(accuracy_score(y_test,
          knn.predict(X_test_s)), 3))

knn5 = KNeighborsClassifier(n_neighbors=5).fit(X_train_s, y_train)
pred_knn = knn5.predict(X_test_s)
print("kNN-5 acc:", round(accuracy_score(y_test, pred_knn), 3))   # ~0.97

logreg = LogisticRegression(max_iter=1000).fit(X_train_s, y_train)
pred_lr = logreg.predict(X_test_s)
print("logreg acc:", round(accuracy_score(y_test, pred_lr), 3))   # ~0.98

print(pd.DataFrame(confusion_matrix(y_test, pred_lr),
                   index=y_test.cat.categories, columns=y_test.cat.categories))
print(classification_report(y_test, pred_lr))
```

## Expected output

- 233 train / 100 test rows.
- k-NN sweep: k=1 ≈ 0.95 (slightly overfit), k=5 ≈ 0.97, k=11/21 slightly
  lower (~0.95–0.96). Best: k=3–5.
- Logistic ≈ 0.98.
- Confusion matrix: mostly diagonal; Adelie↔Chinstrap confused most often.
- Chinstrap has the lowest recall (hardest class — it overlaps Adelie on
  these two features).

## Model answers

1. **stratify=y** — penguin species are imbalanced; an unlucky random
   split could give the test set almost no Chinstraps, making its accuracy
   meaningless (and recall uncomputable).
2. **Fit scaler on train only** — the scaler's mean/std are learned
   statistics; fitting on all data lets test information influence
   training features (leakage) and flatters scores.
3. **Unscaled k-NN** — k-NN classifies by *distance*; a feature with a
   larger range (flipper 172–231) would dominate a smaller-range feature
   (bill length 32–59), silently down-weighting it.
4. **Recall for costly misses** — if missing a species is expensive, you
   want few false negatives per class; recall = detected/total actual, and
   per-class recall is what a confusion matrix shows.
5. **1-point gap caution** — 100 test rows ⇒ each point ≈ 1% of the
   estimate; a 1-point gap is within sampling noise, so you can't claim a
   real winner without CV (Lab 22).

## Challenge solution

```python
for k in [1, 3, 5, 11, 21]:
    knn = KNeighborsClassifier(n_neighbors=k).fit(X_train, y_train)  # raw
    print("unscaled k =", k, "acc:",
          round(accuracy_score(y_test, knn.predict(X_test)), 3))
# Unscaled k-NN drops a few points because flipper length dominates the
# distance. Logistic regression is barely affected: it fits weighted sums
# (coefficients adapt to scale), so scaling matters less.
```