# Lab 11 — Data Acquisition: APIs, JSON, Caching

**Session:** Week 6 · Session 11 · 90 min
**CLO:** CLO-1
**Difficulty:** Intermediate

## Learning objectives

By the end of this lab you can:

1. Make HTTP requests with `requests` and check status codes.
2. Parse JSON responses and flatten nested structures with
   `pd.json_normalize`.
3. Handle errors (timeouts, bad status) without crashing.
4. Cache responses so reruns don't hit the server.

## Problem statement

Your team needs a small, keyless weather feed: 5 days of hourly temperature
for a chosen city from the Open-Meteo API. Requirements: the fetch must
tolerate no-network situations, cache the result locally, and produce a
clean DataFrame. You will also prove the cache works by running twice and
showing the second run reads the file.

## Dataset requirements

Open-Meteo (keyless, free, no sign-up):
`https://api.open-meteo.com/v1/forecast?latitude=..&longitude=..&hourly=temperature_2m&forecast_days=5`.
Use Karachi (24.86, 67.01) or your own city's coordinates. Cache file:
`datasets/weather-cache.csv`.

## Step-by-step tasks

1. **Setup cell:** ensure `datasets/` exists (see Lab 08 pattern).
2. **Fetch:** GET the URL above with `params=` (latitude, longitude,
   `hourly`, `forecast_days`) and a 10-second timeout. Print the status
   code and verify it is 200.
3. **Inspect:** the JSON has `hourly.time` (list of ISO timestamps) and
   `hourly.temperature_2m` (list of floats). Print their lengths — they
   must match (5 days × 24 h = 120).
4. **Flatten:** build a DataFrame with `pd.json_normalize` from the JSON's
   `hourly` dict, then rename columns to `time`, `temp_c`.
5. **Parse:** convert `time` with `pd.to_datetime`, extract `date` and
   `hour` columns, and set `time` as the index.
6. **Cache:** save to `datasets/weather-cache.csv`. Add a guard: if the
   file exists and is less than 12 hours old, load it instead of fetching.
   Print `"using cache"` or `"fetched from API"` accordingly. Run the cell
   twice to show both paths.
7. **Summary:** print mean temp per day (`groupby("date")["temp_c"].mean()`
   rounded to 1).

## Starter code

```python
import requests
import pandas as pd
from pathlib import Path

Path("datasets").mkdir(exist_ok=True)
CACHE = Path("datasets/weather-cache.csv")

URL = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 24.86,
    "longitude": 67.01,
    "hourly": "temperature_2m",
    "forecast_days": 5,
}

# your code here:
#   1) if CACHE exists and is fresh -> df = pd.read_csv(CACHE); print("using cache")
#   2) else: requests.get(URL, params=params, timeout=10);
#      raise for status; json_normalize; save to CACHE; print("fetched from API")
```

## Expected output

- First run: `fetched from API`; second run: `using cache`.
- `df.shape` ≈ `(120, 3)` (`time`, `temp_c`, plus `date`/`hour` if you kept
  them) — exact columns depend on your steps; `time` must be
  `datetime64[ns]`.
- `df["temp_c"].isna().sum() == 0`.
- Daily means: 5 values, plausible for the city (e.g., 25–32 °C for
  Karachi in summer).
- A cell that runs cleanly **with Wi-Fi off** (network error handled, cache
  used).

## Questions

1. What is a status code, and which ones should you treat as errors?
2. Why pass `params=` instead of building the query string by hand?
3. What does `raise_for_status()` do, and why call it before parsing?
4. Why cache? Give two reasons beyond politeness to the server.
5. `json_normalize` vs `pd.DataFrame(json["hourly"])` — when is normalize
   necessary?

## Challenge task

Fetch **two cities** (add a second city's coordinates) and produce a
comparison table: for each city, mean, min, and max temperature over the 5
days. Do it by looping over a list of `(name, lat, lon)` tuples, building
one DataFrame per city, and `concat`ing them with a `city` column. Cache
each city separately (`weather-<city>.csv`).

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Fetch with params + timeout + status check | 3 | 200 asserted |
| JSON flatten + clean DataFrame | 3 | 120 rows, datetime index |
| Cache logic (freshness + both paths) | 4 | both prints demonstrated |
| Error handling (no network) | 3 | graceful, cache fallback |
| Daily mean summary | 2 | 5 plausible values |
| Answers to questions | 2 | Q2, Q4 correct |
| Challenge: two cities + concat | 4 | comparison table, per-city cache |
| **Total** | **21** | |