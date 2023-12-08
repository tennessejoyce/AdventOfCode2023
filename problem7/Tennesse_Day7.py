"""
Day 7: Camel Cards
https://adventofcode.com/2023/day/7
"""
import logging
import argparse
import pathlib
import numpy as np

CARD_RANKS = "23456789TJQKA"
TYPE_RANKS = [(1, 1, 1, 1, 1), (2, 1, 1, 1), (2, 2, 1), (3, 1, 1), (3, 2), (4, 1), (5,)]


def run_part1(input_text: str) -> int:
    """
    Parse the hands and return the total winnings.

    You can determine the total winnings by adding up the result of
    multiplying each hand's bid with its rank.
    """
    hands, bets = parse_input(input_text)
    logging.debug("Parsed hands:\n%s", hands)
    logging.debug("Parsed bets:\n%s", bets)
    sorted_bets = [bets[i] for i in np.argsort(hands)]
    return sum(bet * (i + 1) for i, bet in enumerate(sorted_bets))


def run_part2(input_text: str) -> int:
    """
    Count the total number of scorecards according if each card makes
    a copy of the next N cards, where N is the number of matches.
    """
    return 0


class Hand:
    def __init__(self, cards: str):
        self.cards = list(cards)
        self.lex_value = get_lex_value(self.cards)
        self.type_value = get_type_value(self.cards)

    def __lt__(self, other):
        if self.type_value < other.type_value:
            return True
        elif self.type_value == other.type_value:
            return self.lex_value < other.lex_value
        else:
            return False

    def __repr__(self):
        return f"Hand({''.join(self.cards)})"


def parse_input(input_text: str) -> list[tuple[Hand, int]]:
    """
    Parse the hands from the input text of the form:
        32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483
    """
    hands = []
    bets = []
    for line in input_text.split("\n"):
        cards, bet = line.split()
        hands.append(Hand(cards))
        bets.append(int(bet))
    return hands, bets


def get_lex_value(hand: list[str]) -> int:
    """
    Convert a hand of cards to an integer representation.
    """
    return sum(16**i * CARD_RANKS.index(c) for i, c in enumerate(reversed(hand)))


def get_type_value(hand: list[str]) -> int:
    """
    Convert a hand of cards to an integer representation.
    """
    counts = sorted(np.unique(hand, return_counts=True)[1])[::-1]
    return TYPE_RANKS.index(tuple(counts))


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
