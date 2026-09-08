# Streamlit · 09 — Cheat Sheet

One page. Print it, paste it above your editor, keep it next to your
monitor.

## Running

```bash
pip install streamlit          # once
streamlit hello                # verify the install
streamlit run app.py           # run your app
streamlit run app.py --server.port 8502   # different port
```

**The mental model:** the script re-runs top to bottom on every
interaction. Widget = variable. `if` around widgets controls what shows.

## Text

| Code | Result |
|---|---|
| `st.title("...")` | page title |
| `st.header("...")` | section heading |
| `st.subheader("...")` | sub-heading |
| `st.write(x)` | smart display — text, numbers, dataframes, anything |
| `st.markdown("**bold** *it* `code`")` | formatted text |
| `st.caption("small note")` | small grey note |
| `st.latex("x^2")` | math (optional) |

## Status messages

| Code | Looks like |
|---|---|
| `st.success("...")` | green ✓ |
| `st.info("...")` | blue ℹ |
| `st.warning("...")` | yellow ⚠ |
| `st.error("...")` | red ✗ |
| `st.stop()` | stops the script here |

## Input widgets (all return a value)

```python
st.button("label")              # True only on the click's rerun
st.checkbox("label")            # True / False
st.selectbox("label", options)  # one chosen item
st.multiselect("label", options, default=[...])  # a LIST
st.slider("label", min_value=0, max_value=100, value=50, step=1)
st.number_input("label", min_value=0, value=0, step=1)
st.text_input("label")          # string, "" when empty
st.text_area("label")           # multi-line string
st.file_uploader("label", type=["csv"])   # file-like or None
```

Widget extras: unique labels (or `key="..."`), `st.sidebar.` prefix for
the sidebar, `st.columns(n)` to lay out side by side.

## Data & numbers

```python
st.dataframe(df)                # interactive: sort, scroll, search
st.table(df)                    # static table
st.metric("label", value, delta="+3")   # labeled number with arrow
st.columns(3)                   # returns 3 containers: c1, c2, c3
c1.metric(...)                  # use them as c1.metric(...)
st.expander("Show details")     # collapsible section
with st.expander("..."):        #   ...content...
```

## Charts

```python
st.line_chart(df)               # built-in, takes a dataframe
st.bar_chart(df)
st.area_chart(df)

# Matplotlib / Seaborn — the reliable pattern:
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(df["col"], bins=30, kde=True, ax=ax)   # seaborn: pass ax=ax!
ax.set_title("...")
st.pyplot(fig)
```

## Caching (run expensive work once)

```python
@st.cache_data
def load_data():
    return pd.read_csv("big.csv")   # runs once, reused on reruns
df = load_data()
```

## Session state (remember across reruns)

```python
if "name" not in st.session_state:
    st.session_state.name = "default"
st.session_state.name = ...        # read / write freely
```

## ML prediction app skeleton

```python
@st.cache_data
def train_model():
    ... model.fit(X_train, y_train) ...
    return model

model = train_model()              # trained once
features = pd.DataFrame([[v1, v2]], columns=[...])
pred = model.predict(features)[0]  # cheap — runs every rerun
st.success(f"Predicted: {pred}")
```

## Layout & navigation

```python
st.sidebar.header("Filters")               # everything in the sidebar
page = st.sidebar.radio("Page", ["Overview", "EDA", "Model"])

if page == "Overview":
    ...                                    # one if-block per page
elif page == "EDA":
    ...
```

## The golden rules

1. Widgets are variables; the script re-runs on every change.
2. Cache data loading and model training — never widget state.
3. `st.session_state` for memory across reruns; `st.stop()` to bail out
   gracefully.
4. Seaborn: always `fig, ax = plt.subplots()` and `ax=ax`.
5. Guard uploads (`if uploaded is None: st.stop()`), guard empty
   `multiselect` (`if cols:`), guard division by zero.
6. `print()` goes to the terminal — use `st.write` in the app.
7. Never deploy private data publicly.