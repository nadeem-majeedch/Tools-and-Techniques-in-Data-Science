# Streamlit · 02 — Guided Tutorial: Your First Interactive App

**Time:** ~45–60 min · **CLOs:** CLO-1, CLO-3 · **Level:** Beginner
**Do this after** `streamlit-introduction.md`. You will build one app,
piece by piece, and watch it become interactive.

---

## Setup (2 min)

Create a folder for your experiments and a file:

```bash
mkdir streamlit-practice
cd streamlit-practice
# create app.py with your editor
```

## Step 1 — The skeleton (5 min)

Write this into `app.py` and run `streamlit run app.py`:

```python
import streamlit as st

st.title("My First Interactive App")
st.write("This text is displayed by st.write.")
```

**Watch:** the browser shows the title and the text. Now change the text,
save the file, and look at the app — Streamlit noticed the change and shows
a **Rerun** button in the top-right corner. Click it. **Your script just
re-ran.** This is the rerun model, and it is the single most important idea
in Streamlit.

## Step 2 — Text elements (5 min)

```python
import streamlit as st

st.title("My First Interactive App")
st.header("Step 2: text elements")
st.subheader("Everything below is text")

st.write("Plain text, any length.")
st.markdown("**Bold**, *italic*, and `code` styles.")
st.markdown("- bullet one\n- bullet two")
st.write(3.14159)          # st.write displays numbers too
```

**Watch:** every line becomes part of the page, in order. Top-to-bottom
execution means **the page looks exactly like your script reads**.

## Step 3 — Your first widget (10 min)

```python
import streamlit as st

st.title("My First Interactive App")
st.header("Step 3: a slider")

# A widget is just a variable assignment:
age = st.slider("How old are you?", min_value=10, max_value=30, value=20)

# Use the widget value in normal Python:
st.write(f"You are {age} years old.")
if age >= 18:
    st.success("You are an adult.")
else:
    st.warning("You are a minor.")
```

**Watch:** move the slider. Every movement **re-runs the script**, `age`
gets the new value, and the message updates. You just built interactivity —
the widget line, the f-string, and the `if` are all ordinary Python.

## Step 4 — Two widgets working together (10 min)

```python
import streamlit as st

st.title("My First Interactive App")
st.header("Step 4: widgets work together")

name = st.text_input("Your name?")
city = st.selectbox("Your city?", ["Lahore", "Karachi", "Islamabad", "Other"])

if name:                                    # empty input is falsy
    st.write(f"Hello **{name}** from {city}!")
else:
    st.info("Type your name above.")
```

**Watch:** every keystroke and every dropdown change triggers a rerun. The
page updates without any button. This is Streamlit's default behaviour:
**instant, continuous interactivity.**

## Step 5 — A button that controls a block (10 min)

```python
import streamlit as st

st.title("My First Interactive App")
st.header("Step 5: buttons")

if st.button("Click me"):
    st.balloons()               # a little celebration — proof the click ran
    st.write("The button was clicked! The script re-ran and this block ran.")
else:
    st.write("The button has not been clicked yet.")
```

**Watch:** the button is a widget like any other — its value is `True` for
one rerun after you click it. That's why the `if` works: **every rerun the
script asks "is the button currently True?"**

## Step 6 — Putting it together: a mini profile card (10 min)

Combine every widget from steps 3–5 into one app. Then add this final touch
— `st.session_state`, which remembers values **across** reruns (without it,
everything resets on every rerun; see document 6 for the full story):

```python
import streamlit as st

st.title("My First Interactive App")

# session_state survives reruns — a counter that actually counts:
if "clicks" not in st.session_state:
    st.session_state.clicks = 0

if st.button("Click me"):
    st.session_state.clicks += 1

st.write(f"You clicked the button {st.session_state.clicks} times.")
```

**Watch:** without session state, the count would stay at 1 forever (the
script resets `clicks = 0` on every rerun). With it, the count accumulates.
This one idea unlocks real apps.

## What you learned

- The app is a script that **re-runs top to bottom** on every interaction.
- Widgets are variables: `value = st.widget(...)`.
- `if` statements around widgets control what shows.
- `st.session_state` remembers things across reruns.

You are now ready for the widget catalogue (`streamlit-widgets.md`) and the
full examples (3–6). Rebuild any example there by copying the script — that
is the normal workflow: write, save, rerun, tweak.

---

## Tutorial checkpoint

1. In one sentence, what is a rerun? **CLO-1 · Understand · Easy**
   **Answer:** Streamlit executes the whole script again from top to bottom
   whenever a widget changes or the file is saved.
2. Why does `if st.button(...):` work even though the button is "just a
   widget"? **CLO-1 · Understand · Easy**
   **Answer:** the button returns `True` on the rerun caused by the click, so
   the `if` block runs exactly once per click.
3. Your counter resets to 1 after every click. What is the one-line fix?
   **CLO-1 · Apply · Medium**
   **Answer:** keep the count in `st.session_state` instead of a normal
   variable.