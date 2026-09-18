#!/usr/bin/env bash
# Build the verified writing slice; no model or data experiment is launched.
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"
OUT=${1:-outputs/tii_support}
mkdir -p "$OUT"
OUT=$(cd "$OUT" && pwd)
export TII_BUILD_OUTPUT="$OUT"
command -v pandoc >/dev/null
command -v xelatex >/dev/null
python - <<'PY'
import os
from pathlib import Path
import nbformat
from nbclient import NotebookClient
root=Path.cwd();out=Path(os.environ['TII_BUILD_OUTPUT'])
nb=nbformat.read(root/'paper/theory_main.ipynb',as_version=4)
NotebookClient(nb,timeout=120,kernel_name='python3',resources={'metadata':{'path':str(root)}}).execute()
nbformat.write(nb,out/'theory_main.executed.ipynb')
print('Finite theoretical witness executed; no learned model was trained.')
PY
python paper/figures/motivation.py --output-dir paper/figures
pandoc paper/main.md paper/related_work.md \
  --from markdown --standalone --citeproc \
  --bibliography literature/references.bib \
  --resource-path paper --pdf-engine xelatex \
  -V geometry:margin=22mm -V fontsize=10pt -V papersize=a4 \
  -V colorlinks=true --metadata reference-section-title=References \
  -o "$OUT/tii_frontmatter.pdf"
python -m unittest discover -s tests -p 'test_tii_support_frontmatter.py' -v
printf 'Writing preview: %s/tii_frontmatter.pdf\n' "$OUT"
