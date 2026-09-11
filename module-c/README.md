# Module C — AI-Assisted Data Science (Teaching Pack)

Complete teachable material for the modern AI-assisted data science module
(CLO-3), **11 topics**, each with the same nine sections:

1. Beginner explanation — the idea in plain language
2. Conceptual explanation — how it actually works, WHY before HOW
3. Simple diagram — ASCII, printable, board-drawable
4. Python examples — executable, guarded for missing tools
5. Practical exercise — concrete task with a real dataset
6. Common errors — what students hit and the fix
7. Limitations — honest boundaries of each tool
8. Responsible AI considerations — privacy, verification, disclosure
9. Assessment questions — with answers, tagged in the standard format `**CLO-3 · Apply · Medium**`

## Topic index

| # | Topic | Maps to | Notebook | Lab |
|---|---|---|---|---|
| 01 | PandasAI — natural language over dataframes | Session 26 | `course-notebooks/14-pandasai.ipynb` | Lab 26 |
| 02 | LLM fundamentals | Session 25 | `course-notebooks/15-llm-fundamentals.ipynb` | Lab 25 |
| 03 | Prompt engineering | Session 25 | `course-notebooks/15-llm-fundamentals.ipynb` | Lab 25 |
| 04 | Ollama — local models | Session 27 | `course-notebooks/16-ollama-with-python.ipynb` | Lab 27 |
| 05 | Using Ollama from Python | Session 27 | `course-notebooks/16-ollama-with-python.ipynb` | Lab 27 |
| 06 | Structured outputs (JSON) | Session 28 | `course-notebooks/17-tool-and-function-calling.ipynb` | Lab 28 |
| 07 | Tool/function calling | Session 28 | `course-notebooks/17-tool-and-function-calling.ipynb` | Lab 28 |
| 08 | AI agents | Session 28 | `course-notebooks/18-ai-agents.ipynb` | Lab 28 |
| 09 | n8n automation | Session 29 | `course-notebooks/19-n8n-workflows.ipynb` | Lab 29 |
| 10 | AI-assisted data science workflows | Sessions 23–24, 25, 30 | `course-notebooks/20-end-to-end-data-science-project.ipynb` | Labs 24, 30 |
| 11 | AI in a Streamlit application | Session 28 workshop | Assignment 2 app + project app | Lab 28 |

## The five things students must understand (woven through every topic)

1. **Hallucinations** — an LLM does not know facts; it predicts text. Anything
   it says about your data must be checked against the data.
2. **Generated-code verification** — AI-generated pandas/ML code is *a draft,
   not a result*. Read it, run it, and verify one number by hand (the
   course verification protocol).
3. **Data privacy** — a cloud LLM sees whatever you paste. Local models
   (Ollama) keep data on your machine. Never paste private data into a
   public tool.
4. **Prompt limitations** — a better prompt fixes phrasing, not wrong data or
   missing context. No prompt turns a weak model into a calculator.
5. **Reproducibility & responsible AI** — record tool + version + prompt +
   output + verification (the audit log), disclose every AI-assisted step,
   and treat the model as a suggestion engine you are accountable for.

## The verification protocol (used in topics 01, 03, 05, 06, 10, 11)

Every AI-assisted answer gets three checks:

1. **Read the generated code/prompt** — does it ask the right question?
2. **Verify by hand** — compute one number yourself with pandas.
3. **Log it** — question, tool + version, prompt, output, verification.

A plausible wrong answer is worse than no answer. The audit catches it.

## Setup (once per machine)

```bash
pip install pandasai langchain-community
# Ollama: install from https://ollama.com, then:
ollama pull llama3.2
# n8n (optional): npx n8n        # then open http://localhost:5678
```

All LLM-dependent code below is **guarded** — if the tool isn't installed or
the Ollama server isn't running, the code prints a message and continues, so
examples are safe to paste into a notebook or lecture demo.