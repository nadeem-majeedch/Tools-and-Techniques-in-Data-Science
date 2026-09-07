"""Build the 20 course notebooks from content modules in notebook_src/.

Usage:
    python scripts/build_course_notebooks.py

Each content module (notebook_src/nb_XX_*.py) defines a CELLS list of
(kind, source) tuples where kind is "md" or "code". This script turns
them into real .ipynb files in course-notebooks/.
"""
import importlib
import pathlib
import sys

import nbformat as nbf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

OUT = HERE.parent / "course-notebooks"
OUT.mkdir(exist_ok=True)

ORDER = [
    ("nb_01_python", "01-python-for-data-science.ipynb"),
    ("nb_02_numpy", "02-numpy.ipynb"),
    ("nb_03_pandas", "03-pandas.ipynb"),
    ("nb_04_data_cleaning", "04-data-cleaning.ipynb"),
    ("nb_05_data_aggregation", "05-data-aggregation.ipynb"),
    ("nb_06_data_visualization", "06-data-visualization.ipynb"),
    ("nb_07_eda", "07-eda.ipynb"),
    ("nb_08_git_github", "08-git-github-workflow.ipynb"),
    ("nb_09_apis", "09-apis-and-data-acquisition.ipynb"),
    ("nb_10_ml_intro", "10-intro-to-machine-learning.ipynb"),
    ("nb_11_regression", "11-regression.ipynb"),
    ("nb_12_classification", "12-classification.ipynb"),
    ("nb_13_clustering", "13-clustering.ipynb"),
    ("nb_14_pandasai", "14-pandasai.ipynb"),
    ("nb_15_llm_fundamentals", "15-llm-fundamentals.ipynb"),
    ("nb_16_ollama", "16-ollama-with-python.ipynb"),
    ("nb_17_tool_calling", "17-tool-and-function-calling.ipynb"),
    ("nb_18_ai_agents", "18-ai-agents.ipynb"),
    ("nb_19_n8n", "19-n8n-workflows.ipynb"),
    ("nb_20_e2e_project", "20-end-to-end-data-science-project.ipynb"),
]


def build(mod_name: str, filename: str) -> None:
    mod = importlib.import_module(f"notebook_src.{mod_name}")
    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb.metadata["language_info"] = {"name": "python"}
    nb.cells = [
        nbf.v4.new_markdown_cell(src) if kind == "md" else nbf.v4.new_code_cell(src)
        for kind, src in mod.CELLS
    ]
    nbf.write(nb, OUT / filename)
    print("built", filename)


if __name__ == "__main__":
    for mod, fn in ORDER:
        build(mod, fn)
    print(f"\nDone. {len(ORDER)} notebooks written to {OUT}")