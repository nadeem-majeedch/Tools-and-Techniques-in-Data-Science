# Lab 20 — Solution: Decision Trees & Overfitting

**Session:** W10 S20 · **CLO:** CLO-2

## Complete solution

```python
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score

penguins = sns.load_dataset("penguins").dropna()
X = penguins[["bill_length_mm", "flipper_length_mm"]]
y = penguins["species"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

# unlimited tree
tree = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
print("unlimited train acc:", round(accuracy_score(y_train, tree.predict(X_train)), 3))
print("unlimited test acc:", round(accuracy_score(y_test, tree.predict(X_test)), 3))
# ~1.00 vs ~0.93 — the overfitting gap

# depth sweep
for depth in [1, 2, 3, 5, 10, None]:
    t = DecisionTreeClassifier(max_depth=depth, random_state=42).fit(X_train, y_train)
    print(depth, "-> train", round(accuracy_score(y_train, t.predict(X_train)), 3),
          "test", round(accuracy_score(y_test, t.predict(X_test)), 3))

# final tree
final = DecisionTreeClassifier(max_depth=3, random_state=42).fit(X_train, y_train)
print("final test acc:", round(accuracy_score(y_test, final.predict(X_test)), 3))
print(pd.Series(final.feature_importances_, index=X.columns))
print(export_text(final, feature_names=list(X.columns)))
```

## Expected output

- Unlimited: train ≈ 1.00, test ≈ 0.93 — gap is the overfitting symptom.
- Depth sweep: test accuracy rises to depth 3–5 (~0.96–0.97) then flattens
  or drops; depth 10 ≈ depth 3–5 (no gain, more complexity).
- Final (depth 3): test ≈ 0.96; importance: flipper ≈ 0.7–0.9.
- export_text first rule ≈ "flipper_length_mm ≤ 206.5 → ...".

## Model answers

1. **Unlimited tree memorizes** — with no depth/leaf limits the tree can
   isolate single training points, reaching 100% train accuracy while
   generalizing poorly (high variance).
2. **max_depth limits** — the maximum number of nested decisions from root
   to leaf; depth 3 means at most 3 feature checks per prediction.
3. **Train/test gap as symptom** — the model fits training noise; its
   performance on unseen data (test) diverges from training, and the gap
   size tracks how much memorization is happening.
4. **No scaling needed** — trees split on *thresholds* per feature
   ("flipper ≤ 206.5"), so each feature is considered on its own scale;
   distances between features are never compared.
5. **Explainable trade-off** — in regulated settings (credit, medical),
   stakeholders must understand decisions; a slightly less accurate but
   inspectable model is often the responsible choice.

## Challenge solution

```python
from sklearn.model_selection import GridSearchCV

param_grid = {"max_depth": [2, 3, 4, 5], "min_samples_leaf": [1, 2, 5]}
gs = GridSearchCV(DecisionTreeClassifier(random_state=42),
                  param_grid, cv=5).fit(X_train, y_train)
print("best params:", gs.best_params_)
print("best CV score:", round(gs.best_score_, 3))
print("test acc:", round(accuracy_score(y_test, gs.predict(X_test)), 3))
# e.g. {'max_depth': 3, 'min_samples_leaf': 2} — comparable to the manual
# pick; tuning formalizes the search instead of hand-picking.
```