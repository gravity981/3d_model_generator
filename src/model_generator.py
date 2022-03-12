#!/usr/bin/env python3

import argparse
import itertools
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

    os.makedirs(config.output_dir, exist_ok=False)

    if args.output_format is None:
        config.output_format = default_output_format
    else:
        config.output_format = args.output_format

    config.thumbnails = args.thumbnails
    config.poster = args.poster
    return config


def generate_layer_names_if_not_exist(config: Config):
    for layer in config.data['layers']:
        for layer_conf in layer:
            if 'name' not in layer_conf.keys():
                if 'decal_text' in layer_conf.keys():
                    layer_conf['name'] = layer_conf['decal_text']
                else:
                    layer_conf['name'] = id_generator()


def generate_openscad_parametersets(config: Config) -> dict:
    generate_layer_names_if_not_exist(config)
    parametersets = dict()
    parametersets['fileFormatVersion'] = '1'
    parametersets['parameterSets'] = dict()
    combinations = list(itertools.product(*config.data['layers']))
    for tup in combinations:
        if not tup:
            break
        tup_name = ''
        paramset = dict()
        for dic in tup:
            tup_name += dic['name'] + "_"
            paramset.update(dic)
            if 'global' in config.data.keys():
                paramset.update(config.data['global'])
            paramset.pop('name', None)
        tup_name = tup_name.rstrip('_')
        parametersets['parameterSets'][tup_name] = paramset
    return parametersets


def write_intermediate_files(output_dir: str, openscad_config: dict) -> str:
    os.makedirs('{}/intermediate'.format(output_dir), exist_ok=True)
    generated_config_filepath = '{}/intermediate/openscad.json'.format(output_dir)
    with open(generated_config_filepath, 'w') as fp:
        json.dump(openscad_config, fp, indent=2)
    return generated_config_filepath


def generate_output_files(config: Config, parametersets, parametersets_filepath, dry_run: bool = False) \
        -> (int, bool):
    scad_file = '{}/{}'.format(config.model_dir, config.data['model'])
    count = 0
    for paramset in parametersets.keys():
        if not SystemCommands.generate_3d_model(config.output_dir, paramset, config.output_format,
                                                parametersets_filepath, scad_file, dry_run):
            return 0, False
        if config.thumbnails:
            if not SystemCommands.generate_thumbnail(config.output_dir, paramset, parametersets_filepath,
                                                     scad_file, dry_run):
                return 0, False
        count += 1
    print('created {} 3d file(s)'.format(count))
    return count, True


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
    parametersets_filepath = write_intermediate_files(config.output_dir, openscad_config)

    # create 3d files with openscad and previously generated parameter sets
    count, success = generate_output_files(config, openscad_config['parameterSets'],
                                           parametersets_filepath)
    if not success:
        return False

    # stitch thumbnails together to a poster
    if config.thumbnails and config.poster:
        columns = math.sqrt(next_perfect_square(count))
        if not SystemCommands.generate_poster(columns, config.output_dir):
            return False

    return True


if __name__ == '__main__':
    if not main():
        exit(1)
    exit(0)
