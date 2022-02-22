#!/usr/bin/env python3

import argparse
import os.path
import json
import subprocess

# read command arguments
parser = argparse.ArgumentParser(description='Generate 3D Tokens')
parser.add_argument('-m', '--model-dir', type=str, required=True, help='Path to models directory')
parser.add_argument('-c', '--conf-file', type=str, required=True, help='Path to config file')
parser.add_argument('-o', '--output-dir', type=str, required=True, help='Path to output directory')
parser.add_argument('-f', '--output-format', type=str, required=False, help='Format of output files')
parser.add_argument('-t', '--thumbnails', action='store_true', required=False, help='Create thumbnails too')
parser.add_argument('-p', '--poster', action='store_true', required=False, help='Create poster with stitched thumbnails')
args = parser.parse_args()
if not os.path.isdir(args.model_dir):
    print('model directory not found')
    exit(1)
if not os.path.isfile(args.conf_file):
    print('conf file not found')
    exit(1)
if not os.path.isdir(args.output_dir):
    os.makedirs(args.output_dir)
if args.output_format is not None:
    output_format = args.output_format
else:
    output_format = 'stl'

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
for geometry in config['geometries']:
    for decal in config['decals']:
        if 'decal_name' in decal.keys():
            decal_text = decal['decal_name']
        else:
            decal_text = decal['decal_text']
        parameterset_name = '{}_{}'.format(geometry['token_name'], decal_text)
        openscad_config['parameterSets'][parameterset_name] = dict()
        # append global config to paramset
        for k, v in config['global'].items():
            openscad_config['parameterSets'][parameterset_name][k] = v
        # append geometry config to paramset
        for k, v in geometry.items():
            openscad_config['parameterSets'][parameterset_name][k] = v
        # append decal config to paramset
        for k, v in decal.items():
            openscad_config['parameterSets'][parameterset_name][k] = v

os.makedirs('{}/generated'.format(args.output_dir), exist_ok=True)
os.makedirs('{}/3d'.format(args.output_dir), exist_ok=True)
os.makedirs('{}/thumbnail'.format(args.output_dir), exist_ok=True)

generated_config_filepath = '{}/generated/openscad.json'.format(args.output_dir)
with open(generated_config_filepath, 'w') as fp:
    json.dump(openscad_config, fp, indent=2)
scad_file = '{}/{}'.format(args.model_dir, config['model'])
# create stl files with openscad and previously generated parameter sets
try:
    count = 0
    for paramset in openscad_config['parameterSets'].keys():
        openscad_command = 'openscad -o {}/3d/{}.{} -p {} -P {} {}'\
            .format(args.output_dir, paramset, output_format, generated_config_filepath, paramset, scad_file)
        proc = subprocess.run(openscad_command.split(' '), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        proc.check_returncode()
        print('created \"{}.{}\"'.format(paramset, output_format))
        if args.thumbnails:
            openscad_command = 'openscad -o {}/thumbnail/{}.png -p {} -P {} --imgsize=192,192 {}'\
                .format(args.output_dir, paramset, generated_config_filepath, paramset, scad_file)
            proc = subprocess.run(openscad_command.split(' '), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            proc.check_returncode()
            print('created \"{}.png\"'.format(paramset))
        count += 1
    print('created {} 3d file(s)'.format(count))
except Exception as e:
    print('error executing command: {}'.format(e))
    exit(1)

if args.thumbnails and args.poster:
    command = 'montage -tile {}x0 -geometry +0+0 {}/thumbnail/*.png {}/poster.png'.format(11, args.output_dir, args.output_dir)
    proc = subprocess.run(command.split(' '), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    proc.check_returncode()
    print('created \"poster.png\"')
