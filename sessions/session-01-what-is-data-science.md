# Session 1 — What is Data Science?

**Week 1 · Session 1 · Module A · 90 min · CLO-1 foundation**

## 1. Learning objectives

By the end of this session, students can:
- Explain what data science is and why organizations need it.
- Name the stages of the data science lifecycle in order.
- Distinguish the roles of data analyst, data scientist, and data engineer.
- Map every part of this course (Modules A, B, C) to a lifecycle stage.
- Complete their environment setup checklist (from `resources/setup-guide.md`).

## 2. Key concepts

- Data science = turning data into decisions/insight using computation, statistics, and domain knowledge.
- The data science lifecycle: **Ask → Acquire → Clean → Explore → Model → Communicate**.
- Data ≠ information ≠ knowledge: raw data only becomes useful after processing and interpretation.
- The toolchain of this course (Python, Jupyter, Pandas, scikit-learn, AI tools) maps to lifecycle stages.
- Reproducibility: someone else (or future you) must be able to re-run your work.

## 3. Detailed lecture notes

**Why data science?** Start with a concrete question every student has felt: "How much should a pizza delivery tip be?" or "Will it rain tomorrow?" Organizations face thousands of such questions daily — pricing, churn, fraud, demand. Data science is the discipline of answering them systematically from data instead of gut feeling. Emphasize that the *question* comes first; tools come second.

**What data science actually is.** It sits at the intersection of three fields: statistics (uncertainty, sampling), computer science (scaling, automation), and domain knowledge (understanding what the numbers mean). The famous "data science Venn diagram" is a useful image: where the circles overlap is data science. A data scientist spends most of their time on data preparation and communication, not on fancy models — set this expectation now.

**The lifecycle.** Walk through the 6 stages with a running example (e.g., "Why are tips higher on weekends?"):
1. **Ask** — define a clear, answerable question.
2. **Acquire** — get the data (files, APIs, databases).
3. **Clean** — fix missing values, wrong types, duplicates (usually 60–80% of real effort).
4. **Explore** — visualize and summarize to understand patterns (EDA).
5. **Model** — use statistics/ML to answer the question.
6. **Communicate** — present results so people act on them.

Stress the loop: exploration usually refines the question; you go around the cycle several times.

**Roles.** Data analyst (explore/report, stages 1–4), data scientist (adds modeling, stages 1–6), data engineer (builds and maintains the pipelines that acquire/store data). Beginners often conflate these; knowing the distinction helps career planning.

**Course map.** Module A (weeks 1–8) = stages Acquire→Explore. Module B (weeks 9–12) = Model. Module C (weeks 13–16) = AI-assisted versions of these stages plus Communication and ethics. Show how each module maps to lifecycle stages on the whiteboard.

**Why Python?** Free, readable, huge ecosystem (Pandas, scikit-learn), and the de facto standard in industry. Why Jupyter? Interactive exploration matches how data science actually happens. Why Git? Because reproducibility starts with version control.

## 4. Important terminology

- **Dataset** — a collection of data, usually a table of rows (observations) and columns (features).
- **Observation / record / row** — one instance (e.g., one customer, one day).
- **Feature / variable / column** — one measurable attribute (e.g., `total_bill`, `tip`).
- **EDA** — Exploratory Data Analysis: summarizing and visualizing data before modeling.
- **Model** — a simplified mathematical representation learned from data (e.g., a line that predicts tip from bill).
- **ML** — Machine Learning: letting a program learn patterns from data rather than being explicitly programmed.
- **Insight** — a useful, non-obvious finding derived from data.
- **Reproducibility** — the ability to re-run an analysis and obtain the same results.
- **Data science lifecycle** — the end-to-end process from question to communicated insight.
- **Jupyter notebook** — an interactive document mixing code, text, and visual output.

## 5. Python examples

```python
# Check the environment works — run in a Jupyter cell or terminal
import sys
print("Python version:", sys.version)

# A first taste of "data" in Python: a list of tip percentages
tip_percent = [18, 22, 15, 25, 19, 21, 16]
print("Average tip %:", sum(tip_percent) / len(tip_percent))
print("Max tip %:", max(tip_percent))
```

Explain: this is *calculation*; data science begins when data lives in many files
and questions are too complex for manual computation — that is why Pandas and
NumPy exist (sessions 5–8).

## 6. Beginner example

```python
# The smallest "data science" program: count how many values pass a condition
scores = [45, 72, 88, 51, 93, 67]
passed = [s for s in scores if s >= 60]
print(f"{len(passed)} of {len(scores)} students passed")
```

Point out the question → data → answer shape. That *is* the lifecycle, miniaturized.

## 7. Practical Data Science example

```python
import seaborn as sns
import pandas as pd

tips = sns.load_dataset("tips")          # real restaurant tipping data
print(tips.head())                        # first 5 rows
print(tips["tip"].mean())                 # average tip
print(tips.groupby("day")["tip"].mean())  # average tip by day
```

Walk through: we asked a question ("Do tips vary by day?"), acquired built-in
data, and took a first exploratory peek. Weeks 4–8 will teach exactly these
tools. Do **not** explain `groupby` in depth — it is a preview.

## 8. In-class activity (50 min)

1. **Setup checklist (30 min):** follow `resources/setup-guide.md` — Python, venv,
   `pip install -r requirements.txt`, Jupyter Lab launch, first notebook that
   imports the core libraries. Pair up: strong students help weaker ones.
2. **Question mapping (15 min):** in pairs, write one question you could answer
   with data (e.g., about your university, sports, food). Sketch which lifecycle
   stages your question needs. Two volunteers share with the class.
3. **Lifecycle quiz game (5 min):** instructor names an activity ("fixing missing
   values"), students call out the stage.

## 9. Lab exercise

No formal lab this week. The required "lab" is the **environment setup** from
`resources/setup-guide.md` — every checklist item must be ticked. Confirm with
the instructor that Jupyter runs and `import pandas, numpy, matplotlib, seaborn,
sklearn` all succeed.

## 10. Common mistakes

- Installing packages **globally** instead of inside a virtual environment → later package conflicts. Always activate `.venv` first.
- Skipping the "Ask" stage and jumping straight to code → analyses without purpose.
- Thinking data science = machine learning → neglecting cleaning, EDA, communication (the majority of real work).
- Not checking that Jupyter uses the venv Python → `ModuleNotFoundError` later.
- Expecting to understand every tool today → the course builds up gradually; patience is part of the skill.

## 11. Short assessment questions

1. Put the lifecycle stages in order: Model, Acquire, Ask, Clean, Explore, Communicate.
2. True/False: EDA happens after modeling. (False — before, to understand the data.)
3. Which role focuses mainly on acquiring and storing data at scale? (a) analyst (b) scientist (c) engineer.
4. Why does reproducibility matter for a data science project? Give one reason.
5. Give one example each of a feature and an observation from the `tips` dataset.

## 12. CLO mapping

CLO-1 (foundation): students learn the lifecycle stages that the Pandas/NumPy
tools of Module A serve. This session frames *why* every later tool exists.
No direct CLO-2/CLO-3 content yet — the AI-assisted stage is previewed in Module C.

## 13. Suggested homework

- Tick off the full setup checklist; fix any failures with the troubleshooting table.
- Read: *The Art of Data Science* (Peng & Matsui), chapters 1–2 (free online).
- Bring one dataset you would like to analyze this semester (file, link, or just an idea) — used in Session 15's EDA case study.
- Watch (optional): a 10-minute "what is data science" explainer video of your choice; come with one new term to share.