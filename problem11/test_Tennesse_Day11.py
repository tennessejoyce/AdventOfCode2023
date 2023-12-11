import unittest
from Tennesse_Day11 import expand_1d, expand_2d


class TestExpand1D(unittest.TestCase):
    def test_expand_1d(self):
        x = [0, 1, 2, 2, 4, 4, 4, 4, 5, 7, 7]
        expected_output = [0, 1, 2, 2, 5, 5, 5, 5, 6, 9, 9]
        self.assertEqual(expand_1d(x), expected_output)


class TestExpand2D(unittest.TestCase):
    def test_expand_2d(self):
        coordinates = [
            (0, 0),
            (1, 1),
            (2, 2),
            (2, 3),
            (4, 4),
            (4, 6),
            (4, 6),
            (5, 7),
            (7, 7),
        ]
        expected_output = [
            (0, 0),
            (1, 1),
            (2, 2),
            (2, 3),
            (5, 4),
            (5, 7),
            (5, 7),
            (6, 8),
            (9, 8),
        ]
        self.assertEqual(expand_2d(coordinates), expected_output)


if __name__ == "__main__":
    unittest.main()
