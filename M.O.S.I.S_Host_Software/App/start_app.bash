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
    sudo apt install git libopencv-dev build-essential -y
    git clone https://github.com/PetteriAimonen/focus-stack.git
    cd focus-stack
    make
    sudo make install
    cd ..
    rm -rf focus-stack
fi
if [ ! -d $(pwd)"/venv" ]; then
    python3 -m venv $(pwd)"/venv"
    source $(pwd)"/venv/bin/activate"
    pip install -r $(pwd)"/requirements.txt"
fi
mkdir static/Media
source $(pwd)"/venv/bin/activate"
./app.py $@
