# Content for notebook 20: End-to-end data science project.
CELLS = [
    ("md", """# 20 — End-to-End Data Science Project

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-1 + CLO-2 + CLO-3 — the whole course in one workflow.

Everything so far, in one pipeline: **ask → acquire → clean → explore →
model → communicate**, with an AI-assisted step and an ethics reflection.
This notebook is a template for the final project — adapt it to your own
question and dataset.

**The question we will answer:** can we predict a penguin's *species* from
its measurements, and how does the choice of model change the answer?

---
"""),("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Run a complete data science workflow end-to-end.
2. Justify every cleaning and modeling decision.
3. Compare models honestly with pipelines and cross-validation.
4. Report findings with evidence and stated limitations.
5. Document an AI-assisted step and write a reproducibility + ethics note.

---
"""),("md", """## Step 1 — ASK

A good question is specific, measurable, and answerable with available data:

> *"Can bill length, flipper length, and body mass predict penguin species?
> Which measurements matter most, and how accurate can a simple model be?"*

The answer matters: species identification from measurements is a real
ecology problem (field researchers identify penguins visually; a model could
assist). We will report accuracy **and** its limits.

---
"""),("code", """# Project header - the reproducibility contract of this notebook
#   Question: predict penguin species from measurements
#   Author:   <your name>
#   Date:     <today>
#   Data:     penguins (seaborn) - see datasets/README.md for provenance
#   Reproduce: venv + requirements.txt + Kernel -> Restart & Run All
#   Seeds:    42 everywhere
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

%matplotlib inline
np.random.seed(42)
print("project environment ready")
"""),
    ("md", """## Step 2 — ACQUIRE

Load the data, record where it came from, and do a first inspection. For
your project: same three moves — load, document provenance, look.

---
"""),("code", """df = sns.load_dataset("penguins")
print("source: seaborn built-in (Palmer Archipelago penguin data, CC0)")
print("shape:", df.shape)
print(df.head(3))
"""),
    ("md", """## Step 3 — CLEAN (look → decide → apply → verify)

---
"""),("code", """print("missing before:")
print(df.isna().sum())

# DECIDE: 2 rows missing bill/sex measurements - drop rows missing the
# features we need; the loss (2 of 344 rows) is negligible.
df = df.dropna(subset=["species", "bill_length_mm", "flipper_length_mm", "body_mass_g"])

print("missing after:", df.isna().sum().sum())
print("rows kept:", len(df), "of 344")
"""),
    ("md", """## Step 4 — EXPLORE (the EDA recipe, condensed)

---
"""),("code", """print(df.groupby("species")[["bill_length_mm", "flipper_length_mm", "body_mass_g"]]
        .mean().round(1))

sns.pairplot(df, hue="species", vars=["bill_length_mm", "flipper_length_mm", "body_mass_g"])
plt.show()

# Finding 1: Gentoo differs sharply on flipper length and body mass.
# Finding 2: bill length separates Adelie (short) from Chinstrap/Gentoo (long).
# Implication: these three features should classify species well.
"""),
    ("md", """## Step 5 — MODEL (split once, pipeline, cross-validate, test once)

The honest protocol from notebook 22: lock the test set, compare models with
cross-validation on train, pick a winner, evaluate once on test.

---
"""),("code", """X = df[["bill_length_mm", "flipper_length_mm", "body_mass_g"]]
y = df["species"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

models = {
    "kNN":     make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)),
    "LogReg":  make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "Tree":    DecisionTreeClassifier(max_depth=4, random_state=42),
}

for name, m in models.items():
    cv = cross_val_score(m, X_train, y_train, cv=5)
    print(f"{name:7s} CV accuracy: {cv.mean():.3f} ± {cv.std():.3f}")
"""),
    ("md", """## Step 5b — the winner, evaluated once on test

---
"""),("code", """winner = models["LogReg"].fit(X_train, y_train)
pred = winner.predict(X_test)

print("TEST accuracy:", round(accuracy_score(y_test, pred), 3))
print()
print(classification_report(y_test, pred))
print("Confusion matrix (rows actual, cols predicted):")
print(confusion_matrix(y_test, pred))
"""),
    ("md", """## Step 6 — COMMUNICATE (findings with evidence and limits)

---
"""),("code", """# Finding 1: all three models beat the majority-class baseline by a wide
# margin. The baseline (always predict Adelie) is ~44% here.
baseline = y_train.value_counts(normalize=True).max()
print(f"majority-class baseline: {baseline:.1%}")

# Finding 2: logistic regression reaches ~97% test accuracy; Gentoo is
# perfectly separated, Chinstrap vs Adelie confuse occasionally.
# Finding 3 (limit): the data is small (342 rows) and comes from one
# location - accuracy may not transfer to other penguin colonies.
print("Limitation: small sample, single study site -> report, don't overclaim.")
"""),
    ("md", """## Step 7 — AI-ASSISTED STEP (CLO-3, guarded)

An honest AI-assisted component for this project: use a local model to
*review the findings* — then verify everything against the data. If Ollama
isn't running, the cell prints instructions and the notebook continues; the
verification cells below always run.

---
"""),("code", """import importlib

def module_available(name):
    try:
        importlib.import_module(name)
        return True
    except ImportError:
        return False

if module_available("ollama"):
    import ollama
    try:
        summary = df.groupby("species")[["bill_length_mm", "flipper_length_mm"]].mean().round(1)
        prompt = f\"\"\"
Dataset summary (species-level means): {summary.to_dict()}
My claim: "Gentoo is clearly separable by flipper length and body mass."
Task: is the claim supported? Suggest one follow-up analysis.
\"\"\"
        reply = ollama.chat(model="llama3.2", messages=[
            {"role": "user", "content": prompt}])["message"]["content"]
        print("LLM review:", reply[:300])
        # Disclosure: "AI-assisted review via llama3.2 (local). Every claim
        # below is verified against the data in this notebook."
    except Exception as e:
        print("Ollama not ready:", e)
        print("-> start Ollama + ollama pull llama3.2 for the live review")
else:
    print("ollama client not installed - AI review step skipped")

# Verification (always runs - the numbers are the ground truth):
print(df.groupby("species")["flipper_length_mm"].mean().round(1))
"""),
    ("md", """## Step 8 — REPRODUCIBILITY & ETHICS REFLECTION

---
"""),("code", """# Reproducibility checklist (this notebook passes all):
#   [x] environment: requirements.txt present (see repo root)
#   [x] seeds: np.random.seed(42) + random_state=42 everywhere
#   [x] entry point: this notebook, Restart & Run All
#   [x] relative paths / built-in data: no machine-specific paths
#   [x] AI log: prompt recorded in the AI-assisted cell above

# Ethics checklist:
#   [x] provenance: Palmer penguins, CC0, documented
#   [x] representation: only 3 species, one site - findings may not generalize
#   [x] privacy: no personal data involved
#   [x] communication: limitations stated next to the accuracy number
print("reflection complete - see markdown notes above")
"""),
    ("md", """## Beginner example: the whole course in miniature

Before the exercises, the shortest possible end-to-end: load → clean → one
model → one number.

---
"""),("code", """import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

df = sns.load_dataset("penguins").dropna()
X = df[["bill_length_mm", "flipper_length_mm"]]
y = df["species"]

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
acc = accuracy_score(yte, LogisticRegression(max_iter=1000).fit(Xtr, ytr).predict(Xte))
print("two-feature model test accuracy:", round(acc, 3))
"""),
    ("md", """## Intermediate example: the project template, parameterized

The same workflow as a **reusable function** — swap in your own data and
question. This is the skeleton your final project will grow from.

---
"""),("code", """def run_project(df, features, target, test_size=0.3, seed=42):
    \"\"\"Run the model-comparison core of the project template.\"\"\"
    X = df[features]
    y = df[target]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=test_size,
                                          random_state=seed, stratify=y)
    models = {
        "kNN":    make_pipeline(StandardScaler(), KNeighborsClassifier(5)),
        "LogReg": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
        "Tree":   DecisionTreeClassifier(max_depth=4, random_state=seed),
    }
    results = {}
    for name, m in models.items():
        cv = cross_val_score(m, Xtr, ytr, cv=5)
        results[name] = cv.mean()
        m.fit(Xtr, ytr)
        results[name + "_test"] = accuracy_score(yte, m.predict(Xte))
    return results

results = run_project(df, ["bill_length_mm", "flipper_length_mm", "body_mass_g"], "species")
for k, v in results.items():
    print(f"{k:12s} {v:.3f}")
"""),
    ("md", """## Exercises

---
"""),("md", """### Exercise 1 — Feature ablation

Run the project with only `bill_length_mm`, then with only
`flipper_length_mm`. Which single feature classifies best? (Answer:
flipper length — it separates Gentoo cleanly.)"""),
    ("code", """# your code here
"""),
    ("code", """# Solution
for feature in ["bill_length_mm", "flipper_length_mm"]:
    res = run_project(df, [feature], "species")
    print(feature, "-> test accuracy:", round(res["LogReg_test"], 3))
"""),
    ("md", """### Exercise 2 — Baseline honesty

Compute the majority-class baseline accuracy for the test set and compare it
with the winning model's test accuracy. Write the comparison as a sentence."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
baseline = y_test.value_counts(normalize=True).max()
print(f"baseline {baseline:.1%} vs model {accuracy_score(y_test, pred):.1%} "
      f"-> the model adds {accuracy_score(y_test, pred) - baseline:.1%} over guessing")
"""),
    ("md", """### Exercise 3 — Documentation

Write (in markdown) the "How to reproduce" section for this notebook:
environment, commands, expected outcome."""),
    ("code", """# Answer (markdown):
#   ## How to reproduce
#   1. python -m venv .venv && activate
#   2. pip install -r requirements.txt
#   3. jupyter lab -> open this notebook -> Kernel > Restart & Run All
#   4. Expected: three CV scores ~0.95+, a test accuracy ~0.97,
#      and the figures in Steps 4/5.
print("documentation in markdown")
"""),
    ("md", """## Challenge exercise

Apply the template to a **new dataset**: `sns.load_dataset("titanic")`,
predicting `survived` from `pclass`, `age`, `fare` (clean first!).

1. Clean: drop rows missing those three features.
2. Compare the three models with CV (use `run_project`).
3. Report test accuracy AND the confusion matrix.
4. Write one finding + one limitation (e.g., the training set only includes
   passengers with complete records — who is missing?).
5. Note one ethical consideration: could this model be used to deny
   something? What would you change before deploying it?"""),
    ("code", """# your code here
"""),
    ("code", """# Solution
titanic = sns.load_dataset("titanic").dropna(subset=["survived", "pclass", "age", "fare"])
res = run_project(titanic, ["pclass", "age", "fare"], "survived")
for k, v in res.items():
    print(f"{k:12s} {v:.3f}")

from sklearn.metrics import confusion_matrix
Xtr, Xte, ytr, yte = train_test_split(
    titanic[["pclass", "age", "fare"]], titanic["survived"],
    test_size=0.3, random_state=42, stratify=titanic["survived"])
m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(Xtr, ytr)
print(confusion_matrix(yte, m.predict(Xte)))

# Reflection (markdown):
#   Finding: pclass is the strongest signal; accuracy ~0.8.
#   Limitation: rows with missing age/fare were dropped - the poor are more
#   likely missing fare records, so the training data skews wealthier.
#   Ethics: a "survival predictor" must never be used to allocate scarce
#   resources; report limitations, never deploy unexamined.
"""),
    ("md", """## Recap

- The full loop: **ask → acquire → clean → explore → model → communicate**.
- Model honestly: lock test, CV on train, evaluate once, report baseline.
- Communicate with evidence: findings + limitations, never just numbers.
- AI-assisted steps: guard, document, verify — disclose the prompt.
- Reproducibility: seeds, requirements, entry point, relative paths.
- Ethics: provenance, representation, privacy, and honest limits.

---
"""),
    ("md", """## Questions

1. Order the six lifecycle stages.
2. Why evaluate the test set only once?
3. What does cross-validation add over a single split?
4. Why report the majority-class baseline?
5. What belongs in a "How to reproduce" section?
6. Name one limitation of the penguins model and one of the titanic model.

---
**You have completed the 20-notebook course sequence.** The next step is
your final project — this notebook is its template.
"""),
]