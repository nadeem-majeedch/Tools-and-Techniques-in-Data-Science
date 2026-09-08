# Lab 25 — LLMs for Data Science

**Session:** Week 13 · Session 25 · 90 min
**CLO:** CLO-3
**Difficulty:** Advanced

## Learning objectives

By the end of this lab you can:

1. Write task-specific prompts for analysis questions (system + context).
2. Evaluate an LLM's answer against ground truth you computed yourself.
3. State when an LLM helps and when it is the wrong tool.
4. Keep an AI-use log with prompts, models, and verification results.

## Problem statement

You are told to "use AI to speed up your EDA." Your job is to do it
**safely**: run a small, well-scoped experiment — ask a model (local via
Ollama if available, otherwise use the provided sample outputs below) to
describe the tips dataset, then **verify every claim it makes** against
pandas. The deliverable is a short AI log: prompt → model reply → your
verification → verdict (correct / partially correct / wrong).

## Dataset requirements

Seaborn built-in `tips` (244 rows). Ground-truth values you compute
yourself with pandas.

## Step-by-step tasks

1. **Ground truth first:** compute with pandas: mean tip, mean tip by day,
   correlation of `total_bill` with `tip`, and the smoker split
   (`value_counts(normalize=True)`). Record these numbers — they are your
   referee.
2. **Write the prompt** (markdown cell): include the dataset description
   (columns, 244 rows) and ask three specific questions: (a) "what is the
   mean tip?", (b) "which day has the highest mean tip?", (c) "does being a
   smoker appear to affect tip size?" — plus a request to answer with the
   numbers it used.
3. **Ask a model** (guarded — see starter code). If no model is
   available, use the **provided sample reply** below and treat it as the
   model's answer.
4. **Verify:** for each of the three claims, mark ✓ / ✗ / ~ (correct /
   wrong / close) against your ground truth. Cite the numbers.
5. **Verdict:** write one paragraph: would you ship this answer to a
   stakeholder without checking? Why?
6. **AI log:** a markdown table with columns: question, model used,
   reply (truncated), verified?, verdict.

## Starter code

```python
import pandas as pd
import seaborn as sns

tips = sns.load_dataset("tips")

# 1. ground truth (compute, print, and KEEP for later comparison)
print("mean tip:", round(tips["tip"].mean(), 2))
print(tips.groupby("day")["tip"].mean().round(2))
print("corr bill-tip:", round(tips["total_bill"].corr(tips["tip"]), 3))
print(tips["smoker"].value_counts(normalize=True).round(3))
```

```python
# 3. guarded model call (Ollama; skips cleanly if unavailable)
try:
    import ollama
    prompt = "tips dataset, 244 rows, columns: total_bill, tip, sex, smoker, day, time, size. Answer with numbers: (a) mean tip? (b) day with highest mean tip? (c) does smoker affect tip size?"
    reply = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    print(reply["message"]["content"])
except Exception as e:
    print("Ollama unavailable:", e)
    print("-> use the provided sample reply for this lab")
```

```text
# Provided sample reply (use when no model is available)
(a) The mean tip is about $2.99.
(b) Saturday has the highest mean tip.
(c) Smokers tip slightly less on average, but the difference is small.
```

## Expected output

- Ground truth printed: mean tip ≈ 2.998; highest mean tip day = **Sat**
  (≈ 3.10); correlation ≈ 0.676; smokers ≈ 38.2% of rows.
- Prompt written with dataset context and a "show your numbers" request.
- Model reply recorded (real or sample).
- Verification table: (a) ✓, (b) depends — the sample reply is **wrong**
  (Sat vs Sun ≈ 3.25 — your verdict table must say so), (c) ~ or ✓
  depending on the reply.
- AI log with all 6 columns filled.

## Questions

1. Why compute ground truth *before* asking the model?
2. The sample reply says Saturday; the real answer is Sunday. What in the
   prompt could have helped the model get this right? (Hint: ask for the
   numbers.)
3. When would you trust an LLM summary without checking?
4. What belongs in an AI-use log for a graded assignment?
5. Name one analysis task where an LLM is the *wrong* tool.

## Challenge task

Add a fourth question: "write the pandas code that computes mean tip by
day." Ask the model (or use the sample below), then **run its code** in
this notebook against `tips`. Report: did the code run, and did it produce
the right answer?

```text
# Provided sample code (use when no model is available)
tips.groupby("day")["tip"].mean()
```

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Ground truth computed first | 4 | all four values |
| Prompt with context + numbers request | 3 | criteria met |
| Model call / sample reply recorded | 3 | in AI log |
| Verification table (✓/✗/~ per claim) | 5 | catches the Sat/Sun error |
| Verdict paragraph | 3 | shipping judgment |
| AI log table complete | 4 | 6 columns |
| Answers to questions | 4 | Q1, Q2, Q4 correct |
| Challenge: run the model's code | 4 | ran + correct/not |
| **Total** | **30** | |