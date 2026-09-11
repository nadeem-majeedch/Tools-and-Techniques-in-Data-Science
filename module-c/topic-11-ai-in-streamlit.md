# Module C · Topic 11 — AI in a Streamlit Application

**CLO-3 · Maps to:** Session 28 workshop · Assignment 2 app + Final Project
app · **Level:** Intermediate

---

## 1. Beginner explanation

Streamlit turns a Python script into a web app: widgets like
`st.selectbox` and `st.slider` become buttons and menus, and the script
re-runs whenever the user changes one. Now add AI: a `st.chat_input` box
where the user asks a question, and your app sends it to a **local Ollama
model**, gets an answer, and shows it in the chat. The app becomes a small
"data assistant": user picks filters with widgets, asks questions in plain
English, and gets answers grounded in the loaded data. All local, all free,
no API keys.

## 2. Conceptual explanation (the WHY)

Streamlit's mental model is *script re-run*: every interaction re-executes
the whole script top to bottom. Three consequences:

1. **Data loading must be cached** — `@st.cache_data` makes pandas read the
   CSV once, not on every click. Without it, each question re-reads the file.
2. **Chat state needs `st.session_state`** — the re-run wipes local
   variables, so the conversation history lives in session state and is
   re-painted each run.
3. **The LLM call is just another function** — `ollama.chat(...)` in the app
   is the same call as in a notebook; the app adds the user interface around
   it.

The AI integration pattern (keep it tiny):

- Show the loaded dataframe + widgets (filters) — plain Streamlit.
- A **chat area**: user types a question → you *augment* the prompt with the
  current filter state ("the user has selected day=Sat") → send to the local
  model → display the reply.
- Optionally show the audit line under each reply: *"Answered by llama3.2 —
  verify against the table above."*

This is exactly the final project's required component (interactive app +
AI-assisted analysis) — Assignment 2 teaches the app, this topic adds the AI.

## 3. Simple diagram

```text
  browser                          your machine
  ┌──────────────┐   streamlit    ┌───────────────────────────┐
  │ widgets      │◄──────────────►│ app.py (re-runs on change)│
  │ (filters)    │                │  @st.cache_data: load df  │
  │ chat input   │                │  ┌───────────────────┐    │
  │ chat display │                │  │ question + filter │    │
  └──────┬───────┘                │  │ context           │    │
         │                        │  └─────────┬─────────┘    │
         │ question               │            │ HTTP local   │
         │                        │            ▼              │
         │                        │  ┌───────────────────┐    │
         │                        │  │ Ollama (llama3.2) │    │
         │                        │  │ data stays local  │    │
         │                        │  └─────────┬─────────┘    │
         │ answer                 │            │              │
         └────────────────────────┼────────────┘              │
                                  └───────────────────────────┘
```

## 4. Python examples

```python
# app.py — run with:  streamlit run app.py
import streamlit as st
import pandas as pd
import seaborn as sns

st.set_page_config(page_title="Tips AI Assistant", page_icon="📊")
st.title("Tips — AI-Assisted Explorer")

# 1) Cache the data load (script re-runs on every click!)
@st.cache_data
def load_data():
    return sns.load_dataset("tips")

df = load_data()

# 2) Plain Streamlit widgets
day = st.selectbox("Filter by day", ["All"] + sorted(df["day"].unique()))
show_raw = st.checkbox("Show raw data", value=True)

if day != "All":
    filtered = df[df["day"] == day]
else:
    filtered = df

st.metric("Rows", len(filtered))
if show_raw:
    st.dataframe(filtered)

# 3) AI chat — local model, guarded
st.subheader("Ask a question about the data")
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

question = st.chat_input("e.g. What is the average tip?")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    try:
        import ollama
        # 4) Augment the prompt with the app's current state:
        context = (f"The dataframe has columns: {list(df.columns)}. "
                   f"Current filter: day={day}. "
                   "Answer from the data only; if unsure, say so.")
        reply = ollama.chat(
            model="llama3.2",
            messages=[{"role": "system", "content": context},
                      {"role": "user", "content": question}],
        )["message"]["content"]
    except Exception as e:
        reply = f"(Ollama not available: {e})"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
        st.caption("AI answer — verify against the table above.")
```

## 5. Practical exercise (30 min)

1. Create `app.py` from the example; run `streamlit run app.py`.
2. Confirm: changing the `day` selectbox re-runs the script, the metric and
   table update, and the chat history survives (session state).
3. Ask "what is the average tip?" — then verify the reply against
   `filtered["tip"].mean()` shown via `st.metric`. This is the in-app
   verification loop.
4. Add a second widget (e.g. `st.slider` for minimum party size) and make
   the filter apply to both.
5. Extend the prompt context with the filter state and re-ask — the answer
   should now respect the filter.
6. Write the audit-log line for one AI answer (question, model, context,
   reply, hand-verified number).

## 6. Common errors

| Error | Fix |
|---|---|
| App re-reads the CSV on every click | `@st.cache_data` on the load function |
| Chat history disappears after each answer | keep messages in `st.session_state` |
| Widgets don't affect the AI answer | include the filter state in the prompt context |
| App crashes when Ollama is off | guard the call in try/except and show a message |
| `ollama` import error in app | `pip install ollama` in the same environment that runs streamlit |
| Port already in use | `streamlit run app.py --server.port 8502` |

## 7. Limitations

- **Local model quality ceiling** — chat answers are good for simple
  lookups/summaries; deep multi-step reasoning needs better models or
  cloud (privacy permitting).
- **No memory across sessions** — session state lives per browser tab; a
  refresh resets the conversation.
- **Re-run cost** — every interaction re-runs the script; heavy processing
  belongs in cached functions.
- **Prompt context is manual** — you must construct the context; the app
  won't "understand" the dataframe by itself.
- **Deployment privacy** — deploying the app to a public host makes the data
  visible; keep deployments local/private for real data.

## 8. Responsible AI considerations

- **In-app verification UI** — every AI answer carries a "verify against the
  table" caption; consider showing the source table next to the answer.
- **Privacy by default** — local Ollama keeps data in the app; deploying to
  a public URL leaks whatever the app displays — keep private data local.
- **Prompt injection via chat** — users can type anything into `chat_input`;
  the prompt is untrusted user text — never let the reply execute anything.
- **Disclose in the app** — a footer or README line stating the AI component
  (model, version, local/cloud) satisfies course disclosure.

## 9. Assessment questions

**Q1.** Why does Streamlit need `@st.cache_data` for the data load, and what
happens without it? **CLO-3 · Understand · Easy**
**Answer:** the script re-runs on every interaction; without caching, the
CSV would be re-read (and re-parsed) on every click, slowing the app.

**Q2.** Your app's AI answer ignores the `day` filter the user selected. What
is the likely cause and the fix? **CLO-3 · Analyze · Medium**
**Answer:** the filter state wasn't included in the prompt context — the
model only sees what you put in the prompt. Fix: inject the current widget
values into the prompt.

**Q3.** A user types a question into your app's chat box that includes
"ignore previous instructions…". Why is this a risk, and what do you do?
**CLO-3 · Evaluate · Medium**
**Answer:** prompt injection — untrusted user text can steer the model.
Mitigate by keeping tool/privileged instructions in the system prompt,
never executing model output, and treating all chat input as untrusted.

**Q4.** Your team deploys the app to a public URL so friends can try it. The
data contains store sales by branch. What must you check before deploying?
**CLO-3 · Evaluate · Medium**
**Answer:** data privacy — a public deployment exposes the displayed data to
anyone; use only public/anonymized data, or keep the deployment local and
private.