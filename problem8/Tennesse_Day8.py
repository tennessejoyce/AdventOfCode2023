"""
Day 8: Haunted Wasteland
https://adventofcode.com/2023/day/8
"""
import logging
from utilities import run_aoc
import itertools


def run_part1(input_text: str) -> int:
    """"""
    instructions, network = parse_input(input_text)
    logging.debug(instructions)
    logging.debug(network)
    node = "AAA"
    for i, direction in enumerate(itertools.cycle(instructions)):
        logging.debug(f"{i=}, {node=}, {direction=}")
        if node == "ZZZ":
            break
        node = network[node][direction]
    return i


def run_part2(input_text: str) -> int:
    instructions, network = parse_input(input_text)
    starting_nodes = [n for n in network if n[-1] == "A"]
    ending_nodes = {n for n in network if n[-1] == "Z"}
    logging.debug("Found %s instructions", len(instructions))
    logging.debug("Found %s nodes", len(network))
    logging.debug("Found %s starting nodes: %s", len(starting_nodes), starting_nodes)
    logging.debug("Found %s ending nodes: %s", len(ending_nodes), ending_nodes)
    return 0


def parse_input(input_text: str) -> list[tuple[str, int]]:
    """Parse the instructions and network from the input text."""
    lines = input_text.split("\n")
    instructions = [0 if c == "L" else 1 for c in lines[0]]
    network = {line[:3]: (line[7:10], line[12:15]) for line in lines[2:]}
    return instructions, network


if __name__ == "__main__":
    run_aoc(run_part1, run_part2)
