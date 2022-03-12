#!/bin/bash

echo "test generate built-in example token"
model_generator_wrapper.sh -c /conf/example_token.json
test -d output/example_token/3d || exit 1
test -f output/example_token/3d/token_2CHF_star.stl || exit 1
test -d output/example_token/intermediate || exit 1
test -f output/example_token/intermediate/openscad.json || exit 1
rm -rf output
echo ""

echo "test generate built-in example token with thumbnail"
model_generator_wrapper.sh -c /conf/example_token.json -t
test -d output/example_token/3d || exit 1
test -f output/example_token/3d/token_2CHF_star.stl || exit 1
test -d output/example_token/intermediate || exit 1
test -f output/example_token/intermediate/openscad.json || exit 1
test -d output/example_token/thumbnail || exit 1
test -f output/example_token/thumbnail/token_2CHF_star.png || exit 1
rm -rf output
echo ""

echo "test generate built-in example token with thumbnail and poster"
model_generator_wrapper.sh -c /conf/example_token.json -t -p
test -d output/example_token/3d || exit 1
test -f output/example_token/3d/token_2CHF_star.stl || exit 1
test -d output/example_token/intermediate || exit 1
test -f output/example_token/intermediate/openscad.json || exit 1
test -d output/example_token/thumbnail || exit 1
test -f output/example_token/thumbnail/token_2CHF_star.png || exit 1
test -f output/example_token/poster.png || exit 1
rm -rf output