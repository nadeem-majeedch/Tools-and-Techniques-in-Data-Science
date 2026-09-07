# Content for notebook 16: Ollama with Python.
CELLS = [
    ("md", """# 16 — Ollama with Python

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-3 — Develop AI-assisted data science workflows (local models).

Ollama runs LLMs **on your machine**: private, free, offline after the model
is downloaded. This notebook connects Python to a local model — the engine
behind every AI step in this course.

> **Setup (once):** install from https://ollama.com, then in a terminal:
> `ollama pull llama3.2`. Cells that need a running server are guarded — if
> Ollama isn't running, they print a message and the notebook continues.

---
"""),("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Explain what Ollama is and why local models matter (privacy, cost, offline).
2. Pull and list models from the terminal.
3. Chat with a local model from Python (`ollama.chat`).
4. Use system prompts to steer behavior.
5. Compare local vs. cloud honestly.

---
"""),("md", """## Theory: local vs cloud — the trade-off

| | Local (Ollama) | Cloud (ChatGPT, Gemini) |
|---|---|---|
| Data stays on your machine | yes | no |
| Cost | free | per-usage / subscription |
| Offline | yes | no |
| Model size | limited by your RAM | frontier-scale |
| Capability on hard reasoning | good, not best | best |

The professional skill is **matching model to task**: private or simple tasks
→ local; frontier-hard tasks where data policy allows → cloud. Most of what
data work needs (translating a question into pandas, explaining an error,
summarizing) is well within a small local model's reach.

---
"""),("code", """import importlib

def module_available(name):
    try:
        importlib.import_module(name)
        return True
    except ImportError:
        return False

print("ollama python client installed:", module_available("ollama"))
"""),
    ("md", """## Chat from Python: the three-line API

The client is minimal: `ollama.chat(model, messages)` where messages are a
list of `{"role": ..., "content": ...}`. Roles: `"system"` (instructions),
`"user"` (the request), `"assistant"` (previous replies, in longer
conversations).

---
"""),("code", """import ollama

def chat(model, question, system=""):
    \"\"\"Ask a local model; returns the reply text.\"\"\"
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": question})
    resp = ollama.chat(model=model, messages=messages)
    return resp["message"]["content"]

try:
    reply = chat("llama3.2", "Say hello in one short sentence.")
    print(reply)
except Exception as e:
    print("Ollama not running or model missing:", e)
    print("-> start Ollama, then: ollama pull llama3.2")
"""),
    ("md", """## System prompts: steer the behavior

The same question with different system prompts produces very different
answers. Log the system prompt with the answer — it's part of the AI log.

---
"""),("code", """systems = {
    "concise": "Answer in one sentence.",
    "teacher": "Explain like I am 15 years old.",
    "formatter": "Answer as a bullet list.",
}

question = "What is a train/test split?"

for name, sys_prompt in systems.items():
    try:
        reply = chat("llama3.2", question, system=sys_prompt)
        print(f"--- {name} ---")
        print(reply[:200])
        print()
    except Exception as e:
        print(f"--- {name} --- skipped:", e)
"""),
    ("md", """## Local models behind PandasAI

Notebook 14's `OllamaLLM` is just a wrapper around the same API. This cell
shows the connection — and the guarded pattern used all course long.

---
"""),("code", """# The PandasAI connector (from notebook 14) uses exactly the API above:
#   from pandasai.llm import OllamaLLM
#   llm = OllamaLLM(model="llama3.2")
# Guarded, because pandasai may not be installed:
if module_available("pandasai"):
    from pandasai.llm import OllamaLLM
    print("OllamaLLM available:", OllamaLLM is not None)
else:
    print("pandasai not installed - OllamaLLM lives in pandasai.llm")
"""),
    ("md", """## Beginner example: model not found, handled

A common first-run error is asking for a model that isn't pulled. The fix is
one command — and a guard so your notebook never dies on it.

---
"""),("code", """import ollama

try:
    reply = ollama.chat(model="llama3.2", messages=[
        {"role": "user", "content": "What is 2 + 2?"},
    ])
    print(reply["message"]["content"])
except Exception as e:
    print("Error:", e)
    print("Fix: run 'ollama pull llama3.2' in a terminal, then re-run.")
"""),
    ("md", """## Intermediate example: local review of your EDA

The privacy payoff, made concrete: send your *findings text* (not raw rows)
to a local model — nothing leaves your machine.

---
"""),("code", """import seaborn as sns
import pandas as pd

penguins = sns.load_dataset("penguins").dropna()
mean_mass = penguins.groupby("species")["body_mass_g"].mean().round(0)

findings = f\"\"\"
Dataset: penguins. Mean body mass (g) per species: {mean_mass.to_dict()}.
Claim: Gentoo penguins are much heavier than the other species.
Task: is the claim supported? Suggest one follow-up analysis.
\"\"\"

try:
    reply = chat("llama3.2", findings)
    print(reply[:300])
except Exception as e:
    print("Ollama not available:", e)

# Ground truth, verified without any LLM:
print("\\nGround truth:", mean_mass.to_dict())
print("Claim supported:", mean_mass["Gentoo"] > mean_mass[["Adelie", "Chinstrap"]].max())
"""),
    ("md", """## Exercises

---
"""),("md", """### Exercise 1 — Terminal basics

In a terminal (not in this notebook): run `ollama list` and `ollama ps`.
What models are pulled? Which is loaded? Note the answers in markdown."""),
    ("code", """# Terminal commands (run outside this notebook):
#   ollama list   -> downloaded models
#   ollama ps     -> currently loaded model
print("see terminal - ollama list / ollama ps")
"""),
    ("md", """### Exercise 2 — System prompt comparison

Compare "Explain pandas groupby in one sentence" with and without a
teacher-style system prompt (use the `chat` helper, guarded). Write which
version you'd show a classmate."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
try:
    plain = chat("llama3.2", "Explain pandas groupby in one sentence.")
    teacher = chat("llama3.2", "Explain pandas groupby in one sentence.",
                   system="Explain like I am 15, with an example.")
    print("PLAIN:", plain[:200])
    print("TEACHER:", teacher[:200])
except Exception as e:
    print("Ollama not available:", e)
"""),
    ("md", """### Exercise 3 — The ask helper

Write your own `ask(model, question, system="")` helper (like `chat` above)
and use it to ask three questions about the tips dataset. Log each
question + answer in a small dict."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
def ask(model, question, system=""):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": question})
    return ollama.chat(model=model, messages=messages)["message"]["content"]

log = []
for q in ["What columns are in the tips dataset?",
          "Suggest one visualization for tips by day.",
          "What could go wrong if I predict tips from bill size?"]:
    try:
        log.append({"question": q, "answer": ask("llama3.2", q)[:120]})
    except Exception as e:
        log.append({"question": q, "answer": f"skipped: {e}"})
for entry in log:
    print(entry["question"], "->", entry["answer"][:80])
"""),
    ("md", """## Challenge exercise

Build a **privacy-aware review pipeline** for your project data:

1. Aggregate your dataset into summary tables (means, counts) — never raw
   rows with personal identifiers.
2. Send ONLY the summary text to the local model (guarded) asking for a
   review and one follow-up analysis.
3. Verify the model's suggestions against the data yourself.
4. Write a markdown note: data policy — summaries only, nothing leaves the
   machine (Ollama, local).""""),
    ("code", """# your code here
"""),
    ("code", """# Solution — structure with penguins; adapt to your data
import seaborn as sns, pandas as pd

penguins = sns.load_dataset("penguins").dropna()
summary = penguins.groupby("species")[["bill_length_mm", "body_mass_g"]].mean().round(1)

text = f"Species-level means:\\n{summary.to_string()}\\nWhat pattern stands out? Suggest one analysis."
try:
    reply = chat("llama3.2", text)
    print("MODEL:", reply[:250])
except Exception as e:
    print("Ollama not available:", e)

print("\\nDATA (never sent raw):", summary.to_string())
"""),
    ("md", """## Recap

- Ollama = local LLM runtime: private, free, offline after `ollama pull`.
- Python: `ollama.chat(model, messages)` — system + user roles.
- System prompts steer behavior; log them with the answers.
- Local ≠ infallible: same verification protocol as any LLM.
- Match model to task: local for private/simple, cloud when policy allows.

---
"""),
    ("md", """## Questions

1. What does `ollama pull llama3.2` actually download?
2. Name two advantages and two trade-offs of local models.
3. Write the Python call that chats with a local model.
4. What is a system prompt for?
5. Your data is sensitive. Which LLM setup should you use and why?
6. True/False: because the model runs on your machine, its answers are guaranteed accurate.

---
**Next:** notebook 17 — Tool/function calling.
"""),
]