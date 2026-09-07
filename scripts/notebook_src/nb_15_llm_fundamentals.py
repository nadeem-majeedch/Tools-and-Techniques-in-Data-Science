# Content for notebook 15: LLM fundamentals.
CELLS = [
    ("md", """# 15 — LLM Fundamentals

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-3 — Develop AI-assisted data science workflows.

LLMs (large language models) are the engines behind ChatGPT, Gemini, and the
local models in this course. This notebook builds the mental model you need
to use them *well* in data work: what they are, how to prompt them, and —
most importantly — how to verify them. Fluency is not accuracy.

---
"""),("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Explain what an LLM is and why it can be confidently wrong.
2. Say where LLMs help a data workflow and where they don't.
3. Write prompts with context, task, format, and constraints.
4. Apply the verification protocol: run → understand → check → disclose.
5. Follow the course AI-use rule: disclose, verify, understand.

---
"""),("md", """## Theory: what an LLM actually is

An LLM is a giant neural network trained to **predict the next token** (a
chunk of text) given the previous ones. That simple objective, at massive
scale, produces text that *looks* like reasoning. The catch: it doesn't
"know" facts or "do" math — it generates the most probable next token. So it
can produce a perfectly grammatical, entirely wrong answer (a
**hallucination**).

Consequences for data work:

| Helps | Does not help |
|---|---|
| explaining concepts | doing your calculations (use NumPy) |
| writing/explaining code | recalling exact API signatures across versions |
| drafting markdown/READMEs | making ethical or final decisions |
| reviewing your findings for blind spots | being ground truth — ever |

**The professional stance:** treat the LLM as a *very articulate draft that
must be checked* — a pair programmer, not an oracle.

---
"""),("code", """# What "predicting the next token" looks like, miniaturized:
# a tiny model that completes "The capital of France is" from training data.
toy_model = {
    "The capital of France is": "Paris",
    "Pandas is a": "data analysis library",
}
prompt = "The capital of France is"
print(toy_model.get(prompt, "unknown"))
# Real LLMs do the same at enormous scale — and that scale is why they seem
# to reason. They still only *predict text*.
"""),
    ("md", """## Prompting: context, task, format, constraints

A good prompt specifies four things:

1. **Context** — what dataset/problem you're working on.
2. **Task** — what you want done.
3. **Format** — how the answer should look.
4. **Constraints** — what to avoid or require.

Vague prompt: *"help me with pandas"*
Better prompt:

> "I have a pandas DataFrame with columns day, tip, total_bill. Task: write
> code that computes mean tip percentage by day, sorted descending.
> Constraints: pandas only, no loops, set random_state where relevant.
> Format: the code, then one sentence explaining it."

Build prompts as Python strings so you can log them (reproducibility!).

---
"""),("code", """# A reusable prompt template — log every use
def make_prompt(columns, task, constraints, context=""):
    return f\"\"\"
Context: pandas DataFrame with columns {columns}. {context}
Task: {task}
Constraints: {constraints}
Format: the code, then one sentence explaining what it does.
\"\"\"

prompt = make_prompt(
    columns="day, tip, total_bill",
    task="compute the mean tip percentage (tip / total_bill * 100) by day, sorted descending",
    constraints="pandas only, no explicit loops",
)
print(prompt)
"""),
    ("md", """## The verification protocol

For every AI-generated artifact — code, explanation, or number:

1. **Run it** — does it execute in *your* environment?
2. **Understand it** — can you explain each line? (Your instructor can and will ask.)
3. **Check the numbers** — spot-check one value with your own tools.
4. **Disclose it** — record tool + prompt + how you used it.

Rules one and three are code; rules two and four are professionalism. This
protocol is the course's AI-use policy in action: **disclose, verify,
understand**.

---
"""),("code", """import seaborn as sns
import pandas as pd

tips = sns.load_dataset("tips")

# Suppose an LLM suggested this snippet:
result = (tips.groupby("day", as_index=False)["tip"].mean()
              .sort_values("tip", ascending=False))

# 1. RUN it -> it executes.
# 2. UNDERSTAND it -> group by day, mean of tip, keep day as a column, sort.
# 3. CHECK one number by hand:
manual = tips.loc[tips["day"] == "Sat", "tip"].mean()
model_value = result.loc[result["day"] == "Sat", "tip"].iloc[0]
print("manual:", round(manual, 3), "| model:", round(model_value, 3),
      "| match:", abs(manual - model_value) < 1e-9)

# 4. DISCLOSE in the notebook:
#    "# Suggested by <tool>; verified against manual groupby — matches."
"""),
    ("md", """## Beginner example: prompt + verify in one flow

---
"""),("code", """# Prompt (recorded): "Explain in two sentences what
#   df.groupby('day')['tip'].mean() does."
# Paraphrased answer: "It splits the tips by day, averages each group, and
# returns a Series indexed by day."

import seaborn as sns
tips = sns.load_dataset("tips")

# Verification: run the code, compare one number by hand
series = tips.groupby("day")["tip"].mean()
ok = abs(series["Sat"] - tips[tips["day"] == "Sat"]["tip"].mean()) < 1e-9
print("explanation verified:", ok)
"""),
    ("md", """## Intermediate example: AI-assisted EDA review

A realistic workflow: your findings reviewed by an LLM (via Ollama —
notebook 16 — or any chat tool), with every claim verified against the data.

---
"""),("code", """import seaborn as sns
import pandas as pd

penguins = sns.load_dataset("penguins").dropna()
mean_mass = penguins.groupby("species")["body_mass_g"].mean().round(0)

# Step 1: our claim (recorded before asking the model)
claim = "Gentoo penguins are much heavier than the other species."

# Step 2: the prompt we would send (logged):
prompt_for_llm = f\"\"\"
Dataset: penguins. Mean body mass per species: {mean_mass.to_dict()}.
My claim: {claim}
Task: is my claim supported by the data? Suggest one follow-up analysis.
\"\"\"

# Step 3: verify the claim ourselves (ground truth):
print(mean_mass)
print("claim supported:", mean_mass["Gentoo"] > mean_mass[["Adelie", "Chinstrap"]].max())

# Step 4: disclosure note for the notebook:
#    "Claim reviewed by <model>; verified against groupby means above."
"""),
    ("md", """## Exercises

---
"""),("md", """### Exercise 1 — Prompt makeover

Rewrite this vague prompt using context/task/format/constraints:
*"help me with my data"* (target: penguins, task: check for missing values
per column, format: table, constraint: pandas only). Write your version in a
markdown cell, then build it as a Python string with `make_prompt`."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
prompt = make_prompt(
    columns="species, island, bill_length_mm, body_mass_g",
    task="list the number of missing values per column",
    constraints="pandas only, print a readable table",
    context="Dataset: penguins (seaborn).",
)
print(prompt)
"""),
    ("md", """### Exercise 2 — Spot the unreliable answer

Which of these LLM answers would you trust without checking, and which must
you verify? (a) "the mean of arr is 42.3", (b) "pandas is a data analysis
library", (c) "this code computes the mean tip by day". Write one sentence
per answer."""),
    ("code", """# Answers (markdown):
#   (a) verify — it's a number computed from your data.
#   (b) trust — general knowledge, low stakes.
#   (c) verify — code must run AND match your columns/versions.
print("reasoning in markdown")
"""),
    ("md", """### Exercise 3 — The four steps

Take any code snippet from notebook 11 (regression) and pretend an LLM
wrote it. Walk it through the verification protocol: run it, explain each
line in a comment, check one number, and write the disclosure note."""),
    ("code", """# your code here
"""),
    ("code", """# Solution — the protocol in action
from sklearn.linear_model import LinearRegression
import numpy as np

# 1. RUN
X = np.array([[1], [2], [3], [4]])
y = np.array([2, 4, 6, 8])
m = LinearRegression().fit(X, y)

# 2. UNDERSTAND: fits the line y = a + b*x; coef_ is the slope.
print("slope:", m.coef_[0])

# 3. CHECK: slope of a perfect line through (1,2)..(4,8) is 2.
print("verified:", abs(m.coef_[0] - 2) < 1e-9)

# 4. DISCLOSE: "# Generated with <tool>; verified: slope == 2 by inspection."
"""),
    ("md", """## Challenge exercise

Design a **mini AI-review workflow** for your own project dataset:

1. Write 3 findings about the dataset in finding → evidence → implication
   form (notebook 07's format).
2. Write the prompt you would send to an LLM asking it to (a) check your
   findings against the data, (b) suggest one analysis you missed.
3. Run the verification for all 3 findings yourself (they must be TRUE).
4. Write the disclosure block you would append to your notebook.

The workflow must work with no LLM at all — the verification is the point."""),
    ("code", """# your code here
"""),
    ("code", """# Solution — structure only; fill in with your own dataset
import seaborn as sns
import pandas as pd

penguins = sns.load_dataset("penguins").dropna()

findings = [
    "Gentoo has the longest average flipper length.",
    "Bill length and body mass correlate positively (r > 0.5).",
    "Adelie and Chinstrap have similar mean body mass.",
]

# Verify each finding (ground truth):
checks = [
    penguins.groupby("species")["flipper_length_mm"].mean().idxmax() == "Gentoo",
    penguins["bill_length_mm"].corr(penguins["body_mass_g"]) > 0.5,
    abs(penguins.groupby("species")["body_mass_g"].mean()["Adelie"]
        - penguins.groupby("species")["body_mass_g"].mean()["Chinstrap"]) < 500,
]
for f, ok in zip(findings, checks):
    print("OK " if ok else "FAIL ", f)

# Disclosure block (copy into the notebook):
# "Findings drafted and reviewed with the help of <model>. Each claim was
#  verified against the dataset in the cells above; only verified claims
#  are reported here."
"""),
    ("md", """## Recap

- LLMs predict the next token: **fluent, not infallible**.
- Use them for language-shaped tasks; verify everything numerical.
- Prompts: context + task + format + constraints.
- Protocol: run → understand → check → disclose.
- Course rule: **disclose, verify, understand** — it's a professional habit,
  not paperwork.

---
"""),
    ("md", """## Questions

1. Why can an LLM sound confident and still be wrong?
2. Name the four prompt ingredients.
3. What are the four steps of the verification protocol?
4. Give one data task where an LLM helps and one where it doesn't.
5. What must you check before pasting a DataFrame into an online LLM?
6. Per the course policy, what three things does every AI-assisted deliverable require?

---
**Next:** notebook 16 — Ollama with Python.
"""),
]