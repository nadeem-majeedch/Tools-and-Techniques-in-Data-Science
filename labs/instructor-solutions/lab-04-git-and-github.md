# Lab 04 — Solution: Git & GitHub Workflow

**Session:** W2 S4 · **CLO:** CLO-1, CLO-3

## Complete solution

```bash
git status                       # clean baseline
git log --oneline                # prior commits visible

git switch -c feature/eda-notes
# edit eda-notes.md -> add two bullets
git add eda-notes.md
git commit -m "Add EDA notes: tips has 244 rows, no missing values"

git switch main
# edit eda-notes.md -> add a DIFFERENT bullet (same file, overlapping lines)
git add eda-notes.md
git commit -m "Add note on tip skew visible in histogram"

git merge feature/eda-notes      # CONFLICT expected (same lines changed)
# edit eda-notes.md to keep BOTH bullet sets
git add eda-notes.md
git commit -m "Merge feature/eda-notes, keep both bullet sets"

git push origin main
# on github.com: verify eda-notes.md exists

# simulate a teammate:
git clone <url> ../course-clone
cd ../course-clone
echo "# from clone" > extra.md
git add extra.md && git commit -m "Add extra note from second machine"
git push origin main
cd <original repo>
git pull origin main             # extra.md now appears

git branch -d feature/eda-notes  # merged; deletes local branch only
git branch                       # -> * main
```

## Model answers

1. **add vs commit** — `git add` moves changes into the *staging area*
   (selecting what will be recorded); `git commit` snapshots the staged
   content into history with a message. You can stage selectively.
2. **Why conflict** — both `main` and the feature branch changed the same
   lines of `eda-notes.md`; Git can't know which version to keep, so it
   asks a human.
3. **git push origin main** — uploads local `main` commits to the `origin`
   remote's `main` branch.
4. **Small why-style commits** — history becomes a readable story (why a
   change exists), easy to review, revert, and bisect.
5. **`git commit -am` risk** — it stages *all* modified tracked files; if
   you have unrelated changes they get swept into the commit. Separate
   `git add` lets you commit in logical units.

## Challenge solution

```bash
echo "temporary edit" >> eda-notes.md
git restore eda-notes.md          # discard working-tree change
git status                        # clean again

git commit -m "oops message"
git commit --amend -m "Better message explaining the why"
git log --oneline -1              # single commit, new message

mkdir Labs
cp <lab file> Labs/lab-04-git-and-github.md   # or create it
git add Labs/
git commit -m "Add Lab 04 to Labs directory"
git push
```

Log at the end shows: initial commit → feature commit → main commit →
merge commit → challenge commits; `git status` clean.