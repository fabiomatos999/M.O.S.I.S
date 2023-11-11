#!/usr/bin/env bash
if ! command -v wkhtmltopdf &> /dev/null; then
    sudo apt install wkhtmltopdf -y
fi
if ! command -v ghostscript &> /dev/null; then
    sudo apt install ghostscript -y
fi
if ! command -v python3 &> /dev/null; then
    sudo apt install python3 python3-venv -y
fi
if ! command -v focus-stack &> /dev/null; then
    >&2 echo "FocusStack if not installed. Please download it from here: https://github.com/PetteriAimonen/focus-stack/releases/"
    exit 1
fi
if [ ! -d $(pwd)"/venv" ]; then
    python3 -m venv $(pwd)"/venv"
    source $(pwd)"/venv/bin/activate"
    pip install -r $(pwd)"/requirements.txt"
fi
source $(pwd)"/venv/bin/activate"
./app.py $@
