# Lab 04 — Git & GitHub Workflow

**Session:** Week 2 · Session 4 · 90 min
**CLO:** CLO-1 (reproducibility foundation), CLO-3
**Difficulty:** Beginner

## Learning objectives

By the end of this lab you can:

1. Explain the working tree → staging area → commit pipeline.
2. Create, switch, merge, and delete branches.
3. Push to GitHub and pull changes without losing work.
4. Write commit messages that explain **why**, not just **what**.
5. Recover from a simple "oops" (amend, restore a file).

## Problem statement

Your course repo is about to carry every lab, assignment, and project file
for 16 weeks. You must prove you can operate Git safely: commit cleanly,
work on a branch without breaking `main`, and merge without drama. You will
simulate a realistic solo workflow: a feature branch, a commit, a fix, and
a merge back to `main`.

## Dataset requirements

None — you work with small text/Python files you create.

## Step-by-step tasks

Work in your `data-science-course` repository from Lab 01 (create it if
needed).

1. **Baseline:** confirm `git status` is clean and `git log --oneline`
   shows your previous commits.
2. **Create a branch** `feature/eda-notes` and switch to it.
3. **Add a file** `eda-notes.md` with two bullet points about the tips
   dataset. Stage and commit with a *why*-style message.
4. **Switch back to `main`.** Add a second bullet to `eda-notes.md` —
   deliberately creating a different version. Commit it on `main`.
5. **Merge** the feature branch into `main`. Resolve the conflict in favor
   of keeping **both** bullet sets (edit the file, then `git add` +
   commit). Record the merge commit.
6. **Push** `main` to GitHub. Verify the file on github.com.
7. **Simulate a teammate:** clone the repo into a second folder, add a file,
   commit, and push. Then `git pull` in your original folder — you must see
   the new file.
8. **Cleanup:** delete the merged `feature/eda-notes` branch locally.

## Starter code

```bash
git status
git log --oneline
git switch -c feature/eda-notes
# ... edit eda-notes.md, add two bullets ...
git add eda-notes.md
git commit -m "Add EDA notes for tips dataset"
git switch main
# ... edit eda-notes.md with a different bullet, commit ...
git merge feature/eda-notes
# if conflict: edit file, git add eda-notes.md, git commit
git push origin main
git branch -d feature/eda-notes
```

## Expected output

- `git log --oneline` shows at least: an initial commit, the feature
  commit, a main commit, and a merge commit.
- `git status` clean at the end.
- `git branch` lists only `main` (and `* main`).
- The pushed file appears on github.com.
- The second clone's file appears after `git pull`.

## Questions

1. In your own words: what is the difference between `git add` and
   `git commit`?
2. Why did the merge conflict happen? (Both versions changed the same
   lines.)
3. What does `git push origin main` do, exactly?
4. Why commit small, focused changes with message describing the *why*?
5. What is one risk of `git commit -am` that `git add` + `git commit` avoids?

## Challenge task

Practice recovery: make a small change to a tracked file, then restore it
with `git restore <file>`. Next, commit a message you regret and fix it
with `git commit --amend`. Finally, add a `Labs/` directory with this
lab's file, commit it, and push — your repo is now set up for the rest of
the course. Document all three commands you used in `eda-notes.md`.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Branch created, used, merged, deleted | 4 | log shows feature + merge commits |
| Conflict resolved keeping both versions | 3 | both bullet sets present |
| Pushed to GitHub, verified remotely | 3 | repo visible |
| Clone → push → pull round trip | 3 | second folder worked |
| Why-style commit messages | 2 | reviewed in log |
| Answers to questions | 2 | Q2, Q5 correct |
| Challenge: restore + amend + Labs/ pushed | 3 | all three commands |
| **Total** | **20** | |