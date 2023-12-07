import unittest
from .Tennesse_Day6 import get_num_options1, get_num_options2


class TestGetNumOptions(unittest.TestCase):
    def test_get_num_options1(self):
        self.assertEqual(4, get_num_options1(7, 9))
        self.assertEqual(8, get_num_options1(15, 40))
        self.assertEqual(9, get_num_options1(30, 200))

    def test_get_num_options2(self):
        self.assertEqual(4, get_num_options2(7, 9))
        self.assertEqual(8, get_num_options2(15, 40))
        self.assertEqual(9, get_num_options2(30, 200))


if __name__ == "__main__":
    unittest.main()
