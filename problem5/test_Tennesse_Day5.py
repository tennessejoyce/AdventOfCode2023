import unittest
from Tennesse_Day5 import map_int, Interval, map_intervals, MapRow


class TestApplyMap(unittest.TestCase):
    def test_single_map(self):
        m = [MapRow(Interval(10, 11), -5)]
        self.assertEqual(map_int(8, m), 8)  # Number not in the range of the map
        self.assertEqual(map_int(9, m), 9)  # Number not in the range of the map
        self.assertEqual(map_int(10, m), 5)  # Number in the range of the map
        self.assertEqual(map_int(11, m), 6)  # Number in the range of the map
        self.assertEqual(map_int(12, m), 12)  # Number not in the range of the map

    def test_multiple_maps(self):
        m = [MapRow(Interval(10, 11), -5), MapRow(Interval(15, 19), 5)]
        self.assertEqual(map_int(8, m), 8)  # Number not in the range of the map
        self.assertEqual(map_int(9, m), 9)  # Number not in the range of the map
        self.assertEqual(map_int(10, m), 5)  # Number in the range of the map
        self.assertEqual(map_int(11, m), 6)  # Number in the range of the map
        self.assertEqual(map_int(12, m), 12)  # Number not in the range of the map
        self.assertEqual(map_int(13, m), 13)  # Number not in the range of the map
        self.assertEqual(map_int(14, m), 14)  # Number not in the range of the map
        self.assertEqual(map_int(15, m), 20)  # Number not in the range of the map
        self.assertEqual(map_int(16, m), 21)  # Number not in the range of the map
        self.assertEqual(map_int(19, m), 24)  # Number not in the range of the map
        self.assertEqual(map_int(20, m), 20)  # Number not in the range of the map
        self.assertEqual(map_int(30, m), 30)  # Number not in the range of the map


class TestInterval(unittest.TestCase):
    def test_zero_length_interval(self):
        interval = Interval(5, 5)
        self.assertFalse(bool(interval))

    def test_nonzero_length_interval(self):
        interval = Interval(5, 7)
        self.assertTrue(bool(interval))


class TestMapIntervals(unittest.TestCase):
    def test_map_intervals(self):
        intervals = [Interval(5, 10)]
        rows = [MapRow(Interval(7, 8), 20)]
        mapped_intervals = map_intervals(intervals, rows)
        self.assertEqual(
            mapped_intervals, [Interval(5, 6), Interval(9, 10), Interval(27, 28)]
        )


if __name__ == "__main__":
    unittest.main()
