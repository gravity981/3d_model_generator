#!/bin/bash

sudo docker run -v $PWD:/work gravity981/3dgen \
  -m models \
  -c config/all_tokens.json \
  -o output/all_tokens \
  --thumbnails \
  --poster
