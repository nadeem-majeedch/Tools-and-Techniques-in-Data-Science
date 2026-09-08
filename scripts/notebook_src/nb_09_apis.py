# Content for notebook 09: APIs and data acquisition.
CELLS = [
    ("md", """# 09 — APIs and Data Acquisition

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-1 — Acquire datasets.

Data rarely arrives in a tidy CSV. This notebook covers the acquisition
pipeline: local files, JSON, and public APIs via the `requests` library —
with the robustness habits (timeouts, status checks, caching) that make your
work reliable and reproducible.

---
"""),
    ("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Explain what an API is and read an HTTP response.
2. Fetch JSON from a public API with `requests`.
3. Flatten nested JSON into a DataFrame with `pd.json_normalize`.
4. Handle errors gracefully (status codes, timeouts).
5. Cache API results so reruns don't hammer the server.

---
"""),
    ("code", """# Make sure the datasets/ folder exists next to this notebook.
from pathlib import Path
Path("datasets").mkdir(exist_ok=True)
print("datasets/ ready")
"""),
    ("md", """## Theory: what is an API?

An **API** (Application Programming Interface) is a contract: you send a
request (URL + parameters), the server answers with a **status code** and a
**payload** (usually JSON). Three facts to know:

- `200` means OK; `404` not found; `429` too many requests; `500` server error.
- JSON is just nested dicts and lists — the Python from notebook 01 applies.
- Public APIs are shared infrastructure: be polite (rate limits, caching).

Ethics note: if data exists on a website *for humans* and there is no API,
scraping raises consent and copyright questions. Prefer APIs or official
datasets. (More in the ethics notebook.)

---
"""),("code", """import requests
import pandas as pd

# A keyless public API: Open-Meteo weather forecast
url = "https://api.open-meteo.com/v1/forecast"
params = {"latitude": 31.5, "longitude": 74.3, "current_weather": True}

r = requests.get(url, params=params, timeout=15)
print("status:", r.status_code)
print("content type:", r.headers.get("content-type"))

if r.status_code == 200:
    data = r.json()                     # nested dict
    print(data["current_weather"])
else:
    print("Request failed with", r.status_code)
"""),
    ("md", """## JSON → DataFrame: pd.json_normalize

API responses are nested — `{"hourly": {"time": [...], "temperature_2m": [...]}}`.
`pd.json_normalize` flattens nested records into columns; for arrays of
records it creates one row per record.

---
"""),("code", """# A tiny local JSON to practice on (no network needed for this cell)
import json, tempfile, pathlib

sample = [
    {"id": 1, "title": "learn python", "completed": False, "user": {"name": "Ali"}},
    {"id": 2, "title": "build a model", "completed": True,  "user": {"name": "Sara"}},
]
df = pd.json_normalize(sample)          # user.name becomes a column
print(df)

# Expected output:
#    id            title  completed user.name
# 0   1      learn python      False       Ali
# 1   2     build a model       True      Sara
"""),
    ("md", """## The robust request pattern

Networks fail: timeouts, 404s, rate limits. The professional pattern wraps
the call so one failure cannot kill your notebook, and **caches** results so
you don't re-hit the API on every rerun (polite to the server, reproducible
offline).

---
"""),("code", """import requests
import pandas as pd
from pathlib import Path

CACHE = Path("datasets/weather-cache.csv")

def fetch_weather(lat=31.5, lon=74.3):
    \"\"\"Fetch current weather, with a local CSV cache.\"\"\"
    if CACHE.exists():
        print("using cached data")
        return pd.read_csv(CACHE)

    url = "https://api.open-meteo.com/v1/forecast"
    try:
        r = requests.get(url, params={
            "latitude": lat, "longitude": lon, "current_weather": True,
        }, timeout=15)
        r.raise_for_status()                     # raises on 4xx/5xx
        row = r.json()["current_weather"]
        df = pd.DataFrame([row])
        df.to_csv(CACHE, index=False)            # cache for next time
        print("fetched fresh data")
        return df
    except requests.exceptions.RequestException as e:
        print("network error:", e)
        return pd.DataFrame()                    # graceful degradation

weather = fetch_weather()
print(weather)
"""),
    ("md", """## Beginner example: one request, one dict

---
"""),("code", """import requests

try:
    r = requests.get("https://jsonplaceholder.typicode.com/todos/1", timeout=10)
    r.raise_for_status()
    print(r.json())
except requests.exceptions.RequestException as e:
    print("offline or unreachable:", e)

# Expected output (when online):
#   {'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}
"""),
    ("md", """## Intermediate example: a real acquisition pipeline

Fetch a week of hourly weather, flatten it, summarize it, and cache it. This
is the exact shape of an acquisition stage in the final project.

---
"""),("code", """import requests
import pandas as pd
import time

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 24.86, "longitude": 67.01,          # Karachi
    "hourly": "temperature_2m,relative_humidity_2m",
    "forecast_days": 7,
}

try:
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()

    df = pd.DataFrame({
        "time": data["hourly"]["time"],
        "temp_c": data["hourly"]["temperature_2m"],
        "humidity": data["hourly"]["relative_humidity_2m"],
    })
    df["time"] = pd.to_datetime(df["time"])

    print(df.head(3))
    print("rows:", len(df))
    print("max temp:", df["temp_c"].max(), "| mean humidity:", round(df["humidity"].mean(), 1))

    df.to_csv("datasets/karachi-weather.csv", index=False)   # cache
    time.sleep(1)   # be polite to the API
except requests.exceptions.RequestException as e:
    print("network error:", e)
"""),
    ("md", """## Exercises

---
"""),
    ("md", """### Exercise 1 — Local JSON

Write a list of 3 dicts (your own data, e.g., movies you like) to a JSON
file, read it back with `pd.read_json` (orient records), and print the
DataFrame."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
import pandas as pd, json

movies = [
    {"title": "Inception", "year": 2010, "rating": 8.8},
    {"title": "Interstellar", "year": 2014, "rating": 8.7},
    {"title": "Dune", "year": 2021, "rating": 8.0},
]
with open("datasets/movies.json", "w") as f:
    json.dump(movies, f)

df = pd.read_json("datasets/movies.json")
print(df)
"""),
    ("md", """### Exercise 2 — Status codes

Request `https://httpbin.org/status/404` and `https://httpbin.org/status/200`
(guarded). Print the status code of each and a True/False for success."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
import requests

for code in [200, 404]:
    try:
        r = requests.get(f"https://httpbin.org/status/{code}", timeout=10)
        print(code, "->", r.status_code, "success:", r.ok)
    except requests.exceptions.RequestException as e:
        print(code, "-> offline:", e)
"""),
    ("md", """### Exercise 3 — Normalize

Given the nested JSON below, use `pd.json_normalize` to produce a DataFrame
with columns `name` and `score.math`."""),
    ("code", """import pandas as pd

data = [
    {"name": "Ali", "score": {"math": 85, "english": 78}},
    {"name": "Sara", "score": {"math": 92, "english": 88}},
]

# your code here
"""),
    ("code", """# Solution
df = pd.json_normalize(data)
print(df)
# Expected output:
#     name  score.math  score.english
# 0    Ali          85             78
# 1   Sara          92             88
"""),
    ("md", """## Challenge exercise

Build a **reusable** acquisition function for the JSONPlaceholder todos API
(`https://jsonplaceholder.typicode.com/todos`):

1. `fetch_todos()` — returns a DataFrame of all todos, with timeout + status check.
2. Cache to `datasets/todos.csv`; on second call, print "using cache".
3. Answer: what share of todos are completed? (groupby/mean on `completed`).
4. Guard everything so the notebook still runs offline (print a message)."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
import requests, pandas as pd
from pathlib import Path

CACHE = Path("datasets/todos.csv")

def fetch_todos():
    if CACHE.exists():
        print("using cache")
        return pd.read_csv(CACHE)
    try:
        r = requests.get("https://jsonplaceholder.typicode.com/todos", timeout=15)
        r.raise_for_status()
        df = pd.DataFrame(r.json())
        df.to_csv(CACHE, index=False)
        print("fetched and cached")
        return df
    except requests.exceptions.RequestException as e:
        print("offline - returning empty frame:", e)
        return pd.DataFrame()

todos = fetch_todos()
if len(todos):
    print("share completed:", round(todos["completed"].mean(), 3))
else:
    print("no data this run")
"""),
    ("md", """## Recap

- An API call = URL + params → status code + JSON payload.
- Check `status_code` / use `raise_for_status()` before trusting data.
- `pd.json_normalize` flattens nested JSON into a table.
- Timeouts + try/except keep notebooks alive when the network fails.
- Cache downloads to disk — polite, fast, reproducible.
- Prefer APIs/datasets over scraping; respect terms and rate limits.

---
"""),
    ("md", """## Questions

1. What does a 404 status code mean? What about 429?
2. What is the difference between `r.text` and `r.json()`?
3. Why add a `timeout` to every request?
4. What does `raise_for_status()` do?
5. Why cache API results to a local file?
6. When is scraping inappropriate, and what should you prefer instead?

---
**Next:** notebook 10 — Introduction to Machine Learning.
"""),
]