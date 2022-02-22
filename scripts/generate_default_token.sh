#!/bin/bash

sudo docker run -v $PWD:/work gravity981/3dgen \
  -m models \
  -c config/default_token.json \
  -o output