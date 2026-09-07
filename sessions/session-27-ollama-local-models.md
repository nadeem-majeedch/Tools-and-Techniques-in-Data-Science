# Session 27 — Ollama: Local Models

**Week 14 · Session 27 · Module C · 90 min · CLO-3**

## 1. Learning objectives

By the end of this session, students can:
- Explain why running models locally matters (privacy, cost, offline work).
- Install and run Ollama; pull and switch between models.
- Chat with a local model from Python and from the notebook.
- Compare local vs. cloud models honestly (capability vs. control trade-offs).
- Use a local model as the LLM behind PandasAI and simple scripts.

## 2. Key concepts

- **Ollama = a local LLM runtime:** it downloads models and serves them on your machine (`http://localhost:11434`).
- **Models are files:** `ollama pull llama3.2` fetches one; different models = different size/speed/capability trade-offs.
- The **ollama Python client** talks to the local server; no API key, no network needed after the pull.
- **Local vs. cloud:** local = private, free, offline; cloud = bigger models, more capability, costs + data leaves your machine.
- A small model running locally is often *good enough* for data-analysis tasks (translation, explanation, simple code).
- Same verification rules as ever: local ≠ infallible; audit and check.

## 3. Detailed lecture notes

**Why local models?** Session 26 used Ollama as the engine behind PandasAI.
Today we open the hood. Cloud LLMs (ChatGPT, Gemini) are powerful but: your
data travels to their servers, usage can cost money, and you need internet.
For data work with real datasets — especially personal or institutional data —
sending every DataFrame to a cloud service is often unacceptable (Session 30
makes the privacy stakes concrete). **Ollama runs models entirely on your
machine**: private, free, works offline. The trade: your laptop's memory limits
model size, so you use smaller models than the cloud's best.

**What Ollama actually is.** It's a runtime + model manager. You `ollama pull
<model>` once — that downloads the model weights to your disk. Then
`ollama run llama3.2` gives an interactive chat; the Python client
(`import ollama; ollama.chat(...)`) talks to the same local server
(localhost:11434). Once a model is pulled, everything is offline. The
model-library page (ollama.com/library) lists options; for this course:
`llama3.2` (small, fast, general) as default; `qwen2.5:7b` (stronger, bigger);
`llava` for image tasks (mention only). Size/capability rule of thumb: bigger
model = better reasoning, more RAM, slower responses. A 7B model on a student
laptop is typically the sweet spot for course work.

**The mental model: "small but yours".** Local models trail frontier cloud
models on hard reasoning. But most of what this course needs an LLM for —
translating a question into pandas code, explaining an error, summarizing a
finding — is well within a small model's reach. The professional skill is
*matching model to task*: local for private/simple, cloud for
frontier-hard tasks when data policies allow. Emphasize the engineering frame:
an LLM call is a *function* in your pipeline (input text → output text); Ollama
gives you that function on your own hardware.

**Using it in Python.** The client is minimal:
```python
import ollama
resp = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": "..."}])
print(resp["message"]["content"])
```
Messages are a list of {role, content} — role "system" sets behavior
("you are a data-science teaching assistant; answer briefly"),
"user" is the request. Streaming (`stream=True`) and temperature are options —
keep it simple. Two practical patterns for the course: (1) as the PandasAI LLM
(Session 26's `OllamaLLM` — under the hood it wraps exactly this API); (2)
direct chat for explanation/drafting inside a notebook. For scripting, keep
prompts in variables and log them (Session 24's reproducibility + Session 26's
AI log apply verbatim).

**Comparing local vs. cloud (honest table to teach):** local — private
(data stays put), free, offline, smaller models, slower on big hardware needs.
Cloud — frontier capability, easy API, costs, data leaves machine, terms of
service apply. Neither is "better"; the choice is contextual. Exercise for
students: same prompt to local and (if available) cloud, compare quality on a
data task — see the gap with their own eyes, and see that local is often good
enough.

**Verification unchanged.** A local model can hallucinate exactly like a cloud
one (Session 25). Same protocol: run, understand, check, disclose. Local-ness
is a privacy/control property, not a correctness property.

## 4. Important terminology

- **Ollama** — local LLM runtime + model manager.
- **Model weights** — the trained parameters downloaded as a model file.
- **`ollama pull` / `ollama run`** — download / run a model.
- **`localhost:11434`** — the local server the Python client talks to.
- **Token** — the unit of text the model processes (context limits measured in tokens).
- **System prompt** — instructions setting the model's behavior.
- **Messages** — the `[{role, content}]` chat structure.
- **Local vs. cloud inference** — on-device vs. remote computation trade-offs.
- **Context window** — how much text the model can consider at once.
- **Quantization** — (mention) compressed weights → smaller, faster, slightly weaker models.

## 5. Python examples

```python
# --- Terminal setup (once per machine) ---
# ollama pull llama3.2
# ollama run llama3.2          # interactive chat; type /bye to exit

# --- Python: the whole client in three lines ---
import ollama

resp = ollama.chat(model="llama3.2", messages=[
    {"role": "system", "content": "You are a concise data-science tutor."},
    {"role": "user", "content": "Explain what a train/test split is in two sentences."},
])
print(resp["message"]["content"])
```

```python
# --- Practical: local model behind PandasAI (from Session 26) ---
from pandasai import Agent
from pandasai.llm import OllamaLLM
import seaborn as sns

tips = sns.load_dataset("tips")
agent = Agent(tips, config={"llm": OllamaLLM(model="llama3.2")})
print(agent.chat("What is the average tip on Sunday?"))
# then audit: tips.loc[tips.day == "Sun", "tip"].mean()
```

```python
# --- A reusable helper with a logged prompt (reproducibility!) ---
import ollama

def ask(model: str, question: str, system: str = "") -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": question})
    resp = ollama.chat(model=model, messages=messages)
    return resp["message"]["content"]

print(ask("llama3.2", "List 3 pandas functions for cleaning missing values."))
```

## 6. Beginner example

```python
import ollama

reply = ollama.chat(model="llama3.2", messages=[
    {"role": "user", "content": "Say hello in one sentence."}
])
print(reply["message"]["content"])
```

If this prints a greeting, your local LLM stack works — everything else is
variations on this call.

## 7. Practical Data Science example

```python
import ollama
import seaborn as sns
import pandas as pd

# Real task: let a LOCAL model review our EDA findings (privacy-safe, free)
penguins = sns.load_dataset("penguins").dropna()
mean_mass = penguins.groupby("species")["body_mass_g"].mean().round(0)

findings = f"""
Dataset: penguins. Mean body mass (g): {mean_mass.to_dict()}.
I claim: Gentoo penguins are much heavier than the other species.
Task: is my claim supported? Suggest one follow-up analysis.
"""
reply = ollama.chat(model="llama3.2", messages=[
    {"role": "user", "content": findings},
])
print(reply["message"]["content"])

# Verification: the claim is checkable directly:
print(mean_mass)   # Gentoo ~5076 vs Adelie ~3701, Chinstrap ~3733 -> supported
# Disclosure note for the notebook:
# "Review and follow-up idea generated by llama3.2 (local, via Ollama);
#  claim verified against groupby means above."
```

## 8. In-class activity (50 min)

In `notebooks/week-14/session-27-ollama.ipynb`:

1. **Setup race (10 min):** confirm `ollama --version`, `ollama list`; pull
   `llama3.2` if missing; run the three-line chat.
2. **System-prompt experiment (15 min):** the same question with three system
   prompts ("one sentence", "list format", "explain like I'm 15") — observe how
   the frame changes the output.
3. **Task matching (15 min):** run the penguins review example; then ask a
   harder reasoning question (e.g., a small logic puzzle) and honestly rate the
   answer. Fill in a local-vs-cloud comparison table from experience.
4. **Wrap it in a helper (10 min):** write the `ask()` helper, log three
   prompt/response pairs to your AI log.

## 9. Lab exercise

**Lab 9 is due today** (`labs/lab-09/`): Ollama — pull a model, chat from
Python, use it as the PandasAI engine, compare system prompts, and write a
short reflection on local vs. cloud for your project's data (privacy angle).
Push.

## 10. Common mistakes

- Forgetting to pull the model → "model not found" errors on first use.
- Pulling huge models on a small laptop → slow/OOM; use `llama3.2` or `qwen2.5:7b` for course work.
- Expecting a local 3B model to match frontier cloud quality — match task to model.
- Thinking local = correct — hallucination risk is unchanged (verify!).
- Pasting secrets/keys into prompts logged to disk — keep prompts clean.
- Not logging prompts → unreproducible AI steps (AI log discipline).
- Using cloud LLMs for private data when a local model would do — a privacy decision, not a convenience decision.

## 11. Short assessment questions

1. What does `ollama pull llama3.2` actually download?
2. What are two advantages of local models and two trade-offs?
3. Write the Python call that chats with a local model.
4. What is a system prompt for?
5. Your data is sensitive hospital records. Which LLM setup should you use and why?
6. True/False: because the model runs on your machine, its answers are guaranteed accurate. (False.)

## 12. CLO mapping

CLO-3: Ollama provides the "local models" capability named in the CLO, enabling
private, reproducible AI-assisted workflows. Combined with Session 26's auditing
discipline, it's the complete local-AI data workflow used in Lab 9, Assignment
3, and the project.

## 13. Suggested homework

- Finish Lab 9 and push.
- Practice: run your own project's EDA findings through the local model for review; log the exchange; act on one suggestion (or reject it with a reason).
- Read: the Ollama README on GitHub (ollama/ollama) — the API section, 10 minutes.
- Preview: Session 28 turns the chat into an *agent* — the model gets tools (functions) it can call, like fetching weather or running pandas.