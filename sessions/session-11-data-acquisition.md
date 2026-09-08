# Session 11 — Data Acquisition: Files, APIs, Web Data

**Week 6 · Session 11 · Module A · 90 min · CLO-1**

## 1. Learning objectives

By the end of this session, students can:
- Choose the right acquisition method: local files, public APIs, or (carefully) web pages.
- Fetch JSON from an API with `requests` and turn it into a DataFrame.
- Explain what an API key is, and why some APIs need one.
- Handle common HTTP errors and slow/absent network connections gracefully.
- Describe the ethics and legality of web scraping, and when scraping is not appropriate.

## 2. Key concepts

- **Acquisition is a pipeline stage with its own traps:** formats, encodings, schemas, permissions.
- **APIs** — programmatic interfaces: send a request (URL + params), receive structured data (usually JSON).
- **`requests`** — the standard HTTP library: `get()`, `.status_code`, `.json()`.
- **JSON** — nested key-value text; flatten with `pd.json_normalize`.
- **Scraping ≠ API:** scraping parses HTML meant for humans; it needs consent, rate limiting, and respect for `robots.txt`.
- **Robustness:** check status codes, wrap in `try/except`, cache results.

## 3. Detailed lecture notes

**Why acquisition?** So far data came from built-ins (`sns.load_dataset`) and
CSVs. In the real world you must *obtain* data: download exports, query APIs,
read web pages. Acquisition choices shape everything downstream — a dataset with
the wrong granularity or a schema you don't understand will cost hours later.
The lesson: understand *where data comes from* before you analyze it.

**Files first.** Recap the I/O from Session 8 (`read_csv`, `read_excel`,
`read_json`) and add the sanity checks: print `shape` and `head()`, confirm
`dtypes`. Mention `pd.read_csv(url)` — Pandas can read directly from a URL,
which is convenient but requires care with rate limits and reliability; for
course work, prefer downloading once and caching locally.

**APIs — the modern data source.** An API is a contract: you send a request
(URL, optional parameters, sometimes a key/headers), the server answers with a
status code and a payload (JSON). The `requests` library does this in three
lines: `r = requests.get(url, params={...})`, check `r.status_code == 200`,
then `r.json()`. Show a live demo with a keyless API (Open-Meteo weather:
`https://api.open-meteo.com/v1/forecast?latitude=31.5&longitude=74.3&current_weather=true`).
Parse the JSON: it's nested dicts/lists — `pd.json_normalize(r.json())` flattens
nested records into columns. Emphasize: JSON in Python is just dicts and lists —
the skills from Session 2 apply directly.

**API keys and ethics.** Some APIs require an API key (registration, rate
limits, usage tracking). Rules: never commit keys to Git (`.env` file +
`python-dotenv`, or environment variables; `.gitignore` already ignores `.env`).
Respect rate limits (`time.sleep` between calls); read the terms of service.
Introduce this as professional etiquette, not bureaucracy — APIs are shared
infrastructure.

**Scraping — when no API exists.** Sometimes the only data is HTML. Scraping
parses that HTML (`pd.read_html(url)` or BeautifulSoup). Warn clearly: scraping
raises legal/ethical issues (terms of service, copyright, server load). Rules of
thumb: check `robots.txt`; scrape slowly and politely; only public data; better
yet, prefer official APIs or datasets. This course only *demonstrates* scraping
concepts — we don't run a scraping assignment. This is the first explicit
"responsible data use" moment; it recurs in Session 30.

**Robustness.** Networks fail: timeouts, 404s, rate limiting. Pattern:
```python
r = requests.get(url, timeout=10)
r.raise_for_status()          # raise if 4xx/5xx
data = r.json()
```
`try/except` around the call so one failed request doesn't kill your notebook.
Cache the response (`data.to_csv(...)`) so you don't re-hit the API on every run
— polite to the server and makes your notebook reproducible offline.

## 4. Important terminology

- **API** — Application Programming Interface: a server endpoint for programmatic data access.
- **HTTP status code** — 200 OK, 404 Not Found, 429 Too Many Requests, 500 Server Error.
- **JSON** — JavaScript Object Notation: nested dicts/lists; the lingua franca of APIs.
- **Endpoint** — a specific URL an API exposes (e.g., `/v1/forecast`).
- **Query parameter** — `?key=value` pairs in the URL.
- **API key** — a secret token identifying you; keep it out of Git.
- **`requests`** — Python's HTTP client library.
- **`pd.json_normalize`** — flatten nested JSON into a DataFrame.
- **Scraping** — parsing HTML pages for data; needs consent and care.
- **`robots.txt`** — a site's rules for crawlers/scrapers.
- **Rate limit** — how many requests a server allows per time window.

## 5. Python examples

```python
import requests
import pandas as pd

# --- A keyless public API: Open-Meteo weather forecast ---
url = "https://api.open-meteo.com/v1/forecast"
params = {"latitude": 31.5, "longitude": 74.3, "current_weather": True}

r = requests.get(url, params=params, timeout=10)
print(r.status_code)                  # 200 means OK

if r.status_code == 200:
    data = r.json()
    print(data["current_weather"])    # dict with temperature, windspeed, ...

# --- Generic JSON practice: fake todos from JSONPlaceholder ---
todos = requests.get("https://jsonplaceholder.typicode.com/todos", timeout=10)
df = pd.DataFrame(todos.json())
print(df.head())

# --- Robust pattern ---
def fetch_todos():
    r = requests.get("https://jsonplaceholder.typicode.com/todos", timeout=10)
    r.raise_for_status()              # fail loudly on 4xx/5xx
    return pd.DataFrame(r.json())

try:
    df = fetch_todos()
    df.to_csv("datasets/todos.csv", index=False)   # cache for offline reproducibility
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
```

## 6. Beginner example

```python
import requests

r = requests.get("https://jsonplaceholder.typicode.com/todos/1", timeout=10)
print(r.json())
# {'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}
```

One call, one dict. Everything else is variations: more data, parameters, error handling.

## 7. Practical Data Science example

```python
import requests
import pandas as pd
import time

# Fetch one week of hourly weather for a city, politely and cached
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 24.86, "longitude": 67.01,          # Karachi
    "hourly": "temperature_2m,relative_humidity_2m",
    "forecast_days": 7,
}

r = requests.get(url, params=params, timeout=15)
r.raise_for_status()
data = r.json()

# Flatten nested hourly arrays into a tidy DataFrame
df = pd.DataFrame({
    "time": data["hourly"]["time"],
    "temp_c": data["hourly"]["temperature_2m"],
    "humidity": data["hourly"]["relative_humidity_2m"],
})
df["time"] = pd.to_datetime(df["time"])

print(df.head())
print("Max temp this week:", df["temp_c"].max(), "°C")
print("Mean humidity:", round(df["humidity"].mean(), 1), "%")

# Cache locally so reruns don't hammer the API
df.to_csv("datasets/karachi-weather.csv", index=False)
time.sleep(1)   # be polite to the API
```

## 8. In-class activity (50 min)

In `notebooks/week-06/session-11-data-acquisition.ipynb`:

1. **HTTP basics (10 min):** request `https://httpbin.org/status/404` and inspect
   `r.status_code`; try `200`. Write a markdown table of the codes you saw.
2. **API → DataFrame (20 min):** fetch the weather example for your own city;
   flatten into a DataFrame; compute daily mean temperature via `groupby` on `time.dt.date`.
3. **Robustness (10 min):** wrap your fetch in `try/except`, add `timeout=10`,
   and cache the result with `to_csv`; delete the cache and re-run to see it work.
4. **Ethics discussion (10 min):** three scenarios — scrape a review site vs. use
   its official API vs. buy the dataset. Which is appropriate and why? (This
   feeds the ethics session in Week 15.)

## 9. Lab exercise

**Lab 11** (`labs/lab-11-data-acquisition.md`) — due before Session 12: data
acquisition — fetch a small public API dataset, flatten it, cache it, and load
a local CSV, then answer two checkpoint questions.

## 10. Common mistakes

- Forgetting `.json()` and working with the raw response text (or worse, the response object).
- Not checking `status_code` → silent empty DataFrames on failure.
- No `timeout` → notebooks that hang forever when the network is down.
- Committing an API key to the repo (`.env` is ignored — use it).
- Hammering an API in a loop without `time.sleep` → 429s and possibly a ban.
- Re-fetching on every rerun instead of caching — slow, rude, and unreproducible.
- Scraping sites with `robots.txt` disallowing it or with terms of service against it.

## 11. Short assessment questions

1. What does `r.status_code` tell you? Name one good and one bad code.
2. What is the difference between `r.text` and `r.json()`?
3. Why shouldn't you commit an API key to Git?
4. What is `pd.json_normalize` for?
5. Your loop of API calls starts failing with 429. What happened and what do you do?
6. True/False: if data is available on a website, scraping it is always legal and ethical. (False — check terms, robots.txt, and copyright.)

## 12. CLO mapping

CLO-1: acquisition is the literal "acquire datasets" verb of CLO-1. The
robustness and consent habits introduced here are also the first explicit link
to the ethics dimension of CLO-3 (deepened in Sessions 24 and 30).

## 13. Suggested homework

- Finish Lab 11 (`labs/lab-11-data-acquisition.md`, due before Session 12) and
  push.
- Practice: fetch another keyless API (e.g., `https://api.open-meteo.com` variants, or a country/flag/quote API) and flatten it yourself.
- Read: the `requests` quickstart (requests.readthedocs.io) — sections "Quickstart" and "Errors and Exceptions".
- Preview: build two small DataFrames with a shared key column (`id`); Session 12 shows how `merge`/`concat` combine them and why this is the basis of relational data.