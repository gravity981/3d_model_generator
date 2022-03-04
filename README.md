# 3D Model Generator
This project is about generating parametric 3D models. The generated files can be processed with a slicer and then sent to a 3D printer. 

![latest version](https://img.shields.io/github/v/release/gravity981/3d_model_generator)
![CI](https://github.com/gravity981/3d_model_generator/actions/workflows/continous_integration.yml/badge.svg)

## Tokens
Tokens can be used for example in shopping trolleys.

<img src="example.png" alt="example token" width="200"/>


# Releases
You can download the latest package with stl files from the release section. If you want to build the files on your own or want to modify something, please read on.


# Usage

## Example 1
As soon as you have installed docker on your system it's as simple as that:

`docker run -v /path/to/dir:/work gravity981/3dgen`

Docker is going to fetch the image automatically from dockerhub if it is not already installed on your computer. 
Then it is going tolaunch a container, generate an example model and save it to the directory `/path/to/dir/`.

## Example 2

```
docker run -v $PWD:/work gravity981/3dgen \
  -m models \
  -c config/all_tokens.json \
  -o output/all_tokens \
  --thumbnails \
  --poster
```
This will mount the current working directory (`$PWD`) to the docker container and use models & config from there.
Generated files are saved to your current working directory in output/all_tokens.


## Parameters
Optional parameters can be used to customize the generator output
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

To customize the generated model, have a look at [example_token.json](config/example_token.json). 
There you can see possible parameters which can be configured. 
> :information_source: Available parameters are specific to the selected model.


# Contribute
If you want to add a token have a look at [all_tokens.json](config/all_tokens.json). Open a PR to extend this json file with the config you want to add.

If you want to add another model. Open a PR with an additional scad file and an example config