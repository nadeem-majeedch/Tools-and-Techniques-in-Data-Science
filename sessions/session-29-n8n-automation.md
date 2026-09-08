# Session 29 — n8n: Workflow Automation

**Week 15 · Session 29 · Module C · 90 min · CLO-3**

## 1. Learning objectives

By the end of this session, students can:
- Explain what workflow automation is and why data teams use it.
- Start n8n locally and build a workflow from triggers, nodes, and connections.
- Use HTTP Request, Code, and notification nodes to collect/process data.
- Run a workflow manually and on a schedule; inspect run history.
- Map an n8n workflow to the data lifecycle stages (acquire → process → communicate).
- Plan one automation relevant to their own project.

## 2. Key concepts

- **n8n = a visual automation platform:** workflows of *nodes* connected by wires; each node does one step.
- **Trigger → process → output:** a workflow starts with a trigger (schedule, webhook, manual) and ends with an action (save, notify, store).
- **No code required for most nodes** — but a Code node lets you use the Python-ish skills you have (n8n uses JavaScript by default; mention it).
- **HTTP Request node = Session 11's `requests` in visual form** (acquire data from an API).
- Workflows are **versioned and shareable** (export as JSON) — reproducibility for automation.
- Automations need **guardrails**: error handling, idempotency (re-runs are safe), and logging.

## 3. Detailed lecture notes

**Why automation?** A recurring data task — fetch weather every morning, watch
an API for changes, email a weekly summary — is a perfect automation candidate.
Doing it by hand is error-prone and doesn't scale; scripting it (Sessions 11,
28) works but requires someone to run the script. **n8n** fills the gap: a
visual tool where you wire together steps and let a *schedule or event* run
them. Data teams automate the boring 80% (collection, transformation,
notifications) so humans spend time on the interesting 20% (interpretation).
This is the "automation tools" phrase in CLO-3.

**The mental model: nodes and wires.** A workflow is a directed graph. **Nodes**
are steps — each with inputs and outputs; **connections** (wires) pass data
between them. Every workflow has:
1. **A trigger** — what starts it: *Manual* (run button), *Schedule*
   (cron, e.g., every morning at 8), *Webhook* (an incoming HTTP call).
2. **Processing nodes** — *HTTP Request* (call an API — the visual `requests`),
   *Code* (custom logic), *Set/Edit Fields* (rename/shape data), *Filter*
   (conditional steps).
3. **Output/action nodes** — *Google Sheets / local file*, *Email / notification*,
   *n8n's data store*.
Demo build (live, 10 minutes): **Schedule → HTTP Request (Open-Meteo weather)
→ Code (extract temperature) → Email/console log**. Students see the whole
lifecycle "acquire → process → communicate" as a picture.

**Mapping to your skills.** The *HTTP Request* node does what `requests.get`
did in Session 11 — same URL, same params, same JSON response, no Python needed.
The *Code* node is where Python-ish logic lives (n8n's default is JavaScript —
reassure: the *thinking* transfers; syntax differs). The workflow *is* your
script; the schedule *is* your cron. For data science workflows, the common
shape: pull data → transform into a clean table → append to a dataset or
notify a person. A project example: "every morning, fetch today's weather for
our city and append it to `datasets/weather.csv`" — that's a real, useful,
15-node-max automation.

**Guardrails (the professional part).** Automations run unattended — they must
be safe to fail:
- **Error handling:** every node has error paths; add a notification on failure
  ("workflow failed — check logs").
- **Idempotency:** re-running must not duplicate data — dedupe on append, or
  overwrite a single-row file.
- **Logging:** n8n keeps execution history; export/save workflows as JSON
  (reproducibility — Session 24's theme, applied to automation).
- **Secrets:** API keys go in n8n credentials (encrypted), never in the workflow JSON you share.
These three — failure visibility, safe re-runs, recorded config — are what make
an automation *trustworthy*, and they're what the rubric's
"automation component" checks.

**n8n vs. the agent (Session 28) — one paragraph.** An agent decides *what* to
do, step by step, using LLM reasoning; a workflow does a *fixed, predictable*
sequence. Use workflows when the steps are known; use agents when the path
depends on intermediate results. Many real systems mix both — an agent that
needs data calls a workflow; a workflow that hits an unexpected case calls an
agent. For this course, one solid automation is enough — don't over-engineer.

## 4. Important terminology

- **Workflow** — a connected set of nodes that accomplishes a task.
- **Node** — a single step (trigger, HTTP request, code, notification…).
- **Trigger** — the node that starts the workflow (manual/schedule/webhook).
- **Connection** — data flow between nodes.
- **HTTP Request node** — calls an API (visual `requests`).
- **Code node** — custom logic (JavaScript by default in n8n).
- **Credential** — encrypted stored secrets (API keys).
- **Execution** — one run of a workflow; n8n keeps history.
- **Idempotency** — safe to run repeatedly without duplicating effects.
- **Error path / error handling** — what happens when a node fails.
- **Cron schedule** — time-based trigger pattern (e.g., `0 8 * * *` = daily 8:00).

## 5. Python examples

n8n is visual — but the same task in code makes the mapping obvious:

```python
# What the n8n workflow does, expressed in the Python you already know:
import requests
import pandas as pd
from datetime import date

# 1. Trigger (schedule) -> 2. HTTP Request -> 3. Code -> 4. Save
url = "https://api.open-meteo.com/v1/forecast"
params = {"latitude": 31.5, "longitude": 74.3, "current_weather": True}
data = requests.get(url, params=params, timeout=10).json()["current_weather"]

row = pd.DataFrame([{"date": str(date.today()), **data}])
existing = pd.read_csv("datasets/weather.csv") if pd.io.common.file_exists("datasets/weather.csv") else None
pd.concat([existing, row], ignore_index=True).drop_duplicates("date").to_csv(
    "datasets/weather.csv", index=False)
```

In n8n: `Schedule Trigger` → `HTTP Request` (same URL/params) → `Code` node
(with the equivalent transform) → `Spreadsheet File` node. Same pipeline,
visual wiring. Show both side by side — that's the aha moment.

## 6. Beginner example

The first workflow everyone builds (10 minutes):
1. Add a **Manual Trigger**.
2. Add an **HTTP Request** node → GET `https://jsonplaceholder.typicode.com/todos/1`.
3. Add an **IF** node → check `completed == false`.
4. Connect to a **Console/notification** node that prints "pending".
Run it; inspect the execution data in n8n's UI. If this runs, the platform
mechanics are understood — everything else is more nodes.

## 7. Practical Data Science example

Project-relevant automation (build together in class):

> **Goal:** every morning at 8:00, fetch today's weather for your city and
> append one row to `datasets/weather.csv` (idempotent: no duplicate dates).
>
> **Workflow:** Schedule Trigger (`0 8 * * *`) → HTTP Request
> (Open-Meteo forecast, `current_weather=true`) → Code (build a one-row table,
> dedupe on date) → Spreadsheet File (append to CSV).
> **Guardrails:** add an error branch that emails/slack-notifies on failure;
> verify execution history shows one successful run per day.
> **Reproducibility:** export the workflow JSON into `project/automations/` and
> document credentials are stored in n8n (not in the JSON).

This is the course's automation track in miniature — and a genuinely useful
artifact for the final project's AI-assisted component.

## 8. In-class activity (50 min)

1. **First workflow (15 min):** build the beginner example; run it; read the
   execution data viewer (inputs/outputs per node).
2. **Weather automation (25 min):** build the practical example end-to-end;
   add the failure notification node; run it twice and confirm no duplicate
   date rows (idempotency check).
3. **Map it (10 min):** draw your own workflow for a task from your project
   (paper or whiteboard): trigger, 2–4 nodes, output, one guardrail. Share with
   a partner for feedback.

## 9. Lab exercise

**Quiz 2 at session start** — Weeks 8–14 (EDA, ML, LLM tooling); question bank
with key in `../quizzes/quiz-2.md`.

**Lab 29** (`../labs/lab-29-n8n-workflows.md`) — due before Session 30: build
the weather-collector pipeline in Python (idempotent append), design the n8n
workflow, export the JSON to the repo, and write the reflection (what did
automation save? what could go wrong? how do you keep it trustworthy?). Push.

## 10. Common mistakes

- No trigger → workflow does nothing (or only runs manually forever).
- API keys hard-coded in nodes instead of credentials → leaked when the JSON is shared.
- Non-idempotent appends → duplicate rows on every schedule tick.
- No error handling → a silent failure (automation is worse than no automation when it fails quietly).
- Over-building: 40-node workflows for a task a Code node could do in 10 lines.
- Forgetting execution history is your log — check it before trusting an automation.
- Confusing n8n's JavaScript Code node with Python — the logic transfers; the syntax doesn't (read the docs tab).

## 11. Short assessment questions

1. What are the three parts every workflow has (trigger, processing, output)?
2. Name two trigger types and when you'd use each.
3. Which node replaces `requests.get(...)` from Session 11?
4. What is idempotency, and why does an append-based automation need it?
5. Where should an API key live in n8n, and why?
6. How is a workflow different from an AI agent (Session 28)? (Fixed steps vs. LLM-decided steps.)

## 12. CLO mapping

CLO-3: n8n delivers the "automation tools" in the CLO — a visual, reproducible
way to build data-collection/processing pipelines. Guardrails (idempotency,
error paths, credentials) are the responsible-use dimension, and exported
workflow JSON extends Session 24's reproducibility to automation.

## 13. Suggested homework

- Finish Lab 29 and push (due Session 30, together with Assignment 2).
- Practice: extend your weather workflow — add a Code node computing the 7-day average and a notification when today's temp is >2σ from the mean.
- Read: n8n docs (docs.n8n.io) — "Introduction to workflows" and "Triggers".
- Preview: Session 30 closes the course's substance — ethics & responsible AI, with the final reflection you'll write for the project.