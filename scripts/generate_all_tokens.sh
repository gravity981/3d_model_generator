#!/bin/bash

xvfb-run -a python3 "$PWD/src/model_generator.py" \
  --model-dir "$PWD/models" \
  --conf-file "$PWD/config/all_tokens.json" \
  --output-dir "$PWD/output" \
  --thumbnails

montage -tile 11x0 -geometry +0+0 "$PWD/output/thumbnail/*.png" "$PWD/output/poster.png"
