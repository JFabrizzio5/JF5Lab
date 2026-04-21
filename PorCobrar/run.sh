#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"
if [ -d "./venv" ]; then
    source ./venv/bin/activate
    python3 commands.py
else
    python3 commands.py
fi
