# Module C · Topic 04 — Ollama: Local LLMs on Your Machine

**CLO-3 · Maps to:** Session 27 · Notebook 16 · Lab 27 · **Level:** Beginner

---

## 1. Beginner explanation

Ollama is a free program that runs LLMs **on your own computer**. You
download a model once (e.g. `llama3.2`), and from then on you can chat with
it offline, with no account, no subscription, and no data leaving your
machine. It is to ChatGPT roughly what running your own word processor is to
using a web one: less fancy, fully yours, and private. For a data course it
is the key that makes "AI-assisted" work on real, private datasets.

## 2. Conceptual explanation (the WHY)

Cloud LLMs (ChatGPT, Gemini) run on the provider's servers: your prompt
travels over the internet and their computers generate the reply. Ollama
inverts that — it downloads the model **weights** (the trained neural
network, a few GB) and runs inference locally using your CPU/GPU and RAM.

The trade-off is honest and important:

- **Local (Ollama)** — data stays on your machine; free; offline; model size
  limited by your RAM (practical models: 1–8 GB). Smaller models are weaker
  at hard reasoning.
- **Cloud** — frontier-scale models (much stronger), but your data leaves
  your machine and usage may cost money.

There is no "free lunch" either way: local models are *good enough for
introductory data work* — translating questions into pandas, explaining
errors, drafting text — and that is exactly what this course needs them for.
Ollama also speaks an OpenAI-compatible API, which is why the same Python
code style works for tool calling and agents (topics 06–08).

## 3. Simple diagram

```text
CLOUD MODEL                          LOCAL MODEL (Ollama)
┌──────────────┐                    ┌──────────────────────┐
│ provider     │                    │ YOUR computer        │
│ servers      │                    │                      │
│              │    your prompt     │  llama3.2 weights    │
│   LLM ◄──────┼──── over internet  │  (few GB, downloaded │
│              │                    │   once)              │
│   reply ─────┼──► you             │                      │
└──────────────┘                    │   LLM ◄── prompt     │
   data leaves your machine         │   reply ──► you      │
   (third party sees your data)     └──────────────────────┘
                                       data never leaves your machine
                                       free · offline · private
```

## 4. Terminal commands (the "Python" of this topic is the CLI)

```bash
# install Ollama from https://ollama.com, then:
ollama pull llama3.2        # download the model once (~2 GB)
ollama list                 # show downloaded models
ollama run llama3.2         # interactive chat; type /bye to exit
ollama ps                   # show models currently loaded in memory
```

```text
$ ollama run llama3.2
>>> What is the mean of [1, 2, 3, 4]?
The mean is 2.5.
>>> /bye
```

(Model output varies — and note the model *can* get simple arithmetic right
sometimes and wrong other times: verify, always.)

## 5. Practical exercise (20 min)

1. Install Ollama; run `ollama pull llama3.2` and note the download size.
2. Chat interactively: ask one factual question (observe hallucination risk),
   one pandas question ("write code to drop duplicate rows keeping the last")
   — paste the code and run it in a notebook to confirm it works.
3. Run `ollama ps` while chatting — see the model load into memory.
4. Pull a second, tiny model (`ollama pull llama3.2:1b` — note the tag syntax)
   and compare answer quality on the same question.
5. Write one line in your notes: *when would you choose local vs cloud?*

## 6. Common errors

| Error | Fix |
|---|---|
| `ollama: command not found` | Ollama not installed / not in PATH; reinstall or restart terminal |
| "model not found" | forgot to pull: `ollama pull llama3.2` |
| Slow first reply | model loading into RAM; it's normal — later replies are faster |
| Out of memory / crash | model too big for your RAM; use `llama3.2` or `llama3.2:1b` |
| Port 11434 already in use | another Ollama instance running; stop it or use a different port |

## 7. Limitations

- **Model quality ceiling** — local models are weaker than frontier cloud
  models on hard reasoning, long code, and exact math.
- **Hardware limits** — model size is bounded by RAM/VRAM; big models won't
  run (or will crawl) on modest laptops.
- **Still hallucinates** — local doesn't mean correct; everything about
  verification from topic 02 applies unchanged.
- **One-time download cost** — a few GB per model; needs disk space and a
  decent connection once.
- **No shared state** — the model only knows what you send it; no built-in
  access to the web or your files.

## 8. Responsible AI considerations

- **Privacy is the headline feature** — for real (non-public) data, prefer
  local models; that is a *policy choice*, not just convenience.
- **Local ≠ private automatically** — logs, screenshots, or shared drives can
  still leak; know where your data goes before and after the model.
- **Open weights ≠ open data** — the model was trained on other people's
  content; don't assume its output is freely reusable without checking.
- **Disclose** — using a local model is still an AI-assisted step: log tool,
  model, version, prompt, output.

## 9. Assessment questions

**Q1.** Name two advantages and two limitations of running an LLM locally
with Ollama. *(CLO-3 · Understand · Easy)*
**Answer:** Advantages: data stays on the machine, free, offline. Limits:
smaller/weaker models, bounded by RAM, still hallucinate.

**Q2.** A teammate wants to analyze student grades with ChatGPT by pasting
the CSV. Why is the local Ollama path the better choice here? *(CLO-3 ·
Evaluate · Medium)*
**Answer:** Grades are private data; pasting them to a cloud service sends
them to a third party. Ollama keeps them on the machine while still giving
an LLM assistant.

**Q3.** Your laptop has 8 GB RAM and `ollama run llama3.2` crashes. What do
you try? *(CLO-3 · Apply · Easy)*
**Answer:** use a smaller model (`llama3.2:1b`), close other applications, or
reduce the context used per request.

**Q4.** Ollama gave a confident but wrong answer about your dataset. Does
running it locally change how you handle that? *(CLO-3 · Evaluate · Medium)*
**Answer:** No — local only changes where the model runs, not how reliable
it is; the verification protocol still applies to every output.