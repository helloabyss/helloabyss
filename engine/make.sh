#!/bin/sh
# THE ONE COMMAND
set -e
python3 build.py "${1:-out}"
NODE_PATH=/opt/node22/lib/node_modules node shoot.js "${1:-out}"
rm -f "${1:-out}"/*.html
echo "DONE -> ${1:-out}/"
