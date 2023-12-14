"""
Day 12: Hot Springs
https://adventofcode.com/2023/day/12
"""
import logging
from utilities import run_aoc
import itertools
import numpy as np
from tqdm import tqdm

CODE = ".#?"
FOLDS = 5


def run_part1(input_text: str) -> int:
    records, groups = parse_input(input_text)
    total_options = 0
    for record, group in tqdm(zip(records, groups), total=len(records)):
        num_options = count_options(record, group)
        logging.debug(f"{record}, {group} -> {num_options}")
        total_options += num_options
    return total_options


def run_part2(input_text: str) -> int:
    records, groups = parse_input(input_text)
    total_options = 0
    for record, group in tqdm(zip(records, groups), total=len(records)):
        num_options = count_options_recursive(unfold(record, FOLDS), group * FOLDS)
        logging.debug(f"{record}, {group} -> {num_options}")
        total_options += num_options
    return total_options


def parse_input(input_text: str) -> tuple[list[int], list[int]]:
    records = []
    groups = []
    for line in input_text.splitlines():
        r, g = line.split()
        records.append([CODE.index(c) for c in r])
        groups.append([int(c) for c in g.split(",")])
    return records, groups


def count_options(record, group) -> int:
    """Count the number of options for a record"""
    record_copy = np.array(record)
    num_damaged_unknowns = sum(group) - np.sum(record_copy == 1)
    if num_damaged_unknowns == 0:
        return 1
    elif num_damaged_unknowns < 0:
        return 0
    unknown_idx = np.where(record_copy == 2)[0]
    if len(unknown_idx) < num_damaged_unknowns:
        return 0
    num_options = 0
    for damaged_idx in itertools.combinations(unknown_idx, num_damaged_unknowns):
        record_copy[unknown_idx] = 0
        record_copy[list(damaged_idx)] = 1
        new_groups = get_group_sizes(record_copy)
        if new_groups == group:
            num_options += 1
    return num_options


def count_options_recursive(record, group) -> int:
    """Count the number of options for a record"""
    if len(record) < 8:
        return count_options(record, group)
    split_idx = len(record) // 2
    records_left = record[:split_idx]
    records_right = record[split_idx:]
    can_split = records_left[-1] in [1, 2] and records_right[0] in [1, 2]
    if can_split:
        records_left_split = records_left[:-1] + [1]
        records_right_split = [1] + records_right[1:]
    total_options = 0
    min_left, max_left = get_damaged_range2(records_left, records_right, sum(group))
    for num_left in range(min_left, max_left + 1):
        left_groups, right_groups, is_split = split_groups(group, num_left)
        if is_split:
            if not can_split:
                continue
            # If the group is split, we need to enforce that it continues
            # in the right half.
            left = records_left_split
            right = records_right_split
        else:
            left = records_left
            right = records_right
        options_left = count_options_recursive(left, left_groups)
        options_right = count_options_recursive(right, right_groups)
        logging.debug(
            f"{left}, {right}, {left_groups}, {right_groups} -> {options_left}, {options_right}"
        )
        total_options += options_left * options_right
    return total_options


def unfold(results, folds):
    times_5 = (results + [2]) * folds
    return times_5[:-1]


def split_groups(groups, num_left):
    left_groups = []
    right_groups = []
    remaining_left = num_left
    is_split = False
    for g in groups:
        if g <= remaining_left:
            left_groups.append(g)
            remaining_left -= g
        else:
            if remaining_left > 0:
                left_groups.append(remaining_left)
                right_groups.append(g - remaining_left)
                is_split = True
            else:
                is_split = False
            break
    right_groups.extend(groups[len(left_groups) :])
    return left_groups, right_groups, is_split


def get_group_sizes(record: list[bool]) -> list[int]:
    """Get the group sizes from a record"""
    group_sizes = []
    group_size = 0
    for code in record:
        if code:
            group_size += 1
        elif group_size > 0:
            group_sizes.append(group_size)
            group_size = 0
    if group_size > 0:
        group_sizes.append(group_size)
    return group_sizes


def get_damaged_range(records):
    num_damaged = sum([1 for r in records if r == 1])
    num_unknown = sum([1 for r in records if r == 2])
    return num_damaged, num_damaged + num_unknown


def get_damaged_range2(left, right, num_groups):
    left_min, left_max = get_damaged_range(left)
    right_min, right_max = get_damaged_range(right)
    min_damaged = max(left_min, num_groups - right_max)
    max_damaged = min(left_max, num_groups - right_min)
    return min_damaged, max_damaged


if __name__ == "__main__":
    run_aoc(run_part1, run_part2)
