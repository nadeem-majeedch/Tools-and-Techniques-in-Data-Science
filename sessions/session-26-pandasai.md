# Session 26 — PandasAI: Natural Language Data Queries

**Week 13 · Session 26 · Module C · 90 min · CLO-3**

## 1. Learning objectives

By the end of this session, students can:
- Set up PandasAI with a local LLM (Ollama) or configured provider.
- Ask natural-language questions about a DataFrame and get answers.
- Explain how PandasAI works under the hood (it generates pandas code, then runs it).
- Recognize when the generated answer is wrong and audit it.
- Document AI-assisted queries for reproducibility (record prompt + generated code).

## 2. Key concepts

- **PandasAI = a translator:** your question → pandas code → executed on your DataFrame.
- The **LLM is only the translator** — the numbers come from pandas; the risk is a mistranslated question.
- Because it *generates code*, you can (and must) **read and audit that code**.
- Configure with a local model (Ollama) → private, free, offline-friendly.
- Same verification discipline as Session 25: check the code, check a number by hand.
- API versions change — check your installed `pandasai` version and docs.

## 3. Detailed lecture notes

**Why PandasAI?** Every session so far required you to translate a question into
pandas verbs: "what's the mean tip by day?" → `tips.groupby("day")["tip"].mean()`.
PandasAI inverts this: you type the question, it writes and runs the pandas for
you. That's the essence of AI-assisted data work (CLO-3) — and its danger. The
whole lesson is the pair: **convenience on top, verification underneath.**

**How it works (the mental model).** PandasAI sends your question + the
DataFrame's schema to an LLM, which returns *pandas code*; PandasAI executes
that code and returns the result. Three consequences:
1. The numbers are computed by pandas, not hallucinated — good.
2. But the *question interpretation* can be wrong: "average bill for smokers on
   weekends" might be translated with a wrong filter — the answer is then
   confidently wrong. You must read the generated code.
3. It needs an LLM — cloud (default) or **local via Ollama** (Session 27's
   engine; using `OllamaLLM` keeps data private and costs nothing).

**Setup.** Requirements: `pip install pandasai` (in `requirements.txt`), plus
an LLM. For class: configure `OllamaLLM` with a small local model
(`llama3.2`); cloud providers (OpenAI etc.) need API keys — fine but requires
secrets management (`.env`, Session 11's rule) and costs money. PandasAI's API
has changed across major versions (v2 introduced `Agent` replacing
`SmartDataframe`; v3 restructured config) — show students *how to check*:
`pip show pandasai` and the docs page, then adapt. Teach the pattern, not the
exact call: create an agent bound to the DataFrame, `agent.chat("question")`,
inspect the answer **and the code behind it**.

**Auditing — the core skill.** After every `chat()`:
1. Look at the *generated code* (PandasAI exposes it via
   `agent.last_code_generated` or the "explain" mode depending on version).
2. Read it as *your* code (Session 7–12 skills apply!): right columns? right
   filter? right aggregation?
3. Spot-check the number with one manual pandas line or a known value.
4. Fix/iterate: rephrase the question, add constraints ("use only columns A and
   B", "exclude missing values"), or write the pandas yourself.
A wrong-but-plausible answer is worse than no answer — audit catches it. This
is the same protocol as Session 25, now applied to data queries.

**Reproducibility.** A `chat()` is a black box unless recorded. For the project
and Lab 8, keep an **AI log** (markdown file or notebook section) per
AI-assisted query: the question, the tool + model version, the generated code,
and the verification result. This is exactly the documentation Session 24
demanded and the assessment plan's disclosure rule. `random_state` doesn't
apply to prompts — the *prompt* is the seed of an AI query; recording it is the
equivalent.

**Limits to state honestly.** Natural language is ambiguous; complex multi-step
questions produce tangled generated code; very large DataFrames are slow; the
tool changes fast. Professional framing: PandasAI is a productivity layer for
people who *already* know pandas (that's you, after Module A) — not a
replacement for learning to verify.

## 4. Important terminology

- **PandasAI** — a library that translates natural language into pandas code.
- **Agent** — PandasAI's object bound to your DataFrame (`agent.chat(...)`).
- **`OllamaLLM`** — PandasAI's connector to local Ollama models.
- **Generated code** — the pandas code the LLM produced; always audit it.
- **Schema** — the DataFrame's columns/dtypes sent to the LLM as context.
- **AI log** — recorded question + model + generated code + verification.
- **Verification** — check the code, then check a number by hand.
- **Ambiguity** — unclear questions → wrong translations; add constraints.
- **`.env` / API key** — needed for cloud LLMs; keep secrets out of Git.

## 5. Python examples

```python
# --- Setup (verify versions first: pip show pandasai, ollama) ---
import pandas as pd
import seaborn as sns

# pandasai >= 2.x: Agent; >= 3.x config changed — check docs for your version
from pandasai import Agent
from pandasai.llm import OllamaLLM

llm = OllamaLLM(model="llama3.2")       # local model from Session 27
tips = sns.load_dataset("tips")
agent = Agent(tips, config={"llm": llm})   # v2 style; adapt per your version

# --- Ask, then audit ---
answer = agent.chat("What is the average tip by day of the week?")
print(answer)

# Audit step 1 — inspect the generated code (attribute name varies by version):
print(agent.last_code_generated)        # v2; docs will confirm

# Audit step 2 — verify by hand:
manual = tips.groupby("day")["tip"].mean()
print(manual)
```

```python
# --- Better questions, better answers: add constraints ---
agent.chat("Compute mean tip as a percentage of total bill, grouped by day, "
           "using only the columns day, tip, total_bill. Exclude missing values.")

# --- Non-answer use: ask it to EXPLAIN, then verify the explanation ---
agent.chat("Which two columns are most correlated, and what is the value? "
           "Show the pandas code you use.")
```

## 6. Beginner example

```python
from pandasai import Agent
from pandasai.llm import OllamaLLM
import pandas as pd

df = pd.DataFrame({"fruit": ["apple", "banana", "apple"],
                   "price": [80, 30, 90]})

agent = Agent(df, config={"llm": OllamaLLM(model="llama3.2")})
print(agent.chat("Which fruit is more expensive on average?"))
# -> "apple (85.0)" — then check: df.groupby('fruit')['price'].mean()
```

The whole idea in four lines: DataFrame in, plain-English question, answer out
— *and a verification line to keep it honest*.

## 7. Practical Data Science example

```python
import pandas as pd
import seaborn as sns
from pandasai import Agent
from pandasai.llm import OllamaLLM

penguins = sns.load_dataset("penguins").dropna()
agent = Agent(penguins, config={"llm": OllamaLLM(model="llama3.2")})

# Real workflow: exploration questions in natural language, each audited
q1 = agent.chat("Which species has the longest average flipper length?")
print(q1)                                    # check: groupby mean -> Gentoo

q2 = agent.chat("Is there a correlation between bill length and body mass? "
                "Return the Pearson value and the code used.")
print(q2)                                    # check: df.corr() by hand

# Reproducible AI log entry (markdown, saved to project/ai-notes.md):
# ## Query 2026-04-14
# - Question: "Is there a correlation between bill length and body mass?"
# - Tool: pandasai <version> + OllamaLLM llama3.2
# - Generated code: <paste>
# - Verified: corr() by hand gives 0.595 — matches.
```

## 8. In-class activity (50 min)

In `notebooks/week-13/session-26-pandasai.ipynb`:

1. **Setup check (10 min):** confirm `pandasai` and `ollama` versions; create the
   agent on `tips`; run one simple question.
2. **Audit drill (20 min):** ask 3 questions (simple, filtered, aggregated);
   for each: print the generated code, verify one number by hand, fix the
   question if the code was wrong. Log all three in the AI-log format.
3. **Ambiguity hunt (10 min):** ask a deliberately ambiguous question
   ("what about tips on weekends?") — observe the guess; re-ask with
   constraints; compare answers.
4. **Try to break it (10 min):** ask a question about a column that doesn't
   exist. What happens? (It should error or invent — that's your cue to audit.)

## 9. Lab exercise

**Lab 26 is due today** (`labs/lab-26-pandasai.md`): PandasAI — set up,
answer 4 questions on `tips`, audit each against pandas, and write the report
card with a reflection on what you'd trust and why. **Project proposal also
due today** (`../projects/`). Push both.

## 10. Common mistakes

- Trusting the answer without reading the generated code.
- Asking ambiguous questions, then believing the guess.
- Expecting exact API calls to match tutorials — versions differ; check `pip show pandasai` and docs.
- Forgetting that a cloud LLM receives your *data* — use Ollama locally for private data.
- Skipping hand-verification of one number.
- Not logging the prompt/code → unreproducible AI step in the project.
- Using PandasAI as a crutch instead of learning pandas — Module A is your audit skill.

## 11. Short assessment questions

1. What does PandasAI actually do with your question, step by step?
2. Why must you audit the generated code even when the answer "looks right"?
3. Name two things to record in an AI log entry.
4. What is the advantage of `OllamaLLM` over a cloud LLM for this course?
5. Your question is "tips on weekends?" — why is it ambiguous, and how do you fix it?
6. True/False: PandasAI computes the numbers itself, so results are always correct. (False — pandas computes them, but the *question translation* can be wrong.)

## 12. CLO mapping

CLO-3: PandasAI is the first full "LLM-powered data workflow" tool — using it
correctly (audit + log) is exactly "develop simple AI-assisted data science
workflows … considering reproducibility". Feeds Lab 26 and the project's AI
component.

## 13. Suggested homework

- Finish Lab 8 and push; finalize your project proposal if not submitted.
- Practice: repeat the audit drill on your *own* project dataset — write 3 questions your analysis actually needs and verify the answers.
- Read: PandasAI docs (docs.pandas-ai.com) — the "Getting started" and "Examples" pages for your installed version.
- Preview: `import ollama; ollama.chat(model="llama3.2", messages=[{"role":"user","content":"Hi"}])` — Session 27 explains what's running on your machine and how local models work.