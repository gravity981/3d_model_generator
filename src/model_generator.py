#!/usr/bin/env python3

import argparse
import os.path
import json
import math
import random
import string
from system_commands import SystemCommands


class Config:
    pass


def next_perfect_square(n: int) -> int:
    if n < 0:
        return math.nan
    next_n = math.floor(math.sqrt(n)) + 1
    return next_n * next_n


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choices(chars, k=size))


def init_generator(args) -> Config:
    default_model_dir = '/models'
    default_conf_file = '/conf/example_token.json'
    default_output_dir = '/work/output/{name}'
    default_output_format = 'stl'
    config = Config()
    config.model_dir = args.model_dir
    if config.model_dir is None:
        config.model_dir = default_model_dir
    elif not os.path.isdir(config.model_dir):
        print('model directory not found')
        raise NotADirectoryError(config.model_dir)

    if args.conf_file is None:
        args.conf_file = default_conf_file
    elif not os.path.isfile(args.conf_file):
        print('conf file not found')
        raise FileNotFoundError(args.conf_file)
    with open(args.conf_file) as json_file:
        config.data = json.load(json_file)

    config.output_dir = args.output_dir
    if config.output_dir is None:
        config.output_dir = default_output_dir.format(name=config.data['name'])
    # else:
    #    config.output_dir = config.output_dir.strip('/')

    os.makedirs(config.output_dir, exist_ok=False)

    if args.output_format is None:
        config.output_format = default_output_format
    else:
        config.output_format = args.output_format

    config.thumbnails = args.thumbnails
    config.poster = args.poster
    return config


def generate_openscad_parametersets(config: Config) -> dict:
    openscad_config = dict()
    openscad_config['fileFormatVersion'] = '1'
    openscad_config['parameterSets'] = dict()
    for geometry in config.data['geometries']:
        for decal in config.data['decals']:
            if 'name' in decal.keys():
                decal_text = decal['name']
            elif 'decal_text' in decal.keys():
                decal_text = decal['decal_text']
                decal['name'] = decal_text
            else:
                decal_text = id_generator()
                decal['name'] = decal_text
            if 'name' in geometry.keys():
                geometry_name = geometry['name']
            else:
                geometry_name = id_generator()
                geometry['name'] = geometry_name
            parameterset_name = '{}_{}'.format(geometry_name, decal_text)
            openscad_config['parameterSets'][parameterset_name] = dict()
            # append global config to paramset
            for k, v in config.data['global'].items():
                openscad_config['parameterSets'][parameterset_name][k] = v
            # append geometry config to paramset
            for k, v in geometry.items():
                if k != 'name':
                    openscad_config['parameterSets'][parameterset_name][k] = v
            # append decal config to paramset
            for k, v in decal.items():
                if k != 'name':
                    openscad_config['parameterSets'][parameterset_name][k] = v
    return openscad_config


def main():
    # read command arguments
    parser = argparse.ArgumentParser(prog='3dgen', description='Generate 3D Tokens')
    parser.add_argument('-m', '--model-dir', type=str, required=False, help='Path to models directory')
    parser.add_argument('-c', '--conf-file', type=str, required=False, help='Path to config file')
    parser.add_argument('-o', '--output-dir', type=str, required=False, help='Path to output directory')
    parser.add_argument('-f', '--output-format', type=str, required=False, help='Format of output files')
    parser.add_argument('-t', '--thumbnails', action='store_true', required=False, help='Create thumbnails too')
    parser.add_argument('-p', '--poster', action='store_true', required=False,
                        help='Create poster with stitched thumbnails')
    args = parser.parse_args()

    try:
        config = init_generator(args)
    except Exception as e:
        print('error while initialising generator: {}'.format(e))
        return False

    openscad_config = generate_openscad_parametersets(config)

    os.makedirs('{}/intermediate'.format(config.output_dir), exist_ok=True)
    os.makedirs('{}/3d'.format(config.output_dir), exist_ok=True)
    if config.thumbnails:
        os.makedirs('{}/thumbnail'.format(config.output_dir), exist_ok=True)

    generated_config_filepath = '{}/intermediate/openscad.json'.format(config.output_dir)
    with open(generated_config_filepath, 'w') as fp:
        json.dump(openscad_config, fp, indent=2)
    scad_file = '{}/{}'.format(config.model_dir, config.data['model'])

    # create 3d files with openscad and previously generated parameter sets
    count = 0
    for paramset in openscad_config['parameterSets'].keys():
        if not SystemCommands.generate_3d_model(config.output_dir, paramset, config.output_format,
                                                generated_config_filepath, scad_file):
            exit(1)
        if config.thumbnails:
            if not SystemCommands.generate_thumbnail(config.output_dir, paramset, generated_config_filepath, scad_file):
                exit(1)
        count += 1
    print('created {} file(s)'.format(count))

    # stitch thumbnails together to a poster
    if config.thumbnails and config.poster:
        columns = math.sqrt(next_perfect_square(count))
        SystemCommands.generate_poster(columns, config.output_dir)
    return True


if __name__ == '__main__':
    if not main():
        exit(1)
    exit(0)
