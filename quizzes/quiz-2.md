# Quiz 2 — Weeks 8–14 (Sessions 15–28)

**Administered:** W15 S29, session start · **Time:** ~25 minutes · **Closed notes**
**Covers:** EDA workflow, intro to ML, regression, classification, clustering,
pipelines & cross-validation, reproducible workflows, LLM fundamentals, PandasAI,
Ollama, tool calling & AI agents, Streamlit dashboards.
**CLOs:** CLO-2 (ML), CLO-3 (AI-assisted), CLO-1 (EDA/reproducibility).

Every question carries three tags: **CLO**, **Bloom's level**, **difficulty**.
Remove the `**Answer:**` lines to produce a student paper.

---

## A. EDA workflow

**Q1.1 (Conceptual).** Why run the data-quality pass (missing values,
duplicates, dtypes) *before* plotting?
**Answer:** plots and stats silently mislead on dirty data (e.g., an object
column blocks `.corr()`), and missingness itself is a finding worth
documenting first. **CLO-1 · Evaluate · Medium**

**Q1.2 (Code tracing).** `penguins.select_dtypes("number").corr()` — what
does `select_dtypes` do and why is it required before `.corr()`?
**Answer:** it returns only numeric columns; `.corr()` needs numeric input —
object columns (species, sex) would otherwise break or be silently dropped.
**CLO-1 · Apply · Easy**

**Q1.3 (Scenario).** A histogram of `body_mass_g` shows two clear peaks.
What does bimodality suggest, and what single group-by would test it?
**Answer:** the sample is a mixture of subpopulations (e.g., species);
test with `df.groupby("species")["body_mass_g"].mean()` or a boxplot by
species. **CLO-1 · Analyze · Medium**

## B. Intro to ML & the uniform workflow

**Q2.1 (MCQ).** Why do we evaluate on a held-out test set instead of the
training data?
a) Test data is easier to predict.
b) Training accuracy rewards memorization, not generalization.
c) Test sets are larger.
d) The model performs better on new data by design.
**Answer:** b) — a model can memorize training data; only unseen data shows
whether it learned a general rule. **CLO-2 · Understand · Easy**

**Q2.2 (MCQ).** Which problem is *unsupervised classification*?
a) Predicting house prices from features.
b) Grouping customers by behavior with no labels.
c) Labeling emails spam/not-spam.
d) Predicting churn from historical labels.
**Answer:** b) — no labels → unsupervised; "classification" with labels is
supervised. **CLO-2 · Understand · Easy**

**Q2.3 (Code tracing).** What is wrong with this evaluation, and what does
it actually measure?

```python
model.fit(X_train, y_train)
print(accuracy_score(y_train, model.predict(X_train)))
```

**Answer:** it measures *training* accuracy, which overstates quality; the
honest number comes from `X_test`/`y_test`. **CLO-2 · Analyze · Medium**

**Q2.4 (Conceptual).** What is a baseline prediction, and why compute it
before celebrating a model's score?
**Answer:** the trivial prediction (mean for regression, most-common class
for classification); a model that can't beat it adds no value, so the
baseline defines "good" for the problem. **CLO-2 · Understand · Medium**

## C. Regression

**Q3.1 (MCQ).** R² = 0.76 for a model predicting body mass. What does it
mean?
a) 76% of predictions are correct.
b) 76% of the variance in body mass is explained by the model.
c) The model is wrong 24% of the time.
d) 76% of points lie on the regression line.
**Answer:** b) — R² is explained variance, not accuracy.
**CLO-2 · Understand · Medium**

**Q3.2 (Code tracing).** The coefficient for `size` is ≈ 0.19 in a model
`tip ~ total_bill + size`. Interpret it in one sentence.
**Answer:** holding total_bill constant, each additional person is
associated with ≈ $0.19 more tip. **CLO-2 · Apply · Medium**

**Q3.3 (Debugging).** Adding `bill_depth_mm` raises train R² but lowers
test R². What is happening, and what would you do?
**Answer:** overfitting — the feature fits training noise that doesn't
generalize. Action: drop the feature (or regularize); judge by test/CV
score, not train. **CLO-2 · Analyze · Medium**

**Q3.4 (Scenario).** Residuals have mean ≈ 0 but standard deviation ≈ 260 g.
What can you conclude — and what can you *not* conclude?
**Answer:** can conclude: no systematic bias (errors cancel). Cannot
conclude: the model is good (the spread is still large) or that the
relationship is linear. **CLO-2 · Evaluate · Medium**

## D. Classification

**Q4.1 (MCQ).** Which metric should you watch when missing a rare class is
expensive?
a) accuracy  b) per-class recall  c) training loss  d) number of features
**Answer:** b) — recall per class shows how many true positives of each
class are caught; accuracy hides failures on rare classes.
**CLO-2 · Apply · Medium**

**Q4.2 (Code tracing).** A confusion matrix is mostly diagonal with one
off-diagonal block (Adelie ↔ Chinstrap). What does that tell you?
**Answer:** those two classes are frequently confused — their feature
spaces overlap; the model can't reliably separate them with the given
features. **CLO-2 · Analyze · Medium**

**Q4.3 (Debugging).** k-NN accuracy drops sharply when you stop scaling the
features. Explain why k-NN is scale-sensitive (unlike a decision tree).
**Answer:** k-NN classifies by distance; an unscaled feature with a large
range (flipper 172–231) dominates the distance and down-weights others.
Trees split per-feature on thresholds, so scale doesn't matter.
**CLO-2 · Understand · Medium**

**Q4.4 (Conceptual).** An unlimited decision tree hits 100% training
accuracy but ~90% test accuracy. Name the phenomenon, the two symptoms you
just quoted, and one control.
**Answer:** overfitting — train ≫ test. Controls: `max_depth`,
`min_samples_leaf`, cross-validation. **CLO-2 · Analyze · Easy**

**Q4.5 (Scenario).** Two classifiers differ by 1 accuracy point on a 100-row
test set. Can you declare a winner? Justify.
**Answer:** No — 1 point ≈ 1 row; that's within sampling noise. Use
cross-validation (mean ± std) and/or a larger test set before deciding.
**CLO-2 · Evaluate · Medium**

## E. Clustering

**Q5.1 (MCQ).** Why scale features before k-means?
a) To make the data smaller.
b) k-means uses Euclidean distance; a large-range feature dominates.
c) To convert categorical to numeric.
d) To reduce k.
**Answer:** b) — distance-based; scaling gives every feature equal say.
**CLO-2 · Understand · Easy**

**Q5.2 (Conceptual).** What does `kmeans.inertia_` measure, and why does it
always decrease as k grows? How does that make the elbow a heuristic?
**Answer:** sum of squared distances from points to their centers; more
clusters always let points sit closer to a center, so inertia falls
monotonically. The elbow (where the drop flattens) is a judgment call, not a
proof of the "right" k. **CLO-2 · Understand · Medium**

**Q5.3 (Code tracing).** You ran k-means with `random_state` unset, twice,
and got different clusterings. Explain why and the one-line fix.
**Answer:** k-means starts from random centers and can hit local optima;
fix: `KMeans(n_clusters=k, random_state=42, n_init=10)` (also stabilizes
via multiple restarts). **CLO-2 · Apply · Medium**

## F. Pipelines & cross-validation

**Q6.1 (MCQ).** Why must `StandardScaler` be fit on the training data only?
a) It makes training faster.
b) Fitting on all data leaks test information into training features.
c) The scaler needs labels.
d) It is not required.
**Answer:** b) — the scaler's mean/std are learned statistics; fitting on
the full data lets test-set information influence training (data leakage).
**CLO-2 · Understand · Medium**

**Q6.2 (Conceptual).** Explain, step by step, what `cross_val_score(pipe,
X_train, y_train, cv=5)` does.
**Answer:** splits `X_train` into 5 folds; for each fold, fits the pipeline
on the other 4 and scores on the held-out fold; returns 5 scores. Because
the scaler is inside the pipeline, it is refit per fold — no leakage.
**CLO-2 · Understand · Medium**

**Q6.3 (Scenario).** CV score is 0.97 but the final test score is 0.88.
Give two plausible explanations.
**Answer:** (1) small/noisy test set — the single split is unlucky; (2)
distribution shift between train and test data; (3) the model was tuned on
CV but the gap reveals instability. **CLO-2 · Analyze · Medium**

## G. Reproducible workflows

**Q7.1 (Conceptual).** Why pin exact versions in `requirements.txt`
(`numpy==2.0.1`) instead of `numpy>=2.0`?
**Answer:** a future release can change behavior or results; exact pins let
any machine recreate the environment that produced the numbers.
**CLO-3 · Understand · Easy**

**Q7.2 (Debugging).** A notebook prints different model accuracy on every
run. List three likely causes.
**Answer:** (1) no `random_state` in `train_test_split`; (2) unseeded
`np.random` data generation; (3) unseeded estimators (e.g., KMeans) or
nondeterministic training order. **CLO-3 · Analyze · Medium**

## H. LLM fundamentals

**Q8.1 (MCQ).** What is the purpose of a *system prompt*?
a) To store the model's weights.
b) To set persistent instructions (role, constraints, format) before the
   user's request.
c) To increase the token limit.
d) To verify the model's answer.
**Answer:** b) — system prompts steer behavior; they are instructions, not
verification. **CLO-3 · Understand · Easy**

**Q8.2 (Scenario).** You ask an LLM "which day has the highest mean tip?"
and it answers "Saturday." The correct answer is Sunday. What is the most
likely cause, and how would you change your prompt to reduce this class of
error?
**Answer:** the model pattern-matched without computing; improve by asking
for the numbers/table ("list the mean tip per day and state the max") and by
verifying the reply against pandas yourself. **CLO-3 · Evaluate · Medium**

**Q8.3 (Conceptual).** Under the course AI-use policy, name the three
requirements for using AI on a graded deliverable.
**Answer:** (1) disclose — tool, prompt, and how output was used;
(2) verify — AI-produced code must run and you must understand it;
(3) exams/quizzes are excluded unless stated otherwise.
**CLO-3 · Understand · Easy**

## I. PandasAI

**Q9.1 (Code tracing).** PandasAI's `Agent.chat("What is the mean tip?")`
returns "$2.99". What must you do *before* trusting or reporting that
number?
**Answer:** compute the ground truth yourself (`tips["tip"].mean()`) and
compare; log prompt, tool version, model, and verification result.
**CLO-3 · Evaluate · Medium**

**Q9.2 (Scenario).** Your data contains personal identifiers. Why might you
choose *not* to use cloud-based PandasAI even though it is installed?
**Answer:** queries (and the data behind them) can be sent to an external
LLM backend; with sensitive data use local models (Ollama) or plain pandas.
**CLO-3 · Evaluate · Medium**

## J. Ollama

**Q10.1 (MCQ).** What does `ollama pull llama3.2` do?
a) Installs the Ollama app.
b) Downloads the model weights to your machine for offline use.
c) Uploads your data to a server.
d) Starts a web server.
**Answer:** b) — pull fetches model weights locally; inference then runs on
your machine. **CLO-3 · Understand · Easy**

**Q10.2 (Scenario).** You plan to send project summaries to a local model.
What exactly leaves your machine, and why is it a privacy improvement?
**Answer:** only the text you send (aggregates, summaries) — raw data never
leaves the machine and no third-party server is involved; still verify
answers and be aware of app telemetry/logging. **CLO-3 · Evaluate · Medium**

## K. Tool calling & AI agents

**Q11.1 (MCQ).** In a tool-calling loop, who executes the tool?
a) The LLM.
b) Your code, after the model proposes a tool call.
c) The model's provider.
d) The dataset.
**Answer:** b) — the model proposes; your code validates and executes, then
returns the result as a message. This is the safety property.
**CLO-3 · Understand · Medium**

**Q11.2 (Code tracing).** The agent loop transcript shows:
`user → tool_call(tip_by, {"by": "day"}) → tool result → final answer`.
Why is the tool result returned to the model as a message?
**Answer:** the model's context must include what the tool returned, or it
cannot reason about the next step; the transcript also makes the chain
auditable. **CLO-3 · Apply · Medium**

**Q11.3 (Scenario).** Your agent loop has no `max_steps`. A stubborn mock
keeps requesting tool calls forever. What is the risk and the fix?
**Answer:** an infinite loop / runaway cost; fix: cap steps (`max_steps=6`)
and return "max steps reached" with the transcript. **CLO-3 · Analyze · Medium**

## L. Streamlit dashboards

**Q12.1 (MCQ).** In a Streamlit app, what does `@st.cache_data` do?
a) Saves your data to GitHub.
b) Caches the decorated function's output so reruns (and widgets) don't
   recompute it.
c) Converts pandas to SQL.
d) Deletes duplicate rows.
**Answer:** b) — it memoizes function results, which keeps interactive
apps fast and avoids re-fetching data on every widget interaction.
**CLO-3 · Understand · Medium**

**Q12.2 (Conceptual).** You build a Streamlit dashboard for a non-technical
manager. Give one design choice that would make it trustworthy and one that
would make it misleading.
**Answer:** trustworthy — show the chart's source and sample size, label
axes, state the metric's definition; misleading — hiding missing data,
using a truncated y-axis, or presenting correlation as causation.
**CLO-3 · Evaluate · Medium**

---

## Marking guide (suggested)

| Item | Points |
|---|---|
| Q1.1–Q12.2 (36 questions) | 2 each = 72 |
| **Total** | **72** |

Bloom's spread: Understand ≈ 13, Apply ≈ 9, Analyze ≈ 8, Evaluate ≈ 6.
CLO spread: CLO-1 ≈ 6, CLO-2 ≈ 17, CLO-3 ≈ 13.