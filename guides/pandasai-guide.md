# PandasAI Guide

PandasAI lets you **ask questions about a DataFrame in plain English** and
get back an answer plus the pandas code that produced it. It does this by
sending a description of your data (column names and types — *not* your
rows) to a large language model, which writes pandas code that PandasAI then
runs.

## Why it matters in this course

It is the fastest way to prototype an analysis ("average tip by day of
week?") and the clearest illustration of the CLO-3 lesson: **the model
generates code — you are responsible for verifying it.** It is a *drafting*
tool, never a substitute for knowing pandas.

## Setup (once)

```bash
pip install pandasai
# And have a local model available (keeps your data on your machine):
ollama pull llama3.2     # see the LLM & Ollama Guide
```

## Your first query

```python
import seaborn as sns
from pandasai import Agent
from pandasai.llm import OllamaLLM

tips = sns.load_dataset("tips")

# Point PandasAI at your LOCAL model — data stays on your machine
agent = Agent(tips, config={"llm": OllamaLLM(model="llama3.2")})
answer = agent.chat("What is the average tip by day of the week?")
print("ANSWER:", answer)

# Audit step: look at the code the model generated
print("GENERATED CODE:", getattr(agent, "last_code_generated", None))
```

??? tip "No model installed? You can still see how it works"
    Run Ollama first (`ollama pull llama3.2`). If PandasAI or Ollama is not
    available, the cell should print a friendly message instead of crashing —
    guard your code with `try/except` exactly like the course notebooks do
    (see [Notebook 14](../course-notebooks/14-pandasai.ipynb)).

## The verification protocol (non-negotiable)

Every answer gets three checks before you may use it:

1. **Read the generated code** — does it answer the question you actually asked?
2. **Verify one number yourself** with plain pandas:

```python
import pandas as pd
expected = tips.groupby("day")["tip"].mean()
print(expected)                 # compare with what PandasAI printed
```

3. **Log it** — in your README/report: tool + version, the prompt, the
   generated code, and your verification line.

## Common errors

| Error | Cause / fix |
|---|---|
| `No module named pandasai` | `pip install pandasai` (reinstall after a venv change) |
| `connection refused` on port 11434 | Ollama is not running — start it, then `ollama pull llama3.2` |
| Answer differs from your hand-computed number | The model wrote reasonable-looking but wrong code — that is *why* step 2 exists; rerun with a clearer prompt |
| "Code generated, but not executed" style errors | Ask simpler questions; long multi-step requests trip up small local models |
| Your data "leaked" | You pointed PandasAI at a cloud model by default — always set an **Ollama** LLM for non-public data |

## Limitations (be honest about these)

- The model sees the **schema, not the rows** — it cannot reason about data
  quality you haven't told it about.
- Small local models make mistakes on multi-step aggregations and date logic.
- PandasAI's API changes between versions (e.g. `Agent` vs `SmartDataframe`);
  code from tutorials may need small adjustments.
- It is not a replacement for learning pandas — *you cannot verify what you
  cannot read*.

## Responsible AI considerations

- **Privacy:** prefer the local-Ollama path for any non-public data; never
  paste sensitive data into a cloud LLM.
- **Disclosure:** record in your README that PandasAI assisted, with tool
  version and prompt.
- **Don't delegate judgment:** the model suggests an aggregation; *you*
  decide whether it answers the actual question.

## Go deeper

- Full lecture: [Session 26 — PandasAI](../sessions/session-26-pandasai.md)
- Executed notebook: [Notebook 14 — PandasAI](../course-notebooks/14-pandasai.ipynb)
- Practice: [Lab 26 · PandasAI](../labs/lab-26-pandasai.md)
- Teacher's deep dive: [Module C topic 01](../module-c/topic-01-pandasai.md)
