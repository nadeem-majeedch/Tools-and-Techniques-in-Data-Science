# Module C · Topic 08 — AI Agents

**CLO-3 · Maps to:** Session 28 · Notebook 18 · Lab 28 · **Level:** Intermediate

---

## 1. Beginner explanation

An AI agent is a tool-calling loop on repeat: the model decides what to do
next, your code does it, the result comes back, and the model decides
*again* — until it has what it needs. Where a plain chat answers in one shot,
an agent can **work**: check a column, compute a number, notice it needs more
data, fetch it, recompute, and finally answer. The key rule stays the same:
the model never acts — it *requests* actions from your whitelisted tools,
and you set the loop's boundaries (max steps, allowed tools).

## 2. Conceptual explanation (the WHY)

The agent loop has exactly four steps, repeated:

1. **Think** — the model looks at the conversation so far and decides
   whether it can answer or needs a tool.
2. **Act (request)** — if it needs a tool, it emits a structured tool call.
3. **Observe** — your code runs the tool and appends the real result.
4. **Decide** — back to step 1, with the new information in context.

Why is this a *data science* pattern and not a gimmick? Because real
analyses are multi-step: *"find outliers → check how many → look at their
distribution → summarize."* An agent coordinates those steps while Python
does every computation. The loop is bounded (`max_steps`), the toolset is
whitelisted, and each step is logged — that's what makes it reproducible and
safe enough for beginners to build.

The failure modes are also predictable: loops that never converge (the model
keeps calling tools), loops that call the same tool forever, and final
answers that misread the real results. All three are handled by *bounding
the loop* and *verifying the final answer* — never by trusting the model.

## 3. Simple diagram

```text
        ┌────────────────────────────────────────────┐
        │             THE AGENT LOOP                 │
        │                                            │
        ▼                                            │
  ┌───────────┐    can I answer?  ┌──────────────┐   │
  │   LLM     │ ─── no ─────────► │ tool request │   │
  │ (decides) │ ◄─────────────────│ (whitelist)  │   │
  └───────────┘      yes          └──────┬───────┘   │
        │                                │ your code │
        │                                │ runs it   │
        ▼                                ▼           │
  FINAL ANSWER                 real result appended ─┘
  (still verified!)           (bounded by max_steps)
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

# Tools (whitelist) — plain functions
def avg_tip_by(df, column):
    return df.groupby(column)["tip"].mean().round(2).to_dict()

def count_outliers(df, column, threshold):
    return int((df[column] > threshold).sum())

TOOLS = [
    {"type": "function", "function": {
        "name": "avg_tip_by",
        "description": "Mean tip grouped by a categorical column.",
        "parameters": {"type": "object",
                       "properties": {"column": {"type": "string"}},
                       "required": ["column"]}}},
    {"type": "function", "function": {
        "name": "count_outliers",
        "description": "Count rows where a column exceeds a threshold.",
        "parameters": {"type": "object",
                       "properties": {"column": {"type": "string"},
                                      "threshold": {"type": "number"}},
                       "required": ["column", "threshold"]}}},
]
FUNCTIONS = {"avg_tip_by": avg_tip_by, "count_outliers": count_outliers}

if module_available("ollama"):
    import ollama

    def run_agent(question, max_steps=5):
        """The bounded agent loop — think → request → run → observe."""
        messages = [{"role": "system",
                     "content": "You answer from tool results only. "
                                "Stop when you have the answer."},
                    {"role": "user", "content": question}]
        for step in range(max_steps):
            msg = ollama.chat(model="llama3.2", messages=messages,
                              tools=TOOLS)["message"]
            if not msg.get("tool_calls"):
                print(f"[agent] final answer (step {step + 1}):")
                return msg["content"]
            for call in msg["tool_calls"]:
                name = call["function"]["name"]
                args = json.loads(call["function"]["arguments"])
                print(f"[agent] step {step + 1}: {name}({args})")
                result = FUNCTIONS[name](tips, **args)
                messages.append({"role": "assistant",
                                 "content": json.dumps(call)})
                messages.append({"role": "tool",
                                 "content": json.dumps(result)})
        return "[agent] stopped: max_steps reached without an answer"

    try:
        print(run_agent(
            "Are tips on weekends higher than weekdays? "
            "Compare average tips per day and reason from the numbers."))
    except Exception as e:
        print("Ollama not running:", e)
else:
    print("ollama package not installed:  pip install ollama")
```

## 5. Practical exercise (30 min)

Dataset: `sns.load_dataset("titanic")`.

1. Build `run_agent` with two tools: `survival_rate(by)` and `count(column,
   value)`.
2. Ask a two-step question: *"Which class had the lowest survival rate, and
   how many passengers were in it?"* — watch the agent chain two calls.
3. Deliberately break convergence: allow a tool that always returns the same
   thing and ask a question that can't be answered — observe `max_steps`
   stopping the loop. This is the "infinite loop" lesson.
4. Add logging: write every step (tool, args, result) to a list and print it
   at the end — your audit trail.
5. Write one paragraph: *when would you use an agent instead of writing the
   pandas directly, and when is it overkill?*

## 6. Common errors

| Error | Fix |
|---|---|
| Agent never stops calling tools | always enforce `max_steps`; tell the model to stop when answered |
| Same tool called repeatedly | the result wasn't informative — check what the tool returns; improve the tool, not the prompt |
| Final answer contradicts tool results | the model misread the numbers — verify final claims yourself |
| Tool crashes mid-loop | wrap tool execution in try/except and return the error message as the result |
| No audit trail | log every step; the loop without logs is unreproducible |

## 7. Limitations

- **Small-model ceilings** — multi-step reasoning on `llama3.2` degrades fast;
  keep agent tasks to 2–4 steps.
- **Convergence not guaranteed** — a bounded loop that times out is the
  *expected* failure mode; design for it.
- **Tool explosion** — many tools = worse tool selection; keep 2–5 focused
  tools.
- **Verification burden** — you now verify both tool results *and* the
  model's final interpretation.
- **Not autonomous** — no web access, no memory across sessions, no
  self-improvement; it's a bounded loop you wrote.

## 8. Responsible AI considerations

- **Bounded and whitelisted by design** — max steps + fixed tools are the
  agent's safety rails; removing either turns a demo into a hazard.
- **Every step logged** — an auditable agent is a responsible agent; the log
  is your disclosure record.
- **No acting without results** — the model must ground every claim in real
  tool output; "I think it's high" is not an answer.
- **Human in the loop for decisions** — the agent assembles evidence; a human
  reads the log and makes the call.

## 9. Assessment questions

**Q1.** Name the four steps of the agent loop in order. *(CLO-3 · Understand
· Easy)*
**Answer:** think → request a tool call → run the tool (your code) → observe
the result and decide again (bounded by max steps).

**Q2.** Your agent keeps calling `count_outliers` with the same arguments and
never produces an answer. What's the most likely cause and the fix?
**CLO-3 · Analyze · Medium**
**Answer:** the tool result doesn't advance the task (or the model can't
interpret it), so it retries. Fix: improve/validate the tool result or
bound the loop — and check that the question is answerable with the tools
at all.

**Q3.** Why must the agent loop be bounded even when it "works"? *(CLO-3 ·
Evaluate · Medium)*
**Answer:** unbounded loops waste time/compute and can call tools forever
with no answer; `max_steps` makes failure cheap and predictable.

**Q4.** An agent reports "weekend tips are higher" after calling
`avg_tip_by("day")`. What must you do before trusting that claim?
**CLO-3 · Evaluate · Medium**
**Answer:** verify against the logged tool result (or recompute with pandas)
— the tool output is real, but the model's summarization of it is still
generated text and can misread the numbers.