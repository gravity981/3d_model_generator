#!/bin/bash

mkdir -p ~/.local/share/fonts
cp "$PWD/fonts/*.ttf" ~/.local/share/fonts
fc-cache -f -v
