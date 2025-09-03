#!/bin/bash
pip install pygame pygbag
pygbag --build snake_game.py
# Copy the generated pygbag.js to the build directory
cp $(python -c "import pygbag; import os; print(os.path.join(os.path.dirname(pygbag.__file__), 'pygbag.js'))" build/web/
# Also copy any other necessary assets
cp -r assets/ build/web/ 2>/dev/null || true