"""
Day 5: If You Give A Seed A Fertilizer
https://adventofcode.com/2023/day/5
"""
import logging
from utilities import run_aoc
from dataclasses import dataclass


def run_part1(input_text: str) -> int:
    """
    Count how many numbers match between left and right halves of each row,
    and return the total points of all rows.
    """
    seeds, maps = parse_input(input_text)
    locations = []
    for num in seeds:
        logging.debug("Starting with seed: %s", num)
        for m in maps:
            num = map_int(num, m)
            logging.debug("Mapped to: %s", num)
        logging.debug("Ended at location: %s", num)
        locations.append(num)
    return min(locations)


def run_part2(input_text: str) -> int:
    """
    Count the total number of scorecards according if each card makes
    a copy of the next N cards, where N is the number of matches.
    """
    return 0


def parse_input(input_text: str):
    lines = input_text.split("\n")

    # Parse the seeds.
    seeds = [int(s) for s in lines[0].split(": ")[1].split()]
    logging.debug("Seeds: %s", seeds)
    maps = []
    current_map = None

    for line in lines[1:]:
        if line.endswith("map:"):
            current_map = []
            maps.append(current_map)
        elif line.strip():
            current_map.append(MapRow.from_line(line))

    for m in maps:
        logging.debug("Parsed map with %s rows", len(m))

    return seeds, maps


@dataclass
class Interval:
    start: int
    end: int

    def __len__(self):
        return self.end - self.start

    def __add__(self, num):
        return Interval(self.start + num, self.end + num)

    def __contains__(self, num):
        return self.start <= num < self.end


@dataclass
class MapRow:
    interval: Interval
    offset: int

    @classmethod
    def from_line(cls, line: str):
        dest_start, source_start, length = map(int, line.strip().split())
        return cls(
            interval=Interval(source_start, source_start + length),
            offset=dest_start - source_start,
        )


def map_int(num: int, rows: list[MapRow]) -> int:
    for row in rows:
        if num in row.interval:
            return num + row.offset
    return num


if __name__ == "__main__":
    run_aoc(run_part1, run_part2)
