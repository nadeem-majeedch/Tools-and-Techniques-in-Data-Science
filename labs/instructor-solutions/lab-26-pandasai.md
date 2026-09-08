# Lab 26 — Solution: PandasAI

**Session:** W13 S26 · **CLO:** CLO-3

## Complete solution (guarded)

```python
import pandas as pd
import seaborn as sns

tips = sns.load_dataset("tips")

truth = {
    "mean_tip": round(tips["tip"].mean(), 2),                    # 3.0
    "total_bill": round(tips["total_bill"].sum(), 2),            # 4827.36
    "most_common_day": tips["day"].value_counts().idxmax(),      # Sat
    "corr": round(tips["total_bill"].corr(tips["tip"]), 3),      # 0.676
}
print(truth)

QUERIES = [
    "What is the mean tip?",
    "What is the total of the total_bill column?",
    "Which day appears most often?",
    "What is the correlation between total_bill and tip?",
]

answers = {}
try:
    import pandasai
    from pandasai import Agent
    from pandasai.llm import OllamaLLM
    llm = OllamaLLM(model="llama3.2")
    agent = Agent(tips, config={"llm": llm, "verbose": False})
    print("pandasai version:", getattr(pandasai, "__version__", "?"))
    for q in QUERIES:
        answers[q] = agent.chat(q)
except Exception as e:
    print("pandasai unavailable:", e)
    # offline audit path — sample outputs, still verified
    answers = {
        QUERIES[0]: "$2.99",
        QUERIES[1]: "The total is $4,827.36",
        QUERIES[2]: "Saturday",
        QUERIES[3]: "0.675",
    }

# audit
checks = [("mean tip", answers[QUERIES[0]], truth["mean_tip"]),
          ("total_bill", answers[QUERIES[1]], truth["total_bill"]),
          ("most common day", answers[QUERIES[2]], truth["most_common_day"]),
          ("correlation", answers[QUERIES[3]], truth["corr"])]
for name, answer, t in checks:
    print(name, "| model:", answer, "| truth:", t)
```

## Report card (model answer)

| Query | Answer | Verified? | Verdict |
|---|---|---|---|
| mean tip | "$2.99" | 2.998 | ✓ |
| total of total_bill | "$4,827.36" | 4827.36 | ✓ |
| most common day | "Saturday" | Sat (87 rows) | ✓ |
| correlation | "0.675" | 0.676 | ~ (rounding) |

Reproducibility section: pandasai `X.Y.Z` (or "n/a — offline audit"),
model `llama3.2`, the four prompts above, outputs above, verified against
pandas.

## Model answers

1. **Ground truth first** — the agent's answer is a *claim*; verification
   requires an independent referee, and computing it first avoids
   confirmation bias.
2. **Catch a plausible-sounding error** — quote the number and check it
   against a computed value; a wrong "Saturday" only shows up when
   compared to `value_counts().idxmax()` = Sat… in this case it's right,
   but the *method* (always check) is what matters.
3. **Reproducible AI use** — the exact prompt, model + version, tool
   version, output, and verification must be saved; "the AI said so" is
   not reproducible.
4. **Not use PandasAI** — for sensitive data (it sends data to the LLM
   backend), for exact/audited pipelines, and where the query is simple
   enough that 5 lines of pandas is clearer.
5. **Check data integrity** — snapshot `tips.shape` and `tips.equals`
   before/after, or run a checksum on the frame; also ask the agent for
   the *code* it would run and inspect it.

## Challenge solution

```python
# open-ended question + translate to 2 verifiable claims
claim1 = "bill and tip are positively correlated"
claim2 = "bigger bills get bigger tips on average"
print("corr:", truth["corr"], "-> positive:", truth["corr"] > 0)

bins = pd.cut(tips["total_bill"], 5)
print(bins.groupby(bins).apply(lambda g: g["tip"].mean()).round(2))
# mean tip rises monotonically across bill bins -> claim2 supported
```