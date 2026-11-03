"""Validate structure and publication hygiene without executing ML cells."""
import ast
import json
import re
from pathlib import Path
import nbformat

ROOT = Path(__file__).resolve().parents[1]
for path in sorted((ROOT / "notebooks").glob("*.ipynb")):
    nb = nbformat.read(path, as_version=4)
    nbformat.validate(nb)
    count = 0
    for i, cell in enumerate(nb.cells):
        assert not cell.get("attachments"), f"Embedded attachment: {path.name}:{i}"
        assert not re.search(r"/Users/|drive\.google\.com|data:audio|base64,", cell.source), f"Private path or embedded media: {path.name}:{i}"
        if cell.cell_type == "code":
            ast.parse(cell.source, filename=f"{path.name}:cell-{i}")
            assert cell.execution_count is None and cell.outputs == [], f"Stale output: {path.name}:{i}"
            count += 1
    print(f"OK {path.name}: schema, {count} Python cells, no saved outputs")

for path in [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]:
    for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
        if "://" not in target and not target.startswith("#"):
            assert (path.parent / target.split("#")[0]).exists(), f"Broken link in {path}: {target}"
print("OK local documentation links")

for path in (ROOT / "results").glob("*.json"):
    json.loads(path.read_text())
print("OK result JSON")
print("Not checked: dependency installation, model loading, audio decoding, training or end-to-end execution.")
