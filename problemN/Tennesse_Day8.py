"""
Day 8: Haunted Wasteland
https://adventofcode.com/2023/day/8
"""
import logging
from utilities import run_aoc
import numpy as np


def run_part1(input_text: str) -> int:
    """"""
    return 0


def run_part2(input_text: str) -> int:
    return 0


def parse_input(input_text: str) -> list[tuple[str, int]]:
    """Parse the hands and bids from the input text."""
    hands = []
    bids = []
    for line in input_text.split("\n"):
        cards, bid = line.split()
        hands.append(cards)
        bids.append(int(bid))
    return hands, bids


if __name__ == "__main__":
    run_aoc(run_part1, run_part2)
