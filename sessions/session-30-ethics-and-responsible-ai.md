# Session 30 — Ethics & Responsible AI

**Week 15 · Session 30 · Module C · 90 min · CLO-3**

## 1. Learning objectives

By the end of this session, students can:
- Explain the main ethical risks in data work: bias, privacy, provenance, and misuse of results.
- Give a concrete example of how a dataset or model can embed and amplify bias.
- Apply the course's responsible-AI rules to their own project: disclose, verify, protect data.
- Write a short ethics/reproducibility reflection for a data project.
- Evaluate an AI-assisted result critically rather than trusting its fluency.

## 2. Key concepts

- **Bias enters at every stage:** who is missing from the data? whose patterns dominate the model?
- **Privacy:** data about people needs consent, minimization, and protection — never paste sensitive data into cloud LLMs.
- **Provenance & transparency:** know where data came from, what was done to it, and what AI contributed.
- **Correlation isn't causation** (Session 15) — now with real-world consequences when models act on it.
- **Responsible use ≠ no AI:** it's *documented, verified, bounded* AI — exactly the course rules.
- A reflection isn't a confession — it's evidence of judgment: what you considered and decided.

## 3. Detailed lecture notes

**Why this session?** The course taught you *how* to do data science and *how*
to accelerate it with AI. This session is about doing it *responsibly* — the
second half of CLO-3 ("considering reproducibility, ethics and responsible AI
use"). The message is not "AI is dangerous, be afraid" — it's "these are the
failure modes, here's how to think about them". Every professional data
scientist will make ethical judgment calls; this session gives you vocabulary
and a method.

**Bias — the pipeline view.** Bias is not only a model problem; it enters at
every stage:
- **Data collection:** who's in the dataset and who's missing? A hiring model
  trained on historical hires inherits historical discrimination; a face
  recognizer trained on mostly light-skinned photos performs worse on others.
- **Labeling/measurement:** how was the "answer" recorded? Who decided it?
- **Modeling:** the model optimizes what you told it to optimize — a
  recidivism score trained to predict re-arrest predicts *policing patterns*,
  not crime.
- **Deployment & feedback loops:** a model's decisions shape future data, which
  retrains the model — biases compound (the "feedback loop").
Teach with 2–3 concrete cases (e.g., the well-documented biased
recidivism/facial-recognition studies, or a simpler one: a bank's loan model
trained on historical approvals). The transferable lesson: **ask "who is in
this data, and who is affected by this model?"** — before building, not after.

**Privacy.** Data about people is not just data. Principles to apply: **consent**
(did people agree to this use?), **minimization** (use the least data needed),
**protection** (don't paste names/emails/health info into cloud LLMs; don't
commit CSVs of personal data to public repos — Session 4's `.gitignore`
lesson), **anonymization** (remove identifiers; note that anonymization is
harder than it looks). Course rule: *sensitive data never goes to a cloud LLM*;
use Ollama locally (Session 27) or aggregate before sharing.

**Provenance & transparency.** Every result should be traceable: where the data
came from (license, source — Session 11/23), what cleaning decisions were made
(Session 9's "decide, don't default"), and what AI contributed (the AI log from
Sessions 25–28). Transparency is what makes an analysis *auditable* — a grader,
boss, or regulator can check your claims. This is the ethics half of
Session 24's reproducibility coin.

**Communication ethics.** The chart that exaggerates, the metric chosen to flatter,
the correlation reported as cause — these are everyday ethical failures in
data communication (Session 13's honesty principles, now with stakes). Also: AI
tools make it *easier* to produce fluent, confident, wrong content — your
verification protocol (Session 25) is an ethical practice, not just a quality
practice.

**Writing the reflection (deliverable).** Structure for the project's
reflection (and reuse the disclosure template in your Assignment 2 README):
1. **Data:** source, license, who's represented/missing (bias check).
2. **Decisions:** 2–3 cleaning/model choices and their rationale.
3. **AI use:** what AI assisted, how it was verified, what was disclosed (AI log).
4. **Risks & limits:** what could go wrong if this analysis was used in
   practice, and what you'd do differently.
5. **Responsible-use statement:** one paragraph on what you changed because of
   this course's rules.
A good reflection is specific (names the actual choice and its reasoning) —
vague hand-waving earns no credit.

## 4. Important terminology

- **Bias** — systematic distortion; enters at data, labeling, modeling, deployment stages.
- **Feedback loop** — model decisions shape future data, compounding bias.
- **Privacy / consent / minimization** — people-data principles.
- **Anonymization** — removing identifiers (harder than it looks).
- **Provenance** — documented data origin and transformations.
- **Transparency / auditability** — results traceable to data and decisions.
- **Disclosure** — recording AI assistance (course AI-use policy).
- **Spurious correlation** — association from a third variable; dangerous when acted on.
- **Responsible AI use** — documented, verified, bounded AI use.
- **Reflection** — a written, specific account of ethical considerations and decisions.

## 5. Python examples

Ethical analysis is mostly *thinking* — but here are the concrete checks you can
run (and should):

```python
import pandas as pd
import seaborn as sns

titanic = sns.load_dataset("titanic")

# --- Who is in the data? (representation check) ---
print(titanic["sex"].value_counts(normalize=True))
print(titanic["class"].value_counts(normalize=True))

# --- Is the target itself biased? (survival by class) ---
print(titanic.groupby("class")["survived"].mean())

# --- Missingness as a bias signal: who has no age recorded? ---
print(titanic.groupby("class")["age"].apply(lambda s: s.isna().mean()))

# --- Always report model limitations next to results ---
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

df = titanic.dropna(subset=["survived", "age", "fare", "pclass"])
X = df[["pclass", "age", "fare"]]; y = df["survived"]
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=42, stratify=y)
m = DecisionTreeClassifier(max_depth=4, random_state=42).fit(Xtr, ytr)
acc = m.score(Xte, yte)
print(f"Model accuracy: {acc:.2f}")
print("BUT: trained on passengers with complete records only — older/"
      "poorer passengers are underrepresented in the training data.")
```

## 6. Beginner example

```python
# The bias question in one line — ask it about EVERY dataset:
print("Who is missing from this data, and who will be affected by the results?")
```

If a student can answer that line about their project, they've done the core
ethical work of this course.

## 7. Practical Data Science example

A worked case study for discussion (write on the board, then debrief):

> A team builds a model to approve small loans, trained on 5 years of the
> bank's historical approvals. The model is 85% accurate on historical data —
> and rejects a disproportionate share of applicants from one district.
> The training data reflected past bias: that district was under-served, so
> fewer past approvals → the model learned "district ⇒ risky".
>
> **Where bias entered:** historical data (collection), the label
> ("approved" = good, which encodes past policy), and the feedback loop
> (rejections now → fewer future applications → "confirms" the pattern).
> **What responsible practice looks like:** representation audit before
> modeling (the checks above), fairness metrics on protected groups, human
> review of borderline cases, transparent reporting of limitations.
> **Course-sized takeaway:** even a "simple" 85%-accurate model can be
> ethically harmful if you never asked who's in the data.

## 8. In-class activity (50 min)

1. **Case debrief (20 min):** read/discuss the loan-model case; name the stage
   where bias entered and one mitigation per stage.
2. **Representation audit (15 min):** run the titanic checks above on *your own
   project dataset* (or `tips`/`penguins`): who's missing, and what does that
   mean for your claims?
3. **Reflection sprint (15 min):** draft the five-section reflection for your
   project (10 minutes), then exchange with a partner for one concrete
   improvement (5 minutes).

## 9. Lab exercise

**Lab 30 is due today** (`labs/lab-30-ethics-and-responsible-ai.md`): ethics &
responsible AI — group bias audit, data sheet, AI disclosure; **Lab 29's n8n
pipeline** (`labs/lab-29-n8n-workflows.md`) also lands here. **Assignment 2
also due today** (API + Streamlit app,
`../assignments/assignment-02-api-streamlit-app/`). These are the last graded
deliverables before presentations.

## 10. Common mistakes

- Treating ethics as "don't do bad things" — it's *specific, reasoned decisions*, written down.
- Reporting model accuracy without stating who's in the training data.
- Pasting real personal data into a cloud LLM "just for a quick look".
- Using correlation as a causal claim because the model is accurate.
- Writing a vague reflection ("I think AI is useful but we should be careful") — name the actual choices.
- Believing "the data is neutral" — datasets are created by people with goals and blind spots.
- Ignoring the feedback loop: your model's decisions become tomorrow's training data.

## 11. Short assessment questions

1. Name the four stages where bias can enter a data pipeline.
2. Why is "predict re-arrest" a biased target for recidivism? (It measures policing, not crime.)
3. What is the course rule about sensitive data and cloud LLMs?
4. What does provenance mean, and why does it matter?
5. Why is anonymization harder than deleting names? (Quasi-identifiers, re-identification risk.)
6. List the five sections of the reflection deliverable.

## 12. CLO mapping

CLO-3: ethics and responsible AI use are the explicit final requirements of
CLO-3. This session converts them from slogans into practices — the
representation audit, the privacy rule, the disclosure/verification protocol,
and the written reflection — assessed in Lab 30, Assignment 2's documentation,
and the final project.

## 13. Suggested homework

- Finish Lab 30 + Assignment 2 and push before the deadline.
- Write the full ethics section of your project reflection using the five-part structure.
- Read: one article on a real-world AI bias case (bring one link to share at presentations).
- Prepare: Session 31 — presentations begin. Rehearse your 10-minute deck, and re-read the rubric in `../assessment-plan.md`.