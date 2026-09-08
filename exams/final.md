# Final Exam — Weeks 9–16 (Sessions 17–32)

**Administered:** W16 S32 · **Time:** 120 minutes · **Closed notes for Parts
I–IV;** open-notebook (no internet) for Part V as specified by the instructor.
**Covers:** intro ML, regression, classification, clustering, pipelines &
cross-validation, reproducible workflows, LLM fundamentals, PandasAI, Ollama,
tool calling & AI agents, n8n automation, ethics & responsible AI, Streamlit.
**CLOs:** CLO-2 and CLO-3 (primary), CLO-1 (reproducibility items).
**Bloom's levels:** Remember–Evaluate · **Difficulty:** Easy–Hard.

Format: Part I MCQ (12 × 2), Part II code tracing (8 × 3), Part III debugging
(5 × 4), Part IV short answer (6 × 3), Part V practical coding (3 × 8), Part
VI scenario & ethics (3 × 6). Total 100. Answers embedded — remove
`**Answer:**`/`**Key:**` lines for the student paper.

---

## Part I — Multiple choice (12 × 2 = 24)

**Q1 (MCQ).** Which is the correct scikit-learn workflow?
a) predict → fit → split → evaluate
b) split → fit → predict → evaluate
c) fit → split → evaluate → predict
d) evaluate → fit → predict → split
**Answer:** b) — split first (test untouched), fit on train, predict on
test, then evaluate. **CLO-2 · Understand · Easy**

**Q2 (MCQ).** `train_test_split(X, y, test_size=0.2, random_state=42)`
with 244 rows gives:
a) 49 test / 195 train rows  b) 20 / 224  c) 42 / 202  d) 200 / 44
**Answer:** a) — 20% of 244 ≈ 48.8 → 49 test, 195 train.
**CLO-2 · Apply · Easy**

**Q3 (MCQ).** What does `random_state` do in scikit-learn?
a) Randomizes the data values.
b) Fixes the random split/initialization so results reproduce.
c) Sets the number of CPU cores.
d) Disables randomness for faster training.
**Answer:** b) — reproducibility of the split/estimator.
**CLO-2 · Understand · Easy**

**Q4 (MCQ).** Accuracy is 0.97, but the classifier never predicts the rare
class. The best next step:
a) Report accuracy 0.97.
b) Check per-class recall and compare with a majority-class baseline.
c) Delete the rare class.
d) Increase test size only.
**Answer:** b) — accuracy hides class imbalance; per-class recall plus a
baseline reveals the failure. **CLO-2 · Analyze · Medium**

**Q5 (MCQ).** Why scale features before k-NN but not before a decision tree?
a) Trees are faster with unscaled data.
b) k-NN uses distances; trees split per-feature on thresholds.
c) Scaling changes tree splits.
d) k-NN ignores scale anyway.
**Answer:** b). **CLO-2 · Understand · Medium**

**Q6 (MCQ).** A pipeline `[("scale", StandardScaler()), ("clf",
LogisticRegression())]` inside `cross_val_score` prevents:
a) overfitting the test set.
b) scaling leakage across CV folds.
c) duplicate rows.
d) NaN errors.
**Answer:** b) — the scaler is refit on each fold's training portion only.
**CLO-2 · Understand · Medium**

**Q7 (MCQ).** In an agent loop, the tool result is returned to the model as:
a) a system prompt  b) a message with role `"tool"`  c) a new user prompt
d) a file
**Answer:** b) — role `"tool"` messages feed the result back into context
so the model can decide the next step. **CLO-3 · Understand · Medium**

**Q8 (MCQ).** Which is the correct order of the agent loop?
a) call → reason → observe → decide
b) reason → propose call → execute → observe → decide
c) execute → reason → decide
d) observe → execute → propose
**Answer:** b). **CLO-3 · Understand · Easy**

**Q9 (MCQ).** Ollama runs models:
a) on a remote server.
b) locally on your machine.
c) in the browser.
d) only in n8n.
**Answer:** b) — local inference after `ollama pull`.
**CLO-3 · Remember · Easy**

**Q10 (MCQ).** In n8n, which node starts a workflow "every morning at 8"?
a) HTTP Request  b) Schedule (cron `0 8 * * *`)  c) Code  d) Webhook
**Answer:** b). **CLO-3 · Remember · Easy**

**Q11 (MCQ).** An automation appends today's weather row to a CSV on every
run. After 10 runs there are 10 rows for the same date. The fix:
a) delete the file each run.
b) make the append idempotent — check the date key before appending.
c) use a random filename.
d) append to a log instead.
**Answer:** b) — idempotency (key check) prevents duplicates.
**CLO-3 · Apply · Medium**

**Q12 (MCQ).** A model has lower MAE for males than females. Before claiming
bias, you must check:
a) the model's accuracy.
b) group sizes and whether the gap holds out-of-sample.
c) the number of features.
d) the learning rate.
**Answer:** b) — small groups make error metrics noisy; sample size and
stability come first. **CLO-3 · Evaluate · Medium**

## Part II — Code tracing (8 × 3 = 24)

**Q13.** What prints?

```python
from sklearn.model_selection import train_test_split
X = [[1], [2], [3], [4]]; y = [1, 2, 3, 4]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.5, random_state=1)
print(len(Xtr), len(Xte))
```

**Answer:** `2 2`. **CLO-2 · Apply · Easy**

**Q14.** The pipeline below is fit on `X_train`. What does the final line
estimate, and what would be wrong if the scaler had been fit on all data?

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
pipe = Pipeline([("scale", StandardScaler()),
                 ("clf", KNeighborsClassifier(n_neighbors=5))])
pipe.fit(X_train, y_train)
print(pipe.score(X_test, y_test))
```

**Answer:** test accuracy of a scaled k-NN; fitting the scaler on all data
would leak test statistics into training (data leakage), flattering the
score. **CLO-2 · Analyze · Medium**

**Q15.** What prints?

```python
import numpy as np
np.random.seed(0)
a = np.random.rand(3)
np.random.seed(0)
b = np.random.rand(3)
print((a == b).all())
```

**Answer:** `True` — the same seed reproduces the same sequence.
**CLO-3 · Apply · Easy**

**Q16.** The transcript shows `user → tool_call → tool result → final
answer`. What is the final answer's origin, and why does that matter?
**Answer:** the answer is generated from the tool result in context, not
from the model's memory; the transcript lets you verify the claimed numbers.
**CLO-3 · Analyze · Medium**

**Q17.** What prints?

```python
tips["tip_pct"] = tips["tip"] / tips["total_bill"] * 100
print(tips.groupby("day")["tip_pct"].median().idxmax())
```

**Answer:** `'Thur'` — Thursday has the highest median tip *percentage*.
**CLO-2 · Apply · Medium**

**Q18.** `cross_val_score(pipe, X_train, y_train, cv=5)` returns
`[0.96, 0.98, 0.97, 0.95, 0.99]`. What do the five numbers represent, and
what is the summary statistic you would report?
**Answer:** one accuracy per fold (fit on 4 folds, scored on the held-out
fold); report mean ± std (≈ 0.97 ± 0.015). **CLO-2 · Apply · Medium**

**Q19.** What does this print?

```python
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X_scaled)
print(km.labels_.shape, len(set(km.labels_)))
```

**Answer:** `(n_samples,)` and `3` (labels per point; at most 3 distinct
labels). **CLO-2 · Apply · Medium**

**Q20.** A workflow JSON contains nodes `schedule`, `http_request`, `code`,
`spreadsheet_file`. Describe the data flow in one sentence.
**Answer:** the schedule triggers an HTTP fetch of weather data; the code
node extracts/aggregates it; the spreadsheet-file node appends the result —
trigger → processing → output. **CLO-3 · Understand · Easy**

## Part III — Debugging (5 × 4 = 20)

**Q21.** `model.fit(X_train, y_train)` raises
`ValueError: Found input variables with inconsistent numbers of samples:
[244, 150]`. What is the most likely cause and how do you confirm it?
**Answer:** `X` and `y` come from different frames/rows (e.g., `y` left
over from another dataset, or one was dropna'd and the other not). Confirm
with `X.shape` and `len(y)`; rebuild both from the same cleaned frame.
**CLO-2 · Analyze · Hard**

**Q22.** Two runs of the same notebook give different CV scores. List two
causes and the fixes.
**Answer:** (1) unseeded split — add `random_state`; (2) unseeded
estimator (e.g., KMeans init) — add `random_state`/`n_init`; also check
data-loading order (e.g., dict iteration) for nondeterminism.
**CLO-3 · Analyze · Medium**

**Q23.** `ollama.chat(model="llama3.2", ...)` raises a connection error
even though the package is installed. What is missing, and the fix?
**Answer:** the Ollama *server* isn't running (or the model isn't pulled);
start the Ollama app, then `ollama pull llama3.2`; guard the call so the
notebook degrades gracefully. **CLO-3 · Analyze · Medium**

**Q24.** Your agent loop hangs forever on a stubborn mock. What is missing
and the fix?
**Answer:** no `max_steps` cap; add `max_steps` (e.g., 6) and return the
transcript when the cap is hit. **CLO-3 · Analyze · Medium**

**Q25.** The README reports 0.96 accuracy but the notebook's last run shows
0.97. Why is this a grading problem and what is the fix?
**Answer:** the deliverable is internally inconsistent — graders can't tell
which number is real; fix by re-running the notebook (Restart & Run All)
and updating the README to match the fresh output.
**CLO-3 · Evaluate · Medium**

## Part IV — Short answer (6 × 3 = 18)

**Q26.** Define precision and recall in plain words. When is recall the more
important metric?
**Answer:** precision = of the items predicted positive, how many were
right; recall = of the actual positives, how many were caught. Recall
matters when missing a positive is costly (e.g., disease detection, fraud).
**CLO-2 · Understand · Medium**

**Q27.** What does the elbow method do, and what are its limits?
**Answer:** plots inertia vs k and picks where the drop flattens; it is a
heuristic — no proof of the "right" k, and it fails when clusters aren't
well-separated or are non-spherical. **CLO-2 · Understand · Medium**

**Q28.** Under the course AI-use policy, list the three requirements and
give one example of each applied to a project deliverable.
**Answer:** disclose (tool + prompt + how used — e.g., a note in the README),
verify (AI code must run and be explainable — re-run and comment), and
respect the no-AI rule for exams/quizzes. **CLO-3 · Understand · Easy**

**Q29.** Why send only aggregated summaries to an LLM instead of raw rows?
Give two reasons.
**Answer:** privacy (nothing identifiable leaves the machine) and prompt
quality (aggregates are small, focused, and harder for the model to
misread than thousands of rows). **CLO-3 · Evaluate · Medium**

**Q30.** Your n8n workflow runs daily; the CSV has one row per day. One
morning the API is down. What should the workflow do, and why is a
`collector-errors.log` the right artifact?
**Answer:** it should log the failure and continue (not crash); a log file
survives unattended runs and gives you the evidence to diagnose the missed
day. **CLO-3 · Apply · Medium**

**Q31.** Name three things that make an analysis reproducible, and explain
how each is verified.
**Answer:** (1) pinned environment — `requirements.txt` + fresh-venv run;
(2) seeded randomness — two consecutive Restart & Run All runs identical;
(3) runnable notebook — top-to-bottom execution with no hidden state.
**CLO-3 · Understand · Medium**

## Part V — Practical coding (3 × 8 = 24)

Open-notebook; write runnable code per task.

**Q32.** On `penguins` (dropna): scale the 4 numeric features, run k-means
with k=3, and print the crosstab of `species` × cluster labels. In one
sentence, state what the crosstab shows. *(CLO-2 · Apply · Medium)*
**Key:**

```python
import seaborn as sns, pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
penguins = sns.load_dataset("penguins").dropna()
X = StandardScaler().fit_transform(
    penguins[["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]])
km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X)
print(pd.crosstab(penguins["species"], km.labels_))
# Sentence: each species concentrates in one cluster (near-diagonal table),
# so the measurements recover the three species without labels.
```

**Q33.** Build a pipeline that scales + fits a `LogisticRegression`, score it
with 5-fold CV on the training split, then fit and report test accuracy on
a held-out split. Use `random_state=42` and `stratify`. *(CLO-2 · Apply ·
Medium)*
**Key:**

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

X = penguins[["bill_length_mm", "flipper_length_mm"]]
y = penguins["species"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2,
                                      random_state=42, stratify=y)
pipe = Pipeline([("scale", StandardScaler()),
                 ("clf", LogisticRegression(max_iter=1000))])
scores = cross_val_score(pipe, Xtr, ytr, cv=5)
print("CV:", scores.mean().round(3), "+/-", scores.std().round(3))
pipe.fit(Xtr, ytr)
print("test acc:", pipe.score(Xte, yte).round(3))
```

**Q34.** Write a guarded `ask(model, question, system="")` helper for a
local model, then use it to ask one question about `tips`, and verify the
answer's key claim against pandas. (If no model is running, print a message
and complete the verification against the provided sample reply.)
*(CLO-3 · Apply · Medium)*
**Key:**

```python
try:
    import ollama
    def ask(model, question, system=""):
        messages = ([{"role": "system", "content": system}] if system else [])
        messages.append({"role": "user", "content": question})
        return ollama.chat(model=model, messages=messages)["message"]["content"]
    reply = ask("llama3.2", "Which day has the highest mean tip?",
                system="Answer with the numbers you used.")
    print(reply)
except Exception as e:
    print("Ollama unavailable:", e)
    reply = "Saturday"          # sample reply for offline verification
import seaborn as sns
tips = sns.load_dataset("tips")
truth = tips.groupby("day")["tip"].mean().idxmax()   # Sun
print("model claim correct:", truth in reply or "Sunday" in reply)
```

## Part VI — Scenario & ethics (3 × 6 = 18)

**Q35.** A teammate trained a model on all the data, then evaluated it on a
random 20% *of the same data*, and reports 99% accuracy. Identify the two
methodological errors and what the honest procedure is.
*(CLO-2 · Analyze · Hard)*
**Answer:** (1) no held-out split — training on all data means "test" rows
were seen during training (memorization); (2) the 20% was drawn from data
already used for training — leakage. Honest procedure: split first, fit on
train only, evaluate once on the untouched test set (ideally with CV on
train for model choice).

**Q36.** Your project uses AI to write EDA code. A reviewer asks for
evidence that the code is trustworthy. List the four things you should show.
*(CLO-3 · Evaluate · Hard)*
**Answer:** (1) the disclosure — tool, prompts, how output was used; (2)
verification — the code runs top-to-bottom and outputs match
hand-computed/known values; (3) understanding — you can explain each step;
(4) reproducibility — environment pins and seeds so the run can be
reproduced.

**Q37.** A company deploys your tip-prediction model, and an audit finds the
model systematically underestimates tips for one demographic. You must
respond. Write the three steps you would take and the ethical principle
each demonstrates. *(CLO-3 · Evaluate · Hard)*
**Answer:** (1) investigate — measure per-group error with adequate sample
sizes (transparency); (2) disclose — report the differential performance to
stakeholders before deployment (accountability); (3) mitigate — reweight/
collect more data/choose a different threshold, and document the decision
(fairness). Any answer naming investigation + disclosure + mitigation with
a consistent principle per step is accepted.

---

## Marking guide

| Part | Max | Items |
|---|---|---|
| I MCQ | 24 | 12 × 2 |
| II Code tracing | 24 | 8 × 3 |
| III Debugging | 20 | 5 × 4 |
| IV Short answer | 18 | 6 × 3 |
| V Practical | 24 | 3 × 8 |
| VI Scenario & ethics | 18 | 3 × 6 |
| **Total** | **100** | |

Bloom's spread: Remember 2, Understand 10, Apply 13, Analyze 10, Evaluate 7.
CLO spread: CLO-1 ≈ 2 (Q25, Q31), CLO-2 ≈ 21 items, CLO-3 ≈ 17 items.