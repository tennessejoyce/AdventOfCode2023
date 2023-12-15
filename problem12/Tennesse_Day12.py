"""
Day 12: Hot Springs
https://adventofcode.com/2023/day/12
"""
import logging
from utilities import run_aoc
import itertools
import math
import numpy as np
from tqdm import tqdm
from functools import lru_cache
from enum import Enum

FOLDS = 5


def run_part1(input_text: str) -> int:
    records, groups = parse_input(input_text)
    total_options = 0
    for record, group in tqdm(zip(records, groups), total=len(records)):
        problem = SpringCountingProblem(record, group)
        logging.debug(problem.candidate_starts)
        num_options = problem.count_all()
        logging.debug(f"{record}, {group} -> {num_options}")
        total_options += num_options
    return total_options


def run_part2(input_text: str) -> int:
    records, groups = parse_input(input_text)
    total_options = 0
    for record, group in tqdm(zip(records, groups), total=len(records)):
        problem = SpringCountingProblem(unfold(record, FOLDS), group * FOLDS)
        num_options = problem.count_all()
        logging.debug(f"{record}, {group} -> {num_options}")
        total_options += num_options
    return total_options


def parse_input(input_text: str) -> tuple[list[int], list[int]]:
    records = []
    groups = []
    for line in input_text.splitlines():
        r, g = line.split()
        records.append(parse_records(r))
        groups.append([int(c) for c in g.split(",")])
    return records, groups


DAMAGED = 1
UNDAMAGED = 2
UNKNOWN = 3

STATE_MAP = {"#": DAMAGED, ".": UNDAMAGED, "?": UNKNOWN}
MAYBE_DAMAGED = [DAMAGED, UNKNOWN]
MAYBE_UNDAMAGED = [UNDAMAGED, UNKNOWN]


def parse_records(s: str):
    return [STATE_MAP[c] for c in s]


def cumsum_with_zero(x):
    return np.insert(np.cumsum(x), 0, 0)


def unfold(results, folds):
    times_5 = (results + [2]) * folds
    return times_5[:-1]


class SpringCountingProblem:
    def __init__(self, records: list[int], groups: list[int]):
        self.records = np.array(records)
        self.groups = groups
        self.cumulative_damaged = cumsum_with_zero(self.records == DAMAGED)
        self.cumulative_undamaged = cumsum_with_zero(self.records == UNDAMAGED)
        self.cumulative_unknown = cumsum_with_zero(self.records == UNKNOWN)
        self.candidate_starts = self.get_candidate_starts()

    def num_damaged(self, m1: int, m2: int) -> int:
        return self.cumulative_damaged[m2] - self.cumulative_damaged[m1]

    def num_undamaged(self, m1: int, m2: int) -> int:
        return self.cumulative_undamaged[m2] - self.cumulative_undamaged[m1]

    def num_unknown(self, m1: int, m2: int) -> int:
        return self.cumulative_unknown[m2] - self.cumulative_unknown[m1]

    def prune(self, m1: int, m2: int, n1: int, n2: int) -> bool:
        """Quickly check if a subproblem is unsolvable, based on the
        number of damaged and unknown records.
        """
        num_damaged = self.num_damaged(m1, m2)
        num_unknown = self.num_unknown(m1, m2)
        num_undamaged = self.num_undamaged(m1, m2)
        num_damaged_from_groups = sum(self.groups[n1:n2])
        return (
            num_damaged <= num_damaged_from_groups <= num_damaged + num_unknown
        ) and (num_unknown + num_undamaged >= n2 - n1 - 1)

    def prune_split_left(self, m: int, n: int, num_damaged: int) -> bool:
        """Quickly check if we can split on this position, based on whether
        the left problem passes the pruning check.
        """
        if m <= 1:
            return n == 0
        return self.prune(0, m - 1, 0, n)

    def prune_split_right(self, m: int, n: int, num_damaged: int) -> bool:
        """Quickly check if we can split on this position, based on whether
        the right problem passes the pruning check.
        """
        m_end = m + num_damaged
        if m_end >= len(self.records) - 1:
            return n == len(self.groups) - 1
        return self.prune(m_end + 1, len(self.records), n + 1, len(self.groups))

    def prune_split(self, m: int, n: int, num_damaged: int) -> bool:
        """Quickly check if we can split on this position, based on whether
        the left and right problems pass the pruning check.
        """
        return self.prune_split_left(m, n, num_damaged) and self.prune_split_right(
            m, n, num_damaged
        )

    def can_start_at(self, m, num_damaged):
        """Check if a sequence of exactly 'num_damaged' damaged springs can
        start at position m in the records. It also needs to be terminated
        by an undamaged spring on both sides.
        """
        if (m > 0) and (self.records[m - 1] == DAMAGED):
            return False
        m_end = m + num_damaged - 1
        if m_end > len(self.records) - 1:
            return False
        if (m_end < len(self.records) - 1) and (self.records[m_end + 1] == DAMAGED):
            return False
        for i in range(m, m_end + 1):
            if self.records[i] not in MAYBE_DAMAGED:
                return False
        return True

    def get_candidate_starts(self):
        """Get the candidate starting positions for a damaged sequence"""
        lengths = sorted(list(set(self.groups)))
        candidate_starts_by_length = {num_damaged: [] for num_damaged in lengths}
        for num_damaged in lengths:
            for m in range(len(self.records)):
                if self.can_start_at(m, num_damaged):
                    candidate_starts_by_length[num_damaged].append(m)
        candidate_starts = [
            [
                m
                for m in candidate_starts_by_length[num_damaged]
                if self.prune_split(m, n, num_damaged)
            ]
            for n, num_damaged in enumerate(self.groups)
        ]
        return candidate_starts

    def upper_bound(self) -> int:
        """Get an upper bound on the number of options"""
        return math.prod([len(c) for c in self.candidate_starts])

    @lru_cache(maxsize=1000)
    def direct_count(self, m1: int, m2: int, n1: int, n2: int) -> int:
        """Count the number of options for a record"""
        return count_options(self.records[m1:m2], self.groups[n1:n2])

    def recursive_count(self, m1: int, m2: int, n1: int, n2: int) -> int:
        """Count the number of options for a record"""
        if not self.prune(m1, m2, n1, n2):
            logging.debug(f"Pruned: {m1}, {m2}, {n1}, {n2}")
            return 0
        if (m2 - m1) < 8 or n1 == n2:
            logging.debug(f"Solving directly: {m1}, {m2}, {n1}, {n2}")
            return self.direct_count(m1, m2, n1, n2)
        n_split = (n1 + n2) // 2
        total_options = 0
        for m_split in self.candidate_starts[n_split]:
            if m_split < m1 or m_split >= m2:
                continue
            logging.debug(f"Trying split: {m_split}, {n_split}")
            m_split_end = m_split + self.groups[n_split]
            if m_split - 1 <= m1:
                left_options = 1
            else:
                logging.debug(f"Recursing left: {m1}, {m_split-1}, {n1}, {n_split}")
                left_options = self.recursive_count(m1, m_split - 1, n1, n_split)
            if m_split_end >= m2 - 1:
                right_options = 1
            else:
                n_new = min(n2 - 1, n_split + 1)
                logging.debug(
                    f"Recursing right: {m_split_end + 1}, {m2}, {n_new}, {n2}"
                )
                right_options = self.recursive_count(m_split_end + 1, m2, n_new, n2)
            logging.debug(
                "Found options %d * %d for split %d",
                left_options,
                right_options,
                m_split,
            )
            total_options += left_options * right_options
        logging.debug(
            "Found %d options for %d, %d, %d, %d", total_options, m1, m2, n1, n2
        )
        return total_options

    def count_all(self) -> int:
        """Count the number of options for a record"""
        return self.recursive_count(0, len(self.records), 0, len(self.groups))


def count_options(record, group) -> int:
    """Count the number of options for a record"""
    record_copy = record.copy()
    num_damaged_unknowns = sum(group) - np.sum(record_copy == DAMAGED)
    if num_damaged_unknowns == 0:
        return 1
    elif num_damaged_unknowns < 0:
        return 0
    unknown_idx = np.where(record_copy == UNKNOWN)[0]
    if len(unknown_idx) < num_damaged_unknowns:
        return 0
    num_options = 0
    for damaged_idx in itertools.combinations(unknown_idx, num_damaged_unknowns):
        record_copy[unknown_idx] = UNDAMAGED
        record_copy[list(damaged_idx)] = DAMAGED
        new_groups = get_group_sizes(record_copy)
        if new_groups == group:
            num_options += 1
    return num_options


def get_group_sizes(record: list[bool]) -> list[int]:
    """Get the group sizes from a record"""
    group_sizes = []
    group_size = 0
    for code in record:
        if code == DAMAGED:
            group_size += 1
        elif group_size > 0:
            group_sizes.append(group_size)
            group_size = 0
    if group_size > 0:
        group_sizes.append(group_size)
    return group_sizes


# def count_options_recursive(record, group) -> int:
#     """Count the number of options for a record"""
#     if len(record) < 8:
#         return count_options(record, group)
#     split_idx = len(record) // 2
#     records_left = record[:split_idx]
#     records_right = record[split_idx:]
#     can_split = records_left[-1] in [1, 2] and records_right[0] in [1, 2]
#     if can_split:
#         records_left_split = records_left[:-1] + [1]
#         records_right_split = [1] + records_right[1:]
#     total_options = 0
#     min_left, max_left = get_damaged_range2(records_left, records_right, sum(group))
#     for num_left in range(min_left, max_left + 1):
#         left_groups, right_groups, is_split = split_groups(group, num_left)
#         if is_split:
#             if not can_split:
#                 continue
#             # If the group is split, we need to enforce that it continues
#             # in the right half.
#             left = records_left_split
#             right = records_right_split
#         else:
#             left = records_left
#             right = records_right
#         options_left = count_options_recursive(left, left_groups)
#         options_right = count_options_recursive(right, right_groups)
#         logging.debug(
#             f"{left}, {right}, {left_groups}, {right_groups} -> {options_left}, {options_right}"
#         )
#         total_options += options_left * options_right
#     return total_options


# def split_groups(groups, num_left):
#     left_groups = []
#     right_groups = []
#     remaining_left = num_left
#     is_split = False
#     for g in groups:
#         if g <= remaining_left:
#             left_groups.append(g)
#             remaining_left -= g
#         else:
#             if remaining_left > 0:
#                 left_groups.append(remaining_left)
#                 right_groups.append(g - remaining_left)
#                 is_split = True
#             else:
#                 is_split = False
#             break
#     right_groups.extend(groups[len(left_groups) :])
#     return left_groups, right_groups, is_split


# def get_damaged_range(records):
#     num_damaged = sum([1 for r in records if r == 1])
#     num_unknown = sum([1 for r in records if r == 2])
#     return num_damaged, num_damaged + num_unknown


# def get_damaged_range2(left, right, num_groups):
#     left_min, left_max = get_damaged_range(left)
#     right_min, right_max = get_damaged_range(right)
#     min_damaged = max(left_min, num_groups - right_max)
#     max_damaged = min(left_max, num_groups - right_min)
#     return min_damaged, max_damaged


if __name__ == "__main__":
    run_aoc(run_part1, run_part2)
