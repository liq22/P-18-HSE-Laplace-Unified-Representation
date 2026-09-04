#!/usr/bin/env bash
set -euo pipefail

mkdir -p pdfs

download() {
  curl -L --fail --retry 3 --connect-timeout 20 "$1" -o "pdfs/$2"
}

download https://arxiv.org/pdf/2605.19805 LLapDiff.pdf
download https://arxiv.org/pdf/2206.04843 Neural_Laplace.pdf
download https://arxiv.org/pdf/2107.03502 CSDI.pdf
download https://arxiv.org/pdf/2306.09368 Warpformer.pdf
download https://arxiv.org/pdf/2210.02747 Flow_Matching_future_work.pdf

echo "Downloaded open-access PDFs to literature/pdfs/; the directory is Git-ignored."
