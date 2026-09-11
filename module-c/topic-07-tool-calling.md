# Module C · Topic 07 — Tool / Function Calling

**CLO-3 · Maps to:** Session 28 · Notebook 17 · Lab 28 · **Level:** Intermediate

---

## 1. Beginner explanation

A plain LLM can only *talk*. Tool calling lets it *do*: you define normal
Python functions (your tools), describe them to the model, and let the model
say "call `average_by_day(column='tip')`". Your code runs the function and
feeds the *real result* back to the model. The model still can't compute —
but now it can delegate computation to functions that can. You stay in
control: **the model can only call functions you defined**, with arguments
you allow.

## 2. Conceptual explanation (the WHY)

Tool calling is a two-turn protocol, not magic:

1. **You describe the tools**: for each function you send a schema — name,
   description, and parameter types (OpenAI-style JSON schema).
2. **The model responds with a "tool call"**: instead of prose, it emits
   structured output like `{"name": "average_by_day", "arguments":
   {"column": "tip"}}`. It has *not* run anything.
3. **Your code executes** the function with those arguments and appends the
   real result to the conversation.
4. **The model answers with the result in hand** — now its reply is grounded
   in real numbers.

Why this matters for data science: it turns an LLM into a *coordinator* that
plans ("which column? which aggregation?") while Python does the actual
computation. The safety design is the interesting part — the model never
gets to run arbitrary code. It can only request whitelisted functions, so a
hallucination is caught either by validation or by the function itself.

## 3. Simple diagram

```text
  You ──"average tip by day"──► LLM
                                    │ decides to call a tool
                                    ▼
              ┌─ tool schema (your whitelist) ─┐
              │ average_by_day(column: str)    │
              └────────────────────────────────┘
              ◄─ tool_call: {name, arguments}
  You: run average_by_day("tip")  →  real pandas result
              ── result appended to messages ──► LLM
                                    ▼
              ◄─ final answer grounded in real numbers
```

## 4. Python examples

```python
import importlib, json

def module_available(name):
    try:
        importlib.import_module(name)
        return True
    except ImportError:
        return False

import pandas as pd
import seaborn as sns

tips = sns.load_dataset("tips")

# Step 1: write the tools — plain Python functions, YOUR code
def average_by_day(df, column):
    """Real computation: mean of a column per day."""
    return df.groupby("day")[column].mean().round(2).to_dict()

def total_by_day(df, column):
    """Real computation: sum of a column per day."""
    return df.groupby("day")[column].sum().round(2).to_dict()

# Step 2: describe the tools to the model (whitelist!)
TOOLS = [
    {"type": "function",
     "function": {
         "name": "average_by_day",
         "description": "Mean of a numeric column grouped by day.",
         "parameters": {
             "type": "object",
             "properties": {"column": {"type": "string"}},
             "required": ["column"],
         }}},
    {"type": "function",
     "function": {
         "name": "total_by_day",
         "description": "Sum of a numeric column grouped by day.",
         "parameters": {
             "type": "object",
             "properties": {"column": {"type": "string"}},
             "required": ["column"],
         }}},
]

FUNCTIONS = {"average_by_day": average_by_day, "total_by_day": total_by_day}

if module_available("ollama"):
    import ollama

    def run_with_tools(question, max_turns=3):
        messages = [{"role": "system",
                     "content": "Answer from tool results only."},
                    {"role": "user", "content": question}]
        for _ in range(max_turns):
            msg = ollama.chat(model="llama3.2", messages=messages,
                              tools=TOOLS)["message"]
            if not msg.get("tool_calls"):
                return msg["content"]
            for call in msg["tool_calls"]:
                name = call["function"]["name"]
                args = json.loads(call["function"]["arguments"])
                print(f"  -> calling {name}({args})")
                # Only whitelisted names exist in FUNCTIONS
                result = FUNCTIONS[name](tips, **args)
                messages.append({"role": "assistant",
                                 "content": json.dumps(call)})
                messages.append({"role": "tool",
                                 "content": json.dumps(result)})
        return "gave up after max turns"

    try:
        print(run_with_tools("Which day has the highest mean tip?"))
    except Exception as e:
        print("Ollama not running:", e)
else:
    print("ollama package not installed:  pip install ollama")
```

## 5. Practical exercise (30 min)

Dataset: `sns.load_dataset("titanic")`.

1. Write two tools: `survival_rate_by(class_or_sex)` and `count_by(column)`
   — both plain pandas.
2. Register them with schemas like above.
3. Ask: *"Which passenger class had the lowest survival rate?"* and watch
   the loop: model requests `survival_rate_by("class")` → your code runs →
   model answers from real numbers.
4. Ask a question that needs BOTH tools and verify the multi-call loop.
5. Try to trick it: ask for a tool that isn't registered (e.g. "delete the
   dataset") — show that the whitelist blocks it.

## 6. Common errors

| Error | Fix |
|---|---|
| `tool_calls` key missing | older models/servers need `tools` param support; check `ollama --version` |
| `KeyError: 'arguments'` | arguments may be a string — `json.loads` it first |
| Tool called with wrong column | your function should validate: `if column not in df.columns: raise` |
| Model loops forever | always set `max_turns` and a stop condition |
| Function runs with model-chosen args you dislike | whitelist *values* too (e.g., only allow columns that exist) |
| Forgot to append tool result to messages | the model can't see results unless they're in the conversation |

## 7. Limitations

- **Model picks the arguments** — it can pass a column you didn't intend;
  validate inside the function.
- **Whitelist only** — the model cannot discover tools; it only knows what
  you described, so complex tasks need many schemas.
- **Small models struggle** — tool calling on `llama3.2` works for 1–3 tools;
  big tool sets confuse small models.
- **You still verify the *final* answer** — tool results are real, but the
  model's interpretation of them can still be wrong.
- **Cost of correctness is your code** — the protocol is only as safe as the
  functions you wrote and the validation you added.

## 8. Responsible AI considerations

- **The whitelist is the safety boundary** — never let a model call anything
  outside your registered functions; no "eval", no shell, no file writes
  unless explicitly designed and logged.
- **Injection via tool output** — data returned by a tool goes back into the
  prompt; hostile data can try to steer the model — verify final claims.
- **Audit every call** — log tool name, arguments, result, and final answer.
- **Human accountability** — the model proposes; your code executes; you
  decide. That chain is the responsible-AI design pattern.

## 9. Assessment questions

**Q1.** In tool calling, who actually runs the function? *(CLO-3 · Understand
· Easy)*
**Answer:** Your Python code does. The model only *requests* a call with
arguments; execution and validation are yours.

**Q2.** Why is it safe(ish) for a model to call your tools, but NOT safe to
let it run arbitrary Python? **CLO-3 · Evaluate · Medium**
**Answer:** Tools are whitelisted, validated functions with real results; a
model running arbitrary code could execute anything (deletions, network,
injection). The whitelist bounds the blast radius.

**Q3.** The model calls `average_by_day` with `column="tip"`. The column
doesn't exist in your dataframe. What should your function do? *(CLO-3 ·
Apply · Medium)*
**Answer:** Validate the column against `df.columns` and raise a clear error
(or return a message) — the loop then reports failure honestly instead of
silently computing garbage.

**Q4.** Why is the model's *final answer* still subject to verification even
though the tool results are real? **CLO-3 · Evaluate · Medium**
**Answer:** The tool output is real, but the model's summary/interpretation
of it is still generated text that can misread the numbers — verify the
claim against the tool result directly.