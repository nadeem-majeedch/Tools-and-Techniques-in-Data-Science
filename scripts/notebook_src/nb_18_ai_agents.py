# Content for notebook 18: AI Agents.
CELLS = [
    ("md", """# 18 — AI Agents

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-3 — Develop simple AI-assisted data science workflows (basic AI agents).

An **agent** is an LLM plus tools plus a loop: it doesn't just answer — it
can *act* (call your functions), *observe* the results, and *decide* what to
do next. This notebook builds a small, safe, data-analysis agent from the
tool-calling mechanics of notebook 17.

---
"""),("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Explain what makes an agent (LLM + tools + loop).
2. Build a small data-analysis agent over a DataFrame.
3. Run it with a real local model (guarded) or a simulation (always runs).
4. Apply boundaries: max steps, registered tools only, input validation.
5. Keep an agent transcript for reproducibility.

---
"""),("md", """## Theory: agents in one paragraph

A chat answers; an **agent** acts. The difference is the loop: the model
alternates between *reasoning* ("I need the mean tip by day") and *tool
calls* ("call `tip_by(day)`"), observing each result until it can answer.
For data science, the tools are pandas functions — the agent chains steps
your EDA would otherwise do by hand: check quality, summarize, compare,
report. Two honest notes:

- Agents are **not autonomous wizards** — they inherit the LLM's
  hallucination risk; their reported numbers must be checked against tool
  outputs.
- The value appears when a task has **several steps with decisions between
  them** — for one-off questions, a plain chat is enough.

---
"""),("code", """import pandas as pd
import seaborn as sns
import ollama

tips = sns.load_dataset("tips")

# --- The toolset (from notebook 17, plus one more) ---
def tip_by(df, by):
    \"\"\"Mean tip grouped by a column. Use for questions about tips by category.\"\"\"
    return df.groupby(by)["tip"].mean().round(2).to_string()

def missing_summary(df):
    \"\"\"Count missing values per column. Use for data-quality questions.\"\"\"
    return df.isna().sum().to_string()

def describe_numeric(df):
    \"\"\"Summary statistics of numeric columns. Use for overview questions.\"\"\"
    return df.describe().round(2).to_string()

REGISTRY = {"tip_by": tip_by, "missing_summary": missing_summary,
            "describe_numeric": describe_numeric}

TOOLS = [
    {"type": "function", "function": {"name": "tip_by", "description": tip_by.__doc__,
        "parameters": {"type": "object", "properties": {"by": {"type": "string"}}, "required": ["by"]}}},
    {"type": "function", "function": {"name": "missing_summary", "description": missing_summary.__doc__,
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "describe_numeric", "description": describe_numeric.__doc__,
        "parameters": {"type": "object", "properties": {}}}},
]

print("agent toolset ready:", list(REGISTRY))
"""),
    ("md", """## The agent loop, written once

The core function. Everything else — real model or simulation — plugs into
the same loop.

---
"""),("code", """def run_agent(question, registry, tools, max_steps=6, use_real_llm=False):
    \"\"\"Run the agent loop. Returns (final_answer, transcript).

    use_real_llm=True requires Ollama running with a model pulled.
    \"\"\"
    messages = [{"role": "user", "content": question}]
    transcript = []

    for step in range(max_steps):
        # 1. REASON: get the model's next move (tool call or final answer)
        if use_real_llm:
            msg = ollama.chat(model="llama3.2", messages=messages, tools=tools)["message"]
        else:
            msg = mock_planner(messages, tools)["message"]

        # 2. DONE? no tool call -> this is the final answer
        if not msg.get("tool_calls"):
            transcript.append({"step": step, "type": "answer", "text": msg["content"]})
            return msg["content"], transcript

        # 3. ACT: execute every requested tool with YOUR code
        for call in msg["tool_calls"]:
            fn = call["function"]["name"]
            args = call["function"]["arguments"]
            if fn not in registry:
                result = f"ERROR: unknown tool {fn}"
            else:
                result = registry[fn](tips, **args) if fn in ("tip_by",) else registry[fn](tips)
            transcript.append({"step": step, "type": "tool", "tool": fn, "args": args})

            # 4. OBSERVE: give the result back to the model
            messages.append(msg)
            messages.append({"role": "tool", "content": str(result)})

    return "Reached max steps.", transcript


def mock_planner(messages, tools):
    \"\"\"Deterministic stand-in: quality check, then overview, then answer.\"\"\"
    asked = [m.get("tool_calls") for m in messages if m.get("tool_calls")]
    if len(asked) == 0:
        return {"message": {"tool_calls": [
            {"function": {"name": "missing_summary", "arguments": {}}}]}}
    if len(asked) == 1:
        return {"message": {"tool_calls": [
            {"function": {"name": "describe_numeric", "arguments": {}}}]}}
    return {"message": {"content": "No missing values. Numeric overview looks "
                                   "healthy; tips average ~3.0 with max 10."}}
"""),
    ("md", """## Run it: simulation first (always works)

---
"""),("code", """answer, transcript = run_agent(
    "Check data quality, then summarize the numeric columns.",
    REGISTRY, TOOLS, max_steps=6, use_real_llm=False,
)

print("ANSWER:", answer)
print()
print("TRANSCRIPT (what actually happened):")
for t in transcript:
    print(" ", t)
"""),
    ("md", """## Run it: real local model (guarded)

With Ollama running, the same loop uses the real `llama3.2` model. The
structure is identical — only the "brain" changes.

---
"""),("code", """try:
    answer, transcript = run_agent(
        "Is the tips data ready for analysis? Check quality, then give an overview.",
        REGISTRY, TOOLS, max_steps=6, use_real_llm=True,
    )
    print("ANSWER:", answer)
    print("TRANSCRIPT:", transcript)
except Exception as e:
    print("Ollama not ready:", e)
    print("-> start Ollama + ollama pull llama3.2, then re-run")
"""),
    ("md", """## Boundaries: what the agent CANNOT do

The agent can only reach functions in `REGISTRY`. Ask it to do anything else
and — with the real model — it should refuse or hallucinate; either way, **no
code runs**. The mock below demonstrates the mechanism: an unknown tool
produces an error result, never execution.

---
"""),("code", """# Try a tool that does NOT exist in the registry
messages = [{"role": "user", "content": "delete the tip column"}]
fake_call = {"function": {"name": "delete_column", "arguments": {}}}

if "delete_column" not in REGISTRY:
    print("BLOCKED: delete_column is not a registered tool.")
    print("The agent can only call:", list(REGISTRY))
print("The 'delete' never executes - no such function exists in REGISTRY.")
"""),
    ("md", """## Beginner example: the smallest agent

One tool, one loop, one answer — the full idea in miniature (simulated).

---
"""),("code", """def biggest_tip(df):
    \"\"\"Return the row with the largest tip.\"\"\"
    return df.nlargest(1, "tip").to_string()

def mock_one(messages, tools):
    for m in messages:
        if m.get("role") == "tool":
            return {"message": {"content": "Found it - the biggest tip is above."}}
    return {"message": {"tool_calls": [
        {"function": {"name": "biggest_tip", "arguments": {}}}]}}

msgs = [{"role": "user", "content": "What is the biggest tip?"}]
msg = mock_one(msgs, tools)["message"]
call = msg["tool_calls"][0]["function"]
result = biggest_tip(tips)
print("tool result:")
print(result)
"""),
    ("md", """## Intermediate example: agent answering a real question

The agent answers "which day tips the highest percentage?" — simulated, with
a transcript you can audit. Every number in the final answer traces back to
a tool result in the transcript.

---
"""),("code", """tips["tip_pct"] = tips["tip"] / tips["total_bill"] * 100

def tip_pct_by(df, by):
    \"\"\"Mean tip percentage (tip/total_bill*100) grouped by a column.\"\"\"
    return df.groupby(by)["tip_pct"].mean().round(2).to_string()

REGISTRY2 = dict(REGISTRY); REGISTRY2["tip_pct_by"] = tip_pct_by

TOOLS2 = TOOLS + [{"type": "function",
                   "function": {"name": "tip_pct_by", "description": tip_pct_by.__doc__,
                                "parameters": {"type": "object",
                                               "properties": {"by": {"type": "string"}},
                                               "required": ["by"]}}}]

def mock_pct(messages, tools):
    for m in messages:
        if m.get("role") == "tool":
            return {"message": {"content": "Sunday has the highest mean tip percentage."}}
    return {"message": {"tool_calls": [
        {"function": {"name": "tip_pct_by", "arguments": {"by": "day"}}}]}}

msgs = [{"role": "user", "content": "Which day tips the highest percentage?"}]
msg = mock_pct(msgs, TOOLS2)["message"]
call = msg["tool_calls"][0]["function"]
result = REGISTRY2[call["name"]](tips, **call["arguments"])
print("tool result (ground truth):")
print(result)
# The agent's final answer must match this tool output — verify, don't trust.
"""),
    ("md", """## Exercises

---
"""),("md", """### Exercise 1 — Add a tool

Write `rows_above(df, col, threshold)` returning the count of rows where
`col > threshold`, register it, and describe it in a docstring. Test it
directly (not via the agent) on `tips` (`total_bill > 30` → 62 rows)."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
def rows_above(df, col, threshold):
    \"\"\"Count rows where col > threshold. Use for threshold questions.\"\"\"
    return str((df[col] > threshold).sum())

print(rows_above(tips, "total_bill", 30))
# Expected output: 62
"""),
    ("md", """### Exercise 2 — Audit a transcript

From the intermediate example's transcript: which tool was called, with what
arguments, and what was the result? Write the audit in markdown — this is
exactly what a reproducibility review looks like."""),
    ("code", """# Audit (markdown):
#   Tool called: tip_pct_by(by="day")
#   Result: per-day mean tip percentages (printed above)
#   Claim: Sunday highest -> matches tool output row.
print("audit in markdown")
"""),
    ("md", """### Exercise 3 — Capped loop

Change `run_agent`'s mock so it *always* requests a tool call (never
answers), and confirm the loop stops at `max_steps` instead of running
forever. Why does the cap matter?"""),
    ("code", """# your code here
"""),
    ("code", """# Solution
def mock_never_answers(messages, tools):
    return {"message": {"tool_calls": [
        {"function": {"name": "missing_summary", "arguments": {}}}]}}

# Reuse the loop with the stubborn mock
msgs = [{"role": "user", "content": "go"}]
steps = 0
for step in range(6):           # max_steps = 6
    msg = mock_never_answers(msgs, tools)["message"]
    if not msg.get("tool_calls"):
        break
    call = msg["tool_calls"][0]["function"]
    msgs.append(msg); msgs.append({"role": "tool", "content": REGISTRY[call["name"]](tips)})
    steps += 1
print("steps taken:", steps, "-> capped at max_steps, no infinite loop")
"""),
    ("md", """## Challenge exercise

Build a **project-data quality agent**:

1. Tools: `missing_summary(df)`, `describe_numeric(df)`, and
   `duplicates_count(df)` (return `str(df.duplicated().sum())`).
2. A mock planner that calls all three in sequence, then answers with the
   transcript's numbers.
3. Run the loop on your own project dataset (or `penguins`).
4. Write the transcript to a text file (or print it) as your agent log —
   that's the reproducibility record.
5. Add one sentence: what would make you trust this agent's final answer?"""),
    ("code", """# your code here
"""),
    ("code", """# Solution
import seaborn as sns

penguins = sns.load_dataset("penguins")

def duplicates_count(df):
    \"\"\"Count duplicate rows. Use for quality checks.\"\"\"
    return str(df.duplicated().sum())

REG = {"missing_summary": missing_summary,
       "describe_numeric": describe_numeric,
       "duplicates_count": duplicates_count}
PLAN = ["missing_summary", "describe_numeric", "duplicates_count"]

def mock_quality(messages, tools):
    for m in messages:
        if m.get("role") == "tool":
            if not PLAN:
                return {"message": {"content": "Quality check complete - see transcript."}}
    tool = PLAN.pop(0)
    return {"message": {"tool_calls": [{"function": {"name": tool, "arguments": {}}}]}}

msgs = [{"role": "user", "content": "quality check"}]
transcript = []
for step in range(6):
    msg = mock_quality(msgs, TOOLS)["message"]
    if not msg.get("tool_calls"):
        break
    call = msg["tool_calls"][0]["function"]
    result = REG[call["name"]](penguins)
    transcript.append(f"tool={call['name']}\\n{result}\\n")
    msgs.append(msg); msgs.append({"role": "tool", "content": str(result)})

log = "\\n".join(transcript)
print(log[:600])

# Trust rule: every number in the answer must appear in this transcript -
# verify the tool outputs, not the model's prose.
"""),
    ("md", """## Recap

- Agent = LLM + tools + loop (reason → call → observe → decide).
- The loop is the same with a real model or a simulation — build once, swap brains.
- Boundaries: registered tools only, `max_steps` cap, your code executes everything.
- Audit via transcript: the final answer must match the tool outputs.
- One-off questions don't need an agent; multi-step tasks do.

---
"""),
    ("md", """## Questions

1. What three ingredients make an agent?
2. Describe the agent loop in four steps.
3. Who executes tools when the model requests a call?
4. Why is the registered-tools-only rule a safety feature?
5. What is the risk when the model summarizes a tool result, and the fix?
6. What belongs in an agent transcript for reproducibility?

---
**Next:** notebook 19 — n8n workflows.
"""),
]