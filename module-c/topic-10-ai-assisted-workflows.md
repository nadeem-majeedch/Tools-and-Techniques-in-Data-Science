# Module C · Topic 10 — AI-Assisted Data Science Workflows

**CLO-3 · Maps to:** Sessions 23–24, 25, 30 · Notebook 20 · Labs 24, 30 ·
**Level:** Beginner→Intermediate

---

## 1. Beginner explanation

An AI-assisted workflow is a normal data science pipeline (question →
acquire → clean → EDA → model → report) where an LLM helps at *specific
steps* — drafting code, explaining an error, summarizing findings — and a
human verifies every help it gives. The AI is a **tool inside the pipeline**,
not the pipeline itself. The whole trick of this topic is the discipline
around it: you decide *where* the AI helps, you record *what you asked*, and
you check *everything it produced* against the data. That turns "I let
ChatGPT do my homework" into "I ran a documented, verifiable workflow."

## 2. Conceptual explanation (the WHY)

The core idea is the **verification protocol** — three checks for every
AI-assisted step:

1. **Read** the generated code/prompt — does it do what you asked?
2. **Verify** by hand — compute one number yourself; run the code on real
   data.
3. **Log** — question, tool + version, prompt, output, verdict (✓/✗).

Why these three? Because every failure mode in Module C is caught by one of
them: hallucinations (check 2), mistranslated questions (check 1),
unreproducible steps (check 3). A "plausible wrong answer" is the worst
outcome, and the protocol exists specifically to make it visible.

The workflow pattern that works in practice:

| Pipeline step | AI can help | AI must NOT decide |
|---|---|---|
| Question → plan | brainstorm, outline steps | the actual question/goal |
| Acquire | draft the fetch script | which source, license check |
| Clean | draft the cleaning code | the *reason* for dropping vs filling |
| EDA | suggest what to explore | whether a finding is real |
| Model | draft sklearn code | model choice rationale, evaluation honesty |
| Report | draft prose | claims about the data |
| Every step | explain errors | the final numbers |

The discipline rule: **AI drafts, you decide, data verifies, log records.**

## 3. Simple diagram

```text
  QUESTION
     │
     ▼
  ┌─────────────────────────────────────────────┐
  │  pipeline steps (acquire → clean → EDA →    │
  │  model → report)                            │
  │                                             │
  │   at ANY step:  ┌────────────────────┐      │
  │   AI drafts ───►│ 1. READ the output │      │
  │                 │ 2. VERIFY vs data  │      │
  │                 │ 3. LOG it          │      │
  │                 └─────────┬──────────┘      │
  │                           │ pass?           │
  │                    ┌──────┴──────┐          │
  │                    │ yes → next  │          │
  │                    │ no  → fix   │          │
  │                    └─────────────┘          │
  └─────────────────────────────────────────────┘
     │
     ▼
  REPORT (disclosed AI use + audit log attached)
```

## 4. Python examples

```python
# The audit log — the reproducibility artifact of every AI-assisted step
import csv, datetime

LOG_FILE = "ai_audit_log.csv"

def log_step(step, question, tool, prompt, output, verdict):
    """Append one AI-assisted step to the audit log."""
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.date.today().isoformat(),
                         step, question, tool, prompt,
                         output.replace("\n", " ")[:200], verdict])

# Example: log a PandasAI-assisted EDA question
log_step(
    step="EDA",
    question="mean tip by day",
    tool="PandasAI 3.x + Ollama llama3.2",
    prompt="mean tip by day, table output",
    output="Sat 2.99 ...",          # what the tool returned
    verdict="PASS — matches groupby mean",   # after hand-check
)
print("logged to", LOG_FILE)
```

```python
# The workflow skeleton with AI at exactly two steps, verified both times
import pandas as pd
import seaborn as sns

tips = sns.load_dataset("tips")

# Step 1 — AI drafts cleaning code (then YOU run + verify it)
ai_draft = """# draft from model: drop rows with missing tip"""
print("AI DRAFT:", ai_draft)
clean = tips.dropna(subset=["tip"])          # you chose this line, verified
print("rows before/after:", len(tips), len(clean))

# Step 2 — AI suggests a plot; you build + interpret it
print("AI SUGGESTION: boxplot of tip by day")
import matplotlib.pyplot as plt
clean.boxplot(column="tip", by="day")
plt.title("Tip distribution by day (human-made, human-labelled)")
plt.tight_layout()
plt.show()
# The interpretation in the report is YOURS, checked against the figure.
```

## 5. Practical exercise (30 min)

Dataset: `sns.load_dataset("titanic")`.

1. Write the `log_step` helper and initialize `ai_audit_log.csv` with a
   header row.
2. Use an LLM (Ollama) to draft a cleaning snippet for missing values in
   `age`. Read it. Run it. Log the step with verdict PASS/FAIL.
3. Use PandasAI (or a prompted LLM) for one EDA question. Verify by hand.
   Log it.
4. Use the LLM to draft a two-line *interpretation* of the survival-by-class
   plot — then rewrite the interpretation yourself after checking the
   numbers (this is the "AI drafts, you decide" exercise).
5. Final deliverable: a notebook section titled **AI-assisted steps** with
   the audit log table and a one-paragraph reflection on which steps AI
   genuinely saved time on.

## 6. Common errors

| Error | Fix |
|---|---|
| "I let the AI write the whole analysis" | restrict AI to drafts at defined steps; you run, verify, and decide |
| Verifying nothing | run the verification protocol; one hand-computed number per AI step |
| No log | an unlogged AI step is an undisclosed one — always log |
| Trusting the model's interpretation | interpretations are generated text; check them against the data |
| Re-running gives different results | log model + version + temperature; pin the environment |

## 7. Limitations

- **The bottleneck is human** — the protocol's quality is limited by your
  ability to read code and verify numbers; that's why the course teaches
  pandas first.
- **Slow for tiny tasks** — writing the log and verifying is slower than just
  doing a trivial step by hand; use AI where it genuinely saves time.
- **Model ceiling** — small local models draft decent one-liners and stumble
  on multi-step logic; keep drafts small.
- **No magic productivity** — the time saved drafting is spent verifying;
  the honest benefit is *coverage of more approaches*, not free speed.

## 8. Responsible AI considerations

- **Disclosure is non-negotiable** — every AI-assisted step is logged and
  disclosed in the README/report; undisclosed use is a policy violation.
- **Verification is the accountability mechanism** — the log answers "who is
  responsible for this number?" — always the human.
- **Privacy at every step** — real/private data goes through local tools
  only; prompts never contain personal data.
- **Ethics reflection** — the report includes a short reflection on bias,
  hallucination risk, and what the model could *not* have told you.

## 9. Assessment questions

**Q1.** List the three checks of the verification protocol. *(CLO-3 ·
Understand · Easy)*
**Answer:** read the generated code/prompt; verify one number by hand
against the data; log the step (question, tool, version, prompt, output,
verdict).

**Q2.** Why is a logged, verified AI draft more valuable than a perfect
unverified answer? **CLO-3 · Evaluate · Medium**
**Answer:** the logged one is reproducible, auditable, and attributable —
you can prove where the number came from; an unverified answer can be
plausibly wrong and no one can tell.

**Q3.** Your model drafts a cleaning line that drops rows with missing
`age`. Your teammate wants to use it directly. What do you require first?
**CLO-3 · Evaluate · Medium**
**Answer:** a *reason* for the drop (missingness pattern, proportion), a
hand-check of how many rows are lost, and a logged entry — the model's
suggestion is a draft, not a decision.

**Q4.** A report claims "AI did the whole project". Based on this topic, why
is that sentence itself a red flag? **CLO-3 · Evaluate · Medium**
**Answer:** in a proper AI-assisted workflow the human runs, verifies, and
decides at every step; "the AI did it" means no verification protocol was
applied — which is exactly the failure mode the protocol prevents.