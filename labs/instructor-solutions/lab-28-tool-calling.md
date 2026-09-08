# Lab 28 — Solution: Tool Calling & AI Agents

**Session:** W14 S28 · **CLO:** CLO-3

## Complete solution

```python
import pandas as pd
import seaborn as sns

tips = sns.load_dataset("tips")

def tip_by(df, by):
    return df.groupby(by)["tip"].mean().round(2).to_string()

def missing_summary(df):
    return df.isna().sum().to_string()

def describe_numeric(df):
    return df.describe().round(2).to_string()

REGISTRY = {"tip_by": tip_by, "missing_summary": missing_summary,
            "describe_numeric": describe_numeric}

TOOLS = [
    {"type": "function", "function": {
        "name": "tip_by",
        "description": "Mean tip grouped by a column (e.g. day).",
        "parameters": {"type": "object",
                       "properties": {"by": {"type": "string"}},
                       "required": ["by"]}}},
    {"type": "function", "function": {
        "name": "missing_summary",
        "description": "Count missing values per column.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "describe_numeric",
        "description": "Summary statistics of numeric columns.",
        "parameters": {"type": "object", "properties": {}}}},
]

def execute_tool(name, arguments, df):
    if name not in REGISTRY:
        return f"unknown tool: {name}"
    return REGISTRY[name](df, **arguments)

def mock_model(messages, tools):
    for m in messages:
        if m.get("role") == "tool":
            return {"message": {"content":
                    "The mean tip is highest on Sunday."}}
    return {"message": {"tool_calls": [{"function": {
        "name": "tip_by", "arguments": {"by": "day"}}}]}}

def run_loop(question, use_real_llm=False, max_steps=4):
    messages = [{"role": "user", "content": question}]
    transcript = []
    for _ in range(max_steps):
        if use_real_llm:
            import ollama
            msg = ollama.chat(model="llama3.2", messages=messages,
                              tools=TOOLS)["message"]
        else:
            msg = mock_model(messages, TOOLS)["message"]
        transcript.append(msg)
        if "tool_calls" not in msg:
            return msg["content"], transcript
        for call in msg["tool_calls"]:
            fn = call["function"]
            result = execute_tool(fn["name"], fn.get("arguments", {}), tips)
            messages.append(msg)
            messages.append({"role": "tool", "content": result})
            transcript.append({"tool": fn["name"], "result": result})
    return "max steps reached", transcript

# verify ground truth
print(tip_by(tips, "day"))     # Sun 3.26 is the max

answer, transcript = run_loop("Which day has the highest mean tip?", False)
print("ANSWER:", answer)
for step in transcript:
    print(step)
```

## Agent boundaries (model answer)

> Three boundaries protect the pipeline. (1) **Registered tools only** —
> the executor rejects any tool name outside `REGISTRY`, so a model can
> never invoke arbitrary functions. (2) **Max steps** — the loop stops
> after N rounds, preventing runaway tool-call chains. (3) **Your code
> executes the tools** — the model only *proposes* calls; the arguments
> are validated and executed by our functions, so the model never runs
> code directly on the machine.

## Model answers

1. **Model proposes, code executes** — the model can't run code; it
   returns a structured request, and your process decides whether and how
   to fulfill it (validation, permissions, audit).
2. **description field** — it's the model's only documentation of what
   the tool does and when to use it; poor descriptions → wrong tool
   choices.
3. **Tool results as messages** — the model's context must include what
   the tool returned, or it can't reason about the next step; the
   transcript also makes the chain auditable.
4. **REGISTRY guard** — blocks hallucinated or malicious tool names;
   without it, a bad function name could crash the loop or reach code it
   shouldn't.
5. **max_steps=1** — for single, well-specified lookups; raise it for
   multi-step plans (summarize → verify → compare). A cap always exists.

## Challenge solution

```python
def top_n(df, column, n):
    return df.nlargest(n, column).to_string()

REGISTRY["top_n"] = top_n
TOOLS.append({"type": "function", "function": {
    "name": "top_n",
    "description": "Largest n rows of a column.",
    "parameters": {"type": "object",
                   "properties": {"column": {"type": "string"},
                                  "n": {"type": "integer"}},
                   "required": ["column", "n"]}}})

def mock_planner(messages, tools):
    for m in messages:
        if m.get("role") == "tool":
            return {"message": {"content":
                    "The largest bill is 50.81 (from top_n)."}}
    return {"message": {"tool_calls": [{"function": {
        "name": "top_n", "arguments": {"column": "total_bill", "n": 1}}}]}}
# Transcript shows: user -> top_n -> tool result 50.81 -> answer.
# The number in the answer comes from the tool result, not memory.
```