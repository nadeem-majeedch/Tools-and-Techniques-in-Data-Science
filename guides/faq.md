# Frequently Asked Questions

Short answers to the questions students ask most. Each one links to the full
material. If yours is not here, try the [course schedule](../weekly-schedule.md)
or ask on the course channel.

## Course & navigation

??? question "Where do I start?"
    Follow the learning path on the [Home page](../index.md) top to bottom:
    Python → NumPy → Pandas → cleaning → EDA → visualization → Git → APIs →
    machine learning → Streamlit → PandasAI → LLMs → Ollama → agents → n8n →
    final project. The [Course Schedule](../weekly-schedule.md) shows which
    week each step belongs to.

??? question "What is the difference between a session, a lab, and an assignment?"
    A **session** is a 90-minute lecture with notes and examples. The
    **lab** for that week (in [Labs](../labs/README.md)) is the hands-on
    exercise you submit. **Assignments**
    ([1](../assignments/assignment-01-data-cleaning-eda/README.md) and
    [2](../assignments/assignment-02-api-streamlit-app/README.md)) are two
    larger graded projects that combine many sessions' skills.

??? question "Where are the quiz and exam answer keys?"
    They are intentionally **not published** on this site — quizzes and
    exams are graded in class and your instructor distributes the keys.
    See the [Quizzes](../assessments/quizzes.md) and [Exams](../assessments/exams.md)
    pages for format and how to prepare.

??? question "Where are the lab / assignment solutions?"
    Instructor solutions exist in the repository but are excluded from this
    website. Your instructor decides when to release them. Until then, the
    labs give you expected outputs so you can check your own work.

??? question "How is my final grade calculated? Can I track it myself?"
    The scheme is **Continuous 25%** (Labs 10 · Quizzes 5 · Assignments 10),
    **Midterm 35%**, **Final 40%** (Final exam 25 · Final project 15). Each
    component contributes `(your marks ÷ max marks) × weight` to a score out
    of 100 — see [assessment plan §2](../assessment-plan.md). A ready-made
    [Grade Calculator](../tools/README.md) (Streamlit app) is included in the
    course repository: run `streamlit run tools/grade_app.py`.

## Environment & Python

??? question "`python` is not recognized / not found"
    Python isn't on your PATH. On Windows re-run the installer and tick
    *"Add python.exe to PATH"*; on macOS/Linux try `python3`. Then open a
    **new** terminal. Full steps: [Setup guide](../resources/setup-guide.md).

??? question "`pip install` fails or installs to the wrong place"
    You probably installed outside a virtual environment. Create one once per
    project: `python -m venv .venv`, activate it
    (`.venv\Scripts\activate` on Windows, `source .venv/bin/activate`
    elsewhere), then `pip install -r requirements.txt`.

??? question "Which Python / library versions does the course use?"
    Python 3.11+ with NumPy, Pandas, Matplotlib, Seaborn, scikit-learn,
    requests, jupyter (plus Streamlit for the apps module and pandasai/ollama
    for Module C). The pinned list is `requirements.txt` in the repo root.

??? question "Jupyter shows no kernel or won't start"
    From an **activated** venv run `pip install jupyter`, then
    `jupyter lab`. If a notebook still shows no kernel,
    `pip install ipykernel` and restart Jupyter.

## Git & GitHub

??? question "How do I submit a lab?"
    Push your executed notebook (Run All, outputs visible) to your course
    repository and confirm the commit hash — the exact loop is in the
    [Git & GitHub Guide](git-github-guide.md).

??? question "`git push` says my changes were rejected"
    Someone pushed first. Run `git pull`, resolve any conflict the editor
    shows you, commit, and push again.

??? question "I committed the wrong file / a huge file"
    Unstage with `git restore --staged <file>`, add it to `.gitignore`, and
    make a new commit. For history rewriting (advanced) ask your instructor.

## Streamlit

??? question "`streamlit` is not a recognized command"
    Your venv isn't activated, or Streamlit isn't installed there:
    `pip install streamlit`, then `streamlit run app.py`.

??? question "My app reruns the whole script when I click a widget — is that normal?"
    Yes — that is the Streamlit model. Use `@st.cache_data` for expensive
    loads and `st.session_state` to keep values between reruns. See the
    [Streamlit module](../streamlit/streamlit-introduction.md).

??? question "Charts don't appear / look broken in my app"
    Pass the figure explicitly: `st.pyplot(fig)` for Matplotlib, and use
    `st.dataframe(df)` (not `st.write(df)`) for large tables. The
    [Streamlit FAQ](../streamlit/streamlit-faq.md) covers the top gotchas.

## PandasAI, Ollama & the AI tools

??? question "PandasAI says it can't connect or needs a model"
    PandasAI needs an LLM behind it. For this course, run Ollama first:
    `ollama pull llama3.2`, then create the agent with
    `config={"llm": OllamaLLM(model="llama3.2")}`. See the
    [PandasAI Guide](pandasai-guide.md).

??? question "Ollama is slow or crashes on my laptop"
    Use a smaller model (`llama3.2:3b`), close other apps, and expect CPU-only
    inference to be slow — that is normal without a GPU.

??? question "Can I use ChatGPT instead of Ollama for the labs?"
    For labs graded on Module C you should use the **local** path so no data
    leaves your machine and the environment is identical for everyone. If your
    instructor allows a cloud model, never paste non-public data into it.

??? question "The AI gave me a number that is wrong. Did I do something wrong?"
    Possibly nothing — models hallucinate. The course rule is to **verify one
    number by hand with pandas and log it**. See the
    [LLM & Ollama Guide](llm-ollama-guide.md) and
    [Session 30 · Ethics](../sessions/session-30-ethics-and-responsible-ai.md).

??? question "My agent loops forever / calls tools with nonsense arguments"
    Bound the loop (`max_iterations`), whitelist a few small tools, and
    validate arguments. The exact pattern is in the [AI Agents Guide](ai-agents-guide.md).

??? question "Do I need to install n8n for the n8n lab?"
    The lab works both ways: install n8n (`npx n8n`) for the visual part, or
    follow the workflow-in-Python pattern in
    [Notebook 19](../course-notebooks/19-n8n-workflows.ipynb) — see the [n8n Guide](n8n-guide.md).

## Assessments & policies

??? question "When are the quizzes and exams?"
    Quiz 1: Week 8 Session 15 · Quiz 2: Week 15 Session 29 · Midterm: Week 8
    Session 16 · Final: Week 16 Session 32. Full calendar on the
    [Course Schedule](../weekly-schedule.md).

??? question "Is using AI allowed in my submissions?"
    The course teaches AI-assisted work — but every AI-assisted step must be
    **disclosed, verified, and logged**, and quizzes/exams are AI-free. Read
    the policy in the [Assessment Plan](../assessment-plan.md) before you
    start anything.

??? question "How is the final project graded and presented?"
    Proposal → GitHub repo with README → report → 6-minute presentation in
    Week 16, plus an individual viva. Rubric and templates:
    [Final Project](../projects/README.md).

## Still stuck?

- [Streamlit FAQ](../streamlit/streamlit-faq.md) — app-specific questions
- [Resources](../resources/README.md) — official docs and free books
- [GitHub Discussions / Issues] on the course repository — if you found a
  real bug in the materials, report it there
