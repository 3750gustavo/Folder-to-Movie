#!/bin/bash

VENV_DIR="./.venv"
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    ./install.sh
fi

source "$VENV_DIR/bin/activate"
python3 image_folder_to_movie.py