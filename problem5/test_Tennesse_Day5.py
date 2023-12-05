import unittest
from Tennesse_Day5 import apply_map


class TestApplyMap(unittest.TestCase):
    def test_single_map(self):
        m = [(5, 10, 2)]
        self.assertEqual(apply_map(8, m), 8)  # Number not in the range of the map
        self.assertEqual(apply_map(9, m), 9)  # Number not in the range of the map
        self.assertEqual(apply_map(10, m), 5)  # Number in the range of the map
        self.assertEqual(apply_map(11, m), 6)  # Number in the range of the map
        self.assertEqual(apply_map(12, m), 12)  # Number not in the range of the map

    def test_multiple_maps(self):
        m = [(5, 10, 2), (20, 15, 5)]
        self.assertEqual(apply_map(8, m), 8)  # Number not in the range of the map
        self.assertEqual(apply_map(9, m), 9)  # Number not in the range of the map
        self.assertEqual(apply_map(10, m), 5)  # Number in the range of the map
        self.assertEqual(apply_map(11, m), 6)  # Number in the range of the map
        self.assertEqual(apply_map(12, m), 12)  # Number not in the range of the map
        self.assertEqual(apply_map(13, m), 13)  # Number not in the range of the map
        self.assertEqual(apply_map(14, m), 14)  # Number not in the range of the map
        self.assertEqual(apply_map(15, m), 20)  # Number not in the range of the map
        self.assertEqual(apply_map(16, m), 21)  # Number not in the range of the map
        self.assertEqual(apply_map(19, m), 24)  # Number not in the range of the map
        self.assertEqual(apply_map(20, m), 20)  # Number not in the range of the map
        self.assertEqual(apply_map(30, m), 30)  # Number not in the range of the map


if __name__ == "__main__":
    unittest.main()
