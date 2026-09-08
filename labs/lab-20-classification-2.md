# Lab 20 — Classification II: Decision Trees & Overfitting

**Session:** Week 10 · Session 20 · 90 min
**CLO:** CLO-2
**Difficulty:** Intermediate

## Learning objectives

By the end of this lab you can:

1. Train a decision tree and explain what it learned.
2. Diagnose overfitting from the train/test accuracy gap.
3. Control complexity with `max_depth` and `min_samples_leaf`.
4. Compare a tree to k-NN/logistic regression from Lab 19 on the same data.

## Problem statement

Your Lab 19 models worked — but the team wants an *explainable* model, and
someone suggests a decision tree. Trees can memorize the training data
perfectly while failing on new data. You must demonstrate this overfitting
curve, then tame it with depth limits, and report a final, honest accuracy
comparison against the Lab 19 models.

## Dataset requirements

Same as Lab 19: penguins (dropna), 2 features, 3 species, same split
(test_size=0.3, random_state=42, stratify).

## Step-by-step tasks

1. **Prep (reuse Lab 19):** load, dropna, split, scale (trees don't need
   scaling — but keep X unscaled for them; comment on this).
2. **Unlimited tree:** `DecisionTreeClassifier(random_state=42)`; fit;
   print **train** accuracy and **test** accuracy. The gap is the
   overfitting signal — report both numbers.
3. **Depth sweep:** for `max_depth` in [1, 2, 3, 5, 10, None], fit and
   record (train_acc, test_acc). Print a table. Where does test accuracy
   stop improving?
4. **Pick a depth** that maximizes test accuracy (with a tie-break toward
   simpler); fit the final tree.
5. **Feature importances:** print `pd.Series(tree.feature_importances_,
   index=X.columns)`. Which feature does the tree lean on?
6. **Explainability:** `export_text(tree, feature_names=list(X.columns))`
   and print it. In one sentence, describe the tree's first rule in plain
   English (e.g., "if flipper length ≤ 206, look at bill length next").
7. **Verdict:** compare final test accuracy with the Lab 19 numbers
   (k-NN ≈ 0.94–0.98, logistic ≈ 0.95–0.99). Is the tree competitive? What
   does it buy you that the others don't?

## Starter code

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

# your code here: unlimited tree, depth sweep, final tree, importances,
#                 export_text, verdict
```

## Expected output

- Unlimited tree: train accuracy ≈ 1.00, test ≈ 0.90–0.95 — the gap is
  real and visible.
- Depth sweep: test accuracy climbs to max_depth 3–5, then flattens or
  drops; a table with both columns shown.
- Final tree: test accuracy ≈ 0.93–0.97 at the chosen depth.
- Importances: `flipper_length_mm` dominant (≈ 0.7–0.9).
- `export_text` output printed; first rule stated in English.
- Verdict vs. Lab 19 numbers, with a sentence on explainability.

## Questions

1. Why can an unlimited tree reach 100% train accuracy, and why is that
   bad?
2. What exactly does `max_depth` limit?
3. Why is the train/test gap the *symptom* of overfitting?
4. Why don't decision trees need feature scaling (unlike k-NN)?
5. When would you prefer a slightly less accurate but explainable model?

## Challenge task

Use `GridSearchCV` (or a manual loop) over `max_depth` ∈ {2, 3, 4, 5} ×
`min_samples_leaf` ∈ {1, 2, 5} with 5-fold CV on the **training set only**.
Print the best parameters and the corresponding test accuracy. Compare with
your manual pick from task 4 — did tuning beat hand-picking?

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Unlimited tree gap reported | 4 | both accuracies stated |
| Depth sweep table | 5 | correct trend + chosen depth |
| Final tree + importances | 4 | flipper dominant |
| export_text + plain-English rule | 4 | rule correct |
| Verdict vs Lab 19 | 3 | comparison + explainability point |
| Answers to questions | 3 | Q1, Q4, Q5 correct |
| Challenge: grid search | 5 | best params + test accuracy |
| **Total** | **28** | |