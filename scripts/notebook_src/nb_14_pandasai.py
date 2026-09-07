# Content for notebook 14: PandasAI.
CELLS = [
    ("md", """# 14 — PandasAI: Natural-Language Data Queries

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-3 — Develop AI-assisted data science workflows.

PandasAI inverts the question: instead of translating "mean tip by day" into
`df.groupby("day")["tip"].mean()`, you **type the question** and it writes —
and runs — the pandas for you. Convenience on top, verification underneath:
the whole lesson of this notebook is the pair.

> **Environment note:** PandasAI needs an LLM behind it. This course uses
> Ollama (a local model) so no API key or cloud account is needed — see the
> setup guide and notebook 16. Every cell that requires PandasAI or a
> running model is guarded: if the tool isn't installed, the cell prints a
> message and the notebook continues.

---
"""),("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Explain how PandasAI works (question → generated pandas → executed).
2. Set it up with a local model (Ollama).
3. Ask questions and read the **generated code** behind the answer.
4. Audit answers: check the code, then verify a number by hand.
5. Keep an **AI log** (question, tool, code, verification) for reproducibility.

---
"""),("md", """## Theory: translator, not oracle

PandasAI sends your question plus the DataFrame's schema to an LLM, which
returns *pandas code*; PandasAI executes that code and shows the result.
Three consequences:

1. The numbers are computed by **pandas** — not hallucinated. Good.
2. But the *question interpretation* can be wrong — a mistranslated filter
   produces a confident, wrong answer. You must read the generated code.
3. It needs an LLM. Cloud models (OpenAI etc.) need API keys and send your
   data to a server; **Ollama runs locally** — private, free, offline.

The API has changed across PandasAI versions (v2: `Agent`; v3: restructured
config). Always check `pip show pandasai` and the docs for your version.

---
"""),("code", """# Guarded availability check — this notebook must run everywhere
import importlib

def module_available(name):
    try:
        importlib.import_module(name)
        return True
    except ImportError:
        return False

print("pandasai installed:", module_available("pandasai"))
print("ollama client installed:", module_available("ollama"))
"""),
    ("md", """## Setup (when pandasai is installed)

```python
# Terminal once: pip install pandasai  (already in requirements.txt)
from pandasai import Agent
from pandasai.llm import OllamaLLM

llm = OllamaLLM(model="llama3.2")      # local model (notebook 16)
agent = Agent(df, config={"llm": llm}) # v2 style — check your version's docs
answer = agent.chat("What is the average tip by day?")
```

The cell below does exactly this on the tips data **if available**; otherwise
it prints the setup you need. When PandasAI is present and Ollama is running
with a pulled model, you will see a real answer.

---
"""),("code", """import pandas as pd
import seaborn as sns

if module_available("pandasai"):
    from pandasai import Agent
    from pandasai.llm import OllamaLLM

    tips = sns.load_dataset("tips")
    try:
        agent = Agent(tips, config={"llm": OllamaLLM(model="llama3.2")})
        answer = agent.chat("What is the average tip by day of the week?")
        print("ANSWER:", answer)
        # Audit step 1: inspect the generated code (attribute varies by version)
        code = getattr(agent, "last_code_generated", None)
        print("GENERATED CODE:", code if code is not None else "(not exposed in this version)")
    except Exception as e:
        print("PandasAI/Ollama not ready:", e)
        print("-> Install: pip install pandasai; run Ollama and: ollama pull llama3.2")
else:
    print("pandasai not installed — install it to run this cell:")
    print("pip install pandasai   (and run Ollama with: ollama pull llama3.2)")
"""),
    ("md", """## The audit: verification protocol

Every `chat()` answer gets three checks — the same protocol as the LLM
notebook:

1. **Read the generated code** — right columns? right filter? right aggregation?
2. **Verify by hand** — compute one number with your own pandas.
3. **Log it** — question, tool + version, generated code, verification.

A wrong-but-plausible answer is worse than no answer. Audit catches it.

---
"""),("code", """import pandas as pd
import seaborn as sns

tips = sns.load_dataset("tips")

# The verification line — works with or without PandasAI:
manual = tips.groupby("day")["tip"].mean().round(2)
print("Hand-verified answer (this is ground truth):")
print(manual)

# If the PandasAI cell above ran, compare its answer to this table.
# Mismatch? The question was mistranslated — rephrase it with constraints:
#   "mean tip grouped by day, only columns day and tip, exclude missing"
"""),
    ("md", """## Beginner example: the whole idea in four lines

---
"""),("code", """import pandas as pd

df = pd.DataFrame({"fruit": ["apple", "banana", "apple"],
                   "price": [80, 30, 90]})

# The PandasAI version (when installed):
#   agent.chat("Which fruit is more expensive on average?")  -> "apple (85.0)"
# The verification version (always available):
print(df.groupby("fruit")["price"].mean())
# Expected output:
#   fruit
#   apple     85.0
#   banana    30.0
#   Name: price, dtype: float64
"""),
    ("md", """## Intermediate example: a documented AI-assisted exploration

The professional pattern: use the assistant for *ideas and drafts*, run and
verify everything yourself, and log what happened. This cell builds the AI
log entry for the penguins exploration — it runs even without PandasAI
because the audit is the point.

---
"""),("code", """import pandas as pd
import seaborn as sns

penguins = sns.load_dataset("penguins").dropna()

# Step 1 — what we WOULD ask the assistant:
#   "Which species has the longest average flipper length?
#    Is there a correlation between bill length and body mass?"
# Step 2 — we run and verify (the ground truth):
print(penguins.groupby("species")["flipper_length_mm"].mean().round(0))
print("corr(bill_length, body_mass) =",
      round(penguins["bill_length_mm"].corr(penguins["body_mass_g"]), 3))

# Step 3 — the AI log entry (markdown, saved to project/ai-notes.md):
#   ## Query 2026-04-14
#   - Question: "Which species has the longest average flipper length?"
#   - Tool: pandasai <version> + OllamaLLM llama3.2
#   - Generated code: <pasted from the agent>
#   - Verified: groupby mean shows Gentoo (218.2 mm) — matches.
"""),
    ("md", """## Exercises

---
"""),("md", """### Exercise 1 — Phrase it better

The question "what about tips on weekends?" is ambiguous. Rewrite it with
constraints (columns, aggregation, filter) so a translator cannot guess
wrong. Write your version in a markdown cell."""),
    ("code", """# Example rewrite (markdown):
#   "Compute the mean tip as a percentage of total bill, grouped by day,
#    using only columns day, tip, total_bill, excluding missing values."
print("see markdown answer above")
"""),
    ("md", """### Exercise 2 — Verify a claim

Ask any LLM tool (or use the pattern above): "how many rows does the tips
dataset have, and what is the max tip?" — then verify both facts yourself
with pandas. Write the verification next to the claim."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
import seaborn as sns
tips = sns.load_dataset("tips")
print("rows:", len(tips), "| max tip:", tips["tip"].max())
"""),
    ("md", """### Exercise 3 — AI log

Create a small AI log (a Python dict or markdown cell) with entries for two
questions you would ask about YOUR project dataset: question, tool, generated
code (or "n/a"), verification result."""),
    ("code", """# your code here
"""),
    ("code", """# Solution — a minimal AI log structure
ai_log = [
    {
        "question": "Which day has the highest mean bill?",
        "tool": "pandasai + llama3.2",
        "generated_code": "n/a (not run)",
        "verified": "run groupby('day')['total_bill'].mean() and compare",
    },
]
print(ai_log)
"""),
    ("md", """## Challenge exercise

Write a **guarded function** `ask_df(agent, question)` that:

1. Calls `agent.chat(question)` if an agent is available.
2. Always prints the verification you should run.
3. Never crashes — catches every exception and returns a helpful message.

Then use it (or simulate it) with three questions about `penguins`, and log
the results. The simulation path must work without PandasAI installed."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
import pandas as pd
import seaborn as sns

def ask_df(agent, question):
    if agent is None:
        print(f"[no agent] Question: {question}")
        print("[no agent] Run manually: groupby/describe on the columns in the question")
        return None
    try:
        answer = agent.chat(question)
        print("ANSWER:", answer)
        return answer
    except Exception as e:
        print("agent failed:", e)
        return None

tips = sns.load_dataset("tips")
questions = [
    "What is the average total bill by day?",
    "How many rows have a tip above 5 dollars?",
    "Which day has the most records?",
]
agent = None  # set to a real PandasAI agent if available
for q in questions:
    ask_df(agent, q)
    # verification runs regardless:
    print("   verify:", q, "->", "run the equivalent pandas line yourself")
"""),
    ("md", """## Recap

- PandasAI = question → **generated pandas code** → executed result.
- The numbers come from pandas; the risk is a **mistranslated question**.
- Audit every answer: read the generated code, verify a number by hand.
- Use a local model (Ollama) to keep data private and costs at zero.
- Keep an **AI log** — it's the reproducibility requirement for AI steps.
- Version differences exist — check `pip show pandasai` and the docs.

---
"""),
    ("md", """## Questions

1. What does PandasAI do with your question, step by step?
2. Why must you audit the generated code even when the answer looks right?
3. Name two things an AI log entry records.
4. Why use `OllamaLLM` instead of a cloud LLM in this course?
5. Why is "tips on weekends?" an ambiguous question, and how do you fix it?
6. True/False: PandasAI computes the numbers itself, so results are always correct.

---
**Next:** notebook 15 — LLM fundamentals.
"""),
]