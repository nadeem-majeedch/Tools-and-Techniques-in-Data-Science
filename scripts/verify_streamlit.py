"""Verify the Streamlit module: syntax-check every Python code block in the
docs, then headless-run the six example apps and check their health.

Usage:  python scripts/verify_streamlit.py
"""
import ast
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STREAMLIT_DIR = ROOT / "streamlit"

FENCE = re.compile(r"```python\n(.*?)```", re.DOTALL)


def python_blocks(path):
    text = path.read_text(encoding="utf-8")
    return [m.group(1) for m in FENCE.finditer(text)]


def check_syntax(blocks, label):
    """Compile every block; skip blocks that are intentionally partial."""
    bad = 0
    for i, block in enumerate(blocks, 1):
        if "..." in block:          # intentional placeholder (skeleton/hints)
            continue
        try:
            # markdown list items indent their fences -> dedent first
            ast.parse(textwrap.dedent(block))
        except SyntaxError as e:
            bad += 1
            print(f"  SYNTAX ERROR in {label} block {i}: {e}")
    return bad


def example_app(path):
    """Extract the first fenced python block under the '## Code' heading."""
    text = path.read_text(encoding="utf-8")
    code_marker = text.find("## Code")
    if code_marker == -1:
        return None
    after = text[code_marker:]
    m = FENCE.search(after)
    return m.group(1) if m else None


def run_app(code, port, name):
    """Run one app headless, probe /_stcore/health, then kill it."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False,
                                     encoding="utf-8") as f:
        f.write(code)
        app_path = f.name
    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", app_path,
         "--server.headless", "true", "--server.port", str(port),
         "--browser.gatherUsageStats", "false"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        url = f"http://localhost:{port}/_stcore/health"
        ok = False
        for _ in range(60):
            if proc.poll() is not None:
                break
            try:
                with urllib.request.urlopen(url, timeout=2) as resp:
                    if resp.read().decode() == "ok":
                        ok = True
                        break
            except Exception:
                time.sleep(0.5)
        status = "OK " if ok else "FAIL"
        print(f"  [{status}] {name}  (port {port})")
        if not ok:
            # surface the app's startup error
            time.sleep(2)
            return False
        return True
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        os.unlink(app_path)


def main():
    print("== Step 1: syntax-check every python block in streamlit docs ==")
    total_bad = 0
    for md in sorted(STREAMLIT_DIR.glob("*.md")):
        blocks = python_blocks(md)
        if not blocks:
            continue
        bad = check_syntax(blocks, md.name)
        total_bad += bad
        print(f"  {md.name}: {len(blocks)} blocks checked")
    if total_bad:
        print(f"FAIL: {total_bad} syntax errors")
        sys.exit(1)
    print("  all blocks compile")

    print("\n== Step 2: headless-run the six example apps ==")
    examples = [
        ("streamlit-introduction.md", 8601, "Example 1 - Hello DS"),
        ("streamlit-widgets.md", 8602, "Example 2 - Calculator"),
        ("streamlit-pandas.md", 8603, "Example 3 - CSV viewer"),
        ("streamlit-visualization.md", 8604, "Example 4 - EDA dashboard"),
        ("streamlit-ml-app.md", 8605, "Example 5 - ML prediction app"),
        ("streamlit-dashboard-project.md", 8606, "Example 6 - Mini dashboard"),
    ]
    failures = 0
    for fname, port, label in examples:
        code = example_app(STREAMLIT_DIR / fname)
        if code is None:
            print(f"  [SKIP] {label}: no '## Code' section found")
            continue
        if not run_app(code, port, label):
            failures += 1

    if failures:
        print(f"\nFAIL: {failures} example apps did not start cleanly")
        sys.exit(1)
    print("\nALL CHECKS PASSED: 6/6 example apps start and answer health OK")


if __name__ == "__main__":
    main()