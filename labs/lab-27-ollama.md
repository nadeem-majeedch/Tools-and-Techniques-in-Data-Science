# Lab 27 — Ollama: Local Models from Python

**Session:** Week 14 · Session 27 · 90 min
**CLO:** CLO-3
**Difficulty:** Advanced

## Learning objectives

By the end of this lab you can:

1. Pull, list, and chat with a local model via the terminal and Python.
2. Use system prompts to steer output format.
3. Compare local vs. cloud trade-offs for a concrete task.
4. Log prompts + answers + verification (the course AI protocol).

## Problem statement

Your project must not send private data to the cloud. This lab proves the
local path works: a Python helper that chats with a local Ollama model, a
structured task (turn findings text into a bullet summary), and a privacy
note. If Ollama is not installed/running, you still complete the helper and
the log using the offline fallback described below.

## Dataset requirements

Seaborn built-in `penguins` (dropna). You will send **aggregates only** —
never raw rows with identifiers.

## Step-by-step tasks

1. **Terminal check (outside the notebook):** `ollama list` and
   `ollama pull llama3.2` if needed. Record what `ollama list` shows.
2. **Helper:** write `ask(model, question, system="")` that builds the
   messages list, calls `ollama.chat`, and returns the reply text (guard
   the import and the call — see starter code).
3. **Aggregate first:** compute `summary = penguins.groupby("species")
   [["bill_length_mm", "body_mass_g"]].mean().round(1)` and convert to
   text with `summary.to_string()`. This text — not the DataFrame — is
   what the model sees.
4. **Task:** ask the model (system: "You are a careful data analyst. Do not
   invent numbers.") to: state the heaviest species and one follow-up
   question. Print the reply.
5. **Verify:** check the reply's claim against the summary yourself (e.g.,
   is the heaviest species it names actually the max?). Mark ✓/✗.
6. **Privacy note (markdown):** 3 sentences — what data left your machine,
   what stayed, and why aggregates are the safe unit to send.
7. **Offline fallback:** if Ollama is unavailable, write the *expected
   structure* of the reply in a comment and complete steps 5–6 using the
   provided sample reply below.

## Starter code

```python
import pandas as pd
import seaborn as sns

penguins = sns.load_dataset("penguins").dropna()
summary = penguins.groupby("species")[["bill_length_mm", "body_mass_g"]].mean().round(1)
summary_text = summary.to_string()
print(summary_text)
```

```python
# guarded helper — run this even without Ollama (it prints a message)
try:
    import ollama

    def ask(model, question, system=""):
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": question})
        return ollama.chat(model=model, messages=messages)["message"]["content"]

    prompt = ("Dataset summary (means by species):\n" + summary_text +
              "\nWhich species is heaviest? Suggest one follow-up analysis.")
    reply = ask("llama3.2", prompt, system="You are a careful data analyst. Do not invent numbers.")
    print(reply)
except Exception as e:
    print("Ollama unavailable:", e)
    print("-> offline fallback (sample reply):")
    print("Gentoo is the heaviest species (mean body mass ~5076 g). "
          "Follow-up: compare flipper length between species.")
```

```text
# Provided sample reply (use for verification steps when offline)
"Gentoo is the heaviest species (mean body mass ~5076 g). Follow-up:
 compare flipper length between species."
```

## Expected output

- `ollama list` output recorded (or "not installed" noted).
- Helper `ask` defined with guard; prompt includes the summary text and a
  "do not invent numbers" system prompt.
- Reply printed; heaviest-species claim verified ✓ against the summary
  (Gentoo ≈ 5076 g is correct).
- Privacy note: only the 3-row aggregate left the machine; raw rows never
  sent.
- Everything above reproducible with or without Ollama running.

## Questions

1. What exactly does `ollama pull llama3.2` download, and where does it
  live?
2. Why send `summary.to_string()` instead of the raw DataFrame?
3. What does a system prompt change compared to only a user message?
4. Name one task where the local 3B model is likely to fail — and what you
   would do instead.
5. "It runs on my machine, so it is private." What is wrong with that
   statement? (Think: logs, telemetry, the model file itself.)

## Challenge task

Compare two system prompts on the same question (e.g., "one sentence" vs.
"three bullet points, each with a number") and record both replies in your
AI log. Then answer: which format would you paste into a project report,
and why? Add both prompts and both replies to a markdown log cell.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Terminal steps recorded | 3 | ollama list / pull |
| `ask` helper + guard | 4 | correct messages structure |
| Aggregates-only pipeline | 4 | summary text sent, not rows |
| Task + verification | 5 | claim checked against data |
| Privacy note | 3 | 3 sentences, correct |
| Offline fallback works | 3 | lab completable without Ollama |
| Answers to questions | 4 | Q2, Q3, Q5 correct |
| Challenge: prompt comparison | 4 | both replies logged + choice |
| **Total** | **30** | |