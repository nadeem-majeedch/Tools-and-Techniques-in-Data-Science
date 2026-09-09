# Publishing this Course Website

This repository is also a **GitHub Pages website** built with
[MkDocs](https://www.mkdocs.org/) and the
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.
Every Markdown file already in the repository becomes a page — the website
is a second view of the same files, not a copy.

- `mkdocs.yml` — the whole site configuration (theme, navigation, what to
  publish).
- `.github/workflows/website.yml` — builds and deploys the site on every push
  to `main`.
- `index.md` — the Home page (separate from `README.md`, which stays the
  GitHub repository readme).

## 1. Publish the site (about two minutes)

1. Push this repository to GitHub (branch `main`).
2. In the repo: **Settings → Pages → Build and deployment → Source →
   *GitHub Actions***.
3. Push any commit to `main` (or run the *Deploy website to GitHub Pages*
   workflow manually from the **Actions** tab).
4. Your site appears at `https://<your-org>.github.io/<your-repo>/`.

> **Visibility:** GitHub Pages publishes publicly when the repository is
> public. This site is deliberately **student-facing** — answer keys and
> instructor solutions are excluded from the build (see below). Keep the
> repository private until you are ready to share, and check the license
> note in the repository README before publishing.

## 2. What is published (and what is not)

`mkdocs.yml` sets `docs_dir: .`, so the whole repository is the source tree.
`exclude_docs` removes instructor-only material from the **build only** —
nothing in the repository itself is deleted:

```yaml
exclude_docs:
  - quizzes/                    # quiz banks with inline answer keys
  - exams/                      # midterm/final with answer keys
  - labs/instructor-solutions/
  - streamlit/labs/solutions/
  - assignments/assignment-01-data-cleaning-eda/instructor-solution.md
  - assignments/assignment-01-data-cleaning-eda/instructor-clean.csv
  - assignments/assignment-02-api-streamlit-app/instructor-solution.md
  - projects/final-project/viva-questions.md
```

To publish a different set (for example, an instructor-only site), edit this
list — and adjust the `nav` section, which references the pages shown in the
sidebar.

## 3. Preview locally

Content stays at the repository root (single source of truth); MkDocs needs
it under `docs/`, so a small script mirrors it there first (this also strips
the instructor-only files):

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate   | macOS/Linux: source .venv/bin/activate
pip install -r website-requirements.txt
python scripts/build_site_src.py    # populates docs/ from the repo content
mkdocs serve
```

Open http://127.0.0.1:8000. `mkdocs serve` rebuilds automatically as you
edit files, but **re-run `scripts/build_site_src.py` after adding/renaming
files**. To produce a static build without serving:
`python scripts/build_site_src.py && mkdocs build`.

## 4. Customize

| You want to… | Edit |
|---|---|
| Change the site title / description | `site_name`, `site_description` in `mkdocs.yml` |
| Add the real repository URL (edit buttons, GitHub link) | uncomment `site_url` / `repo_url` near the top of `mkdocs.yml` |
| Change colors or font | `theme.palette` / `theme.font` in `mkdocs.yml` (see [Material docs](https://squidfunk.github.io/mkdocs-material/setup/changing-the-colors/)) |
| Change the sidebar order | the `nav:` block — order there also drives the Previous/Next footer on every page |
| Add or hide a page | add/remove its path in `nav` (hide from *build* with `exclude_docs`) |
| Change syntax highlighting, collapsibles, admonitions | `markdown_extensions` in `mkdocs.yml` |
| Use a custom domain | repo **Settings → Pages → Custom domain** (and set `site_url`) |

## 5. How pages map to the course

| Site section | Source files |
|---|---|
| Home | `index.md` |
| Course Overview · CLOs · Course Schedule | `course-outline.md` · `CLOs.md` · `weekly-schedule.md` |
| Weekly Lectures (32 pages, Previous/Next chain) | `sessions/session-01…32.md` |
| Labs (32 pages) | `labs/lab-01…32.md` |
| Assignments (2) | `assignments/assignment-0*/README.md` |
| Quizzes · Exams (format pages, no keys) | `assessments/quizzes.md` · `assessments/exams.md` |
| Final Project | `projects/` + `projects/final-project/` |
| Python Setup | `resources/setup-guide.md` |
| Streamlit Guide | `streamlit/` module |
| PandasAI · LLM/Ollama · Agents · n8n Guides | `guides/` + deep links into `module-c/` and `course-notebooks/` |
| FAQ | `guides/faq.md` |

## 6. Keeping it working

- The deployment workflow runs `python scripts/build_site_src.py` then builds
  with **`mkdocs build --strict`** — a broken internal link or malformed page
  fails the workflow instead of shipping a broken site. Fix the reported
  warning and push again.
- `scripts/build_site_src.py` and the `exclude_docs` list in `mkdocs.yml`
  both control what is published; keep the instructor-only exclusions in
  sync in both places (they are each other's safety net).
- `.github/workflows/website.yml` pins the build tools in
  `website-requirements.txt`; bump those versions deliberately.
- `/docs/` and `/site/` (local build products) are gitignored.
- Sessions, labs, and guides can be added without touching the config — but
  to appear in the sidebar and in the Previous/Next chain they must be added
  to `nav` in `mkdocs.yml`.
