#!/usr/bin/env bash
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed"
    exit
fi
if [ ! -d $(pwd)"/venv" ]; then
    sudo apt install python3-venv -y
    python3 -m venv $(pwd)"/venv"
    source $(pwd)"/venv/bin/activate"
    pip install -r $(pwd)"/requirements.txt"
fi
source $(pwd)"/venv/bin/activate"
./app.py $@
