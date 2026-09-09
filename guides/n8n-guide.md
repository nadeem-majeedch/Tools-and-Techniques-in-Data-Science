# n8n Guide

**n8n** is a visual automation tool: you connect *nodes* on a canvas —
trigger → fetch data → transform → save/notify — and n8n runs the workflow on
a schedule or when an event happens. It lets you automate the boring parts of
a data pipeline (re-fetch a report every morning, clean it, append it to a
file, email the summary) **without writing a web server**.

## Why it matters in this course

Automation is the CLO-3 skill of turning a one-off analysis into a
**reproducible process that runs without you**. A scheduled n8n workflow is
reproducibility in practice: same time, same steps, same output location,
every run logged.

## Core concepts

| Concept | Meaning |
|---|---|
| Workflow | the whole automation, drawn as nodes connected by lines |
| Trigger node | starts the run — a schedule (cron), webhook, or manual click |
| Action node | does work — HTTP Request, spreadsheet/file, database, etc. |
| Data between nodes | every node passes JSON items to the next node |
| Execution | one run of the workflow (n8n keeps a log — your audit trail) |

```text
(Schedule: every day 08:00) ─▶ (HTTP Request: Open-Meteo archive API)
        ─▶ (Code: reshape JSON to a flat table) ─▶ (Google Sheets / CSV file)
        ─▶ (optional: AI Agent node or notification)
```

## Setup (once)

```bash
# Simplest: run n8n with npx (Node.js required)
npx n8n            # opens the editor at http://localhost:5678
```

n8n runs **locally** on your machine — your data and credentials stay with
you (only the workflow definitions and app are downloaded). For class work,
install it, create a local account, and you are ready.

## A first workflow (~10 minutes)

1. Add a **Schedule Trigger** node → set to every day (or every hour for
   testing).
2. Add an **HTTP Request** node: `GET https://archive-api.open-meteo.com/v1/archive`
   with parameters for your city and date range — a **keyless** public API,
   so no account needed.
3. Add a **Code** node that takes the nested JSON and returns one item per
   day (flatten + convert to a table).
4. Add an output node (save to CSV/Google Sheets, or a **Telegram/email**
   node) — done: you now have an automated data collector.

## The workflow-in-Python pattern (no n8n needed)

You do not need n8n installed to learn its logic. The same workflow written
as Python is what [Notebook 19](../course-notebooks/19-n8n-workflows.ipynb)
teaches — a plain script that fetches, transforms, and saves, wrapped so it
can be scheduled:

```python
# collect_weather.py — run it from a scheduler (cron / Task Scheduler)
import pandas as pd
import requests

def run():
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {"latitude": 31.5, "longitude": 74.3,
              "start_date": "2026-01-01", "end_date": "2026-01-07",
              "daily": "temperature_2m_max", "timezone": "Asia/Karachi"}
    data = requests.get(url, params=params, timeout=20).json()
    frame = pd.DataFrame({
        "date": data["daily"]["time"],
        "tmax": data["daily"]["temperature_2m_max"],
    })
    frame.to_csv("weather.csv", index=False)
    print(f"Saved {len(frame)} days")

if __name__ == "__main__":
    run()
```

## Common errors

| Error | Fix |
|---|---|
| Workflow runs but saves nothing | inspect the **execution data** between nodes (click the node) — the output shape is probably nested |
| API call fails | check the URL/params in the HTTP node; many APIs need exact date formats |
| "Credentials required" | prefer keyless APIs (Open-Meteo) for class work; never commit real credentials |
| Schedule never fires | local n8n must be *running*; for always-on automation you would deploy n8n to a server |
| JSON too nested | use a Code node to flatten before saving |

## Responsible automation

- A scheduled workflow touches real files/services — keep it **read-only
  where possible** and test each node manually before enabling the schedule.
- Log runs (n8n execution history does this automatically) so you can tell
  what happened and when.
- Don't automate sending messages/emails to people without consent, and never
  paste private data into a cloud LLM inside a workflow.
- Disclose automation in your README/report, exactly like any other
  AI-assisted step.

## Go deeper

- Full lecture: [Session 29 — n8n Automation](../sessions/session-29-n8n-automation.md)
- Executed notebook: [Notebook 19 — n8n Workflows](../course-notebooks/19-n8n-workflows.ipynb)
- Practice: [Lab 29 · n8n Workflows](../labs/lab-29-n8n-workflows.md)
- Teacher's deep dive: [Module C topic 09](../module-c/topic-09-n8n.md)
- AI agents (the loop n8n's AI node wraps): [AI Agents Guide](ai-agents-guide.md)
