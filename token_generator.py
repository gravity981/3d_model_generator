import argparse
import os.path
import json
import subprocess

# read command arguments
parser = argparse.ArgumentParser(description='Generate 3D Tokens')
parser.add_argument('-s', '--scad-file', type=str, required=True, help='Path to SCAD file')
parser.add_argument('-c', '--conf-file', type=str, required=True, help='Path to config file')
args = parser.parse_args()
if not os.path.isfile(args.scad_file):
    print('scad file not found')
    exit(1)
if not os.path.isfile(args.conf_file):
    print('conf file not found')
    exit(1)

# generate openSCAD parameter sets
try:
    with open(args.conf_file) as json_file:
        config = json.load(json_file)
except Exception as e:
    print('error reading file \"{}\": {}'.format(args.conf_file, e))
    exit(1)
openscad_config = dict()
openscad_config['fileFormatVersion'] = '1'
openscad_config['parameterSets'] = dict()
for token in config['tokens']:
    for decal in config['decals']:
        if 'decal_name' in decal.keys():
            decal_text = decal['decal_name']
        else:
            decal_text = decal['decal_text']
        parameterset_name = '{}_{}'.format(token['token_name'], decal_text)
        openscad_config['parameterSets'][parameterset_name] = dict()
        for k, v in token.items():
            openscad_config['parameterSets'][parameterset_name][k] = v
        for k, v in config['keyring_hole'].items():
            openscad_config['parameterSets'][parameterset_name][k] = v
        for k, v in decal.items():
            openscad_config['parameterSets'][parameterset_name][k] = v
os.makedirs("generated", exist_ok=True)
generated_config_filepath = 'generated/openscad.json'
with open(generated_config_filepath, 'w') as fp:
    json.dump(openscad_config, fp, indent=2)

# create stl files with openscad and previously generated parameter sets
os.makedirs("output", exist_ok=True)
try:
    for paramset in openscad_config['parameterSets'].keys():
        openscad_command = 'openscad -o output/{}.stl -p {} -P {} {}'.format(paramset, generated_config_filepath,
                                                                        paramset, args.scad_file)
        command_tokens = openscad_command.split(' ')
        proc = subprocess.run(command_tokens)
        proc.check_returncode()
except Exception as e:
    print('error executing command: {}'.format(e))
    exit(1)
