"""Execute every notebook in course-notebooks/ and save the executed versions.

Usage:
    python scripts/execute_notebooks.py

Each notebook is run with a per-cell timeout. Executed outputs are written
back into the same .ipynb file so the delivered notebooks contain results.
Notebooks whose cells are guarded (Ollama not running, pandasai missing,
no network) still pass as long as no cell raises an unhandled error.
"""
import pathlib
import sys
import traceback

from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError
import nbformat

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "course-notebooks"

CELL_TIMEOUT = 180  # seconds per cell


def execute_one(path: pathlib.Path) -> bool:
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
        print(f"FAIL {path.name}")
        print("     " + str(exc).splitlines()[-1] if str(exc) else "")
        traceback.print_exc(limit=2)
        nbformat.write(nb, path)
        return False
    except Exception:
        print(f"ERROR {path.name}")
        traceback.print_exc(limit=2)
        return False
    nbformat.write(nb, path)
    return True


def main() -> None:
    files = sorted(OUT.glob("*.ipynb"))
    if not files:
        print("no notebooks found in", OUT)
        sys.exit(1)
    results = []
    for f in files:
        ok = execute_one(f)
        results.append((f.name, ok))
        print(("ok   " if ok else "FAIL ") + f.name)

    failed = [name for name, ok in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} notebooks executed cleanly")
    if failed:
        print("failed:", ", ".join(failed))
        sys.exit(1)


if __name__ == "__main__":
    main()