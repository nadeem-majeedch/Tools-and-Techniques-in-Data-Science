# Course Outline — Introduction to Data Science

## 1. Course identity

| Field | Value |
|---|---|
| Course title | Introduction to Data Science — Tools and Techniques in Data Science |
| Program | BS Data Science |
| Semester | 3rd |
| Duration | 16 weeks |
| Sessions | 2 per week, 90 minutes each (32 sessions total) |
| Language | Python |
| Prerequisites | Basic programming concepts (variables, loops, functions); high-school level statistics is helpful but not required |

## 2. Description

The course gives students hands-on command of the core toolchain of modern data
science. Module A builds the data-handling foundation: Python with Jupyter, version
control with Git/GitHub, NumPy, Pandas, data acquisition, data cleaning, and
exploratory visualization with Matplotlib and Seaborn. Module B introduces basic
machine learning with scikit-learn — regression, classification, clustering, and
model evaluation. Module C explores AI-assisted data science: interacting with LLMs
through PandasAI and local models via Ollama, automating workflows with n8n, and
building simple AI agents — all under a lens of reproducibility, ethics, and
responsible AI use.

## 3. Learning outcomes (CLOs)

| # | CLO | Cognitive level | Module |
|---|---|---|---|
| CLO-1 | Apply Python and standard data science libraries to acquire, clean, manipulate, visualize and explore datasets. | Apply | A |
| CLO-2 | Apply appropriate data science tools and basic machine learning techniques to solve introductory data-driven problems. | Apply / Analyze | B |
| CLO-3 | Develop simple AI-assisted data science workflows using LLMs, local models, automation tools and basic AI agents while considering reproducibility, ethics and responsible AI use. | Apply / Create | C |

Full definitions and mapping: [CLOs.md](CLOs.md)

## 4. Module structure

| Module | Weeks | Topics | CLO |
|---|---|---|---|
| A | 1–8 | Course intro & data science lifecycle; Python refresher; Jupyter; Git/GitHub; NumPy; Pandas (Series/DataFrame, I/O, indexing); data cleaning; data acquisition (files, APIs); combining data; Matplotlib & Seaborn; EDA workflow | CLO-1 |
| B | 9–12 | Intro to ML & scikit-learn; train/test split; linear regression; classification (k-NN, logistic regression, decision trees); clustering (k-means); cross-validation & pipelines; final project kickoff; reproducible workflows | CLO-2 |
| C | 13–16 | LLMs for data science; PandasAI; Ollama local models; simple AI agents; n8n automation; reproducibility; ethics & responsible AI; final project presentations | CLO-3 |

## 5. Session format (90 minutes)

| Block | Time | Activity |
|---|---|---|
| Concept & demo | ~25 min | Instructor-led topic introduction with live demos |
| Hands-on | ~50 min | Guided notebook exercises (see `notebooks/`) |
| Wrap-up & checkpoint | ~15 min | Summary, checkpoint questions, preview of next session |

Most sessions pair a short in-class exercise with the weekly lab, which students
finish and submit before the following session.

## 6. Tools & environment

| Tool | Purpose | Used in |
|---|---|---|
| Python 3.11+ | Programming language | All |
| Jupyter Lab | Interactive notebooks | All |
| Git / GitHub | Version control, collaboration, submission | Weeks 2+ (all submissions) |
| NumPy | Numerical computing | Weeks 3, 8 |
| Pandas | Data manipulation & cleaning | Weeks 4–8 |
| Matplotlib, Seaborn | Visualization & EDA | Weeks 7–8 |
| Scikit-learn | Machine learning | Weeks 9–12 |
| PandasAI | Natural-language data queries (LLM) | Week 13 |
| Ollama | Local LLM runtime | Week 14 |
| n8n | Workflow automation | Week 15 |

Setup instructions: [resources/setup-guide.md](resources/setup-guide.md)

## 7. Assessment map

| Component | Count | Weight* | CLOs assessed |
|---|---|---|---|
| Labs | 10 | 25% | 1, 2, 3 |
| Quizzes | 3 | 10% | 1, 2, 3 |
| Assignments | 3 | 15% | 1, 2, 3 |
| Midterm exam | 1 | 15% | 1, 2 |
| Final exam | 1 | 15% | 1, 2, 3 |
| Final project | 1 | 20% | 1, 2, 3 |

\* Proposed weights. Full rubric and policy details: [assessment-plan.md](assessment-plan.md)

## 8. Reference materials

Primary references (no purchase required — official docs and free books are used):

- *Python for Data Analysis* (W. McKinney) — free online edition
- *Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow* (A. Géron) — chapters 1–6, 9
- *The Art of Data Science* (R. Peng & E. Matsui) — free online
- Official docs: pandas, NumPy, Matplotlib, Seaborn, scikit-learn
- Ollama docs (ollama.com) and n8n docs (docs.n8n.io)

A curated reading list and cheatsheet links: [resources/README.md](resources/README.md)

## 9. Policies

Attendance, late-submission, academic-integrity, and AI-use policies are defined in
[assessment-plan.md](assessment-plan.md). Note that this course teaches AI-assisted
workflow development (CLO-3) — the AI-use policy therefore focuses on **disclosure
and understanding**, not prohibition.