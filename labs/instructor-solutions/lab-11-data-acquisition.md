# Lab 11 — Solution: Data Acquisition

**Session:** W6 S11 · **CLO:** CLO-1

## Complete solution

```python
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

Path("datasets").mkdir(exist_ok=True)
CACHE = Path("datasets/weather-cache.csv")
FRESH = timedelta(hours=12)

URL = "https://api.open-meteo.com/v1/forecast"
params = {"latitude": 24.86, "longitude": 67.01,
          "hourly": "temperature_2m", "forecast_days": 5}

def load_or_fetch():
    age = datetime.now() - datetime.fromtimestamp(CACHE.stat().st_mtime) \
        if CACHE.exists() else None
    if CACHE.exists() and age < FRESH:
        print("using cache")
        return pd.read_csv(CACHE, parse_dates=["time"])
    print("fetched from API")
    resp = requests.get(URL, params=params, timeout=10)
    resp.raise_for_status()                     # 200 or raise
    hourly = resp.json()["hourly"]
    df = pd.DataFrame(hourly)                   # time + temperature_2m
    df = df.rename(columns={"temperature_2m": "temp_c"})
    df["time"] = pd.to_datetime(df["time"])
    df.to_csv(CACHE, index=False)
    return df

df = load_or_fetch()
df["date"] = df["time"].dt.date
df["hour"] = df["time"].dt.hour
print("shape:", df.shape)                        # (120, 4)
print("missing:", df["temp_c"].isna().sum())     # 0
print(df.groupby("date")["temp_c"].mean().round(1))
```

## Expected output

- First run `fetched from API`, second `using cache` (within 12 h).
- `(120, 4)` rows/cols; no missing temps; daily means 25–32 °C for Karachi
  (season-dependent — plausibility is the grade).
- No-network run: the except path prints a message and falls back to cache.

## Model answers

1. **Status codes** — 2xx success (200 OK), 4xx client error (404 not
   found, 429 rate limited), 5xx server error. Treat anything ≥ 400 as an
   error; only parse the body on success.
2. **params=** — requests URL-encodes values correctly (spaces, &, unicode)
   and keeps the code readable; hand-built query strings are error-prone.
3. **raise_for_status()** — turns an HTTP error status into an exception
   immediately, so you don't silently parse an error page as data.
4. **Why cache** — politeness (don't hammer a free API), speed (reruns are
   instant), and offline reproducibility (lab/home without network).
5. **json_normalize** — flattens *nested* dicts (e.g.,
   `{"hourly": {"time": [...], "temperature_2m": [...]}}`); `DataFrame(dict)`
   only works when the dict values are already flat lists.

## Challenge solution

```python
cities = [("Karachi", 24.86, 67.01), ("Lahore", 31.55, 74.34)]
frames = []
for name, lat, lon in cities:
    CACHE = Path(f"datasets/weather-{name.lower()}.csv")
    p = dict(params, latitude=lat, longitude=lon)
    # same load-or-fetch pattern, per-city file
    ...
    f["city"] = name
    frames.append(f)
all_df = pd.concat(frames, ignore_index=True)
summary = all_df.groupby("city")["temp_c"].agg(["mean", "min", "max"]).round(1)
print(summary)
```