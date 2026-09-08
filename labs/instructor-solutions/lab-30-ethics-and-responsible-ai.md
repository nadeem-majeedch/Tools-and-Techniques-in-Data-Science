# Lab 30 — Solution: Ethics & Responsible AI

**Session:** W15 S30 · **CLO:** CLO-3

## Complete solution

```python
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

tips = sns.load_dataset("tips")
X = tips[["total_bill"]]
y = tips["tip"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
model = LinearRegression().fit(X_train, y_train)

test = X_test.copy()
test["tip"] = y_test
test["pred"] = model.predict(X_test)
test["abs_err"] = (test["tip"] - test["pred"]).abs()

for group in ["sex", "smoker", "day"]:
    print("---", group)
    print(test.groupby(group)["abs_err"].agg(["mean", "count"]).round(3))
```

## Expected output (approx, seed 42)

- sex: Male MAE ≈ 0.70 (n≈27), Female ≈ 0.66 (n≈22) — small gap.
- smoker: Yes ≈ 0.67 (n≈18), No ≈ 0.70 (n≈31) — small gap.
- day: Thur ≈ 0.62 (n≈15), Fri ≈ 0.80 (n≈6), Sat ≈ 0.73 (n≈17), Sun ≈
  0.62 (n≈11) — largest spread (≈0.18), driven partly by tiny groups
  (Friday n=6).

Reading: the largest gap is by day, but Friday's n=6 makes its MAE noisy —
sample-size trap before any fairness claim.

## Model answers

1. **MAE gap ≠ proof of bias** — check group sizes (a 0.20 gap on n=5 is
   noise), whether the gap persists out-of-sample, and whether the model
   is *used* in a way that harms anyone; differential error alone is a
   signal to investigate, not a verdict.
2. **Small test group** — error metrics are averages; with 3 rows one
   outlier moves the mean enormously, so the estimate has no statistical
   meaning.
3. **Data sheet extras** — provenance, collection purpose, sampling
   method, privacy (identifiers), known biases and limitations — facts
   about *how the data came to be*, which no summary statistics capture.
4. **AI for bug fixes** — yes, under the course policy, if disclosed:
   record the tool, the prompt, and what you verified (that the fix works
   and you understand it).
5. **"Public data = no privacy issue"** — public ≠ anonymous; re-
   identification, sensitive attributes, and terms-of-use restrictions
   still apply; "public" also doesn't cover *your* handling of it.

## Data sheet (model answer — adapt to project)

> **Source & license:** seaborn-built-in Palmer Penguins (CC0, Gorman et
> al. 2014). **Who/why:** collected by researchers measuring penguins on
> three Antarctic islands. **Does not contain:** names, coordinates, or
> any personal identifiers. **Limitations:** only 3 colonies; 11 rows
> missing sex; not a random sample of all penguins.

## AI disclosure (model answer)

| Step | AI used? | What I verified |
|---|---|---|
| Data loading | no | — |
| EDA code | yes (code completion) | every cell ran; outputs cross-checked with describe() |
| Model choice | yes (asked for options) | chose via CV comparison myself |
| Debugging | yes (error explanations) | fixed code re-run green |
| Report writing | yes (drafting) | numbers replaced with my own computed values |

## Challenge solution

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score

Xc = tips[["total_bill", "tip"]]
yc = (tips["smoker"] == "Yes").astype(int)          # 1 = smoker
Xtr, Xte, ytr, yte = train_test_split(Xc, yc, test_size=0.3,
                                      random_state=42, stratify=yc)
knn = KNeighborsClassifier(n_neighbors=5).fit(Xtr, ytr)
print(classification_report(yte, knn.predict(Xte)))
base_acc = accuracy_score(yte, np.zeros_like(yte))  # predict all "No"
print("majority-class baseline acc:", round(base_acc, 3))
# If kNN accuracy ≈ baseline, the model learned little beyond the class
# prior. Next step: class_weight, recall-focused metric, or more features.
```