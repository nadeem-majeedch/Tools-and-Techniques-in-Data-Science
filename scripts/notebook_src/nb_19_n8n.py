# Content for notebook 19: n8n workflows.
CELLS = [
    ("md", """# 19 — n8n Workflows

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-3 — Develop AI-assisted data science workflows (automation tools).

n8n is a **visual automation platform**: you wire together *nodes* (steps)
and let a schedule or event run the workflow. Data teams automate the boring
80% — collection, transformation, notifications — so humans focus on the
interesting 20%. This notebook teaches the mental model, then builds the
*exact same pipeline in Python* so you can run it anywhere.

> n8n itself is a separate application (install: `npx n8n` or Docker; see
> `resources/setup-guide.md`). The Python code here is the "workflow in
> code" — same steps, executable in this notebook.

---
"""),("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Explain the node-and-wire model of a workflow.
2. Identify the three parts of every workflow: trigger, processing, output.
3. Map an n8n workflow to the data lifecycle (acquire → process → communicate).
4. Build the equivalent pipeline in Python with idempotency and error handling.5. Read and export a workflow as JSON (reproducibility).

---
"""),
    ("code", """# Make sure the datasets/ folder exists next to this notebook.
from pathlib import Path
Path("datasets").mkdir(exist_ok=True)
print("datasets/ ready")
"""),
    ("md", """## Theory: nodes and wires

Every n8n workflow has:

1. **A trigger** — what starts it: *Manual* (run button), *Schedule* (cron,
   e.g. every morning at 8), *Webhook* (incoming HTTP call).
2. **Processing nodes** — *HTTP Request* (call an API — the visual
   `requests`), *Code* (custom logic), *Filter* (conditions), *Set* (shape data).
3. **Output nodes** — *Spreadsheet File* (CSV), *Email / notification*,
   *Google Sheets*, etc.

A real project example: **Schedule → HTTP Request (weather API) → Code
(extract temperature) → Email** = "every morning, email me today's
weather." That's the whole lifecycle as a picture.

The professional rules for automations (they run unattended!):

- **Idempotency** — re-running must not duplicate data.
- **Error handling** — failures must be visible (notify on error).
- **Secrets** — API keys live in n8n credentials, never in shared JSON.
- **Versioning** — export workflows as JSON into your repo.

---
"""),("code", """# The workflow-as-code version of the classic n8n demo:
#   Manual/Schedule -> HTTP Request -> Code -> File/Notification
import requests
import pandas as pd
from pathlib import Path

CACHE = Path("datasets/n8n-weather-demo.csv")

def trigger_manual():
    \"\"\"Trigger node: return the task context.\"\"\"
    return {"task": "daily weather"}

def http_request(lat, lon):
    \"\"\"HTTP Request node: fetch current weather from Open-Meteo.\"\"\"
    url = "https://api.open-meteo.com/v1/forecast"
    r = requests.get(url, params={"latitude": lat, "longitude": lon,
                                  "current_weather": True}, timeout=15)
    r.raise_for_status()
    return r.json()["current_weather"]

def code_node(payload):
    \"\"\"Code node: shape the payload into one table row.\"\"\"
    return pd.DataFrame([payload])

def output_node(df):
    \"\"\"Output node: append to CSV, idempotently (no duplicate timestamps).\"\"\"
    if CACHE.exists():
        old = pd.read_csv(CACHE)
        df = pd.concat([old, df], ignore_index=True).drop_duplicates("time")
    df.to_csv(CACHE, index=False)
    return df

# Run the workflow once
try:
    context = trigger_manual()
    payload = http_request(31.5, 74.3)
    table = code_node(payload)
    result = output_node(table)
    print(f"workflow ran: {len(result)} rows cached (idempotent)")
    print(result.tail(2))
except Exception as e:
    print("workflow failed:", e)
"""),
    ("md", """## The idempotency guarantee, demonstrated

Run the "workflow" twice — the CSV must not grow. This is the single most
important property of an automation: re-runs are safe.

---
"""),("code", """import pandas as pd
from pathlib import Path

CACHE = Path("datasets/n8n-weather-demo.csv")

def run_workflow():
    if CACHE.exists():
        old = pd.read_csv(CACHE)
    else:
        old = pd.DataFrame()
    row = pd.DataFrame([{"time": "demo-2026-04-10T08:00", "temperature": 21.5}])
    merged = pd.concat([old, row], ignore_index=True).drop_duplicates("time")
    merged.to_csv(CACHE, index=False)
    return len(merged)

n1 = run_workflow()
n2 = run_workflow()
n3 = run_workflow()
print("rows after runs 1, 2, 3:", n1, n2, n3, "-> no duplicates")
"""),
    ("md", """## A workflow as JSON (what n8n exports)

n8n workflows are JSON: nodes with types, names, and connections. You can
version this file in Git — the automation becomes reproducible. This cell
builds the JSON for our weather workflow by hand so you can see its shape.

---
"""),("code", """import json

workflow = {
    "name": "Daily Weather Fetch",
    "nodes": [
        {"name": "Schedule", "type": "n8n-nodes-base.scheduleTrigger",
         "parameters": {"rule": {"interval": [{"field": "hours", "hoursInterval": 24}]}}},
        {"name": "HTTP Request", "type": "n8n-nodes-base.httpRequest",
         "parameters": {"url": "https://api.open-meteo.com/v1/forecast",
                        "method": "GET",
                        "queryParameters": {"parameters": [
                            {"name": "current_weather", "value": "true"}]}}},
        {"name": "Code", "type": "n8n-nodes-base.code",
         "parameters": {"jsCode": "return [items[0].json.current_weather];"}},
        {"name": "Save to CSV", "type": "n8n-nodes-base.spreadsheetFile"},
    ],
    "connections": {
        "Schedule": {"main": [[{"node": "HTTP Request", "type": "main", "index": 0}]]},
        "HTTP Request": {"main": [[{"node": "Code", "type": "main", "index": 0}]]},
        "Code": {"main": [[{"node": "Save to CSV", "type": "main", "index": 0}]]},
    },
}

with open("datasets/weather-workflow.json", "w") as f:
    json.dump(workflow, f, indent=2)
print("exported datasets/weather-workflow.json")
print("nodes:", [n["name"] for n in workflow["nodes"]])
"""),
    ("md", """## Beginner example: one trigger, one request

The minimal workflow: Manual Trigger → HTTP Request → console. In n8n you
build it in under two minutes; here is the same logic in Python.

---
"""),("code", """import requests

try:
    r = requests.get("https://jsonplaceholder.typicode.com/todos/1", timeout=10)
    r.raise_for_status()
    print("HTTP Request node output:", r.json())
except requests.exceptions.RequestException as e:
    print("request failed:", e)

# Expected output (online):
#   HTTP Request node output: {'userId': 1, 'id': 1,
#      'title': 'delectus aut autem', 'completed': False}
"""),
    ("md", """## Intermediate example: a scheduled-style pipeline with a notification

"Every morning, check today's forecast; if rain is expected, notify." In
n8n this is Schedule → HTTP Request → Filter (rain) → Notification. In
Python: the same steps as functions — with the filter making the decision.

---
"""),("code", """def fetch_forecast(lat, lon):
    \"\"\"HTTP Request: get today's precipitation forecast.\"\"\"
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon,
              "daily": "precipitation_sum", "forecast_days": 1}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json()["daily"]["precipitation_sum"][0]

def filter_rain(rain_mm, threshold=1.0):
    \"\"\"Filter node: only 'notify' when rain exceeds the threshold.\"\"\"
    return rain_mm >= threshold

def notify(message):
    \"\"\"Notification node: in n8n this would be an email/Slack node.\"\"\"
    print("NOTIFY:", message)

try:
    rain = fetch_forecast(31.5, 74.3)
    print(f"forecast rain: {rain} mm")
    if filter_rain(rain):
        notify("Bring an umbrella tomorrow.")
    else:
        notify("No umbrella needed.")
except Exception as e:
    print("workflow failed:", e)
"""),
    ("md", """## Exercises

---
"""),("md", """### Exercise 1 — Map the lifecycle

Draw (in markdown) the node chain for: *"every Friday, fetch the week's
sales from the API and email the total to the manager."* Label each node as
trigger / processing / output."""),
    ("code", """# Answer (markdown):
#   Schedule (Fri 17:00)  -> trigger
#   HTTP Request (sales API) -> processing (acquire)
#   Code (sum the week)   -> processing (transform)
#   Email node            -> output (communicate)
print("diagram in markdown")
"""),
    ("md", """### Exercise 2 — Idempotent append

Write a function `append_idempotent(csv_path, new_rows, key)` that appends
rows only if `key` is not already present. Test it by calling it twice with
the same key and checking the file length."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
from pathlib import Path

def append_idempotent(csv_path, new_rows, key):
    path = Path(csv_path)
    df = pd.DataFrame(new_rows)
    if path.exists():
        old = pd.read_csv(path)
        df = pd.concat([old, df], ignore_index=True).drop_duplicates(key)
    df.to_csv(path, index=False)
    return len(df)

path = Path("datasets/ex2-append.csv")
rows = [{"day": "Mon", "sales": 100}]
print(append_idempotent(path, rows, "day"))   # 1
print(append_idempotent(path, rows, "day"))   # still 1 - no duplicate
"""),
    ("md", """### Exercise 3 — Error visibility

Wrap the beginner HTTP example so that a failure prints a clear message
instead of crashing the "workflow". Use `try/except` and a status check."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
import requests

try:
    r = requests.get("https://jsonplaceholder.typicode.com/todos/99999", timeout=10)
    r.raise_for_status()
    print("ok:", r.json())
except requests.exceptions.HTTPError:
    print("ERROR: request failed with", r.status_code)
except requests.exceptions.RequestException as e:
    print("ERROR: network problem:", e)
"""),
    ("md", """## Challenge exercise

Design and build the full **"daily weather collector"** automation in code:

1. Trigger: a `run_daily()` function that simulates a schedule.
2. Acquire: fetch `current_weather` from Open-Meteo for two cities (Lahore
   and Karachi) in a loop, politely (`time.sleep(1)` between calls).
3. Transform: build one tidy DataFrame with columns `city, time,
   temperature, windspeed`.
4. Output: `append_idempotent` to `datasets/weather-collector.csv` on key
   (`city`, `time`).
5. Guardrails: `try/except` around each city; print a summary of what was
   added vs. skipped.
6. Export the equivalent n8n workflow JSON (a `for` loop over two cities) to
   `datasets/weather-collector-workflow.json`."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
import requests, pandas as pd, time, json
from pathlib import Path

CSV = Path("datasets/weather-collector.csv")

def run_daily():
    rows, added, skipped = [], 0, 0
    for city, lat, lon in [("Lahore", 31.5, 74.3), ("Karachi", 24.86, 67.01)]:
        try:
            r = requests.get("https://api.open-meteo.com/v1/forecast",
                             params={"latitude": lat, "longitude": lon,
                                     "current_weather": True}, timeout=15)
            r.raise_for_status()
            w = r.json()["current_weather"]
            rows.append({"city": city, "time": w["time"],
                         "temperature": w["temperature"],
                         "windspeed": w["windspeed"]})
            added += 1
        except Exception as e:
            print(f"skipped {city}: {e}")
            skipped += 1
        time.sleep(1)

    if rows:
        df = pd.DataFrame(rows)
        if CSV.exists():
            df = pd.concat([pd.read_csv(CSV), df], ignore_index=True).drop_duplicates(["city", "time"])
        df.to_csv(CSV, index=False)
    print(f"run complete: {added} added, {skipped} skipped, total rows {len(df) if rows else 0}")

run_daily()
"""),
    ("md", """## Recap

- Workflows = triggers + processing nodes + outputs, wired visually in n8n.
- The Python equivalents teach the same logic and run anywhere.
- **Idempotency** — re-runs are safe (dedupe on append).
- **Error visibility** — failures print/notify instead of dying silently.
- **Secrets** — API keys live in n8n credentials, not in shared JSON.
- Export workflow JSON to your repo → automation becomes reproducible.

---
"""),
    ("md", """## Questions

1. What are the three parts of every workflow?
2. Name two trigger types and when to use them.
3. Which n8n node replaces `requests.get(...)`?
4. What is idempotency, and why does an append-based automation need it?
5. Where should an API key live in n8n, and why?
6. How is a workflow different from an AI agent (notebook 18)?

---
**Next:** notebook 20 — End-to-End Data Science Project.
"""),
]