#!/usr/bin/env bash
# Regenerate the styled HTML resume from the markdown source.
set -euo pipefail

cd "$(dirname "$0")"
python3 md_to_html.py Geoffrey_Dagley_Resume_2.md Geoffrey_Dagley_Resume_2.html
