# 3D Token Generator
This project is about generating parametric tokens for 3D printing. Tokens can be used for example on shopping trolleys.

# Prerequisites
* install the following tools on your linux system
  * python3
  * OpenSCAD

# Usage
1. execute `install_fonts.sh`, this will install the required font
2. execute `create_all_tokens.sh`, this will create tokens based on `all_tokens.json`
3. As an alternative, call `python3 token_generator.py -s token_3d.scard -c CONFIG_FILE` with your own `CONFIG_FILE`

# Remarks
Tested with Ubuntu 18, python 3.6.9 and OpenSCAD version 2021.01
