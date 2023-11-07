#!/usr/bin/env bash
if ! command wkhtmltopdf; then
    sudo apt install wkhtmltopdf -y
fi
if ! command ghostscript; then
    sudo apt install ghostscript -y
fi
if ! command python3; then
    sudo apt install python3 python3-venv -y
fi
if [ ! -d $(pwd)"/venv" ]; then
    python3 -m venv $(pwd)"/venv"
    source $(pwd)"/venv/bin/activate"
    pip install -r $(pwd)"/requirements.txt"
fi
source $(pwd)"/venv/bin/activate"
./app.py $@
