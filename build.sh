#!/bin/bash
pip install pygame pygbag
pygbag --build snake_game.py
cp "$(python -c "import pygbag; import os; print(os.path.join(os.path.dirname(pygbag.__file__), 'pygbag.js'))" build/web/
cp -r assets/ build/web/ 2>/dev/null || true