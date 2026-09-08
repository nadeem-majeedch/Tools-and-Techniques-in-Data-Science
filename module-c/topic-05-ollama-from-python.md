# Module C · Topic 05 — Using Ollama from Python

**CLO-3 · Maps to:** Session 27 · Notebook 16 · Lab 27 · **Level:** Beginner

---

## 1. Beginner explanation

The `ollama run` terminal chat is fine for experiments, but real data work
needs Python: you want to send prompts *from your notebook*, capture the
reply in a variable, and loop over many questions. The Python package
`ollama` is a thin client: `ollama.chat(model=..., messages=...)` sends your
messages to the local Ollama server and returns the model's reply as a
Python dict. Everything from topic 02 (tokens, temperature, system prompts)
is still true — you're just driving it from code.

## 2. Conceptual explanation (the WHY)

Ollama runs a local HTTP server (default port 11434) that speaks the
OpenAI-compatible chat API. The Python client is a convenience wrapper
around that HTTP endpoint:

1. You build a `messages` list — each item has a `role` (`system`, `user`,
   or `assistant`) and `content`.
2. `ollama.chat` POSTs the messages to the server; the server runs the model
   locally.
3. The reply comes back as a dict: `reply["message"]["content"]`.

Why the `messages` list matters: the model has no memory. The list *is* the
memory — every turn you send the whole conversation. For a data workflow you
can build prompts programmatically: inject a real schema, loop over
questions, save every reply to your audit log. That turns a chat toy into a
reproducible step in your pipeline.

## 3. Simple diagram

```text
Python (your notebook)
   messages = [{"role":"system","content": ...},
               {"role":"user","content": ...}]
        │  HTTP POST (localhost:11434)
        ▼
┌───────────────────────┐
│  Ollama server        │  runs llama3.2 locally
│  (runs the model)     │
└───────────┬───────────┘
            │  HTTP reply
            ▼
   reply["message"]["content"]   →  your variable
   "The mean tip on Saturday is 3.03..."
        │
        ▼
   you verify against pandas, then log question+prompt+reply
```

## 4. Python examples

```python
import importlib

def module_available(name):
    try:
        importlib.import_module(name)
        return True
    except ImportError:
        return False

if module_available("ollama"):
    import ollama

    MODEL = "llama3.2"

    def ask(system, user, temperature=0.2):
        """Send one chat turn and return the text reply."""
        reply = ollama.chat(
            model=MODEL,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
            options={"temperature": temperature},
        )
        return reply["message"]["content"]

    try:
        # Example: turn a data question into a first draft of pandas code
        system = ("You write short, working pandas code. Use only the "
                  "columns given. Return only code.")
        user = ("DataFrame `df` with columns: month, sales. Write code to "
                "find the month with the highest sales.")
        draft = ask(system, user)
        print("MODEL DRAFT:\n", draft)

        # The output is a DRAFT — this is where you take over:
        #   1. read it, 2. run it, 3. verify against real data.
        print("\n-> Next step: run this code on real data and verify.")
    except Exception as e:
        print("Ollama not running — start it and pull llama3.2:", e)
else:
    print("ollama package not installed:  pip install ollama")
```

Practical loop — many questions, one session:

```python
if module_available("ollama"):
    import ollama

    system = "Answer with one short sentence from the data given."
    questions = [
        "Which day has the highest total tips?",
        "Does smoking correlate with larger tips?",
    ]
    try:
        for q in questions:
            r = ollama.chat(model="llama3.2",
                            messages=[{"role": "system", "content": system},
                                      {"role": "user", "content": q}])
            print("Q:", q)
            print("A:", r["message"]["content"])
            print("---")
    except Exception as e:
        print("Ollama not running:", e)
```

## 5. Practical exercise (25 min)

Dataset: `sns.load_dataset("tips")`.

1. Write an `ask()` helper (like above) with a system prompt that demands
   short answers.
2. Loop over 3 questions about tips; save each (question, reply) pair to a
   list.
3. For one reply, verify the claim with pandas (e.g., "highest total tips by
   day" → `tips.groupby("day")["tip"].sum()`).
4. Try `temperature=0.0` vs `temperature=0.9` on the same question and
   compare (low = same answer every run, dry; high = varies, creative).
5. Append a short audit log to your notebook: question, model, temperature,
   reply, hand-verified number, verdict.

## 6. Common errors

| Error | Fix |
|---|---|
| `ConnectionError` / refuses to connect | Ollama server not running — start Ollama first |
| "model not found" | `ollama pull llama3.2` once |
| Forgot system message → rambling answers | always set a system role for data tasks |
| `KeyError: 'message'` | check `resp` — it's a dict; print the whole reply to see the shape |
| Answer changes between runs | sampling; set `options={"temperature": 0.2}` |
| Sending the whole dataframe in a prompt | model context can't hold it; send schema + samples instead |

## 7. Limitations

- **No memory across calls** — you must re-send context each time; the
  `messages` list grows with the conversation.
- **Latency** — local inference is slower than a cloud API; long loops over
  many questions take time.
- **Context window** — a few thousand tokens; big data summaries don't fit;
  send aggregated facts, not rows.
- **Non-determinism** — same prompt can give different answers; fix
  temperature and log everything for reproducibility.
- **Not a database** — the model answers from the prompt you built; if the
  prompt lacks facts, the answer is guesswork.

## 8. Responsible AI considerations

- **Build privacy into the code** — the Python path keeps data local; never
  swap in a cloud client for the same prompts on real data without policy
  review.
- **Log every call** — question, model, temperature, reply, verification:
  this is your reproducibility + disclosure record.
- **Verify before you trust** — the loop example above demonstrates why:
  fluent replies are drafts, not findings.
- **Beware prompt injection from data** — if you embed dataset text into a
  prompt, that text can steer the model; treat it as untrusted input.

## 9. Assessment questions

**Q1.** Why must you re-send the conversation history on every `ollama.chat`
call? *(CLO-3 · Understand · Easy)*
**Answer:** The model has no memory — the `messages` list is the entire
state; each call is stateless inference over what you send.

**Q2.** The same question returns different answers on two runs. What causes
this and how do you make the step reproducible? *(CLO-3 · Analyze · Medium)*
**Answer:** token sampling is random. Set a low temperature, and log the
exact model, prompt, and options with the output so the step can be
re-run/audited.

**Q3.** Write the two lines of code that send a system+user message to
llama3.2 and print the reply. *(CLO-3 · Apply · Medium)*
**Answer:**
```python
resp = ollama.chat(model="llama3.2", messages=[{"role": "system", "content": s},
                                               {"role": "user", "content": u}])
print(resp["message"]["content"])
```

**Q4.** Why is "send the whole CSV in the prompt" a bad idea even with a
local model? *(CLO-3 · Evaluate · Medium)*
**Answer:** the context window can't hold it (truncation), and the model
won't reliably compute over thousands of rows — summarize/aggregate first,
then ask.