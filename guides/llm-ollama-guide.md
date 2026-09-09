# LLM & Ollama Guide

Large language models (LLMs) predict the next word — over and over — which is
why they can write sentences, code, and summaries. For data science they are
useful **assistants**: they draft pandas code, explain output, and summarize
findings. They are **not** databases or calculators: everything they say must
be checked against your data.

**Ollama** runs LLMs *locally on your own machine*. No API key, no per-token
billing, no data leaving your computer — at the price of needing a
reasonably modern laptop (a 4–8 GB model like `llama3.2` runs fine on 8 GB
RAM).

## Setup (once)

```bash
# 1. Install Ollama from https://ollama.com (Windows/macOS/Linux installers)
# 2. Pull a model
ollama pull llama3.2

# Test it from the terminal
ollama run llama3.2      # type a question, Ctrl+D to exit

# 3. Python client
pip install ollama
```

## Concepts you will be asked about

| Term | Meaning |
|---|---|
| Token | the unit the model reads/writes (~¾ of a word); longer context = more tokens |
| Temperature | randomness of output: `0` = deterministic-ish, `1` = creative. Set `0` for data work so answers are reproducible |
| System prompt | standing instructions before your question ("You write short, working pandas code…") |
| Hallucination | a confident, wrong statement — the model predicts text, it does not *know* |
| Context window | how much text the model can "see" at once; overflow makes it forget the start |

## Chat from Python

The model has **no memory** — the `messages` list *is* the memory; you resend
the whole conversation every turn.

```python
import ollama

MODEL = "llama3.2"

def ask(system, user, temperature=0):
    """Send one question to the local model and return its text reply."""
    reply = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        options={"temperature": temperature},
    )
    return reply["message"]["content"]

# Example: ask for a first draft of pandas code, then verify it yourself
system = "You write short, working pandas code. Return only code."
user = ("DataFrame `df` has columns: month, sales. "
        "Write code for total sales per month.")
print(ask(system, user))
```

??? tip "Reproducible AI answers"
    Log model name + version (`ollama list`), the exact prompt, temperature,
    and the output — then a teammate (or your future self) can reproduce the
    exchange. This is the course audit-log rule from
    [Session 24](../sessions/session-24-reproducible-workflows.md).

## Hallucinations & how to stay safe

- An LLM does not know facts; it produces text that *sounds* right. "The mean
  is 3.1" from a model is a **claim**, not a result.
- The course rule: **read the output, verify one number by hand with pandas,
  and log the verification.** Never put an unverified model number in a lab,
  assignment, or report.
- Give the model real context (actual column names, actual dtypes) rather
  than asking it to imagine a dataset.

## Common errors

| Error | Cause / fix |
|---|---|
| `connection refused` / "could not connect to Ollama" | Ollama isn't running — start the app or `ollama serve`, then `ollama pull llama3.2` |
| Model downloads slowly or "out of memory" | choose a smaller model (`llama3.2:3b`) or pull at night; close other apps |
| Different answer every run | set `options={"temperature": 0}` |
| Model invents columns | your prompt didn't include the real schema — paste actual column names |
| Slow on a laptop | models without a GPU use the CPU; a 3B model is a good default for class work |

## Privacy

Local Ollama = your data never leaves the machine. Cloud LLMs (ChatGPT,
Claude, Gemini, most API services) process whatever you paste — so the
course rule is: **never paste non-public data into a cloud LLM**, and prefer
Ollama for anything real. (See [Session 30 — Ethics](../sessions/session-30-ethics-and-responsible-ai.md).)

## Go deeper

- Full lectures: [Session 25 — LLMs for Data Science](../sessions/session-25-llms-for-data-science.md) · [Session 27 — Ollama & Local Models](../sessions/session-27-ollama-local-models.md)
- Executed notebooks: [Notebook 15 — LLM Fundamentals](../course-notebooks/15-llm-fundamentals.ipynb) · [Notebook 16 — Ollama with Python](../course-notebooks/16-ollama-with-python.ipynb)
- Practice: [Lab 25](../labs/lab-25-llms-for-data-science.md) · [Lab 27 · Ollama](../labs/lab-27-ollama.md)
- Teacher's deep dives: [Module C topics 02–05](../module-c/topic-02-llm-fundamentals.md)
- Structured JSON output (for feeding model replies into pandas): [Module C topic 06](../module-c/topic-06-structured-outputs.md)
