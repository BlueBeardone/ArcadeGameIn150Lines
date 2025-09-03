#!/bin/bash
pip install pygame pygbag
pygbag --build snake_game.py

# Copy the pygbag.js file from the package installation
PYGBAG_JS_PATH=$(python -c "import pygbag; import os; print(os.path.join(os.path.dirname(pygbag.__file__), 'pygbag.js'))")
cp "$PYGBAG_JS_PATH" build/web/

# Copy index.html
cp index.html build/web/

# Create assets directory if it doesn't exist
mkdir -p build/web/assets