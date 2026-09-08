# Session 28 — Simple AI Agents

**Week 14 · Session 28 · Module C · 90 min · CLO-3**

## 1. Learning objectives

By the end of this session, students can:
- Explain what an AI agent is: an LLM that can call tools in a loop.
- Define the agent loop: think → call tool → observe result → decide.
- Define a Python function as a "tool" the model can call.
- Run a simple tool-calling agent with Ollama and inspect the tool calls.
- Automate one small data-analysis subtask and document it.

## 2. Key concepts

- **Agent = LLM + tools + a loop:** the model doesn't just answer — it can *do* things and see results.
- **Tool calling:** the model outputs a structured request ("call `get_weather(city=...)`"); your code executes it and returns the result.
- **The loop:** the model alternates between reasoning and tool calls until it has what it needs.
- **You write the tools, you set the boundaries:** an agent can only call functions you define — that's the safety design.
- Agents are **not autonomous wizards**: they inherit the LLM's hallucination risk; every tool result they report must still be verified.
- The reproducibility rule extends: record the prompt, the tool calls, and the final answer.

## 3. Detailed lecture notes

**From chat to agent.** Until now the LLM only produced text. An **agent**
turns it into an actor: the model can request a *tool call* ("call function
`tip_summary(by='day')`"), your code runs the tool, and the result is fed back
to the model. The model then continues — perhaps calling another tool, or
producing the final answer. The pattern is a loop: **reason → call tool →
observe → reason again**. This is how "AI assistants" that check the weather,
query databases, or summarize files actually work. For data science, the agent
loop is a natural fit: the "tools" are pandas functions and analysis steps.

**How tool calling works (mechanics).** The model is told which tools exist —
name, description, and parameter schema. When appropriate, it responds with a
structured tool request instead of plain text:
```
ToolCall: get_tip_summary(by="day")
```
Your code receives this, runs the real function, and returns the output as a
new "tool" message. The model sees the result and decides what's next. You are
the one who *writes and executes* the tools — the model never runs arbitrary
code itself. That division is the safety property: **the agent can only do
what you've coded it to do.** The tool's docstring (description) is the model's
instruction manual — write it carefully ("Returns the mean tip grouped by the
given column; use when asked about tips by category").

**Building a data-analysis agent (course scale).** Keep it deliberately small:
1. Write 2–3 pure Python functions over a DataFrame (e.g., `summary_stats(df)`,
   `tip_by(df, by)`, `detect_missing(df)`).
2. Describe them to the model (tool schema).
3. Loop: ask the agent a question ("which day has the highest tips, and how many
   rows are missing?"); it calls tools; you run them; feed results back; repeat
   until it answers.
Implementation with Ollama: the Python client supports `tools=` in `chat()`
(OpenAI-style JSON schema; requires Ollama ≥ 0.4 server and the model to
support tool calling — `llama3.2` does; verify versions in class). Walk through
the request/response cycle and *print* the tool calls so students see the
interleaving — the "agent" is just this visible loop, not magic.

**Why agents for data science?** The honest pitch: for one-off questions, a
plain chat (Sessions 25–27) is enough. An agent pays off when a task has
several steps with decisions between them — e.g., "check the data quality, then
summarize the worst column, then tell me if I should clean or drop it". The
agent can chain those steps itself, using your verified functions. For this
course, the goal is to *see the loop working* on one realistic subtask — not to
build a general assistant. Scope discipline (Session 23's lesson) applies to
agents too.

**Risks to teach (briefly, honestly).** The loop can run long (cap it — max N
tool calls), tools can be called with wrong arguments (validate inputs in your
functions), and the model can misreport what a tool returned (it summarizes —
the underlying result is ground truth; keep the transcript). Two rules: (1)
log the full transcript (prompt, calls, results) for reproducibility; (2) the
final numbers you report come from *your* tools' outputs, not from the model's
prose. This is the Session 25 verification protocol, agent edition.

## 4. Important terminology

- **Agent** — LLM + tools + loop: can act and observe.
- **Tool / function calling** — the model requests a function; your code executes it.
- **Tool schema** — name + description + parameters, telling the model what's callable.
- **Agent loop** — reason → call tool → observe → reason, until done.
- **Tool result / observation** — the function's output fed back to the model.
- **Max iterations** — cap on loop length (safety valve).
- **Tool transcript** — the logged record of every call (reproducibility).
- **Boundaries** — the agent can only call the functions you wrote.
- **Ground truth** — actual tool outputs; the model's summaries must be checked against them.

## 5. Python examples

```python
import ollama
import seaborn as sns
import pandas as pd

tips = sns.load_dataset("tips")

# --- 1. Write the tools (plain functions, YOUR code) ---
def tip_by(df: pd.DataFrame, by: str) -> str:
    """Mean tip grouped by a column. Use for questions about tips by category."""
    return df.groupby(by)["tip"].mean().round(2).to_string()

def missing_summary(df: pd.DataFrame) -> str:
    """Count missing values per column. Use when asked about data quality."""
    return df.isna().sum().to_string()

# --- 2. Describe the tools to the model (schema) ---
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

# --- 3. The agent loop (one iteration shown; loop until no tool call) ---
messages = [{"role": "user",
             "content": "Which day has the highest average tip? Also, are there any missing values?"}]

resp = ollama.chat(model="llama3.2", messages=messages, tools=tools)
msg = resp["message"]
print("Model wants to call:", msg.get("tool_calls"))

# --- 4. Execute the requested tool and feed the result back ---
if msg.get("tool_calls"):
    for call in msg["tool_calls"]:
        fn = call["function"]["name"]
        args = call["function"]["arguments"]
        result = {"tip_by": tip_by, "missing_summary": missing_summary}[fn](tips, **args)
        messages.append(msg)                                  # the tool request
        messages.append({"role": "tool", "content": str(result)})  # the observation

    final = ollama.chat(model="llama3.2", messages=messages, tools=tools)
    print(final["message"]["content"])
```

```python
# --- The loop, made safe and visible: cap iterations, log everything ---
def run_agent(question, tools, max_steps=5):
    messages = [{"role": "user", "content": question}]
    log = []
    for step in range(max_steps):
        resp = ollama.chat(model="llama3.2", messages=messages, tools=tools)
        msg = resp["message"]
        log.append(msg)
        if not msg.get("tool_calls"):
            return msg["content"], log
        for call in msg["tool_calls"]:
            result = EXECUTE[call["function"]["name"]](**call["function"]["arguments"])
            messages.append(msg)
            messages.append({"role": "tool", "content": str(result)})
            log.append({"tool_call": call, "result": result})
    return "Reached max steps.", log
```

## 6. Beginner example

```python
# The smallest agent: one tool (a calculator), one question.
import ollama

def add(a: float, b: float) -> str:
    """Add two numbers. Use for arithmetic questions."""
    return str(a + b)

tools = [{"type": "function",
          "function": {"name": "add", "description": add.__doc__,
                       "parameters": {"type": "object",
                                      "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                                      "required": ["a", "b"]}}}]

resp = ollama.chat(model="llama3.2",
                   messages=[{"role": "user", "content": "What is 12 + 30?"}],
                   tools=tools)
print(resp["message"].get("tool_calls"))   # asks to call add(12, 30)
print(add(12, 30))                          # YOU run it: 42
```

## 7. Practical Data Science example

```python
# An agent that answers "Is this dataset analysis-ready?" using your tools
import ollama
import seaborn as sns
import pandas as pd

penguins = sns.load_dataset("penguins")

def missing_summary(df):
    """Count missing values per column."""
    return df.isna().sum().to_string()

def describe_numeric(df):
    """Summary statistics of numeric columns."""
    return df.describe().round(2).to_string()

# (tools schema as above — abbreviated here)
# Question: "Should I drop missing values before modeling? Base your answer on
#            the data, calling tools as needed."
# Expected flow: missing_summary -> describe_numeric -> final answer.
# Verification rule: the counts in the answer must match the tool outputs you
# logged. Record the whole transcript in project/ai-notes.md.
```

## 8. In-class activity (50 min)

In `notebooks/week-14/session-28-agents.ipynb`:

1. **The loop, printed (15 min):** run the tips agent from section 5; print
   `tool_calls` and each tool result *before* the final answer — students see
   the interleaving.
2. **Your own tool (20 min):** write one more tool for the tips data (e.g.,
   `top_rows_by`, returning the top-5 rows of a column), add it to the schema,
   and ask a question that needs *both* your new tool and an existing one.
3. **Boundary check (15 min):** ask the agent to do something its tools can't
   (e.g., "delete a column") — watch it either refuse or hallucinate; then
   confirm that no code ran (the agent can only call your functions). Write one
   sentence on why boundaries are the safety feature.

## 9. Lab exercise

No graded lab this session — it's a build day: continue your **Assignment 2
Streamlit app** (due Session 30) and the project's AI component. Today's
agent loop is exactly the pattern you'll reuse there.

## 10. Common mistakes

- Expecting the model to run code itself — it only *requests* tool calls; your code executes them.
- Writing vague tool descriptions → the model never calls the tools (descriptions are the model's manual).
- No max-iteration cap → loops that run away (and cost time).
- Trusting the model's summary of a tool result instead of reading the logged result.
- Forgetting to append the tool result to the message history → the model can't see its own observations.
- Letting the agent decide things your tools don't cover — it will improvise; bound it.
- Not logging the transcript → unreproducible agent step in the project.

## 11. Short assessment questions

1. What three ingredients make an "agent"?
2. Describe the agent loop in four steps.
3. Who executes the tool when the model requests a call? (Your code.)
4. Why is "the agent can only call functions you define" a safety feature?
5. What is the risk of the model summarizing a tool result, and what's the fix?
6. What belongs in an agent transcript for reproducibility?

## 12. CLO mapping

CLO-3: agents are the "basic AI agents" named in the CLO. This session turns
them from buzzword to mechanism — a bounded loop over *your* verified functions —
and keeps the reproducibility (transcript) and responsibility (boundaries,
verification) requirements front and center.

## 13. Suggested homework

- Build one agent that automates a small step of *your* project (e.g., "check
  cleaning completeness" or "summarize the cleaned dataset"); log the transcript.
- Decide which AI component your project will use (PandasAI/Ollama step vs. n8n automation) and note it in your plan.
- Read: Ollama blog/docs on function calling (github.com/ollama/ollama — "Function calling" section).
- Preview: Session 29 moves from code agents to *visual* automation with n8n — workflows that collect and process data without writing a loop.