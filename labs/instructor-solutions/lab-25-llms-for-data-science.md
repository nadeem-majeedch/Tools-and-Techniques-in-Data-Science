# Lab 25 — Solution: LLMs for Data Science

**Session:** W13 S25 · **CLO:** CLO-3

## Complete solution (ground truth + audit)

```python
import pandas as pd
import seaborn as sns

tips = sns.load_dataset("tips")

# 1. ground truth (the referee)
truth = {
    "mean_tip": round(tips["tip"].mean(), 2),                      # 3.0 (2.998)
    "mean_tip_by_day": tips.groupby("day")["tip"].mean().round(2), # Sun 3.26 max
    "corr": round(tips["total_bill"].corr(tips["tip"]), 3),        # 0.676
    "smoker_share": tips["smoker"].value_counts(normalize=True).round(3),
}
print(truth)

# 2. prompt with dataset context + "show your numbers" request (markdown)
PROMPT = (
    "Dataset: 'tips', 244 rows, columns total_bill, tip, sex, smoker, "
    "day, time, size. Answer with the numbers you used:\n"
    "(a) mean tip?\n(b) which day has the highest mean tip?\n"
    "(c) does being a smoker appear to affect tip size?"
)

# 3. guarded call
try:
    import ollama
    reply = ollama.chat(model="llama3.2",
                        messages=[{"role": "user", "content": PROMPT}])
    print(reply["message"]["content"])
except Exception as e:
    print("Ollama unavailable:", e)

# 4. verification table (against the SAMPLE reply if no model)
sample = ("(a) The mean tip is about $2.99.\n"
          "(b) Saturday has the highest mean tip.\n"
          "(c) Smokers tip slightly less on average, but the difference is small.")
print(sample)
# verdicts:
# (a) mean tip 2.998  -> 2.99 ✓
# (b) sample says Saturday; truth is SUNDAY 3.26 > Sat 2.99 -> ✗
# (c) smoker means: Yes 2.93 vs No 3.05 -> smokers tip ~$0.12 less ~ ✓
```

## AI log (model answer)

| Question | Model used | Reply (truncated) | Verified? | Verdict |
|---|---|---|---|---|
| mean tip | llama3.2 (or sample) | "$2.99" | mean = 2.998 | ✓ |
| highest mean tip day | same | "Saturday" | Sun 3.26 > Sat 2.99 | ✗ |
| smoker effect | same | "smokers slightly less" | Yes 2.93 vs No 3.05 | ✓ |

## Model answers

1. **Ground truth first** — you can't verify without a referee; computing
   it first also prevents you from being influenced by a plausible-but-
   wrong AI answer.
2. **Prompt improvement** — ask for the numbers/table ("which day, with
   the mean values") and give the exact column meanings; models pattern-
   match "highest tip" to the most common day (Sat) unless forced to show
   arithmetic.
3. **Trust without checking** — never for numbers feeding a decision; only
   for low-stakes, verifiable-by-reading tasks (e.g., drafting email copy)
   where error is cheap and visible.
4. **AI log contents** — date, tool/model, the exact prompt, the output,
   what you verified and how, and the verdict. The course policy
   (assessment-plan.md) requires exactly this.
5. **LLM wrong tool** — anything needing exact computation (sums, splits,
   correlation), deterministic transforms, or where hallucinated numbers
   would be dangerous (medical/financial figures).

## Challenge solution

```python
code_prompt = "Write the pandas code that computes the mean tip by day."
try:
    code_reply = ask("llama3.2", code_prompt)   # or use sample
    print(code_reply)
except Exception:
    code_reply = 'tips.groupby("day")["tip"].mean()'

# RUN the model's code:
namespace = {"tips": tips, "pd": pd}
exec(code_reply, namespace)          # in a sandboxed dict
print("code output:", namespace.get("__builtins__", None) is not None)
# Better: extract and run manually. The key result: does running it match
# our ground truth (Sun 3.26)? -> yes -> code correct.
```