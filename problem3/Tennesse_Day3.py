"""
Day 3: Gear Ratios
https://adventofcode.com/2023/day/3
"""
import logging
import argparse
import pathlib
import numpy as np
from typing import Iterator
import functools


def run_part1(input_text: str) -> int:
    """Solve Part 1"""
    symbol_locs = [(x, y) for x, y, value in grid_iter(input_text) if is_symbol(value)]
    next_to_symbol = {n for x, y in symbol_locs for n in get_neighbors(x, y)}
    counter = EngineCounter()
    for x, y, value in grid_iter(input_text):
        if x == 0:
            counter.reset()
        if value.isdigit():
            counter.add(int(value))
            if (x, y) in next_to_symbol:
                counter.mark_valid()
        else:
            counter.reset()
    return sum(counter.part_numbers)


def run_part2(input_text: str) -> int:
    """Solve Part 2"""
    asterisks = [(x, y) for x, y, value in grid_iter(input_text) if value == "*"]
    neighboring_gears = {}
    for aloc in asterisks:
        for nloc in get_neighbors(*aloc):
            neighboring_gears.setdefault(nloc, set()).add(aloc)
    logging.debug("Neighboring gears:\n%s", neighboring_gears)
    counter = GearCounter()
    for x, y, value in grid_iter(input_text):
        if x == 0:
            counter.reset()
        if value.isdigit():
            counter.add(int(value))
            if (x, y) in neighboring_gears:
                counter.connect(neighboring_gears[(x, y)])
        else:
            counter.reset()
    sum_of_ratios = 0
    for aloc, part_numbers in counter.part_numbers_by_gear.items():
        logging.debug("Asterisk at %s has part numbers %s", aloc, part_numbers)
        if len(part_numbers) == 2:
            gear_ratio = part_numbers[0] * part_numbers[1]
            logging.debug("\tThis is a gear with ratio %s", gear_ratio)
            sum_of_ratios += gear_ratio
        else:
            logging.debug("\tThis is not a gear")
    return sum_of_ratios


def grid_iter(input_text: str) -> Iterator[tuple[int, int, str]]:
    """
    Iterate over the input text, yielding a tuple of (x, y, value) for each
    square in the grid.
    """
    for y, line in enumerate(input_text.split("\n")):
        for x, value in enumerate(line):
            yield x, y, value


@functools.cache
def is_symbol(value: str) -> bool:
    """
    Return True if the value is a symbol, False otherwise.
    """
    return value not in "0123456789."


def get_neighbors(x: int, y: int) -> list[tuple[int, int]]:
    """
    Return a list of the coordinates of the neighbors of the square at (x, y).
    """
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            neighbors.append((x + dx, y + dy))
    return neighbors


class EngineCounter:
    def __init__(self):
        self.part_numbers = []
        self.current = 0
        self.valid = False

    def add(self, value):
        self.current = 10 * self.current + value

    def mark_valid(self):
        self.valid = True

    def reset(self):
        if self.valid:
            logging.debug("Found valid part number: %s", self.current)
            self.part_numbers.append(self.current)
        elif self.current > 0:
            logging.debug("Invalid part number: %s", self.current)
        self.current = 0
        self.valid = False


class GearCounter:
    def __init__(self):
        self.part_numbers_by_gear = {}
        self.current = 0
        self.asterisks = set()

    def add(self, value):
        self.current = 10 * self.current + value

    def connect(self, aloc: set[tuple[int, int]]):
        self.asterisks |= aloc

    def reset(self):
        if len(self.asterisks) > 0:
            logging.debug(
                "Found valid part number %s connecting to %s",
                self.current,
                self.asterisks,
            )
        for aloc in self.asterisks:
            self.part_numbers_by_gear.setdefault(aloc, []).append(self.current)
        self.current = 0
        self.asterisks = set()


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filepath", type=pathlib.Path)
    parser.add_argument("--part", type=str, choices=["1", "2", "both"], default="both")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    # Set up the logging configuration.
    if args.debug:
        # If debug mode is on, log both debug and info level messages,
        # and also includes the line number in the log.
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(levelname)s - %(message)s - [LINE:%(lineno)d]",
        )
    else:
        # If debug mode is off, log only info level messages.
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
        )

    # Load the input from a text file.
    input_text = args.input_filepath.read_text()

    # Run solutions for one or both parts. The functions run_part1 and
    # run_part2 should be defined above.
    if args.part == "1" or args.part == "both":
        logging.info("Running Part 1...")
        answer1 = run_part1(input_text)
        logging.info("Answer to Part 1: %s", answer1)

    if args.part == "2" or args.part == "both":
        logging.info("Running Part 2...")
        answer2 = run_part2(input_text)
        logging.info("Answer to Part 2: %s", answer2)
