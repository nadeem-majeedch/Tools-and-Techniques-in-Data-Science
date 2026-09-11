"""Mirror the course repository's Markdown content into docs/ for MkDocs.

MkDocs requires its content (docs_dir) to live in a child directory of the
config file, while this repository keeps its canonical content at the repo
root (sessions/, labs/, ...). This script creates that child directory by
copying only the files that should be published on the student-facing site.

Run it before `mkdocs serve` / `mkdocs build`:

    python scripts/build_site_src.py
    mkdocs serve            # or: mkdocs build

CI does exactly this in .github/workflows/website.yml.

Any file/folder listed in EXCLUDE is deliberately NOT published (answer keys,
instructor solutions). Keep EXCLUDE in sync with exclude_docs in mkdocs.yml —
both act as a safety net, so if one is forgotten the other still protects.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "docs"

# Directories whose entire public content is copied into docs/.
# quizzes/ and exams/ are intentionally NOT copied — they hold answer keys.
DIRS = [
    "sessions",
    "labs",
    "streamlit",
    "module-c",
    "assignments",
    "projects",
    "resources",
    "course-notebooks",
    "datasets",
    "guides",
    "assessments",
    "tools",
]

# Files (relative to the repo root) that become top-level pages.
# README.md is deliberately omitted: it is the GitHub repository readme, and
# index.md is the website Home page (MkDocs rejects a duplicate homepage).
FILES = [
    "index.md",
    "DEPLOYING.md",
    "course-outline.md",
    "CLOs.md",
    "weekly-schedule.md",
    "assessment-plan.md",
]

# Paths (inside the copied dirs) that must never reach the site.
EXCLUDE = {
    # Instructor-only material
    "labs/instructor-solutions",
    "streamlit/labs/solutions",
    "assignments/assignment-01-data-cleaning-eda/instructor-solution.md",
    "assignments/assignment-01-data-cleaning-eda/instructor-clean.csv",
    "assignments/assignment-02-api-streamlit-app/instructor-solution.md",
    "projects/final-project/viva-questions.md",
}


def ignore(dirname: str, names: list[str]) -> set[str]:
    """shutil ignore callback: drop EXCLUDE paths and caches from the copy."""
    rel_dir = Path(dirname).resolve()
    skipped: set[str] = set()
    for name in names:
        if name == "__pycache__" or name.endswith(".pyc"):
            skipped.add(name)
            continue
        rel = rel_dir.joinpath(name).relative_to(ROOT)
        parts = rel.parts
        if any("/".join(parts[: n + 1]) in EXCLUDE for n in range(len(parts))):
            skipped.add(name)
    return skipped


def main() -> None:
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir()

    for d in DIRS:
        src = ROOT / d
        if src.is_dir():
            shutil.copytree(src, DEST / d, ignore=ignore)
        else:
            print(f"warning: expected directory not found: {d}")

    for f in FILES:
        src = ROOT / f
        if src.is_file():
            shutil.copy2(src, DEST / f)
        else:
            print(f"warning: expected file not found: {f}")

    print(f"docs/ populated with {len(list(DEST.rglob('*.md')))} markdown files")


if __name__ == "__main__":
    main()
