# Lab 26 — PandasAI: Natural-Language Queries

**Session:** Week 13 · Session 26 · 90 min
**CLO:** CLO-3
**Difficulty:** Advanced

## Learning objectives

By the end of this lab you can:

1. Run natural-language queries on a DataFrame with PandasAI.
2. Audit an AI-generated answer against the data.
3. Handle the "AI is wrong" case with evidence.
4. Document PandasAI usage reproducibly (version, model, prompt, result).

## Problem statement

PandasAI promises "ask your DataFrame in English." Your task: a controlled
audit. Run four queries on `tips`, verify each answer against pandas, and
deliver a report card: for each query — the answer, your verification, and
a verdict. If PandasAI is not installed or no LLM is available, run the
**audit protocol on provided sample outputs** instead (the skills you grade
are the same: verification and documentation).

## Dataset requirements

Seaborn built-in `tips` (244 rows). PandasAI optional — guarded.

## Step-by-step tasks

1. **Ground truth:** compute with pandas: (a) mean tip, (b) total revenue
   (`sum` of total_bill), (c) day with most rows, (d) correlation between
   `total_bill` and `tip`. Record all four.
2. **Try PandasAI** (guarded — see starter code). If it imports and an LLM
   is reachable, run the four queries. Otherwise print
   `"pandasai unavailable — using provided sample outputs"` and continue.
3. **Queries** (write them exactly):
   - "What is the mean tip?"
   - "What is the total of the total_bill column?"
   - "Which day appears most often?"
   - "What is the correlation between total_bill and tip?"
4. **Audit:** for each answer, compare to ground truth; mark ✓/✗/~ and
   quote the numbers. Note the API you used (`Agent` or `SmartDataframe`)
   and its version if importable.
5. **Report card:** a markdown table: query | answer | verified? | verdict.
   Include one sentence on anything surprising.

## Starter code

```python
import pandas as pd
import seaborn as sns

tips = sns.load_dataset("tips")

# 1. ground truth
truth = {
    "mean_tip": round(tips["tip"].mean(), 2),
    "total_bill": round(tips["total_bill"].sum(), 2),
    "most_common_day": tips["day"].value_counts().idxmax(),
    "corr": round(tips["total_bill"].corr(tips["tip"]), 3),
}
print(truth)

# 2. guarded PandasAI
try:
    import pandasai  # noqa
    from pandasai import Agent
    from pandasai.llm import OllamaLLM
    llm = OllamaLLM(model="llama3.2")
    agent = Agent(tips, config={"llm": llm, "verbose": False})
    print("pandasai ready; version:", getattr(pandasai, "__version__", "?"))
    # agent.chat("What is the mean tip?")  -> uncomment per query
except Exception as e:
    print("pandasai unavailable:", e)
    print("-> using provided sample outputs")
```

```text
# Provided sample outputs (audit these when no LLM is available)
Q1 mean tip            -> "$2.99"
Q2 total of total_bill -> "The total is $4,827.36"
Q3 most common day     -> "Saturday"
Q4 correlation         -> "0.675"
```

## Expected output

- Ground truth printed: mean tip 2.998; total_bill 4827.36; most common
  day **Sat**; correlation 0.676.
- A guarded cell that either runs PandasAI or degrades with a clear
  message.
- Report card: Q1 ✓, Q2 ✓ (if the sample: 4827.36 ✓), Q3 ✓ (Sat), Q4 ✓
  (~0.675–0.676). If a real model answers differently, the ✗ verdict must
  cite the pandas number.
- A documented "what I ran" section: pandasai version (or "n/a"), model,
  the four prompts, and the answers.

## Questions

1. Why is the *first* step computing ground truth, not asking the agent?
2. The agent answers "Saturday" for most common day. What verification
   would catch an error that still *sounds* right?
3. What does "reproducible AI use" require beyond saving the answer?
4. When would you NOT use PandasAI even though it is installed?
5. How would you check that the agent didn't quietly delete or alter data?

## Challenge task

Ask one **open-ended** question ("summarize the relationship between bill
size and tip") and, without trusting it, translate the summary into two
verifiable claims. Verify both with pandas (e.g., correlation sign and a
binned means table: `pd.cut(tips["total_bill"], 5).groupby(...)["tip"].mean()`).
Add both verifications to your report card.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Ground truth computed | 4 | all four values |
| Guarded PandasAI setup | 4 | import guard + message |
| Four queries run/recorded | 4 | prompts in report |
| Audit verdicts per query | 6 | correct ✓/✗ with numbers |
| Report card table | 4 | query/answer/verified/verdict |
| Reproducibility section | 4 | version + model + prompts |
| Answers to questions | 4 | Q1, Q2, Q5 correct |
| Challenge: open-ended audit | 6 | 2 claims verified |
| **Total** | **36** | |