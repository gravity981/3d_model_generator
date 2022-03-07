import unittest
import sys
sys.path.append('../src')
sys.path.append('..')

from src import model_generator as modgen
import math


class TestModelGenerator(unittest.TestCase):

    def test_next_perfect_square(self):
        self.assertEqual(modgen.next_perfect_square(0), 1)
        self.assertEqual(modgen.next_perfect_square(1), 4)
        self.assertEqual(modgen.next_perfect_square(12), 16)
        self.assertEqual(modgen.next_perfect_square(102), 121)
        self.assertTrue(math.isnan(modgen.next_perfect_square(-1)))


if __name__ == '__main__':
    unittest.main()
