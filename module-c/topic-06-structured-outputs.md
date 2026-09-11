# Module C · Topic 06 — Structured Outputs (Getting JSON Out of an LLM)

**CLO-3 · Maps to:** Session 28 · Notebook 17 · Lab 28 · **Level:** Beginner→Intermediate

---

## 1. Beginner explanation

LLMs reply in *free text* — great for chatting, useless for code. When your
program needs the answer ("the best day was Friday, mean tip 3.10"), free
text means parsing prose: fragile and error-prone. The fix is to force the
model to reply in a **structure**: JSON. Ollama has a `format="json"` mode
that makes the model emit valid JSON (a dict you can load with
`json.loads`). Now the model's answer is a *data object* your code can use —
and that is the bridge to tool calling and agents (topics 07–08).

## 2. Conceptual explanation (the WHY)

Under the hood, `format="json"` constrains the model's token sampling to
tokens that keep the output parseable as JSON — it biases the decoder
towards JSON-legal continuations. It is **not** a guarantee the JSON
*semantically* matches what you asked for, only that it *parses*. The JSON
could parse perfectly and still contain the wrong day, a hallucinated
number, or missing keys. So the pipeline is always:

1. Force JSON (parseable by construction, mostly).
2. Load it with `json.loads` — if that fails, you have a real error to handle.
3. **Validate the schema** — check the keys you expect exist and values have
   the right types.
4. **Validate the values** — is the day actually one of the days in the data?
   Is the number plausible? This is where hallucination gets caught.

Structured output turns "trust the model's prose" into "treat the model's
answer as untrusted data" — exactly the right mental model.

## 3. Simple diagram

```text
 prompt: "Return JSON: {\"best_day\": ..., \"mean_tip\": ...}"
        │
        ▼
  LLM with format="json"  ──►  text that parses as JSON
        │
        ▼
  json.loads(...)
        │
        ▼
  {"best_day": "Sat", "mean_tip": 3.03}     ← parses fine
        │
        ▼
  VALIDATE: "Sat" in df["day"]?  ✓      ← semantics check
            3.03 == groupby mean?  ✗ ← CATCHES HALLUCINATION
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

if module_available("ollama"):
    import ollama

    try:
        # Step 1: force JSON output
        resp = ollama.chat(
            model="llama3.2",
            messages=[
                {"role": "system",
                 "content": "You answer data questions with JSON only."},
                {"role": "user",
                 "content": "DataFrame tips, columns: total_bill, tip, day. "
                            "Which day has the highest total tips and what is "
                            "the mean tip that day? Return JSON with keys "
                            "best_day and mean_tip."},
            ],
            format="json",              # <-- force valid JSON
        )
        text = resp["message"]["content"]
        print("RAW:", text)

        # Step 2: parse
        answer = json.loads(text)
        print("PARSED:", answer)

        # Step 3: validate schema + values
        assert "best_day" in answer and "mean_tip" in answer, "missing keys"
        assert isinstance(answer["mean_tip"], (int, float)), "wrong type"

        # Step 4: verify against real data
        import pandas as pd
        import seaborn as sns
        tips = sns.load_dataset("tips")
        truth = (tips.groupby("day")["tip"].sum().idxmax())
        print("MODEL best_day:", answer["best_day"],
              "| DATA best_day:", truth)
    except Exception as e:
        print("Ollama not running:", e)
else:
    print("ollama package not installed:  pip install ollama")
```

Safe parsing — never crash on a bad reply:

```python
import json

def parse_json_safely(text):
    """Try to parse; return None if the model broke the format."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None

# Use it:
parsed = parse_json_safely('{"best_day": "Sat", "mean_tip": 3.03}')
print(parsed)

# A model can also wrap JSON in prose or code fences — strip them first:
text = '```json\n{"best_day": "Sat"}\n```'
clean = text.strip().removeprefix("```json").removesuffix("```").strip()
print(json.loads(clean))
```

## 5. Practical exercise (25 min)

Dataset: `sns.load_dataset("titanic")`.

1. Ask for JSON with keys `survival_rate` and `most_dangerous_class`
   (use `format="json"`).
2. Parse it with `json.loads` and print the dict.
3. Add the schema check (`assert` the keys exist) — then break the model
   intentionally with a vague prompt and watch the validation catch it.
4. Verify both values against real pandas output
   (`titanic["survived"].mean()`, `groupby("class")["survived"].mean()`).
5. Write a `parse_json_safely` helper and use it in your notebook's audit log.

## 6. Common errors

| Error | Fix |
|---|---|
| `json.JSONDecodeError` | model wrapped in prose/code fences — strip first; or retry once |
| Parses but wrong keys | validate schema with asserts; re-prompt with explicit key names |
| Parses but wrong values | semantics check against real data — this is the hallucination catch |
| Numbers as strings ("3.03") | cast types after parsing, then validate with `isinstance` |
| Forgot `format="json"` | free-text answers are not guaranteed parseable |

## 7. Limitations

- **Format ≠ correctness** — valid JSON can still be factually wrong; the
  value checks are on you.
- **Small models break format** — tiny models sometimes emit invalid JSON
  even with `format="json"`; build the retry/skip path in.
- **Schema drift** — models may invent extra keys or rename yours; validate
  what you need, ignore the rest, don't trust the rest.
- **No nested guarantees** — `format="json"` helps top-level structure;
  deeply nested/complex schemas are less reliable.
- **Slower, more tokens** — JSON output costs tokens and can be slower than a
  one-word answer.

## 8. Responsible AI considerations

- **Untrusted-data mindset** — a parsed JSON answer is *input to your code*,
  not a fact; validate before it influences anything.
- **Never auto-execute** — if the structured output contains code or a tool
  name, treat it as untrusted; the agent loop (topic 08) must whitelist
  tools, never let the model pick arbitrary functions.
- **Log both raw and parsed** — the raw text can hold injection content;
  keep it in the audit log.
- **Failure handling is a safety feature** — refusing a malformed reply
  loudly beats silently using a plausible wrong value.

## 9. Assessment questions

**Q1.** What exactly does Ollama's `format="json"` guarantee? *(CLO-3 ·
Understand · Easy)*
**Answer:** That the output is parseable JSON (approximately) — it does not
guarantee the content is correct or matches your requested keys.

**Q2.** The model returns `{"best_day": "Saturday", "mean_tip": "3.03"}`.
It parses fine. List the two validation problems. *(CLO-3 · Analyze ·
Medium)*
**Answer:** (1) type: `mean_tip` is a string, not a number; (2) value/schema:
"Saturday" is not a value in the data's `day` column (data has Sat) and the
number must be checked against the real aggregation.

**Q3.** Write the three lines that parse a JSON reply and handle a malformed
one gracefully. **CLO-3 · Apply · Medium**
**Answer:**
```python
try:
    answer = json.loads(text)
except json.JSONDecodeError:
    answer = None   # handle: log, retry once, or skip
```

**Q4.** Why must structured output be validated against the real data and not
just parsed? **CLO-3 · Evaluate · Medium**
**Answer:** parsing only proves the text is JSON; the values are still
generated guesses — validating against the data is the only check that
catches hallucinated numbers before they enter your analysis.