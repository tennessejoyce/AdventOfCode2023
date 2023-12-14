import unittest
import numpy as np
from Tennesse_Day12 import (
    get_group_sizes,
    count_options,
    count_options_recursive,
    split_groups,
)


class TestSplitGroups(unittest.TestCase):
    def test_split_groups1(self):
        groups = [3, 1, 2, 4, 5]
        num_left = 6
        expected_left_groups = [3, 1, 2]
        expected_right_groups = [4, 5]
        expected_is_split = False
        left_groups, right_groups, is_split = split_groups(groups, num_left)
        self.assertEqual(left_groups, expected_left_groups)
        self.assertEqual(right_groups, expected_right_groups)
        self.assertEqual(is_split, expected_is_split)

    def test_split_groups2(self):
        groups = [3, 1, 2, 4, 5]
        num_left = 8
        expected_left_groups = [3, 1, 2, 2]
        expected_right_groups = [2, 5]
        expected_is_split = True
        left_groups, right_groups, is_split = split_groups(groups, num_left)
        self.assertEqual(left_groups, expected_left_groups)
        self.assertEqual(right_groups, expected_right_groups)
        self.assertEqual(is_split, expected_is_split)


class TestGetGroupSizes(unittest.TestCase):
    def test_get_group_sizes(self):
        record = np.array([0, 1, 1, 1, 0, 1, 0, 1, 1])
        expected_group_sizes = [3, 1, 2]
        self.assertEqual(get_group_sizes(record), expected_group_sizes)


class TestCountOptions(unittest.TestCase):
    def test_count_options1(self):
        record = np.array([2, 1, 1, 1, 2, 0, 1, 0, 2, 0, 2, 2, 0, 0, 1, 2, 2, 2, 0])
        group = [5, 1, 2, 1, 1]
        expected_options = 2
        self.assertEqual(count_options(record, group), expected_options)

    def test_count_options2(self):
        record = np.array([2, 2, 2, 2, 2, 2, 1, 1, 2, 0, 2])
        group = [1, 1, 2]
        expected_options = 6
        self.assertEqual(count_options(record, group), expected_options)


class TestCountOptionsRecursive(unittest.TestCase):
    def test_count_options1(self):
        record = np.array([2, 1, 1, 1, 2, 0, 1, 0, 2, 0, 2, 2, 0, 0, 1, 2, 2, 2, 0])
        group = [5, 1, 2, 1, 1]
        expected_options = 2
        self.assertEqual(count_options_recursive(record, group), expected_options)

    def test_count_options2(self):
        record = np.array([2, 2, 2, 2, 2, 2, 1, 1, 2, 0, 2])
        group = [1, 1, 2]
        expected_options = 6
        self.assertEqual(count_options_recursive(record, group), expected_options)


if __name__ == "__main__":
    unittest.main()
