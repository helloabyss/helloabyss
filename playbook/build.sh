#!/usr/bin/env bash
# Build the playbook PDF: render from HTML, then stamp running feet.
set -euo pipefail
cd "$(dirname "$0")"
node build.mjs
python3 stamp.py
