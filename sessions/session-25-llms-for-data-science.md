# Session 25 — LLMs for Data Science

**Week 13 · Session 25 · Module C · 90 min · CLO-3**

## 1. Learning objectives

By the end of this session, students can:
- Explain in plain terms what an LLM is and why it sometimes sounds so confident.
- Identify where LLMs genuinely help a data workflow (code, explanation, drafting) and where they don't (facts, calculations, decisions).
- Write effective prompts for data tasks: context, task, format, constraints.
- Use an LLM as a *pair programmer* for data code — and verify every result.
- Apply the course's AI-use rule: disclose, verify, understand.

## 2. Key concepts

- **LLM = language model:** a system that predicts the next token — that's why it's fluent and can still be wrong ("hallucination").
- LLMs are **assistants, not authorities**: they excel at language-shaped tasks, fail at math/facts unless checked.
- **Prompting = specifying the task**: context + instruction + format + constraints beats one vague sentence.
- **Verify everything:** AI-generated code must run, AI claims must be checked against your data/docs.
- **When to use / not use:** drafting, explaining, boilerplate, debugging help — yes; final facts, critical calculations, decisions on data you haven't inspected — no.
- Course AI-use policy (from `../assessment-plan.md`): disclose, verify, understand — applies to every deliverable.

## 3. Detailed lecture notes

**What an LLM actually is.** Under the hood, an LLM (GPT-class, Llama, etc.) is
a giant neural network trained to predict the next word given the previous ones.
That simple objective, at massive scale, produces text that *looks* like
reasoning. Crucial implication for students: fluency ≠ accuracy. The model
doesn't "know" facts or "do" math — it generates the most probable next token.
So it can produce a perfectly grammatical answer that is entirely wrong
(a **hallucination**). Never treat LLM output as ground truth; treat it as a
*very articulate draft that must be checked*.

**Where LLMs genuinely help data work.** Be concrete and honest — this is the
professional framing:
- **Code help:** "explain this error", "refactor this function", "write a
  groupby that...", "why does my plot look empty?" — enormous time-saver for
  syntax/API questions (but versions change — verify against your installed
  versions, e.g., `pandas.__version__`).
- **Explaining concepts:** "explain R² like I'm 15" — great for study.
- **Drafting:** markdown write-ups, comments, READMEs, email summaries.
- **Structured assistance:** with the right prompt, it can suggest an analysis
  plan or review your EDA findings for blind spots (e.g., "what might I have
  missed?").
Where it does **not** help: doing your calculations (it's not a calculator —
Session 6's NumPy is), recalling exact API signatures across versions, making
ethical judgment calls, or *deciding* — you remain responsible for every
conclusion.

**Prompting for data tasks.** The skill that transfers everywhere. A good prompt
specifies four things: **context** (what dataset/problem), **task** (what you
want), **format** (how the answer should look), **constraints** (what to
avoid). Template:
> "I have a pandas DataFrame with columns [..]. Task: write code that [..].
> Constraints: use pandas, no loops if avoidable, set random_state=42. Output:
> the code plus a one-line explanation."
Compare a vague prompt ("help me with pandas") vs. the template — students feel
the difference immediately. Iteration is normal: ask for a correction, ask it
to explain its own code, ask for an alternative approach. The output is a
starting point, not an endpoint.

**Verification protocol (the non-negotiable).** For every AI-generated artifact:
1. **Run it** — does it execute in *your* environment?
2. **Understand it** — can you explain each line? (The instructor can and will ask — assessment-plan.)
3. **Check the numbers** — spot-check with a hand computation or a known value (Session 6's seed discipline helps).
4. **Disclose it** — note tool + prompt + how you used it (per the AI-use policy; this feeds the reproducibility docs from Session 24).
This is exactly the "responsible AI use" of CLO-3: using the tool without
losing the ability to validate its output.

**The ethical frame (preview of Session 30).** LLMs multiply the classic data
pitfalls: hallucinated citations, plausible-but-wrong conclusions, biased
training data, hidden privacy issues when you paste real data into a cloud
service. Two rules now: never paste personal/sensitive data into an online
LLM, and never let an LLM's confidence substitute for your verification.
Details and case studies in Session 30.

## 4. Important terminology

- **LLM** — large language model; predicts next tokens; fluent, not infallible.
- **Token** — a chunk of text the model works with (~a word or part of one).
- **Hallucination** — confident, false output.
- **Prompt** — your instruction to the model.
- **Context / task / format / constraints** — the four prompt ingredients.
- **Few-shot prompting** — giving examples in the prompt (mention; use sparingly).
- **Pair programmer** — using the LLM as a coding assistant, not an oracle.
- **Verification protocol** — run → understand → check → disclose.
- **AI-use policy** — disclose, verify, understand (course rule).
- **Sensitive data** — personal/private data that must not be sent to cloud LLMs.

## 5. Python examples

```python
# The pattern that matters: LLM suggests, YOU verify.

# Suppose the LLM suggested this snippet for the tips data:
import seaborn as sns
import pandas as pd

tips = sns.load_dataset("tips")
result = tips.groupby("day", as_index=False)["tip"].mean().sort_values("tip", ascending=False)

# Verification steps:
# 1. RUN it -> executes cleanly
print(result)
# 2. UNDERSTAND it: group by day, mean tip, keep day as a column, sort desc
# 3. CHECK: compare with a hand/known value
print("Saturday mean (manual):", round(tips.loc[tips["day"] == "Sat", "tip"].mean(), 2))
print("Model value            :", round(result.loc[result["day"] == "Sat", "tip"].iloc[0], 2))
# 4. DISCLOSE in the notebook: "# Generated with <tool>; verified: matches manual calc"
```

```python
# A good prompt, written as a template you'd paste into the chat:
prompt = """
Context: pandas DataFrame `df` with columns total_bill, tip, size, day, time.
Task: write pandas code that computes the mean tip percentage
      (tip / total_bill * 100) by day, sorted descending.
Constraints: use pandas only, no explicit loops, set random_state where relevant.
Format: the code, then one sentence explaining what it does.
"""
```

## 6. Beginner example

```python
# Beginner prompt + verification in one flow:
# Prompt: "Explain, in two sentences, what df.groupby('day')['tip'].mean() does."
# Answer (paraphrase): it splits tips by day, averages each group, returns a
# Series indexed by day.
# Verification: run it and compare with a manual mean for one day. If they
# match, the explanation was right.
import seaborn as sns
tips = sns.load_dataset("tips")
assert abs(tips.groupby("day")["tip"].mean()["Sat"] -
           tips[tips["day"] == "Sat"]["tip"].mean()) < 1e-9
print("Verified: LLM's explanation matches reality.")
```

## 7. Practical Data Science example

```python
# A realistic AI-assisted EDA step, documented per course policy
import seaborn as sns
import pandas as pd
import numpy as np

penguins = sns.load_dataset("penguins").dropna()

# Step 1 — we ask the LLM for a review of our findings (prompt recorded):
# "Here are 3 EDA findings about the penguins dataset [list]. What patterns
#  might I have missed? Suggest one additional analysis."
# Step 2 — the LLM suggests checking body_mass by species with a boxplot.
# Step 3 — WE run and verify:
print(penguins.groupby("species")["body_mass_g"].mean().round(0))
sns.boxplot(data=penguins, x="species", y="body_mass_g")

# Step 4 — we accept the idea because it checks out (Gentoo clearly heavier),
# and disclose in the notebook:
# "Idea suggested by an LLM (ChatGPT, prompt recorded in project/ai-notes.md);
#  verified against the data above."
```

## 8. In-class activity (50 min)

In `notebooks/week-13/session-25-llms.ipynb`:

1. **Prompt makeover (15 min):** take a vague prompt ("help me with pandas") and
   rewrite it with context/task/format/constraints; swap with a partner and
   compare outputs (use the same LLM tool for fairness).
2. **Generate → verify (20 min):** ask the LLM for code that computes tip
   percentage by day *and* smoker status; run it; verify one cell by hand;
   fix whatever fails; add the disclosure note.
3. **Spot the hallucination (15 min):** give the LLM a factual question about
   your dataset (e.g., "how many rows does tips have?") and one about pandas
   history — discuss why it can be confidently wrong, and which answers you'd
   trust without checking.

## 9. Lab exercise

No lab this session.
From here: Lab 26 (PandasAI), Lab 27 (Ollama), Lab 28 (tool calling &
agents), Lab 29 (n8n), Lab 30 (ethics).

## 10. Common mistakes

- Treating LLM output as fact — no verification, no disclosure.
- Asking the LLM to do the math instead of NumPy/Pandas — it's not a calculator.
- Pasting sensitive/real personal data into a cloud LLM (privacy breach — Session 30).
- Copy-pasting code that uses a different package version than yours (check `pip show` / imports).
- Vague prompts → vague answers; spend 30 seconds writing the prompt.
- Letting the AI's confident tone override your own judgment — you own the conclusions.
- Using an LLM on quizzes/exams — against the course AI-use policy.

## 11. Short assessment questions

1. Why can an LLM sound confident and still be wrong?
2. Name the four prompt ingredients and give an example of each for a data task.
3. What are the four steps of the verification protocol?
4. Give one data-task where an LLM genuinely helps and one where it doesn't.
5. What must you do before pasting a DataFrame into an online LLM? (Check for sensitive data; anonymize or don't.)
6. Per the course policy, what three things does every AI-assisted deliverable require?

## 12. CLO mapping

CLO-3: LLM literacy is the foundation of "develop simple AI-assisted data
science workflows" — knowing what the tool is, when to use it, and how to
verify it. The disclose-verify-understand protocol is reused in every later
session and in the project's AI component and reflection.

## 13. Suggested homework

- Apply the verification protocol to one snippet of your Assignment 2 pipeline code (even if not AI-generated, practice the four steps).
- Practice: write three good prompts for tasks in your own project (code, explanation, plan review).
- Read: the course AI-use policy in `../assessment-plan.md` again — know it cold.
- Preview: `pip show pandasai` and check the version — Session 26 turns natural language into pandas queries with PandasAI.