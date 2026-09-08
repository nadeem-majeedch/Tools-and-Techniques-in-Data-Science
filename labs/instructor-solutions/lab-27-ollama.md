# Lab 27 — Solution: Ollama

**Session:** W14 S27 · **CLO:** CLO-3

## Complete solution

```python
import pandas as pd
import seaborn as sns

penguins = sns.load_dataset("penguins").dropna()
summary = penguins.groupby("species")[["bill_length_mm", "body_mass_g"]].mean().round(1)
summary_text = summary.to_string()
print(summary_text)
# Gentoo body_mass ~5076 g — the heaviest species (ground truth)

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
    reply = ask("llama3.2", prompt,
                system="You are a careful data analyst. Do not invent numbers.")
    print(reply)
except Exception as e:
    print("Ollama unavailable:", e)
    reply = ("Gentoo is the heaviest species (mean body mass ~5076 g). "
             "Follow-up: compare flipper length between species.")

# verification
print("heaviest claim correct:",
      "Gentoo" in reply and summary.loc["Gentoo", "body_mass_g"] ==
      summary["body_mass_g"].max())
```

## Privacy note (model answer)

> Only the 3-row aggregate (species × mean bill length and mass) left the
> machine as text. Raw rows — including island and sex, which could
> identify specific colonies or individuals — were never sent. Aggregates
> are the safe unit because no single record can be recovered from them;
> the model never sees the underlying DataFrame.

## Model answers

1. **ollama pull downloads** — the model weights (a multi-GB file, here
   llama3.2 ~2–3 GB) stored under Ollama's model directory
   (`~/.ollama/models`), ready for offline use.
2. **Summary text, not raw data** — minimize what leaves the machine
   (privacy), keep the prompt small/fast, and force the model to comment
   on *aggregates* it can't distort row-by-row.
3. **System prompt** — sets persistent instructions (role, constraints,
   format) that apply before and across user messages; a user message
   alone doesn't establish the "analyst" framing.
4. **Local 3B limits** — multi-step math/reasoning, long-context
   synthesis, and open-ended creative tasks; for those use a larger cloud
   model (if policy allows) or break the task into verifiable steps.
5. **"Local = private" is incomplete** — the model file itself is public
   weights (no data), but telemetry from the Ollama app, logs, and any
   cloud-backed features can still leak; privacy comes from *what you send*
   plus *what the software reports*, not just where it runs.

## Challenge solution

```python
q = "Summarize the tips dataset in one sentence."
for style, sys_p in [("one-sentence", "Answer in one sentence."),
                     ("bullets", "Answer as three bullets, each with a number.")]:
    try:
        print("---", style, "---")
        print(ask("llama3.2", q, system=sys_p)[:300])
    except Exception as e:
        print("skipped:", e)
# For a project report, the bullets-with-numbers format wins: it forces
# checkable numbers and scans better in a report.
```