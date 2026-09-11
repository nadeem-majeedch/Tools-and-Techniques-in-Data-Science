# Module C · Topic 09 — n8n: Automating Data Workflows

**CLO-3 · Maps to:** Session 29 · Notebook 19 · Lab 29 · **Level:** Beginner

---

## 1. Beginner explanation

n8n is a free, visual automation tool. You build **workflows** by dragging
**nodes** (steps) and connecting them: *trigger → fetch data → process →
save/notify*. Each node does one job — an HTTP request, a filter, a
calculation, a message. Instead of writing a Python script that runs once,
you get a workflow that can **run on a schedule, forever**, with no code
except the small "Code" node when you need logic. It's the glue that turns
one-off notebook analyses into repeating data pipelines.

## 2. Conceptual explanation (the WHY)

A workflow is a directed graph of nodes; data flows along the connections as
JSON. Typical pipeline:

1. **Trigger** — when does it run? (schedule: daily at 8am; webhook: when
   someone calls a URL; manual).
2. **Fetch** — HTTP Request node calls an API (keyless ones like Open-Meteo
   need no credentials — perfect for this course).
3. **Process** — Filter/Edit Fields/Code nodes clean or reshape the JSON.
4. **Store / notify** — save to a file (Google Sheets is common but needs
   auth; for this course, write to a local file or send an email/slack
   message) or just log the result.

Why teach n8n in a data science course? Because **reproducibility has a
schedule problem**: analyses rot when data stops updating. An n8n workflow
refetches and re-processes on schedule, so the notebook downstream always
sees fresh data. It is also the "automation" pillar of CLO-3 — alongside
LLMs and agents — and it composes with them: an n8n node can call your
Ollama server or trigger a Python script.

Data privacy note up front: n8n nodes that call third-party services send
data there. For private data, run n8n locally (it is a local server, like
Ollama) and use local-only nodes.

## 3. Simple diagram

```text
  ┌─────────┐    ┌──────────────┐    ┌───────────────┐
  │TRIGGER  │───►│HTTP REQUEST  │───►│FILTER / EDIT  │
  │daily    │    │open-meteo    │    │(clean JSON)   │
  │8:00     │    │(keyless API) │    │               │
  └─────────┘    └──────────────┘    └───────┬───────┘
                                             │
                          ┌──────────────────┘
                          ▼
              ┌──────────────────────┐
              │ CODE / AGGREGATE     │   small logic if needed
              └──────────┬───────────┘
                         ▼
              ┌──────────────────────┐
              │ WRITE TO FILE        │  local CSV (private, no cloud)
              │ + NOTIFY (optional)  │
              └──────────────────────┘
```

## 4. Examples — the workflow, not the code

n8n is visual, but the **Code node** uses JavaScript. Here is the minimal
pattern (the only "code" most workflows need):

```js
// Code node — input comes in as items[]; each item has .json
// Task: keep only rows where temperature is above 30
const hot = [];
for (const item of $input.all()) {
  if (item.json.temperature > 30) {
    hot.push({ json: item.json });
  }
}
return hot;
```

And the mental mapping for Python users:

| Python concept | n8n equivalent |
|---|---|
| `requests.get(url)` | HTTP Request node |
| `df[df["x"] > 30]` | Filter node or Code node |
| `df.groupby(...).mean()` | Code node (or Aggregation) |
| `df.to_csv("out.csv")` | Write Binary File / Google Sheets node |
| `cron`/`schedule` | Schedule Trigger node |
| `if __name__ == "__main__"` | Manual/Test trigger |

Practical workflow to build (Lab 29): **daily weather → CSV**.

1. Schedule Trigger: every day 08:00.
2. HTTP Request: Open-Meteo archive/forecast API for one city (keyless —
   no credentials).
3. Code node: extract `time` + `temperature_2m`, round values.
4. Write Binary File: append to `weather.csv` (local — private by default).
5. Manual test, then activate. Open the file tomorrow: fresh data, no human.

## 5. Practical exercise (30 min)

1. Start n8n locally (`npx n8n` → http://localhost:5678).
2. Build the 4-node weather workflow above with Open-Meteo
   (https://api.open-meteo.com/v1/forecast?latitude=31.5&longitude=74.3&hourly=temperature_2m).
3. Run it manually; inspect the JSON between nodes (click a node → Output).
4. Add a Filter node: keep only hours above 30 °C.
5. Change the trigger to "every minute" temporarily, run twice, confirm two
   rows are appended — then revert to daily. Note in your lab: *what would
   break if a third party changed the API response?* (schema drift).

## 6. Common errors

| Error | Fix |
|---|---|
| HTTP Request fails | check the URL in a browser first; APIs change — test node by node |
| "Credentials required" on a keyless API | wrong node config; Open-Meteo needs none — remove credential fields |
| Node output empty | earlier node returned an unexpected shape — inspect each node's Output tab |
| Workflow runs but file unchanged | Write Binary File needs the data as binary; use "Convert to File"/correct field mapping |
| `.env`/config mistakes | keep secrets out of workflows; for this course, prefer keyless APIs |
| npx n8n slow to start | first run downloads the package; subsequent starts are fast |

## 7. Limitations

- **Visual ≠ simpler at scale** — big branching workflows get unreadable;
  keep pipelines linear and small.
- **Local execution** — n8n must be running to run workflows; a laptop that
  sleeps skips the schedule (deployment is a separate topic).
- **Code node is JavaScript** — students switching from Python face a small
  syntax gap.
- **Third-party nodes send data outward** — each integration is a privacy
  decision.
- **Schema drift** — external APIs change shape without warning; workflows
  need re-testing, exactly like code.

## 8. Responsible AI considerations

- **Privacy per node** — the local file/HTTP nodes keep data local; every
  third-party node is a data transfer — check before adding.
- **Keyless by design** — this course requires keyless APIs; no secrets in
  workflows, no shared credentials.
- **Logging & monitoring** — a workflow that fails silently is worse than no
  workflow; add error handling and check outputs on a schedule.
- **Automation ≠ approval** — an automated pipeline still needs a human to
  review results before they influence decisions.

## 9. Assessment questions

**Q1.** List the four typical stages of an n8n data workflow. *(CLO-3 ·
Understand · Easy)*
**Answer:** trigger → fetch (HTTP) → process (filter/code) → store/notify.

**Q2.** Why is a scheduled n8n workflow an answer to the reproducibility
problem? **CLO-3 · Analyze · Medium**
**Answer:** analyses rot when data stops updating; a scheduled workflow
refetches/refreshes data automatically so downstream notebooks always see
fresh, consistent input.

**Q3.** Your workflow calls a free weather API that suddenly changes its JSON
shape. What happens and what's the professional response? *(CLO-3 ·
Evaluate · Medium)*
**Answer:** nodes downstream fail or silently produce empty/wrong output —
schema drift. Response: test node by node, pin/validate the schema, add
error handling, and check logs on a schedule.

**Q4.** A teammate suggests adding a "Google Sheets" node so the weather data
syncs to the cloud. What must the team consider first, given the course
privacy rule? **CLO-3 · Evaluate · Medium**
**Answer:** data privacy — syncing to the cloud sends the data to a third
party; only do it with explicit policy approval, and prefer local file
output for anything non-public.