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

    @unittest.skip('unreliable, existing output_dir path')
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
        self.assertRaises(FileExistsError, modgen.init_generator, args)

    def test_generate_openscad_parametersets_empty_config(self):
        config = modgen.Config()
        config.data = dict()
        config.data['geometries'] = dict()
        parametersets = modgen.generate_openscad_parametersets(config)
        self.assertIn('fileFormatVersion', parametersets)
        self.assertIn('parameterSets', parametersets)


if __name__ == '__main__':
    unittest.main()
