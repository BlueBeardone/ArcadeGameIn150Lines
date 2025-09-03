#!/bin/bash
pip install pygame pygbag
pygbag --build snake_game.py
mkdir -p itch_build
cp -r build/web/* itch_build/
cp index.html itch_build/
cd itch_build && zip -r ../snake_game_itch.zip . && cd ..