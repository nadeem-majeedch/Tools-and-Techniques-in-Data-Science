# Module C · Topic 02 — LLM Fundamentals

**CLO-3 · Maps to:** Session 25 · Notebook 15 · Lab 25 · **Level:** Beginner

---

## 1. Beginner explanation

A Large Language Model (LLM) is a program that **predicts the next word**.
Show it "The capital of France is", and it completes: "Paris". That's the
entire trick — repeated billions of times, with a giant neural network
trained on an enormous amount of text. It has **no database of facts** and
no ability to compute. It has *patterns*. When you ask it something, it is
not looking anything up; it is generating the most *plausible-sounding*
continuation. That's why it can sound brilliant and be wrong with the same
confidence — a behaviour called **hallucination**.

## 2. Conceptual explanation (the WHY)

Internally, text is split into **tokens** (roughly word pieces: "data" might
be one token, "sci" + "ence" two). The model assigns a **probability to
every possible next token** based on the context so far — a softmax over its
whole vocabulary. Generating text = sampling from those probabilities, one
token at a time.

Three knobs matter for data work:

- **Temperature** (0–1+): low → always pick the most probable token
  (predictable, dry); high → pick unlikely tokens (creative, sloppy).
  For data analysis: low (0–0.3).
- **System prompt**: instructions that set the role and rules for the whole
  conversation, separate from the user's message.
- **Context window**: how many tokens the model can "see" at once. Whole
  dataframes do not fit — that's why you send schema and samples, not rows.

The model's knowledge is frozen at training time and stored as **weights**,
not retrievable facts. It cannot count reliably, cannot do exact arithmetic,
and will confidently answer questions whose answer it never learned.
Anything factual or numerical it says must be verified.

## 3. Simple diagram

```text
 "The capital of       tokens: [The][ capital][ of]
  France is"
        │
        ▼
  ┌───────────────────────────┐
  │ Neural network (weights)  │   trained once on billions of words
  └────────────┬──────────────┘
               │ assigns probability to EVERY next token
               ▼
   "Paris"   0.82  ← most likely → chosen (low temperature)
   "a"       0.07
   "the"     0.04
   "Berlin"  0.01  ← plausible-sounding, WRONG, but possible!
   ...        ...
        │
        ▼
   Output: "Paris"   -- and the process repeats for the next token
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

    try:
        # system message sets rules; user message asks the task
        messages = [
            {"role": "system",
             "content": "You are a careful data assistant. If you are not "
                        "sure, say 'I am not sure' instead of guessing."},
            {"role": "user",
             "content": "Compute 123 * 456 exactly."},
        ]
        reply = ollama.chat(model="llama3.2", messages=messages)
        print("MODEL SAYS:", reply["message"]["content"])
        # Always compare against ground truth:
        print("PYTHON SAYS:", 123 * 456)
    except Exception as e:
        print("Ollama not running — start it and pull llama3.2:", e)
else:
    print("ollama package not installed:  pip install ollama")
```

The point of the example: the model may or may not get the arithmetic right.
**Never let a model be your calculator.**

## 5. Practical exercise (20 min)

1. In a notebook, ask `ollama.chat` the same arithmetic question 3 times and
   compare answers (LLMs are not deterministic — sampling!).
2. Ask a factual question about *this course's* schedule: *"When is the
   midterm?"* — the model has never seen your syllabus. Observe what it
   invents. This is the cleanest hallucination demo possible.
3. Repeat with a system prompt "If unsure, say you don't know" and note the
   difference in behaviour (not a guarantee — just better behaviour).
4. Write one paragraph: *where can an LLM help your data workflow, and where
   must it never be the final authority?*

## 6. Common errors

| Error | Why it happens | Fix |
|---|---|---|
| "The model got my facts wrong" | treating it as a fact database | it predicts text; verify facts externally |
| "The answer changes every run" | sampling is random | set temperature low; treat output as draft |
| "It can't do my arithmetic" | not a calculator | compute with Python; use the model only for phrasing/planning |
| "It made up a column name" | hallucinated schema | give it real column names in the prompt |
| "It ignored my instructions" | vague or buried system prompt | make the system prompt short, specific, first |

## 7. Limitations

- **Hallucination**: fluent, confident, wrong. No built-in "I checked that".
- **No exact computation**: arithmetic, counting, and comparisons are unreliable.
- **Stale knowledge**: training data has a cutoff; course-specific facts are absent.
- **Context limits**: cannot "read" whole datasets; only small excerpts fit.
- **No source memory**: it does not remember where it learned something, so
  it cannot cite its own claims.

## 8. Responsible AI considerations

- **Verification culture**: every model claim about data is a *hypothesis*,
  checked against actual data before use.
- **Privacy**: anything you paste into a cloud LLM leaves your machine.
  Course policy: local Ollama for real data; never paste grades, IDs, or
  personal data.
- **Honest disclosure**: the report/README lists every LLM-assisted step
  (tool, version, prompt, how output was verified).
- **Confidence is not accuracy**: teach students to distrust fluent
  certainty — the model's confidence has no relationship to correctness.

## 9. Assessment questions

**Q1.** In one sentence, what does an LLM actually do when you ask it a
question? *(CLO-3 · Understand · Easy)*
**Answer:** It predicts the most probable next token, repeatedly — it does
not look up facts or compute.

**Q2.** Why is an LLM's confident answer about your course's exam date likely
wrong? *(CLO-3 · Analyze · Medium)*
**Answer:** The model never saw your syllabus; its knowledge is frozen at
training time, so anything course-specific is generated (hallucinated) text
that only *sounds* plausible.

**Q3.** Your analysis must be reproducible. A teammate re-ran the LLM step
and got a different answer. What caused it and what do you do? *(CLO-3 ·
Evaluate · Medium)*
**Answer:** Sampling is non-deterministic. Fix temperature (low), save the
prompt + model + version + output in the audit log, and verify the answer
against data by hand so the result doesn't depend on a lucky sample.

**Q4.** Give one task an LLM is genuinely good at in a data workflow and one
task it must never do alone. *(CLO-3 · Evaluate · Medium)*
**Answer:** Good: translating a question into a first draft of pandas code,
explaining an error, drafting a report section. Never alone: computing
final numbers or making a decision — those must be verified by code/data.