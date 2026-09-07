# Content for notebook 17: Tool and function calling.
CELLS = [
    ("md", """# 17 — Tool / Function Calling

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-3 — Develop AI-assisted data science workflows (basic AI agents).

A plain chat LLM only produces text. **Tool calling** lets it *request*
actions: "call `tip_by(by='day')`". Your code executes the function and
feeds the result back. That loop — reason → call → observe → reason — is the
engine of AI agents (notebook 18).

---
"""),("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Explain tool calling: model requests → your code executes.
2. Describe a tool to a model (name, description, parameters).
3. Run a real tool-calling round trip with Ollama (guarded).
4. Simulate the loop offline with a mock model (always runs).
5. State the safety property: the model can only call functions YOU wrote.

---
"""),("md", """## Theory: the mechanics

1. You give the model a **tool schema**: name, description, and parameters.
2. When appropriate, the model replies with a structured **tool call**
   instead of text: `call tip_by(by="day")`.
3. **Your code** runs the real function (the model never runs code itself).
4. The result is returned to the model as a **tool result** message.
5. The model continues — more calls, or the final answer.

Two consequences to internalize:

- The **tool description is the model's instruction manual** — write it
  carefully ("use when asked about tips by category").
- Safety: the model can only do what you've coded. That boundary is the
  feature, not a limitation.

---
"""),("code", """import pandas as pd
import seaborn as sns

tips = sns.load_dataset("tips")

# Step 1: write the tools (plain functions - YOUR code)
def tip_by(df, by):
    \"\"\"Mean tip grouped by a column. Use for questions about tips by category.\"\"\"
    return df.groupby(by)["tip"].mean().round(2).to_string()

def missing_summary(df):
    \"\"\"Count missing values per column. Use for data-quality questions.\"\"\"
    return df.isna().sum().to_string()

# Step 2: describe the tools to the model (OpenAI-style schema)
tools = [
    {"type": "function",
     "function": {"name": "tip_by", "description": tip_by.__doc__,
                  "parameters": {"type": "object",
                                 "properties": {"by": {"type": "string"}},
                                 "required": ["by"]}}},
    {"type": "function",
     "function": {"name": "missing_summary", "description": missing_summary.__doc__,
                  "parameters": {"type": "object", "properties": {}}}},
]

# Step 3: a registry mapping names to functions (the only code the model can reach)
TOOLS = {"tip_by": tip_by, "missing_summary": missing_summary}
print("tools registered:", list(TOOLS))
"""),
    ("md", """## The real round trip (guarded)

With Ollama running and a tool-capable model (`llama3.2`), the model decides
to call a tool, you run it, and the answer follows. Guarded: without Ollama,
the cell prints instructions — the *mechanics* are then taught by the
simulation in the next section.

---
"""),("code", """import importlib, ollama

def module_available(name):
    try:
        importlib.import_module(name)
        return True
    except ImportError:
        return False

if not module_available("ollama"):
    print("ollama client not installed - see setup guide")
else:
    try:
        messages = [{"role": "user",
                     "content": "Which day has the highest average tip? Also, are there missing values?"}]
        resp = ollama.chat(model="llama3.2", messages=messages, tools=tools)
        msg = resp["message"]
        print("model asks to call:", msg.get("tool_calls"))

        if msg.get("tool_calls"):
            for call in msg["tool_calls"]:
                fn = call["function"]["name"]
                args = call["function"]["arguments"]
                result = TOOLS[fn](tips, **args)
                print(f"  -> running {fn}{args}:\\n{result}\\n")
                messages.append(msg)
                messages.append({"role": "tool", "content": str(result)})
            final = ollama.chat(model="llama3.2", messages=messages, tools=tools)
            print("FINAL:", final["message"]["content"])
    except Exception as e:
        print("Ollama not ready:", e)
        print("-> start Ollama and pull a model to see the real round trip")
"""),
    ("md", """## The offline simulation: see the loop with no LLM

The loop's structure doesn't depend on the model. Here a *mock* model
"decides" to call `tip_by("day")` — your code runs it exactly as it would
for a real LLM. This always runs, anywhere, and it teaches the mechanics.

---
"""),("code", """def mock_model(messages, tools):
    \"\"\"A stand-in 'model' that always asks for tip_by(day) once.\"\"\"
    for m in messages:
        if m.get("role") == "tool":
            return {"message": {"content": "Thanks - that answers it."}}
    return {"message": {"tool_calls": [
        {"function": {"name": "tip_by", "arguments": {"by": "day"}}}
    ]}}

messages = [{"role": "user", "content": "What is the mean tip by day?"}]
for step in range(3):
    msg = mock_model(messages, tools)["message"]
    if "tool_calls" not in msg or not msg["tool_calls"]:
        print("FINAL ANSWER:", msg["content"])
        break
    call = msg["tool_calls"][0]["function"]
    result = TOOLS[call["name"]](tips, **call["arguments"])
    print(f"step {step}: model called {call['name']}{call['arguments']}")
    print(f"         tool result:\\n{result}")
    messages.append(msg)
    messages.append({"role": "tool", "content": str(result)})
"""),
    ("md", """## Beginner example: one tool, one question

The smallest possible round trip — a calculator tool.

---
"""),("code", """def add(a, b):
    \"\"\"Add two numbers. Use for arithmetic questions.\"\"\"
    return str(a + b)

tools_calc = [{"type": "function",
               "function": {"name": "add", "description": add.__doc__,
                            "parameters": {"type": "object",
                                           "properties": {"a": {"type": "number"},
                                                          "b": {"type": "number"}},
                                           "required": ["a", "b"]}}}]

# Mock round trip: model asks to call add(12, 30) -> YOU run it -> 42
mock_call = {"function": {"name": "add", "arguments": {"a": 12, "b": 30}}}
result = add(**mock_call["function"]["arguments"])
print("model requested:", mock_call["function"])
print("your code executed:", result)

# Expected output:
#   model requested: {'name': 'add', 'arguments': {'a': 12, 'b': 30}}
#   your code executed: 42
"""),
    ("md", """## Intermediate example: a safe agent loop (guarded + simulated)

A capped loop that either uses the real model or the mock — identical
structure either way. The cap (`max_steps`) is the safety valve.

---
"""),("code", """import ollama

def run_loop(use_real_llm, question, tools, max_steps=5):
    \"\"\"Run the tool-calling loop. use_real_llm=True needs Ollama.\"\"\"
    messages = [{"role": "user", "content": question}]
    transcript = []
    for step in range(max_steps):
        if use_real_llm:
            msg = ollama.chat(model="llama3.2", messages=messages, tools=tools)["message"]
        else:
            msg = mock_model(messages, tools)["message"]
        transcript.append(msg)
        if not msg.get("tool_calls"):
            return msg["content"], transcript
        for call in msg["tool_calls"]:
            fn, args = call["function"]["name"], call["function"]["arguments"]
            result = TOOLS[fn](tips, **args)
            messages.append(msg)
            messages.append({"role": "tool", "content": str(result)})
            transcript.append({"tool_call": fn, "args": args})
    return "Reached max steps.", transcript

try:
    answer, transcript = run_loop(False, "What is the mean tip by day?", tools)
    print("ANSWER:", answer)
    print("TRANSCRIPT:", [t if isinstance(t, str) else t.get("tool_call") for t in transcript])
except Exception as e:
    print("loop failed:", e)
"""),
    ("md", """## Exercises

---
"""),("md", """### Exercise 1 — Describe your own tool

Write a function `top_rows(df, col, n=5)` that returns the top-n rows by a
column, and write its docstring as a tool description. Print the docstring —
that's what the model reads."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
def top_rows(df, col, n=5):
    \"\"\"Return the n rows with the highest values of col. Use for 'top' questions.\"\"\"
    return df.nlargest(n, col).to_string()

print(top_rows.__doc__)
print(top_rows(tips, "tip", 3))
"""),
    ("md", """### Exercise 2 — Build a schema

Turn `top_rows` into a tool schema (dict) with parameters `col` (string,
required) and `n` (integer, optional, default 5). Print the schema."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
schema = {"type": "function",
          "function": {"name": "top_rows", "description": top_rows.__doc__,
                       "parameters": {"type": "object",
                                      "properties": {"col": {"type": "string"},
                                                     "n": {"type": "integer"}},
                                      "required": ["col"]}}}
print(schema)
"""),
    ("md", """### Exercise 3 — Extend the registry

Add `top_rows` to a new registry dict and run the **mock loop** with a mock
that calls it. Confirm the tool result comes back."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
REGISTRY = {"tip_by": tip_by, "missing_summary": missing_summary, "top_rows": top_rows}

def mock_top(messages, tools):
    for m in messages:
        if m.get("role") == "tool":
            return {"message": {"content": "got it."}}
    return {"message": {"tool_calls": [
        {"function": {"name": "top_rows", "arguments": {"col": "tip", "n": 3}}}
    ]}}

messages = [{"role": "user", "content": "top 3 tips?"}]
msg = mock_top(messages, tools)["message"]
call = msg["tool_calls"][0]["function"]
result = REGISTRY[call["name"]](tips, **call["arguments"])
print(result)
"""),
    ("md", """## Challenge exercise

Build a two-tool loop from scratch (simulated, so it always runs):

1. Tools: `describe_numeric(df)` (returns `df.describe()`) and
   `corr_pair(df, a, b)` (returns the Pearson correlation of two columns).
2. A mock model that calls `describe_numeric`, then `corr_pair("total_bill",
   "tip")`, then answers.
3. The loop must: run each requested tool, append tool results to messages,
   cap at 5 steps, and print a transcript.
4. Write one sentence: why does the model never execute code directly?"""),
    ("code", """# your code here
"""),
    ("code", """# Solution
def describe_numeric(df):
    \"\"\"Summary statistics of numeric columns. Use for overview questions.\"\"\"
    return df.describe().round(2).to_string()

def corr_pair(df, a, b):
    \"\"\"Pearson correlation between columns a and b. Use for relationship questions.\"\"\"
    return str(round(df[a].corr(df[b]), 3))

REG = {"describe_numeric": describe_numeric, "corr_pair": corr_pair}
PLAN = [("describe_numeric", {}), ("corr_pair", {"a": "total_bill", "b": "tip"})]

def mock_planner(messages, tools):
    for m in messages:
        if m.get("role") == "tool":
            return {"message": {"content": "Analysis complete."}}
    step = PLAN.pop(0)
    return {"message": {"tool_calls": [
        {"function": {"name": step[0], "arguments": step[1]}}]}}

messages = [{"role": "user", "content": "Overview, then bill-tip correlation."}]
for step in range(5):
    msg = mock_planner(messages, tools)["message"]
    if not msg.get("tool_calls"):
        print("FINAL:", msg["content"]); break
    call = msg["tool_calls"][0]["function"]
    result = REG[call["name"]](tips, **call["arguments"])
    print(f"called {call['name']} ->\\n{result[:120]}\\n")
    messages.append(msg); messages.append({"role": "tool", "content": str(result)})

print("Safety: the model only requests; YOUR code executes every call.")
"""),
    ("md", """## Recap

- Tool calling = model *requests* a function; **your code executes it**.
- Tool schema = name + description + parameters (description is the manual).
- The loop: reason → call → observe → reason, capped at `max_steps`.
- The mock simulation teaches the mechanics without any LLM.
- Safety boundary: the model can only reach the functions you registered.

---
"""),
    ("md", """## Questions

1. Who executes a tool when the model requests a call? (Your code.)
2. Why is the tool description so important?
3. What is the agent loop, in four steps?
4. Why does `max_steps` exist?
5. What must you append to the messages after running a tool? (The tool result.)
6. Why is "the model can only call functions you define" a safety feature?

---
**Next:** notebook 18 — AI Agents.
"""),
]