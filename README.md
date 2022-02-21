# 3D Model Generator
This project is about generating parametric 3D models. The generated files can be processed with a slicer and then sent to a 3D printer. 

![latest version](https://img.shields.io/github/v/release/gravity981/3d_model_generator)

## Tokens
Tokens can be used for example in shopping trolleys.

<img src="example.png" alt="example token" width="200"/>


# Releases
You can download the latest package with stl files from the release section. If you want to build the files on your own or want to modify something, please read on.


# Prerequisites
A Linux Docker environemnt is required to use the 3d model generator

# Usage
1. `docker pull gravity981/3dgen`
2. `sudo docker run -ti -v /path/to/git/repo:/work gravity981/3dgen`
3. on the docker shell: `xvfb-run -a scripts/generate_all_tokens.sh`

Have a look at [default_token.json](config/default_token.json) to see the possible parameters which can be configured. Change it according to your needs.

The output of the generator is one or more stl files. In order to 3d-print the tokens the stl files have to be processed with a slicer.


# Remarks
Tested with Ubuntu 18, python 3.6.9 and OpenSCAD version 2021.01


# Contribute
Have a look at [all_tokens.json](config/all_tokens.json). Open a PR to extend this json file with the config you want to add.
