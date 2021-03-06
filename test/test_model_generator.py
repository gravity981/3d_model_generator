import itertools
import json
import random
import unittest
from src import model_generator as modgen
import math
import os


class Args:
    pass


def get_test_suite_dir():
    return os.path.dirname(os.path.realpath(__file__))


class TestModelGenerator(unittest.TestCase):

    def test_calculate_next_perfect_squares(self):
        self.assertEqual(modgen.next_perfect_square(0), 1)
        self.assertEqual(modgen.next_perfect_square(1), 4)
        self.assertEqual(modgen.next_perfect_square(12), 16)
        self.assertEqual(modgen.next_perfect_square(102), 121)
        self.assertTrue(math.isnan(modgen.next_perfect_square(-1)))

    def test_init_generator_no_model_dir(self):
        args = Args()
        args.model_dir = 'asd'
        self.assertRaises(NotADirectoryError, modgen.init_generator, args)

    def test_init_generator_no_conf_file(self):
        args = Args()
        args.model_dir = None
        args.conf_file = None
        self.assertRaises(FileNotFoundError, modgen.init_generator, args)

    def test_init_generator_broken_config_file(self):
        args = Args()
        args.model_dir = None
        args.conf_file = os.path.join(get_test_suite_dir(), 'data/broken_config.json')
        args.output_dir = None
        self.assertRaises(KeyError, modgen.init_generator, args)

    def test_init_generator_output_dir_exists(self):
        args = Args()
        args.model_dir = None
        args.conf_file = os.path.join(get_test_suite_dir(), 'data/well_formed_config.json')
        args.output_dir = os.path.join(get_test_suite_dir(), 'data')
        self.assertRaises(FileExistsError, modgen.init_generator, args)

    def test_init_generator_happy_case(self):
        args = Args()
        args.model_dir = None
        args.conf_file = os.path.join(get_test_suite_dir(), 'data/well_formed_config.json')
        args.output_dir = os.path.join(get_test_suite_dir(), 'out')
        args.output_format = None
        args.thumbnails = None
        args.poster = None
        print(get_test_suite_dir())
        config = modgen.init_generator(args)
        self.assertIsInstance(config.model_dir, str)
        self.assertIsInstance(config.output_dir, str)
        self.assertIsInstance(config.data, dict)
        self.assertIsInstance(config.output_format, str)
        self.assertIsNone(config.thumbnails)
        self.assertIsNone(config.poster)

    def test_generate_openscad_parametersets_empty_config(self):
        config = modgen.Config()
        config.data = dict()
        config.data['layers'] = list()
        parametersets = modgen.generate_openscad_parametersets(config)
        self.assertIn('fileFormatVersion', parametersets)
        self.assertIn('parameterSets', parametersets)
        self.assertEqual(len(parametersets['parameterSets']), 0)

    def test_generate_openscad_parametersets_example_config(self):
        config = modgen.Config()
        config.data = dict()
        config.data['global'] = dict()
        config.data['global']['diameter'] = 5
        config.data['layers'] = list()
        config.data['layers'].append([{'height': 4}, {'height': 3}])
        config.data['layers'].append([{'text': 'hello'}, {'decal_text': 'world'}])
        random.seed(123)
        parametersets = modgen.generate_openscad_parametersets(config=config)
        self.assertEqual(len(parametersets['parameterSets']), 4)
        self.assertIn('BDOD6B_IAPDVC', parametersets['parameterSets'])
        self.assertEqual(parametersets['parameterSets']['BDOD6B_IAPDVC']['diameter'], 5)
        self.assertEqual(parametersets['parameterSets']['BDOD6B_IAPDVC']['height'], 4)
        self.assertEqual(parametersets['parameterSets']['BDOD6B_IAPDVC']['text'], 'hello')
        self.assertNotIn('name', parametersets['parameterSets']['BDOD6B_IAPDVC'])
        self.assertIn('BDOD6B_world', parametersets['parameterSets'])
        self.assertEqual(parametersets['parameterSets']['BDOD6B_world']['diameter'], 5)
        self.assertEqual(parametersets['parameterSets']['BDOD6B_world']['height'], 4)
        self.assertEqual(parametersets['parameterSets']['BDOD6B_world']['decal_text'], 'world')
        self.assertNotIn('name', parametersets['parameterSets']['BDOD6B_world'])
        self.assertIn('TL4FMM_IAPDVC', parametersets['parameterSets'])
        self.assertEqual(parametersets['parameterSets']['TL4FMM_IAPDVC']['diameter'], 5)
        self.assertEqual(parametersets['parameterSets']['TL4FMM_IAPDVC']['height'], 3)
        self.assertEqual(parametersets['parameterSets']['TL4FMM_IAPDVC']['text'], 'hello')
        self.assertNotIn('name', parametersets['parameterSets']['TL4FMM_IAPDVC'])
        self.assertIn('TL4FMM_world', parametersets['parameterSets'])
        self.assertEqual(parametersets['parameterSets']['TL4FMM_world']['diameter'], 5)
        self.assertEqual(parametersets['parameterSets']['TL4FMM_world']['height'], 3)
        self.assertEqual(parametersets['parameterSets']['TL4FMM_world']['decal_text'], 'world')
        self.assertNotIn('name', parametersets['parameterSets']['TL4FMM_world'])

    def test_generate_output_files_from_example_config(self):
        openscad_test_filepath = os.path.join(get_test_suite_dir(), 'data/well_formed_openscad.json')
        with open(openscad_test_filepath) as json_file:
            parametersets = json.load(json_file)
        config = modgen.Config()
        config.model_dir = '/models'
        config.data = dict()
        config.data['model'] = 'test.scad'
        config.output_dir = '/out'
        config.output_format = 'stl'
        config.thumbnails = True
        count, success = modgen.generate_output_files(config, parametersets['parameterSets'], openscad_test_filepath, True)
        self.assertTrue(success)
        self.assertEqual(count, 4)

    @classmethod
    def tearDownClass(cls):
        os.removedirs(os.path.join(get_test_suite_dir(), 'out'))


if __name__ == '__main__':
    unittest.main()
