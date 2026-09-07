# Content for notebook 08: Git/GitHub workflow.
CELLS = [
    ("md", """# 08 — Git & GitHub Workflow

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-1 / CLO-3 — reproducible, versioned work.

Git tracks the *history* of your project: every commit is a recoverable
checkpoint. GitHub hosts repositories and adds collaboration (pull requests,
issues). For this course, Git is also the submission channel — your commit
history shows your real workflow.

This notebook demonstrates Git **safely**: every command runs inside a
temporary folder, never in your course repository.

---
"""),("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Explain the three Git areas: working directory, staging, repository history.
2. Run the daily loop: `add` → `commit` → `push`.
3. Read history with `git log` and check state with `git status`.
4. Create and switch branches; understand pull requests.
5. Follow the course submission workflow (repo + meaningful commits).

---
"""),("md", """## Theory: the mental model

Three places for your files:

1. **Working directory** — the files you are editing.
2. **Staging area** — files selected for the next snapshot (`git add`).
3. **Repository history** — the snapshots themselves (`git commit`).

Pushing copies history to a **remote** (GitHub). The classic confusions:

- `git commit` does **not** upload to GitHub — `git push` does.
- `git add` selects; `git commit` photographs; `git push` uploads.

Write messages that explain **why**: `fix: drop duplicate rows before
aggregation` beats `update`.

---
"""),("code", """# First: confirm git is installed and see the version
import subprocess, sys

def git(*args, cwd=None):
    \"\"\"Run a git command and return (returncode, stdout, stderr).\"\"\"
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

code, out, err = git("--version")
print(out or err)

# Expected output (your version may differ):
#   git version 2.x.x
"""),
    ("md", """## Create a repository in a temp folder

Everything below happens in a throwaway directory — safe to experiment in.
In real life you would `git init` in your project folder (or `git clone` an
existing repo).

---
"""),("code", """import tempfile, os, pathlib

work = pathlib.Path(tempfile.mkdtemp(prefix="git-demo-"))
print("temp repo:", work)

# A small "analysis file" to version
(work / "analysis.py").write_text(
    "# step 1: load data\\nprint('loading...')\\n", encoding="utf-8"
)

code, out, err = git("init", cwd=work)
print(out or err)
code, out, err = git("status", cwd=work)
print(out)
"""),
    ("md", """## The daily loop: add, commit, log

---
"""),("code", """# Stage the file, then commit it
print(git("add", "analysis.py", cwd=work)[1] or "staged")
print(git("commit", "-m", "feat: start the analysis script", cwd=work)[1])

# Look at the history we just created
print(git("log", "--oneline", cwd=work)[1])

# Edit the file, and see Git notice the change
(work / "analysis.py").write_text(
    "# step 1: load data\\nprint('loading...')\\n\\n# step 2: clean\\nprint('cleaning...')\\n",
    encoding="utf-8",
)
print(git("status", "--short", cwd=work)[1])
"""),
    ("md", """## Committing changes: the discipline

Commit often, commit small, commit with meaning. One commit per completed
step beats one giant commit at midnight. `git diff` shows exactly what
changed before you commit — always glance at it.

---
"""),("code", """print(git("diff", cwd=work)[1])   # shows the added "step 2" lines

git("add", "analysis.py", cwd=work)
print(git("commit", "-m", "feat: add cleaning step", cwd=work)[1])
print(git("log", "--oneline", cwd=work)[1])

# Expected output:
#   diff --git a/analysis.py b/analysis.py
#   ... (the added cleaning lines)
#   [main <hash>] feat: add cleaning step
#   <hash2> feat: add cleaning step
#   <hash1> feat: start the analysis script
"""),
    ("md", """## Branches: parallel lines of work

A **branch** is an independent line of development — the default is `main`.
Create one to experiment safely; switch back when done. Merging brings the
branch back into `main`. On GitHub, a **pull request** proposes that merge
and is the place for review.

---
"""),("code", """# Create and switch to an experiment branch
print(git("switch", "-c", "feature/eda", cwd=work)[1])

# Make a change on the branch
(work / "eda.py").write_text("print('explore!')\\n", encoding="utf-8")
git("add", "eda.py", cwd=work)
print(git("commit", "-m", "feat: add eda scratch", cwd=work)[1])

# Switch back to main - eda.py is not there (it lives on the branch)
print(git("switch", "main", cwd=work)[1])
print("files on main:", sorted(p.name for p in work.iterdir() if p.is_file()))

# Merge the branch back
print(git("merge", "feature/eda", cwd=work)[1])
print("files after merge:", sorted(p.name for p in work.iterdir() if p.is_file()))
"""),
    ("md", """## The remote: pushing to GitHub

Pushing sends local history to GitHub. The commands (run once per repo on
GitHub, not executed here because they need your account):

```bash
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

And on a fresh machine, to get the repo:

```bash
git clone https://github.com/username/repo.git
```

Inside this course you will do this once in Session 4 and then push after
every lab. The submission is the **repository URL**; the instructor reads
your commit history.

---
"""),("code", """# What the remote step looks like (informational - not executed):
#   git remote add origin https://github.com/you/data-science-course.git
#   git push -u origin main
#   git clone https://github.com/you/data-science-course.git

print("push happens on GitHub with your credentials - see setup-guide.md")
"""),
    ("md", """## The course submission workflow

1. Work in your notebook, save, **Restart & Run All**.
2. `git status` — review what changed.
3. `git add labs/lab-01/` — stage *only* the relevant files.
4. `git commit -m "feat: finish lab-01 numpy exercises"`.
5. `git push origin main`.
6. Paste the repo URL where the assignment asks for submission.

Habits that get full marks:

- Meaningful commit messages (why, not just what).
- No large data files or `.env` secrets committed (see `.gitignore`).
- A commit after every completed exercise — not one at the deadline.

---
"""),("code", """# The five-command loop, as a reference cell (run inside YOUR repo):
#   git status
#   git add <files>
#   git commit -m "feat: <what and why>"
#   git push origin main

print("workflow: status -> add -> commit -> push")
"""),
    ("md", """## Beginner example: your first repo, end to end

---
"""),("code", """import tempfile, pathlib, subprocess

def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()

demo = pathlib.Path(tempfile.mkdtemp(prefix="first-repo-"))
run("git init", demo)
(demo / "hello.txt").write_text("hello data science\\n", encoding="utf-8")
run("git add hello.txt", demo)
print(run('git commit -m "docs: first file"', demo).splitlines()[0])
print(run("git log --oneline", demo))
"""),
    ("md", """## Intermediate example: a branching workflow

Combine everything: main branch with a clean history, an experiment branch
that is merged after a successful test. This is how teams work, and it is
exactly what the final project's shared repo expects.

---
"""),("code", """import tempfile, pathlib, subprocess

def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()

repo = pathlib.Path(tempfile.mkdtemp(prefix="branch-demo-"))
run("git init", repo)
run("git config user.email demo@example.com", repo)   # local identity for the demo
run("git config user.name Demo", repo)

demo_py = repo / "model.py"
demo_py.write_text("def predict(x):\\n    return x * 2\\n", encoding="utf-8")
run("git add model.py", repo)
run('git commit -m "feat: baseline model"', repo)

run("git switch -c feature/tuning", repo)
demo_py.write_text("def predict(x):\\n    return x * 2 + 1\\n", encoding="utf-8")
run("git add model.py", repo)
run('git commit -m "tune: add intercept term"', repo)

run("git switch main", repo)
run("git merge feature/tuning", repo)
print(run("git log --oneline", repo))
print(run("git status --short", repo) or "clean working tree")
"""),
    ("md", """## Exercises

Use throwaway temp folders (or your own repo) for these.

---
"""),("md", """### Exercise 1 — Three commits

Create a temp repo, add a file, and make **three** commits that each add one
meaningful line. Show `git log --oneline`."""),
    ("code", """# your code here (reuse the run() helper pattern above)
"""),
    ("code", """# Solution sketch
import tempfile, pathlib, subprocess

def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()

repo = pathlib.Path(tempfile.mkdtemp(prefix="ex1-"))
run("git init", repo)
f = repo / "notes.md"
lines = ["# Notes\\n", "## Idea 1: EDA first\\n", "## Idea 2: baseline before model\\n"]
for i, line in enumerate(lines):
    if i == 0:
        f.write_text(line, encoding="utf-8")
    else:
        f.write_text(f.read_text() + line, encoding="utf-8")
    run("git add notes.md", repo)
    run(f'git commit -m "docs: add note {i+1}"', repo)
print(run("git log --oneline", repo))
"""),
    ("md", """### Exercise 2 — Status reading

Make a change, run `git status --short` and `git diff`, then revert the
change with `git checkout -- <file>` (or `git restore <file>`). Confirm the
file is back to its committed version."""),
    ("code", """# your code here
"""),
    ("md", """### Exercise 3 — Branching

From the exercise-1 repo, create `feature/plots`, add a plotting line, commit,
switch back to `main`, and merge. Verify the line is present."""),
    ("code", """# your code here
"""),
    ("md", """## Challenge exercise

Simulate a **merge conflict** (the moment every beginner fears) and resolve it:

1. Create a repo with `data.py` containing `x = 1`.
2. On branch `main`, change it to `x = 2`, commit.
3. On a branch created **before** that change, change `x = 3`, commit.
4. Merge the branch into main — Git cannot decide, and reports a conflict.
5. Resolve it by editing the file to keep one value, then `git add` +
   `git commit` to finish the merge.

A merge conflict is not data loss — it is Git asking you to decide. See the
solution cell for the full script."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
import tempfile, pathlib, subprocess

def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()

repo = pathlib.Path(tempfile.mkdtemp(prefix="conflict-"))
run("git init", repo)
f = repo / "data.py"
f.write_text("x = 1\\n", encoding="utf-8")
run("git add data.py", repo)
run('git commit -m "init: x = 1"', repo)

run("git switch -c feature/a", repo)          # branch from x = 1
f.write_text("x = 3\\n", encoding="utf-8")
run("git add data.py", repo)
run('git commit -m "feature: x = 3"', repo)

run("git switch main", repo)                  # back to x = 1
f.write_text("x = 2\\n", encoding="utf-8")
run("git add data.py", repo)
run('git commit -m "main: x = 2"', repo)

print(run("git merge feature/a", repo))       # CONFLICT expected
print("--- file during conflict ---")
print(f.read_text())

# Resolve: keep x = 2, drop the conflict markers
f.write_text("x = 2\\n", encoding="utf-8")
run("git add data.py", repo)
print(run('git commit -m "merge: resolved to x = 2"', repo).splitlines()[0])
print(run("git log --oneline", repo))
"""),
    ("md", """## Recap

- Three areas: working directory → staging (`git add`) → history (`git commit`).
- `git push` uploads to GitHub; `git commit` alone does not.
- Read state with `git status` and `git diff`; read history with `git log`.
- Branches = parallel work; pull requests = reviewed merges on GitHub.
- Conflicts are decisions, not disasters — resolve, stage, commit.
- Course habit: commit after every exercise, message explains *why*.

---
"""),
    ("md", """## Questions

1. What is the difference between `git add` and `git commit`?
2. What is the difference between `git commit` and `git push`?
3. What does `git status` show?
4. Which command creates a branch and switches to it in one step?
5. What is a pull request for?
6. True/False: a merge conflict means your work is lost.

---
**Next:** notebook 09 — APIs and data acquisition.
"""),
]