#!/bin/sh
# Build the Overleaf/CMT source package of the ICDE manuscript and verify it compiles in a clean directory.
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
OUT=${1:-$ROOT/submission_icde}
TMP=$(mktemp -d)
mkdir -p "$TMP/src"
cd "$ROOT/paper_icde"
cp -r main.tex title.tex numbers.tex numbers_icde.tex references_verified.bib IEEEtran.cls IEEEtran.bst sections tables figs "$TMP/src/"
cd "$TMP/src"
pdflatex -interaction=nonstopmode main >/dev/null; bibtex main >/dev/null; pdflatex -interaction=nonstopmode main >/dev/null; pdflatex -interaction=nonstopmode main >/dev/null
grep -q "^!" main.log && { echo "LaTeX errors"; exit 1; }
cp main.pdf "$OUT/CaliberGraph_ICDE2027.pdf"
rm -f main.aux main.log main.out main.blg main.pdf
cp main.bbl main.bbl.keep 2>/dev/null || true
rm -f main.bbl.keep
cd "$TMP/src" && rm -f "$OUT/CaliberGraph_ICDE_overleaf.zip" && zip -qr "$OUT/CaliberGraph_ICDE_overleaf.zip" .
echo "built: $(pdfinfo "$OUT/CaliberGraph_ICDE2027.pdf" | grep Pages)"
rm -rf "$TMP"
