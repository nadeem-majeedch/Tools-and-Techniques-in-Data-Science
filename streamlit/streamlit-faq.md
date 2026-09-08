# Streamlit · 08 — FAQ: Common Questions and Gotchas

Answers to the questions beginners actually ask. If your app misbehaves,
read this list before searching the internet.

---

### 1. Why does my app run the whole script every time I click something?

That's the design. Streamlit **re-runs the script top to bottom on every
interaction** (a "rerun"). It's what makes apps so easy to write — your
code is always in sync with the widget values. The cost is that expensive
work repeats, which is why caching (`@st.cache_data`) exists. Once you
internalize "rerun", most Streamlit surprises disappear.

### 2. My button doesn't "remember" anything. Why?

Buttons are `True` only for the single rerun caused by the click. If you
store the result in a normal variable, it's gone on the next rerun. Use
`st.session_state` for anything that must survive across reruns:

```python
if "count" not in st.session_state:
    st.session_state.count = 0
```

### 3. What exactly does `st.session_state` do?

It's a per-user, per-session dictionary that persists across reruns. Use it
for counters, chat history, choices that should stick. Do **not** use it
for expensive computation — that's what caching is for.

### 4. `@st.cache_data` — when does it actually run my function?

The first time you call it with a given set of arguments. If the arguments
are the same on the next rerun, the stored result is returned instead.
Change an argument → new computation, new cache entry. That's why caching
"doesn't work" when a widget value is one of the arguments — every new
value is a new cache key. Cache on *data*, not on *widgets*.

### 5. My chart is empty. Why?

Most common causes: (a) the dataframe is empty after filtering — check
`len(df)` and show `st.warning(...)`; (b) you forgot `st.pyplot(fig)`; (c)
seaborn drew into the wrong axes — always `fig, ax = plt.subplots()` and
pass `ax=ax` to seaborn.

### 6. My app shows an error/red text. What do I do?

Read the red traceback in the app — it's the real Python error, usually a
column name, a division by zero, or a missing value. Then check the
"Common mistakes" table in the relevant document. To see the full
traceback, scroll down in the app or run the script directly
(`python app.py` won't run Streamlit, but the pure-Python parts will run
and often reveal the error).

### 7. How do I stop an app? How do I change the port?

`Ctrl+C` in the terminal stops it. If port 8501 is busy:
`streamlit run app.py --server.port 8502`.

### 8. Can I share my app with my classmates?

Yes, two levels:
- **Same network:** run `streamlit run app.py --server.address 0.0.0.0`
  and share your machine's IP — classmates on the same Wi-Fi can open it.
- **Public:** deploy to a free hosting service (Streamlit Community Cloud,
  Render, Hugging Face Spaces). Basic deployment is covered in document 7;
  the rule for this course: **never deploy an app containing private data**
  — public hosting means public data.

### 9. Why is `st.file_uploader` giving me a weird object instead of a DataFrame?

It returns a file-like object, not a DataFrame. Convert with pandas:
`df = pd.read_csv(uploaded)`. Check `uploaded is not None` first — on the
first run nothing is uploaded yet.

### 10. My `multiselect` crashes when I select nothing.

`st.multiselect` returns an **empty list** when nothing is selected, and
`df[[]]` errors. Guard it:

```python
cols = st.multiselect("Columns", df.columns, default=df.columns[:2])
if cols:                    # empty list is falsy
    st.dataframe(df[cols])
else:
    st.info("Pick at least one column.")
```

### 11. Widgets with the same label conflict. Why?

Streamlit identifies widgets by label. Two widgets with the same label on
the same page collide. Fix: give them unique labels, or add `key=`:
`st.selectbox("Day", days, key="eda_day")`.

### 12. My app is slow. Where do I start?

Three usual suspects, in order: (1) the data is reloaded on every rerun →
cache the load; (2) the model retrains on every rerun → cache the
training; (3) you're plotting the full dataframe → downsample or aggregate
before plotting.

### 13. What's the difference between `st.dataframe` and `st.table` again?

`st.dataframe`: interactive — sortable, scrollable, searchable; use for
real data exploration. `st.table`: static; use for small fixed results
(top-5, a summary). See document 4.

### 14. Why doesn't `print()` show anything?

`print` goes to the terminal where `streamlit run` is executing, not to the
app page. To see values in the app, use `st.write(...)`.

### 15. Do I need to know HTML/CSS/JavaScript for this course's apps?

No. The whole module is pure Python. (If you later deploy to a custom
domain you'll meet config files, but nothing in this course requires web
code.)

### 16. How do I add an AI chatbot to my Streamlit app?

See Module C topic 11 (`../module-c/topic-11-ai-in-streamlit.md`):
`st.chat_input` + `st.session_state` for history + a local Ollama call.
The short version: the chat history must live in session state, and the
LLM call is just a function the app runs on rerun.

### 17. My deployed app shows the wrong data / leaks data.

Never deploy an app that reads private files or hardcodes credentials.
Load data from a public source or let users upload it (the uploader pattern
from document 4 keeps data off the server entirely).

### 18. Where is the full reference?

`streamlit-cheatsheet.md` (this module) and the official docs:
https://docs.streamlit.io — search any `st.` function name.