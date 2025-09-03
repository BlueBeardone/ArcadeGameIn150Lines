@echo off
pip install pygame pygbag
pygbag --build snake_game.py
xcopy index.html build\web\index.html /Y