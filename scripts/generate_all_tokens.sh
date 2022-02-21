#!/bin/bash

python3 "$PWD/src/model_generator.py" \
  --scad-file "$PWD/models/token_3d.scad" \
  --conf-file "$PWD/config/all_tokens.json" \
  --output-dir "$PWD/output" \
  --thumbnails
