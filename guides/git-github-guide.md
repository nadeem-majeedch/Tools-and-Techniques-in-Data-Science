# Git & GitHub Guide

Git is the version-control tool that records the history of your code;
GitHub is a website that hosts those repositories and lets you submit,
share, and collaborate on them. In this course **almost every deliverable is
submitted through Git/GitHub**, so this guide is your quick reference.

## Why data scientists use Git

- **History & undo** — every version of your notebooks and scripts is one
  command away; you never lose work to a bad edit.
- **Reproducibility** — the commit history shows exactly *when* and *how* a
  file changed, which is the backbone of the course's reproducibility rule:
  *someone else (or future you) can re-run your work*.
- **Submission** — instructors grade the repository: commit messages, an
  executed notebook with visible outputs, and a README are all part of the
  grade for labs, [assignments](../assignments/README.md), and the
  [final project](../projects/README.md).

## Install & first-time setup (once)

```bash
# Windows: https://git-scm.com/download/win
# macOS:   brew install git        | Linux: sudo apt install git
git --version

# Tell Git who you are (your commits carry this identity)
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
```

## The daily loop (the only commands you need 90% of the time)

```bash
git status            # what has changed? (check this often)
git add <files>       # stage changes you want to record
git commit -m "Describe the change in one clear sentence"
git push              # upload your commits to GitHub
git pull              # download others' changes (do this before you start)
```

Worked example — submitting a lab:

```bash
git clone https://github.com/<your-account>/<your-lab-repo>.git
cd <your-lab-repo>
# ... work on lab-07-pandas-part-1.ipynb, execute every cell, save ...
git status                             # see the notebook listed as modified
git add lab-07-pandas-part-1.ipynb
git commit -m "Lab 07: pandas Series and DataFrame selection"
git push
```

??? tip "A good commit message explains *why*, not just *what*"
    ✅ `Lab 09: fill missing age with group median and log the reason`
    ❌ `update`
    ❌ `final final v2 REALLY final.ipynb`

## Common situations

| Situation | What to do |
|---|---|
| "Please tell me who you are" | run the two `git config --global` lines above |
| You staged the wrong file | `git restore --staged <file>` to unstage |
| You want to undo an *uncommitted* change | `git restore <file>` (careful — permanent) |
| `push` is rejected (remote has new commits) | `git pull` first, then `git push` again |
| You committed a large generated file by mistake | remove it, add it to `.gitignore`, commit the fix |
| You need the notebook's output visible in GitHub | save the notebook after **Run All**, then commit it |

## Branches (enough to be safe)

A branch is a parallel copy of your history — useful for experiments and for
instructors' review workflows:

```bash
git branch experiment     # create a branch
git switch experiment     # switch to it
# ... work, commit ...
git switch main
git merge experiment      # bring the branch's commits into main
```

You do **not** need pull requests for individual labs, but they are the
standard way teams collaborate on the [final project](../projects/README.md):
each member works on a branch and opens a pull request to merge their work
into `main`.

## Course conventions (read before submitting)

- **Execute and save** every notebook (Run All) so graders see outputs — a
  notebook of unrun cells is not a submission.
- Keep generated artifacts out of the repo (`.gitignore` exists for this).
- A short, descriptive README tells the grader what the deliverable is and
  how to run it.
- Don't commit secrets, API keys, or data you were not given permission to
  share.

## Go deeper

- Full lecture: [Session 4 — Git & GitHub](../sessions/session-04-git-and-github.md)
- Hands-on notebook: [Notebook 08 — Git/GitHub workflow](../course-notebooks/08-git-github-workflow.ipynb)
- Practice: [Lab 04 · Git & GitHub workflow](../labs/lab-04-git-and-github.md)
- Environment setup (installing Git, first clone): [Setup guide](../resources/setup-guide.md)

> Git feels awkward for the first week and natural after that. The rule that
> fixes most problems: **check `git status` before every commit and after
> every pull.**
