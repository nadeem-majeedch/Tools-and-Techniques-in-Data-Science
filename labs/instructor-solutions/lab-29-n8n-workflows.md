# Lab 29 — Solution: n8n Workflows & Idempotency

**Session:** W15 S29 · **CLO:** CLO-3

## Complete solution

```python
import requests
import pandas as pd
from pathlib import Path
from datetime import date, datetime

Path("datasets").mkdir(exist_ok=True)
CSV = Path("datasets/weather-collector.csv")
LOG = Path("datasets/collector-errors.log")
URL = "https://api.open-meteo.com/v1/forecast"

def collect_weather(day: date) -> pd.DataFrame:
    params = {"latitude": 24.86, "longitude": 67.01,
              "hourly": "temperature_2m",
              "start_date": day.isoformat(), "end_date": day.isoformat()}
    resp = requests.get(URL, params=params, timeout=10)
    resp.raise_for_status()
    temps = resp.json()["hourly"]["temperature_2m"]
    return pd.DataFrame([{
        "date": day.isoformat(),
        "city": "Karachi",
        "mean_temp_c": round(sum(temps) / len(temps), 1),
        "max_temp_c": max(temps),
        "fetched_at": datetime.now().isoformat(timespec="minutes"),
    }])

def append_if_new(df, path):
    if path.exists():
        existing = pd.read_csv(path)
    else:
        existing = pd.DataFrame(columns=df.columns)
    if df["date"].isin(existing["date"]).any():
        print("skipped (duplicate)")
        return
    pd.concat([existing, df], ignore_index=True).to_csv(path, index=False)
    print("appended")

# run twice — same date
today = date.today()
try:
    row = collect_weather(today)
    print(row.to_string(index=False))
    append_if_new(row, CSV)
    append_if_new(row, CSV)          # second run -> skipped
except Exception as e:
    with open(LOG, "a") as f:
        f.write(f"{datetime.now()} fetch failed: {e}\n")
    print("fetch failed:", e)

print(pd.read_csv(CSV))              # exactly one row for today

# JSON export
workflow = {"nodes": [
    {"id": "trigger", "type": "schedule", "config": {"cron": "0 8 * * *"}},
    {"id": "http", "type": "http_request",
     "config": {"url": URL, "params": {"latitude": 24.86}}},
    {"id": "code", "type": "code", "config": {"extract": "hourly temps"}},
    {"id": "output", "type": "spreadsheet_file", "config": {"csv": str(CSV)}},
    {"id": "error", "type": "email", "config": {"on": "http failure"}},
]}
import json
with open("datasets/weather-workflow.json", "w") as f:
    json.dump(workflow, f, indent=2)
print([n["type"] for n in json.load(open("datasets/weather-workflow.json"))["nodes"]])
```

## Expected output

- Design diagram: `Schedule (0 8 * * *) → HTTP Request (Open-Meteo) →
  Code (extract temps) → Spreadsheet File (append CSV)`, plus an error
  branch to Email.
- Two runs: `appended` then `skipped (duplicate)`; CSV has exactly 1 row
  for the date after any number of reruns.
- `collector-errors.log` exists, empty on success.
- Loaded JSON prints `['schedule', 'http_request', 'code',
  'spreadsheet_file', 'email']`.

## Model answers

1. **Idempotency** — an operation is idempotent if repeating it produces
   the same result (no duplicates). The date-key check before appending is
   what makes the pipeline idempotent.
2. **mode="a" duplicates** — append mode never checks what's already in
   the file; each run writes another copy of the same rows.
3. **Code node vs HTTP node** — the HTTP node fetches raw data; the Code
   node transforms it (aggregating 24 hourly temps into one daily row),
   which a plain HTTP request cannot do.
4. **Log file** — automations run unattended; a printed message vanishes.
   A log file survives for review and is the standard artifact for
   diagnosing nightly runs.
5. **Machine off at 8:00** — the run is missed (no backfill by default);
   n8n retries (on failure) and missed-run policies exist precisely so
   unattended pipelines don't silently skip data.

## Challenge solution

```python
cities = [("Karachi", 24.86, 67.01), ("Lahore", 31.55, 74.34)]
for city, lat, lon in cities:
    params = {"latitude": lat, "longitude": lon,
              "hourly": "temperature_2m",
              "start_date": today.isoformat(), "end_date": today.isoformat()}
    temps = requests.get(URL, params=params, timeout=10).json()["hourly"]["temperature_2m"]
    row = pd.DataFrame([{"date": today.isoformat(), "city": city,
                         "mean_temp_c": round(sum(temps)/len(temps), 1),
                         "max_temp_c": max(temps),
                         "fetched_at": datetime.now().isoformat(timespec="minutes")}])
    # idempotency key = date + city
    if CSV.exists() and ((existing["date"] == row["date"].iloc[0]) &
                         (existing["city"] == city)).any():
        print(city, "skipped (duplicate)")
    else:
        pd.concat([existing, row]).to_csv(CSV, index=False)
        print(city, "appended")
```

Rerun: both cities `skipped` — no new rows.