# Lab 28 — Tool Calling & AI Agents

**Session:** Week 14 · Session 28 · 90 min
**CLO:** CLO-3
**Difficulty:** Advanced

## Learning objectives

By the end of this lab you can:

1. Describe functions to an LLM with OpenAI-style tool schemas.
2. Implement the model→tool→result round trip.
3. Run the loop with a real model **or** a deterministic mock.
4. Explain why the *model proposes, your code executes* split is a safety
   property.

## Problem statement

You must give an LLM the ability to *compute* instead of guess: three
pandas tools (mean tip by day, missing-value count, numeric summary) plus a
loop that executes whatever tool call the model proposes. The twist: the
deliverable must work with a real local model **and** with a mock — because
in production the loop is the same either way.

## Dataset requirements

Seaborn built-in `tips` (244 rows).

## Step-by-step tasks

1. **Tools:** write three plain functions:
   - `tip_by(df, by)` → `df.groupby(by)["tip"].mean().round(2).to_string()`
   - `missing_summary(df)` → `df.isna().sum().to_string()`
   - `describe_numeric(df)` → `df.describe().round(2).to_string()`
   Build a `REGISTRY = {name: func}` dict.
2. **Schemas:** for each tool, write the OpenAI-style schema dict
   (`type: "function"`, `name`, `description`, `parameters` with
   `properties` and `required`). `tip_by` needs a `by` string property.
3. **Executor:** `execute_tool(name, arguments, df)` that looks the
   function up in `REGISTRY` and calls it with the arguments. Add a
   **guard**: if the name is not in `REGISTRY`, return
   `"unknown tool: <name>"` instead of raising.
4. **Mock model:** write `mock_model(messages, tools)` that:
   - returns a tool call for `tip_by(by="day")` on the first user message,
   - and returns a final answer ("The mean tip is highest on Sunday.")
     once a tool result is present in the messages.
5. **Loop:** implement `run_loop(question, use_real_llm)` (max 4 steps):
   append user message → get model message → if it has `tool_calls`,
   execute each and append the tool result as role `"tool"` → else return
   the answer. Print the transcript (each step) so the loop is auditable.
6. **Run both paths:** `run_loop("Which day has the highest mean tip?",
   use_real_llm=False)` (mock — must print the transcript) and, guarded,
   the same question with `use_real_llm=True` (Ollama; degrades to a
   message if unavailable).
7. **Verify the mock's final answer** against `tip_by(tips, "day")` — the
   real max is Sun ≈ 3.26, so the mock is correct; state this in a comment.
8. **Agent boundaries (session topic):** in one markdown paragraph, list
   the three boundaries your loop enforces (registered tools only, max
   steps, your code executes the tools) and why each one is a safety
   property. Then automate a small project subtask: run the loop on your
   own project DataFrame with `missing_summary` and `describe_numeric`
   (mock path) and save the transcript to a text file as an agent log.

## Starter code

```python
import pandas as pd
import seaborn as sns

tips = sns.load_dataset("tips")

# 1. tools + registry
def tip_by(df, by):
    return df.groupby(by)["tip"].mean().round(2).to_string()

def missing_summary(df):
    return df.isna().sum().to_string()

def describe_numeric(df):
    return df.describe().round(2).to_string()

REGISTRY = {"tip_by": tip_by, "missing_summary": missing_summary,
            "describe_numeric": describe_numeric}

# 2. schemas (write these yourself — one per tool)
# tip_by_schema = {"type": "function", "function": {...}}
# your code here

# 3-6. executor, mock, loop, runs
# your code here
```

## Expected output

- `REGISTRY` has 3 entries; schemas printed for inspection.
- `execute_tool("tip_by", {"by": "day"}, tips)` returns the day table;
  `execute_tool("hack", {}, tips)` returns `"unknown tool: hack"`.
- Mock path prints a transcript showing: user → tool_call → tool result →
  final answer.
- Real path (if Ollama up) prints a transcript too; otherwise a clear
  skip message.
- Final answer verified: Sun has the highest mean tip.

## Questions

1. Why does the model send a *proposal* (tool call) instead of running code
   itself?
2. What is the purpose of the `description` field in a schema?
3. Why must tool results come back to the model as messages? What would the
   model miss without them?
4. What does the `REGISTRY` guard protect against?
5. When would you set `max_steps` to 1? When would you raise it?

## Challenge task

Add a **fourth tool** of your own (e.g., `top_n(df, column, n)` returning
the largest rows) with a correct schema, and extend the mock to call it in
a two-step plan: first `top_n` on `total_bill`, then answer. Run the mock
path and show the transcript proves the answer came from the tool result,
not from the model's memory.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Three tools + registry | 4 | functions correct |
| Schemas with required fields | 5 | all three complete |
| Executor + unknown-tool guard | 4 | tested both ways |
| Mock model (tool call → answer) | 5 | correct flow |
| Loop with transcript | 5 | auditable steps |
| Both paths run | 3 | mock always, real guarded |
| Verification comment | 3 | Sun ≈ 3.26 |
| Answers to questions | 3 | Q1, Q3, Q4 correct |
| Challenge: 4th tool + 2-step plan | 4 | works in mock |
| **Total** | **36** | |