#!/bin/bash

sudo docker run -v $PWD:/work gravity981/3dgen \
  -m models \
  -c config/example_token.json \
  -o output/example_token