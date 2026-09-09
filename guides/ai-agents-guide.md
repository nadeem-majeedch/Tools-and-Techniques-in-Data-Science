# AI Agents Guide

An **AI agent** is an LLM in a loop: it decides what to do, calls a tool you
gave it, looks at the result, and repeats — until it answers the question or
hits a limit you set. The magic is not the model; it is the **loop plus
tools you control**.

## The idea, step by step

1. You define a small set of **tools** — plain Python functions the agent is
   *allowed* to call (e.g. `mean_sales(df)`, `fetch_weather(city)`).
2. The agent sees your question, the tool list, and (for each tool) its
   description.
3. The agent replies with a request to call a tool with specific arguments.
4. Your code runs the tool and hands the result back to the model.
5. Repeat until the agent produces a final answer — or you stop it.

```text
You  ──question──▶  LLM  ──call tool X(args)──▶  Your Python function
▲                      │                                │
│                      └────────result ◀────────────────┘
└── answer or next tool call ◀── (loop, bounded by max_iterations)
```

## A minimal agent in Python

```python
import json
import ollama

MODEL = "llama3.2"

def mean_sales(df):
    """Tool 1: total sales per month, as a dict."""
    return df.groupby("month")["sales"].sum().to_dict()

def max_month(df):
    """Tool 2: month with the highest sales."""
    return df.groupby("month")["sales"].sum().idxmax()

TOOLS = {
    "mean_sales": {"function": mean_sales,
                   "description": "Total sales per month."},
    "max_month":  {"function": max_month,
                   "description": "Month with highest sales."},
}

def run_agent(question, df, max_iterations=3):
    messages = [{"role": "user", "content": question}]
    for _ in range(max_iterations):                 # ← the bound that saves you
        reply = ollama.chat(model=MODEL, messages=messages)
        content = reply["message"]["content"]
        # Does the model ask to call a tool? (simplified parse — real code
        # uses structured tool calling; see Notebook 17)
        if content.startswith("TOOL:"):
            name, args = content[5:].split("|", 1)
            result = TOOLS[name]["function"](df)    # you RUN the tool
            messages.append({"role": "assistant", "content": content})
            messages.append({"role": "user",
                             "content": f"Tool result: {json.dumps(result)}"})
        else:
            return content                          # a final answer
    return "(stopped: iteration limit reached)"

print(run_agent("Which month had the highest sales?", sales_df))
```

??? info "Why this is course-shaped"
    This exact pattern — a whitelist of tools, a bounded loop, and you (not
    the model) executing the tool — is what [Notebook 17](../course-notebooks/17-tool-and-function-calling.ipynb)
    and [Notebook 18](../course-notebooks/18-ai-agents.ipynb) build up to,
    and it is what tools like n8n's AI Agent node wrap in a visual interface.

## Safety rules (they are graded)

1. **Whitelist tools** — the agent can only call functions you wrote and
   listed. No tool, no "surprise" behavior.
2. **Bound the loop** — `max_iterations` and a timeout. An unbounded agent
   can loop forever and burn your CPU on pointless calls.
3. **Validate arguments** — the model's arguments are text; check types and
   ranges before calling your function.
4. **Never give the agent destructive tools** — no `os.remove`, no internet
   write access, no sending email in class projects.
5. **Verify the final answer** — the agent's summary is still an LLM claim;
   run your own check against the data.

## Common errors

| Error | Fix |
|---|---|
| Agent loops forever | set `max_iterations` and return early on final answers |
| Tool called with wrong arguments | validate/coerce args; give each tool a precise description |
| Model "calls" a tool that doesn't exist | keep tool names short and list them explicitly in the prompt |
| Agent invents the tool result | it can't if *you* run the tool — never trust a "result" the model wrote by itself |
| Answer still wrong | the question was too big for a local model; break it into steps |

## Go deeper

- Full lecture: [Session 28 — AI Agents](../sessions/session-28-ai-agents.md)
- Executed notebooks: [Notebook 17 — Tool calling](../course-notebooks/17-tool-and-function-calling.ipynb) · [Notebook 18 — AI Agents](../course-notebooks/18-ai-agents.ipynb)
- Practice: [Lab 28 · Tool calling](../labs/lab-28-tool-calling.md)
- Teacher's deep dives: [Module C topics 07–08](../module-c/topic-07-tool-calling.md)
- Visual agent nodes (no code): [n8n Guide](n8n-guide.md) · [Session 29](../sessions/session-29-n8n-automation.md)
