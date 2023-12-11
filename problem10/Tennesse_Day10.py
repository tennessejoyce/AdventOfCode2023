"""
Day 10: Pipe Maze
https://adventofcode.com/2023/day/10
"""
import logging
from utilities import run_aoc
import networkx as nx


def run_part1(input_text: str) -> int:
    """"""
    G, starting_position = parse_input(input_text)
    logging.debug("Number of nodes: %d", G.number_of_nodes())
    distances = {
        node: len(path) for node, path in nx.shortest_path(G, starting_position).items()
    }
    logging.debug("Number of nodes connected to start: %d", len(distances))
    logging.debug("Farthest node: %s", max(distances, key=distances.get))
    return max(distances.values())


def run_part2(input_text: str) -> int:
    return 0


def parse_input(input_text: str) -> list[tuple[str, int]]:
    """Parse the hands and bids from the input text."""
    lines = input_text.splitlines()
    num_rows = len(lines)
    num_cols = len(lines[0])
    starting_position = None
    G = nx.Graph()
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "|":
                G.add_edge((i, j), (i - 1, j))
                G.add_edge((i, j), (i + 1, j))
            elif char == "-":
                G.add_edge((i, j), (i, j - 1))
                G.add_edge((i, j), (i, j + 1))
            elif char == "L":
                G.add_edge((i, j), (i - 1, j))
                G.add_edge((i, j), (i, j + 1))
            elif char == "J":
                G.add_edge((i, j), (i - 1, j))
                G.add_edge((i, j), (i, j - 1))
            elif char == "7":
                G.add_edge((i, j), (i + 1, j))
                G.add_edge((i, j), (i, j - 1))
            elif char == "F":
                G.add_edge((i, j), (i + 1, j))
                G.add_edge((i, j), (i, j + 1))
            if char == ".":
                continue
            elif char == "S":
                starting_position = (i, j)
    logging.debug(f"Starting position: {starting_position}")
    # Remove any nodes that got created outside the grid when adding edges.
    for i, j in G.nodes:
        if i < 0 or i >= num_rows or j < 0 or j >= num_cols:
            G.remove_node((i, j))
    return G, starting_position


if __name__ == "__main__":
    run_aoc(run_part1, run_part2)
