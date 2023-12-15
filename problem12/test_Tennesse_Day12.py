import unittest
import numpy as np
from Tennesse_Day12 import SpringCountingProblem, parse_records


class TestSpringCountingProblem(unittest.TestCase):
    def setUp(self):
        records = parse_records(".??..??...?##")
        groups = [1, 1, 3]
        self.problem = SpringCountingProblem(records, groups)

    def test_num_damaged(self):
        self.assertEqual(self.problem.num_damaged(0, 5), 0)
        self.assertEqual(self.problem.num_damaged(9, 12), 1)

    def test_num_undamaged(self):
        self.assertEqual(self.problem.num_undamaged(0, 5), 3)
        self.assertEqual(self.problem.num_undamaged(9, 12), 1)

    def test_num_unknown(self):
        self.assertEqual(self.problem.num_unknown(0, 5), 2)
        self.assertEqual(self.problem.num_unknown(9, 12), 1)

    def test_prune(self):
        self.assertTrue(self.problem.prune(0, 5, 0, 2))
        self.assertFalse(self.problem.prune(11, 13, 0, 2))
        self.assertFalse(self.problem.prune(0, 8, 0, 3))
        self.assertTrue(self.problem.prune(0, 13, 0, 3))
        self.assertFalse(self.problem.prune(8, 13, 0, 3))
        self.assertTrue(self.problem.prune(8, 13, 2, 3))

    def test_can_start_at(self):
        self.assertTrue(self.problem.can_start_at(1, 2))
        self.assertFalse(self.problem.can_start_at(1, 3))
        self.assertTrue(self.problem.can_start_at(10, 3))
        self.assertFalse(self.problem.can_start_at(9, 3))

    def test_get_candidate_starts(self):
        self.assertEqual(
            self.problem.candidate_starts,
            [[1, 2], [5, 6], [10]],
        )

    def test_count_all(self):
        self.assertEqual(
            self.problem.count_all(),
            4,
        )


if __name__ == "__main__":
    unittest.main()
