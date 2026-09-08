# Streamlit · 03 — Widgets: Making Your App Interactive

**Time:** ~60 min · **CLOs:** CLO-1, CLO-3 · **Level:** Beginner
**Prerequisite:** tutorial (document 2) — you know the rerun model.

---

## 1. The widget rule

```python
value = st.widget_name(label, options..., default...)
```

Every widget is one line that returns a value. **The variable is the
widget.** The script re-runs whenever the user changes it, and the variable
holds the new value. There is no event system, no callbacks — just reruns
and variables.

## 2. The widget catalogue

### Buttons and toggles

```python
if st.button("Run analysis"):        # True only on the rerun caused by the click
    st.write("Analysis running...")

checked = st.checkbox("Show details")  # True/False
if checked:
    st.write("Details are shown.")
```

`st.button` — one-shot action. `st.checkbox` — persistent on/off state.

### Choosing from options

```python
day = st.selectbox("Pick a day", ["Mon", "Tue", "Wed"])   # one choice
days = st.multiselect("Pick days", ["Mon", "Tue", "Wed"], default=["Mon"])
# multi returns a LIST of the chosen values
```

`st.selectbox` — a dropdown; returns the selected item. `st.multiselect` —
a checkbox list; returns a **list** (possibly empty!). Handle the empty
case, or filter logic breaks.

### Numbers

```python
price = st.slider("Price", min_value=0, max_value=100, value=50, step=5)
age = st.number_input("Age", min_value=0, max_value=120, value=18, step=1)
```

`st.slider` — drag to choose, good for ranges. `st.number_input` — type a
number (or use arrows), good for precise values.

### Text

```python
name = st.text_input("Name")          # one line of text
question = st.text_area("Question")   # several lines
```

Both return strings. An empty input returns `""` (falsy) — check `if name:`
before using it.

### Files

```python
uploaded = st.file_uploader("Upload a CSV", type=["csv"])
if uploaded is not None:
    import pandas as pd
    df = pd.read_csv(uploaded)        # pandas reads it directly!
    st.write(df.head())
```

`st.file_uploader` gives you a file-like object pandas can read. This is
how users bring *their* data into *your* app.

## 3. Quick reference — what each widget returns

| Widget | Returns | Typical use |
|---|---|---|
| `st.button` | `True`/`False` (one rerun) | trigger an action |
| `st.checkbox` | `True`/`False` | show/hide a section |
| `st.selectbox` | the chosen item | pick one category |
| `st.multiselect` | a list of items | pick several categories |
| `st.slider` | a number (or tuple for range) | continuous value |
| `st.number_input` | a number | precise value |
| `st.text_input` | a string | short text |
| `st.text_area` | a string | long text |
| `st.file_uploader` | file-like or `None` | load a file |

---

# Example 2 — Interactive Calculator

A complete calculator app using `number_input`, `selectbox`, and `button`.

## Explanation

Three widgets in: two numbers and an operation. The app stores the chosen
operation and numbers as variables (widget rule), then performs the
calculation with plain Python. A button controls *when* the calculation
happens so the result doesn't flash during typing. This is the pattern
behind every "run my analysis" button in a data app.

## Code

Save as `app.py`:

```python
import streamlit as st

st.title("🧮 Interactive Calculator")
st.markdown("Pick two numbers and an operation, then press **Calculate**.")

# 1) Widgets -> variables
num1 = st.number_input("First number", value=0.0, step=1.0)
num2 = st.number_input("Second number", value=0.0, step=1.0)
operation = st.selectbox("Operation", ["+", "-", "*", "/"])

# 2) Guard against division by zero BEFORE calculating
if operation == "/" and num2 == 0:
    st.error("Cannot divide by zero — change the second number.")
    st.stop()                       # stop the script here

# 3) Calculate with plain Python
if st.button("Calculate"):
    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "*":
        result = num1 * num2
    else:
        result = num1 / num2

    # 4) Show the result nicely
    st.success(f"{num1} {operation} {num2} = **{result:,.2f}**")
```

## Expected result

- Title and instruction text at the top.
- Two number boxes (default `0`), an operation dropdown, a Calculate button.
- Pick `5` and `3`, choose `*`, click **Calculate** →
  `5 * 3 = 15.00` in a green success box.
- Choose `/` and set the second number to `0` → a red error message appears
  immediately, and the app stops before the button section.

## Exercise

1. Add a fourth widget: `st.checkbox("Show the calculation steps")` that
   prints `num1`, `num2`, and the operation in an expander
   (`st.expander("Steps")`).
2. Handle the power operation `**` as a fifth choice in the selectbox.
3. Format the result to a whole number when both inputs are integers
   (hint: `if num1 == int(num1)`).

## Challenge

Turn the calculator into a **grade calculator**: `number_input` marks for
three assessments (Quiz 1, Quiz 2, Final), each with a weight
(`st.slider` 0–100 for each), and the app computes the weighted total and
shows `st.success` (pass ≥ 50) or `st.error` (fail). Use `st.progress(...)`
to visualize the total out of 100.

---

## Common widget mistakes

| Mistake | Fix |
|---|---|
| `multiselect` result used as a single value | it returns a **list** — loop over it or check `if days:` |
| Division by zero crashes the app | check before calculating, `st.error` + `st.stop()` |
| Text input used before it has a value | `if name:` guard — empty strings are falsy |
| Widgets with the same label | each widget needs a unique label (or a `key=`) |
| Button "does nothing" | buttons are `True` for one rerun — put the action *inside* the `if` |
| File uploader crashes on non-CSV | check the file extension or wrap `pd.read_csv` in try/except |

## Checkpoint questions

1. What does `st.multiselect` return when nothing is selected? *(CLO-1 ·
   Understand · Easy)*
   **Answer:** an empty list `[]`.
2. Why does `st.button` behave differently from `st.checkbox`? *(CLO-1 ·
   Understand · Medium)*
   **Answer:** the button is `True` only for the single rerun caused by the
   click; the checkbox keeps its state across reruns until the user changes
   it.
3. How do you stop an app gracefully when the user's input is invalid?
   *(CLO-1 · Apply · Medium)*
   **Answer:** show `st.error(...)` and call `st.stop()`.