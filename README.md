# 3D Model Generator
This project is about generating parametric 3D models. The generated files can be processed with a slicer and then sent to a 3D printer. 

![CI](https://github.com/gravity981/3d_model_generator/actions/workflows/continous_integration.yml/badge.svg)


## Tokens
Tokens can be used for example in shopping trolleys.

<img src="example.png" alt="example token" width="200"/>


## Model Package Releases
![latest version](https://img.shields.io/github/v/release/gravity981/3d_model_generator)

You can download the latest package with stl files from the github release section. If you want to build the files on your own or want to modify something, please read on.

## 3dgen Docker Image
https://hub.docker.com/r/gravity981/3dgen

![3dgen version](https://img.shields.io/docker/v/gravity981/3dgen)
![docker pulls](https://img.shields.io/docker/pulls/gravity981/3dgen)

# Usage

## Example 1
As soon as you have installed docker on your system it's as simple as that:

`docker run -v /path/to/dir:/work gravity981/3dgen`

Docker is going to fetch the image automatically from dockerhub if it is not already installed on your computer. 
Then it is going to launch a container, generate an example model and save it to the directory `/path/to/dir/`.

## Example 2

```
docker run -v $PWD:/work gravity981/3dgen \
  -c config/example_token.json \
  -o output/example_token \
  --thumbnails
```
This will mount the current working directory (`$PWD`) to the docker container to make it work with input/output files from there.
In this example the generated model file is saved to your current working directory under `output/example_token`.

To customize a model, have a look at [example_token.json](config/example_token.json). 
This file contains parameters which can be customized for the token model. 
Create your own copy of this file and pass it with the `-c` argument to the generator. 
Make sure it is located in the directory which is mounted to the docker container. 
> :information_source: Customizable parameters are specific to the selected model.

The options `--thumbnails` causes the generator to output an additionl picture (.png) of the model.


## Arguments
Optional Arguments can be passed to get more control over the generator output
```
usage: 3dgen [-h] [-m MODEL_DIR] [-c CONF_FILE] [-o OUTPUT_DIR]
             [-f OUTPUT_FORMAT] [-t] [-p]

Generate 3D Tokens

optional arguments:
  -h, --help            show this help message and exit
  -m MODEL_DIR, --model-dir MODEL_DIR
                        Path to models directory
  -c CONF_FILE, --conf-file CONF_FILE
                        Path to config file
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Path to output directory
  -f OUTPUT_FORMAT, --output-format OUTPUT_FORMAT
                        Format of output files
  -t, --thumbnails      Create thumbnails too
  -p, --poster          Create poster with stitched thumbnails
```

# Contribute
If you want to add a token have a look at [all_tokens.json](config/all_tokens.json). Open a PR to extend this json file with the config you want to add.

If you want to add another model. Open a PR with an additional scad file and an example config
