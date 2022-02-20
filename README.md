# 3D Token Generator
This project is about generating parametric tokens for 3D printing. Tokens can be used for example in shopping trolleys.

<img src="example.png" alt="example token" width="200"/>

# Prerequisites
install the following tools on your linux system
* python3
* OpenSCAD
* optional: meshlab

# Usage
1. execute `install_fonts.sh`, this will install the required default font
2. execute `create_all_tokens.sh`, this will create tokens based on `all_tokens.json`
3. As an alternative, call `python3 token_generator.py -s token_3d.scard -c CONFIG_FILE` with your own `CONFIG_FILE`

Have a look at [default_token.json]() to see the possible parameters which can be configured. Change it according to your needs.

The output of the generator is one or more stl files. In order to 3d-print the tokens the stl files have to be processed with a slicer.
# Remarks
Tested with Ubuntu 18, python 3.6.9 and OpenSCAD version 2021.01

# Contribute
Have a look at [all_tokens.json](). Open a PR to extend this json file with the config you want to add.
