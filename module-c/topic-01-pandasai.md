# Module C · Topic 01 — PandasAI: Natural Language over Dataframes

**CLO-3 · Maps to:** Session 26 · Notebook 14 · Lab 26 · **Level:** Beginner

---

## 1. Beginner explanation

PandasAI lets you ask a dataframe questions in plain English and get an
answer back. Instead of writing `tips.groupby("day")["tip"].mean()`, you
type *"What is the average tip by day of the week?"*. Under the hood, a
language model (here a **local** Ollama model, so your data never leaves
your machine) writes the pandas code for you, Python runs it, and PandasAI
shows you the result. Think of it as a *pair programmer that speaks pandas
fluently but still needs you to check its work*.

## 2. Conceptual explanation (the WHY)

PandasAI is not magic and it is not a calculator. It is a **translation
layer**:

1. Your question goes to an LLM, along with the dataframe's column names and
   types (the *schema*).
2. The LLM returns **pandas code** — e.g. `df.groupby('day')['tip'].mean()`.
3. PandasAI **executes that code locally** on the real dataframe.
4. You get the result.

Two consequences matter. First, the model never sees your data rows — only
column names and types — which is why it can work with local models
privately. Second, the answer is only as good as the generated code: if the
model misreads the question, you get a *correct-looking wrong answer*. That
is why the course verification protocol (read → verify by hand → log) is
mandatory for every `chat()` call.

## 3. Simple diagram

```text
 You type: "Average tip by day?"
                 │
                 ▼
        ┌──────────────────┐
        │  LLM (Ollama)    │  sees only: column names + types
        │  llama3.2        │
        └────────┬─────────┘
                 │ writes pandas code
                 ▼
        ┌──────────────────┐
        │ Python executes  │  runs on YOUR dataframe (data stays local)
        │ the code         │
        └────────┬─────────┘
                 ▼
        "day   tip
         Thur  2.77
         Fri   2.73
         ..."      <-- YOU must verify this against real data
```

## 4. Python examples

```python
import importlib

def module_available(name):
    """True if a package is installed (so examples degrade gracefully)."""
    try:
        importlib.import_module(name)
        return True
    except ImportError:
        return False

import pandas as pd
import seaborn as sns

if module_available("pandasai"):
    from pandasai import Agent
    from pandasai.llm import OllamaLLM

    tips = sns.load_dataset("tips")

    try:
        # Point PandasAI at your LOCAL model — data never leaves the machine
        agent = Agent(tips, config={"llm": OllamaLLM(model="llama3.2")})
        answer = agent.chat("What is the average tip by day of the week?")
        print("ANSWER:", answer)

        # Audit step 1: look at the code the model generated
        code = getattr(agent, "last_code_generated", None)
        print("GENERATED CODE:", code if code is not None else "(not exposed in this version)")
    except Exception as e:
        print("PandasAI/Ollama not ready:", e)
        print("-> pip install pandasai ; run Ollama ; ollama pull llama3.2")
else:
    print("pandasai not installed — install it to run this cell:")
    print("pip install pandasai   (and run Ollama with: ollama pull llama3.2)")
```

**The verification line — works with or without PandasAI:**

```python
import pandas as pd
import seaborn as sns

tips = sns.load_dataset("tips")

# Ground truth, computed by hand with plain pandas:
manual = tips.groupby("day")["tip"].mean().round(2)
print(manual)

# If the PandasAI answer above differs from this table, the question was
# mistranslated. Rephrase with constraints:
#   "mean tip grouped by day, columns day and tip only"
```

## 5. Practical exercise (25 min)

Dataset: `sns.load_dataset("titanic")`.

1. Ask PandasAI: *"Survival rate by passenger class."*
2. **Read the generated code.** Does it compute `mean` of `survived`
   grouped by `class`? Or something subtly different?
3. Verify by hand with `titanic.groupby("class")["survived"].mean()`.
4. Now ask a *vague* question: *"Who survived?"* and observe how bad
   answers come from bad questions.
5. Write the audit log entry: question, model, generated code, hand-check,
   verdict (✓ / ✗).

## 6. Common errors

| Error | Why it happens | Fix |
|---|---|---|
| `ImportError: pandasai` | package not installed | `pip install pandasai` |
| `Connection refused` / "Ollama not running" | server not started | start Ollama, `ollama pull llama3.2`, retry |
| Plausible-looking wrong number | LLM misread the question | rephrase with constraints; verify by hand |
| "answer is a code block" | model returned code, not result | ask for a number/table explicitly; check the agent version |
| Question too vague ("show me the data") | no task specified | say what to compute and for which groups |

## 7. Limitations

- **No guarantee of correctness** — the output is code an LLM *guessed*;
  hallucinated column names produce errors, mistranslated questions produce
  wrong-but-plausible numbers.
- **Schema-only vision** — PandasAI does not reason over row values; subtle
  questions (outliers, units) are easily missed.
- **Small models, simple questions** — `llama3.2` handles one-step
  aggregations well and multi-step reasoning poorly.
- **Version churn** — PandasAI's API changed between versions (import paths,
  `Agent` vs `SmartDataframe`); code from tutorials may need adjusting.
- **Not a replacement for learning pandas** — you cannot verify what you
  cannot read.

## 8. Responsible AI considerations

- **Verification is mandatory**: every answer is checked against hand-computed
  pandas before it goes in any report.
- **Privacy**: because PandasAI with Ollama keeps data local, prefer it for
  any non-public data. Never paste sensitive data into a cloud LLM.
- **Disclosure**: record in the README/report that PandasAI assisted, with
  tool version and prompt.
- **Don't delegate judgment**: the model suggests an aggregation; you decide
  whether it answers the actual business question.

## 9. Assessment questions

**Q1.** What exactly does the LLM inside PandasAI see about your dataframe?
*(CLO-3 · Understand · Easy)*
**Answer:** column names and types (the schema), not the rows — which is why
local models can be used without leaking the data itself.

**Q2.** PandasAI says the average tip on Saturday is 3.03. Your own
`groupby("day")["tip"].mean()` says 2.99. What is the most likely cause and
what do you do? *(CLO-3 · Evaluate · Medium)*
**Answer:** the model mistranslated the question (wrong filter/grouping).
Do not trust the answer; rephrase with explicit constraints, re-run, and
re-verify. Log the mismatch.

**Q3.** Why is PandasAI "not a replacement for learning pandas"? Give one
reason. *(CLO-3 · Evaluate · Medium)*
**Answer:** you must be able to read and verify the generated code; without
pandas skills you cannot detect a plausible wrong answer.

**Q4.** Your dataframe contains student grades. Is it acceptable to paste the
whole dataframe into a free public LLM chat to "clean it"? *(CLO-3 ·
Evaluate · Medium)*
**Answer:** No — that sends private data to a third party. Use the local
Ollama path (data stays on the machine) or anonymize first.