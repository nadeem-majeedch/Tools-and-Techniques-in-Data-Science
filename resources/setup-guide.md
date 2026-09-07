# Setup Guide

Goal: a working environment for all 32 sessions — Python + Jupyter for Modules A–B
and Ollama + n8n for Module C. Do this once, at the start of the course.

## 1. Install Python

1. Install **Python 3.11 or newer** from https://www.python.org/downloads/
   (Windows: check *"Add python.exe to PATH"* during install).
2. Verify in a terminal:
   ```bash
   python --version
   ```
   (On macOS/Linux use `python3` if `python` is not defined.)

## 2. Create a virtual environment

From the course repository root:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate
```

Your prompt should now show `(.venv)`.

## 3. Install Python packages

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs NumPy, Pandas, Matplotlib, Seaborn, scikit-learn, Jupyter,
requests, PandasAI, and the Ollama Python client.

## 4. Launch Jupyter

```bash
jupyter lab
```

Create a test notebook, run `import numpy, pandas, matplotlib, seaborn, sklearn`,
and save it — if all imports succeed, the core stack works.

## 5. Set up Git & GitHub

1. Create a free account at https://github.com.
2. Configure Git once:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```
3. Authentication: use a Personal Access Token or SSH key
   (https://docs.github.com/en/authentication). SSH is recommended:
   ```bash
   ssh-keygen -t ed25519 -C "you@example.com"
   ```
   and add the public key under GitHub → Settings → SSH and GPG keys.

## 6. Install Ollama (Module C, Week 14)

1. Download from https://ollama.com and install.
2. Verify and pull a small model:
   ```bash
   ollama --version
   ollama pull llama3.2
   ```
3. Test from Python (inside your `.venv`):
   ```python
   import ollama
   print(ollama.chat(model="llama3.2", messages=[{"role": "user", "content": "Hi"}])["message"]["content"])
   ```
   Any model from https://ollama.com/library works; `llama3.2` is a good default.

## 7. Install n8n (Module C, Week 15)

Option A — via npx (Node.js required; install from https://nodejs.org):
```bash
npx n8n
```
Then open http://localhost:5678.

Option B — via Docker:
```bash
docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
```

Local runtime data is stored outside the repository (see `.gitignore`).

## 8. Verify everything

Run this checklist and tick each item off:

- [ ] `python --version` → 3.11+
- [ ] `pip install -r requirements.txt` completes
- [ ] Jupyter Lab opens and a test notebook runs with all imports
- [ ] `git push` works from a test repository
- [ ] `ollama pull llama3.2` completes and the Python chat test prints a reply
- [ ] n8n opens at http://localhost:5678

## Troubleshooting

| Problem | Fix |
|---|---|
| `pip` not found | Activate the venv first (step 2) |
| Jupyter kernel uses wrong Python | `pip install ipykernel` and restart the kernel |
| Ollama not found in Python | Restart the terminal so PATH updates, reinstall `ollama` package |
| Port 5678 busy | Stop other n8n instances; `npx n8n` keeps data in `~/.n8n` |