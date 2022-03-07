#!/usr/bin/env python3

import argparse
import os.path
import json

from command_executor import CommandExecutor

default_model_dir = '/models'
default_conf_file = '/conf/example_token.json'
default_output_dir = '/work/output/{name}'
default_output_format = 'stl'

# read command arguments
parser = argparse.ArgumentParser(prog='3dgen', description='Generate 3D Tokens')
parser.add_argument('-m', '--model-dir', type=str, required=False, help='Path to models directory')
parser.add_argument('-c', '--conf-file', type=str, required=False, help='Path to config file')
parser.add_argument('-o', '--output-dir', type=str, required=False, help='Path to output directory')
parser.add_argument('-f', '--output-format', type=str, required=False, help='Format of output files')
parser.add_argument('-t', '--thumbnails', action='store_true', required=False, help='Create thumbnails too')
parser.add_argument('-p', '--poster', action='store_true', required=False, help='Create poster with stitched thumbnails')
args = parser.parse_args()

if args.model_dir is None:
    args.model_dir = default_model_dir
elif not os.path.isdir(args.model_dir):
    print('model directory not found')
    exit(1)

if args.conf_file is None:
    args.conf_file = default_conf_file
elif not os.path.isfile(args.conf_file):
    print('conf file not found')
    exit(1)
try:
    with open(args.conf_file) as json_file:
        config = json.load(json_file)
except Exception as e:
    print('error reading file \"{}\": {}'.format(args.conf_file, e))
    exit(1)

if args.output_dir is None:
    args.output_dir = default_output_dir.format(name=config['name'])
else:
    args.output_dir = args.output_dir.strip('/')
try:
    os.makedirs(args.output_dir, exist_ok=False)
except FileExistsError as e:
    print('error creating output directory \"{}\": {}'.format(args.output_dir, e))
    exit(1)

if args.output_format is None:
    output_format = default_output_format
else:
    output_format = args.output_format

# generate openSCAD parameter sets
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

os.makedirs('{}/intermediate'.format(args.output_dir), exist_ok=True)
os.makedirs('{}/3d'.format(args.output_dir), exist_ok=True)
if args.thumbnails:
    os.makedirs('{}/thumbnail'.format(args.output_dir), exist_ok=True)

generated_config_filepath = '{}/intermediate/openscad.json'.format(args.output_dir)
with open(generated_config_filepath, 'w') as fp:
    json.dump(openscad_config, fp, indent=2)
scad_file = '{}/{}'.format(args.model_dir, config['model'])

# create 3d files with openscad and previously generated parameter sets
count = 0
for paramset in openscad_config['parameterSets'].keys():
    if not CommandExecutor.generate_3d_model(args.output_dir, paramset, output_format, generated_config_filepath, scad_file):
        exit(1)
    if args.thumbnails:
        if not CommandExecutor.generate_thumbnail(args.output_dir, paramset, generated_config_filepath, scad_file):
            exit(1)
    count += 1
print('created {} file(s)'.format(count))

# stitch thumbnails together to a poster
if args.thumbnails and args.poster:
    columns = CommandExecutor.next_perfect_square(count)
    CommandExecutor.generate_poster(columns, args.output_dir)
