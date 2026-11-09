"""Regenerate t1_starter.ipynb from the `# %%` cells of t1_starter.py (stdlib only)."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
INSTALL = "# Colab / fresh env only:\n%pip install -q anndata scipy numpy pandas veckit==0.1.2"


def cells(src: str):
    out = []
    for chunk in re.split(r"^# %%", src, flags=re.M)[1:]:
        head, _, body = chunk.partition("\n")
        if head.strip() == "[markdown]":
            md = "\n".join(l[2:] if l.startswith("# ") else l.lstrip("#") for l in body.strip().splitlines())
            out.append({"cell_type": "markdown", "metadata": {}, "source": md})
        else:
            out.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
                        "source": body.strip()})
    out.insert(1, {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": INSTALL})
    return out


def build() -> dict:
    return {"cells": cells((HERE / "t1_starter.py").read_text()), "nbformat": 4, "nbformat_minor": 5,
            "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}}}


if __name__ == "__main__":
    (HERE / "t1_starter.ipynb").write_text(json.dumps(build(), indent=1) + "\n")
    print("wrote t1_starter.ipynb")
