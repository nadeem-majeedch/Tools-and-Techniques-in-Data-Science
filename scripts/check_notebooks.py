"""Check every notebook in course-notebooks/ executes without errors.

Unlike scripts/execute_notebooks.py (which writes outputs back into the
.ipynb files), this script NEVER modifies notebook contents: notebooks are
read, executed in memory, and discarded. It is safe to run repeatedly and is
what CI uses (.github/workflows/notebooks.yml).

Behavior:
- Every code cell runs with a per-cell timeout.
- Any unhandled exception in any cell fails the check.
- Optional services (Ollama daemon, pandasai on some Python versions) are NOT
  required: notebooks 14-18 guard those calls with try/except and degrade
  gracefully. Network is only needed by notebook 09/19 (keyless Open-Meteo /
  JSONPlaceholder APIs) — GitHub runners have network.
- A writable HOME and a git identity are configured so notebook 08's real
  `git init` / `git commit` demos succeed in their throwaway temp repos.

Usage:
    python scripts/check_notebooks.py                # check all
    python scripts/check_notebooks.py 03 12          # check only 03 and 12
"""
from __future__ import annotations

import os
import pathlib
import subprocess
import sys

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

HERE = pathlib.Path(__file__).resolve().parent
NB_DIR = HERE.parent / "course-notebooks"

CELL_TIMEOUT = 120  # seconds per cell; notebooks are small and CI-friendly


def _git_identity_available() -> bool:
    """True if `git commit` can run without extra configuration."""
    try:
        r = subprocess.run(
            ["git", "config", "user.email"],
            capture_output=True,
            text=True,
            shell=False,
        )
    except FileNotFoundError:
        return True  # git absent: notebook 08 degrades on its own? (git is required in practice)
    return r.returncode == 0 and r.stdout.strip() != ""


def _prepare_environment() -> None:
    """Make the environment notebook-friendly (esp. notebook 08's git demos)."""
    # Notebook 08 creates throwaway repos and commits. On fresh CI machines
    # no global git identity exists, which would make `git commit` fail. Set
    # env-level identity (does not touch any config file or global state).
    if not _git_identity_available():
        os.environ.setdefault("GIT_AUTHOR_NAME", "CI Notebook Checker")
        os.environ.setdefault("GIT_AUTHOR_EMAIL", "ci@example.com")
        os.environ.setdefault("GIT_COMMITTER_NAME", "CI Notebook Checker")
        os.environ.setdefault("GIT_COMMITTER_EMAIL", "ci@example.com")
    # Ensure a writable HOME for matplotlib config / jupyter runtime dirs.
    os.environ.setdefault("HOME", str(pathlib.Path.cwd()))


def check_one(path: pathlib.Path) -> tuple[bool, str]:
    """Execute one notebook in memory. Returns (ok, message)."""
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=CELL_TIMEOUT,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    )
    try:
        client.execute()
    except CellExecutionError as exc:
        tail = str(exc).strip().splitlines()[-1] if str(exc).strip() else "cell error"
        return False, tail
    except Exception as exc:  # timeout, dead kernel, ...
        return False, f"{type(exc).__name__}: {exc}"
    return True, ""


def main() -> None:
    wanted = [a for a in sys.argv[1:] if not a.startswith("-")]
    files = sorted(NB_DIR.glob("*.ipynb"))
    if wanted:
        files = [f for f in files if any(f.name.startswith(w) for w in wanted)]
    if not files:
        print(f"no notebooks matched in {NB_DIR}")
        sys.exit(1)

    _prepare_environment()

    results: list[tuple[str, bool, str]] = []
    for f in files:
        ok, msg = check_one(f)
        results.append((f.name, ok, msg))
        print(("ok   " if ok else "FAIL ") + f.name, flush=True)
        if not ok:
            print("     " + msg, flush=True)

    failed = [r for r in results if not r[1]]
    print(f"\n{len(results) - len(failed)}/{len(results)} notebooks executed without errors")
    if failed:
        print("failed:", ", ".join(r[0] for r in failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
