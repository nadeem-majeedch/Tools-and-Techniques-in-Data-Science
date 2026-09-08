# Lab 29 — n8n Workflows & Idempotency

**Session:** Week 15 · Session 29 · 90 min
**CLO:** CLO-3
**Difficulty:** Advanced

## Learning objectives

By the end of this lab you can:

1. Model a data task as trigger → processing → output (the n8n mental model).
2. Build the equivalent pipeline in Python with error handling.
3. Make an automation **idempotent** so reruns don't duplicate data.
4. Export/read a workflow as JSON (reproducibility).

## Problem statement

n8n is installed on the instructor machine (or via Docker) — but automations
must be *designed* before they are *clicked*. Your task: design a
"daily weather collector" workflow (every morning at 8:00 → fetch Karachi
weather → append to a CSV → notify on failure), implement the **same
pipeline in Python** (so it runs anywhere), and make it safe to run twice
without creating duplicate rows. If n8n is available, build the visual
version too; the Python version is always required.

## Dataset requirements

Open-Meteo API (keyless, as in Lab 11). Cache/output:
`datasets/weather-collector.csv`.

## Step-by-step tasks

1. **Design (markdown diagram):** write the workflow as
   `Trigger → HTTP Request → Code → Spreadsheet File → (on error) Email`,
   labeling each node with the data it passes (e.g., "hourly temp list").
   Name the trigger type (Schedule) and its cron `0 8 * * *`.
2. **Python pipeline:** write `collect_weather(date)` returning a one-row
   DataFrame: `date, city, mean_temp_c, max_temp_c, fetched_at` from the
   Open-Meteo forecast (hourly temps for that day).
3. **Idempotent append:** `append_if_new(df, path)` that:
   - loads the existing CSV if it exists (else creates an empty frame),
   - checks whether `date` is already present,
   - appends only if absent, prints `"appended"` or `"skipped (duplicate)"`.
   This is the key deliverable — explain in a comment why plain `to_csv`
   with `mode="a"` would duplicate rows on rerun.
4. **Error handling:** wrap the fetch in try/except; on failure, write
   `"fetch failed: <error>"` to `datasets/collector-errors.log` and print a
   message — never crash.
5. **Run twice:** call `collect_weather` + `append_if_new` twice (same
   date). First run appends, second skips. Verify the CSV has exactly 1
   row for that date.
6. **JSON export (reproducibility):** write the workflow design as a JSON
   dict (`nodes`: trigger, http, code, output; each with `type`,
   `config`) and save to `datasets/weather-workflow.json`. Load it back and
   print the node types — this is the artifact you would import into n8n.

## Starter code

```python
import requests
import pandas as pd
from pathlib import Path
from datetime import date

Path("datasets").mkdir(exist_ok=True)
CSV = Path("datasets/weather-collector.csv")
LOG = Path("datasets/collector-errors.log")
URL = "https://api.open-meteo.com/v1/forecast"

def collect_weather(day: date) -> pd.DataFrame:
    """One-row frame: date, city, mean_temp_c, max_temp_c, fetched_at."""
    # your code here: params latitude=24.86, longitude=67.01,
    #                 hourly=temperature_2m, start_date/end_date=day

def append_if_new(df, path):
    """Append df if its 'date' is not already in path. Idempotent."""
    # your code here

# run twice, same date
today = date.today()
collect_weather(today)   # prints the fetched row
# append_if_new(...) x2 -> appended, then skipped (duplicate)
```

## Expected output

- Design diagram with 5 labeled nodes + trigger cron.
- `collect_weather` returns a one-row frame with the 5 columns; temps
  plausible for Karachi.
- Two runs: `appended` then `skipped (duplicate)`; CSV has exactly one row
  for that date even after 5 more reruns.
- `collector-errors.log` empty on success (exists, no entries).
- `weather-workflow.json` loads back; printed node types include
  `schedule`, `http`, `code`, `output`.

## Questions

1. What is idempotency, and which step makes this pipeline idempotent?
2. Why would `df.to_csv(path, mode="a", header=False)` duplicate rows?
3. What does the `Code` node in n8n do that the `HTTP Request` node can't?
4. Why keep error output in a log file instead of just printing it?
5. A schedule runs at `0 8 * * *`. What happens if the machine is off at
   8:00 — and why does n8n offer retries?

## Challenge task

Extend the pipeline to **two cities** (add Lahore 31.55, 74.34): loop over
a list of `(city, lat, lon)`, collect both, append both idempotently (key =
date + city), and print a small comparison table. Update the JSON export
with a second HTTP node. Verify rerunning appends nothing.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Design diagram + cron | 4 | 5 nodes labeled |
| `collect_weather` one-row frame | 4 | correct columns + fetch |
| Idempotent append | 5 | appended/skipped logic correct |
| Error handling + log | 4 | never crashes, log written |
| Two-run proof | 3 | exactly 1 row per date |
| JSON export/import | 4 | node types printed |
| Answers to questions | 3 | Q1, Q2, Q5 correct |
| Challenge: two cities | 4 | idempotent per city, table |
| **Total** | **31** | |