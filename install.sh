#!/bin/bash

VENV_DIR="./.venv"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
echo "Environment setup complete. You can now run the application."