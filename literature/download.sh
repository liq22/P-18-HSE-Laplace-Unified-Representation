#!/usr/bin/env bash
set -euo pipefail

mkdir -p pdfs

download() {
  local url="$1"
  local output="$2"
  curl -L --fail --retry 3 --connect-timeout 20 "$url" -o "pdfs/$output"
}

download https://arxiv.org/pdf/2605.19805 LLapDiff.pdf
download https://arxiv.org/pdf/2206.04843 Neural_Laplace.pdf
download https://arxiv.org/pdf/2210.02747 Flow_Matching.pdf
download https://arxiv.org/pdf/2302.00482 OT_CFM.pdf
download https://arxiv.org/pdf/2303.08797 Stochastic_Interpolants.pdf
download https://arxiv.org/pdf/2011.13456 Score_SDE.pdf
download https://arxiv.org/pdf/1608.06019 Domain_Separation_Networks.pdf

echo "Downloaded open-access PDFs to literature/pdfs/. The directory is Git-ignored."
