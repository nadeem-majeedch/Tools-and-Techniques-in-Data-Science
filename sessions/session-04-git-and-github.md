# Session 4 — Git & GitHub

**Week 2 · Session 4 · Module A · 90 min · CLO-1**

## 1. Learning objectives

By the end of this session, students can:
- Explain what version control is and why data projects need it.
- Create a repository, stage, commit, and push changes to GitHub.
- Clone a repository and pull updates.
- Create and switch branches; open a pull request.
- Use Git to submit every course deliverable (labs, assignments, project).

## 2. Key concepts

- Git tracks **history**, not just files — every version is recoverable.
- Commit = a snapshot with a message; commit often, with meaningful messages.
- Working directory → `git add` (stage) → `git commit` (snapshot) → `git push` (remote).
- A **branch** is a parallel line of work; the default is `main`.
- GitHub is a hosting service for Git repositories (plus issues, PRs, collaboration).
- For data science: your data *story* includes your code history — it proves how results were produced.

## 3. Detailed lecture notes

**Why Git?** The oldest excuse for losing work is "I saved over it." Version
control removes that class of disaster: every commit is a checkpoint you can
return to. For a course, Git also powers *submission and grading*: the commit
history shows your actual workflow (did you build gradually, or paste everything
at 11:59 PM?). For a data scientist, Git is the minimum reproducibility tool —
your future self and your collaborators need to see exactly how the analysis
evolved.

**The mental model.** Three places: your **working directory** (files you edit),
the **staging area** (`git add` — files selected for the next snapshot), and the
**repository history** (`git commit` — the snapshot itself). Pushing copies
history to a **remote** (GitHub). The famous diagram: `git add` moves changes
right, `git commit` photographs them, `git push` uploads the photos.

**Commit messages.** Write messages that explain *why*, not what: "fix: drop
duplicate rows before aggregation" beats "update". Conventional prefixes (`feat:`,
`fix:`, `docs:`) are common in industry; introduce them lightly, don't police.

**Branches.** Why branch? So you can experiment without breaking working code.
`git switch -c branch-name` creates and moves to a branch; `git switch main`
returns; merging integrates changes. This course uses branches lightly (mainly
for the final project), but the concept matters — it's how real teams work.

**Pull requests.** On GitHub, a PR proposes merging one branch into another and
is the place for review/discussion. For this course, students submit by pushing
to their repo and sharing the link; the instructor may comment on PRs for
assignments. Show a live PR round-trip if time permits.

**GitHub for submission workflow (this course):** clone/`git init` → work in
notebooks → `git add .` → `git commit -m "message"` → `git push`. Repeat after
every lab. Deliverables state "submit the repository URL"; the instructor checks
the latest commit.

## 4. Important terminology

- **Repository (repo)** — a project folder tracked by Git.
- **Commit** — a saved snapshot of the project with a message.
- **Stage** — select changes to include in the next commit (`git add`).
- **Remote** — a copy of the repo on another machine (usually GitHub).
- **Push / Pull** — upload commits / download commits.
- **Clone** — copy a remote repo to your machine for the first time.
- **Branch** — an independent line of development.
- **Pull request (PR)** — a proposed merge of one branch into another, with review.
- **Merge conflict** — when two edits touch the same lines; Git asks you to decide.
- **`main`** — the default branch name (older repos call it `master`).

## 5. Python examples

Git is a shell tool, not a Python library — but the workflow is exercised *from*
the notebook-centric workflow. Run these in a terminal (Git Bash on Windows):

```bash
# One-time setup
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Create a repo from an existing folder
cd ~/data-science-course
git init
git status                 # what is changed/untracked

# The daily loop: add -> commit -> push
git add notebooks/week-01/session-02-python-refresher.ipynb
git commit -m "feat: complete python refresher notebook"
git push origin main

# Branching
git switch -c feature/eda   # create + switch
git switch main             # back to main
```

```python
# A Python-side tip: never commit secrets or large data.
# Check .gitignore covers .env and data files (already done for this course).
import pandas as pd
df = pd.read_csv("data.csv")  # if this file is >10MB, it should NOT be in git
```

## 6. Beginner example

```bash
echo "my first file" > hello.txt
git init
git add hello.txt
git commit -m "docs: add hello.txt"
```

Three commands and your project is versioned. From here, everything else is
variation: more files, more commits, a remote.

## 7. Practical Data Science example

```bash
# A realistic submission workflow for Lab 04 (due before Session 5)
cd ~/data-science-course

# 1. Work on the lab notebook, then review what changed
git status
git diff labs/lab-04-git-and-github.md   # skim the diff

# 2. Stage only the lab files (avoid committing unrelated work)
git add labs/lab-04-git-and-github.md
git commit -m "feat: finish lab-01 numpy exercises"

# 3. Publish to GitHub
git push origin main

# 4. The submission is the URL: https://github.com/username/data-science-course
```

Discuss: what does the instructor see? Commit history with timestamps — a
complete, auditable record of your work. This *is* reproducibility in action.

## 8. In-class activity (50 min)

Work in pairs; each partner creates their own repo:

1. **First repo (15 min):** create `my-first-repo` on GitHub (empty, no README),
   clone it locally, add a `README.md` describing yourself, commit and push.
2. **Commit discipline (15 min):** make three small commits (not one big one):
   "docs: add readme", "docs: add goals", "feat: add first notebook link".
   Then use `git log --oneline` to read your own history.
3. **Branch + PR (20 min):** create branch `feature/experiment`, add a line to
   the README, commit, push, open a PR, merge it. Swap roles — partner reviews
   your PR and leaves one comment.

## 9. Lab exercise

No graded lab this session. **Submission setup deliverable (due Session 6 with Lab 1):**
your course repo on GitHub with (a) `.gitignore` present, (b) a `README.md`,
(c) at least three commits with meaningful messages. Lab 1 will be submitted
through this repo for the first time.

## 10. Common mistakes

- Committing large data files or `.env` secrets → bloated, insecure repos. Rely on `.gitignore`.
- `git add .` when the repo contains unrelated work → messy history. Stage deliberately.
- Committing "work in progress" garbage messages ("changes", "update", "final_v2").
- Forgetting `git pull` before `git push` on a shared repo → rejected push (non-fast-forward).
- Thinking `git commit` also uploads to GitHub — it doesn't; `git push` does. (Most common confusion.)
- Editing files directly on GitHub's web editor and then pushing locally → conflicts.

## 11. Short assessment questions

1. What is the difference between `git add` and `git commit`?
2. What is the difference between `git commit` and `git push`?
3. Which command shows the current state of your working directory?
4. How do you create a new branch and switch to it in one command?
5. Why should you commit after every completed lab exercise?
6. True/False: a merge conflict means your work is lost. (False — Git asks you to choose/merge.)

## 12. CLO mapping

CLO-1: Git/GitHub is the submission and collaboration channel for all data-handling
work in Module A. It also plants the reproducibility habit that CLO-3 formalizes
(Sessions 24, 30) and that the final project rubric rewards.

## 13. Suggested homework

- Complete the "Submission setup deliverable" above (repo + README + 3 commits).
- Practice: clone a public repo (e.g., a small one from your instructor), make a
  change, and open a PR if it accepts contributions — or just practice on your own repo.
- Read: *Pro Git* chapter 1 (free at git-scm.com/book) — the first three sections only.
- Prepare: bring your repo URL to Session 6; Lab 1 will be submitted through it.