"""
Day 7: Camel Cards
https://adventofcode.com/2023/day/7
"""
import logging
from utilities import run_aoc
import numpy as np

CARD_RANKS = "23456789TJQKA"
CARD_RANKS_JOKER = "J23456789TQKA"
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
    hand_values = [hand_to_int(hand, CARD_RANKS, use_jokers=False) for hand in hands]
    sorted_bets = [bets[i] for i in np.argsort(hand_values)]
    return sum(bet * (i + 1) for i, bet in enumerate(sorted_bets))


def run_part2(input_text: str) -> int:
    """
    Count the total number of scorecards according if each card makes
    a copy of the next N cards, where N is the number of matches.
    """
    hands, bets = parse_input(input_text)
    logging.debug("Parsed hands:\n%s", hands)
    logging.debug("Parsed bets:\n%s", bets)
    hand_values = [
        hand_to_int(hand, CARD_RANKS_JOKER, use_jokers=True) for hand in hands
    ]
    sorted_bets = [bets[i] for i in np.argsort(hand_values)]
    return sum(bet * (i + 1) for i, bet in enumerate(sorted_bets))


def parse_input(input_text: str) -> list[tuple[str, int]]:
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
        hands.append(cards)
        bets.append(int(bet))
    return hands, bets


def hand_to_int(hand: str, card_ranks: str, use_jokers: bool) -> int:
    """
    Convert a hand of cards to an integer representation.
    """
    lex_value = sum(16**i * card_ranks.index(c) for i, c in enumerate(reversed(hand)))
    if use_jokers and "J" in hand and hand != "JJJJJ":
        # Replace all jokers with the most common non-joker card
        # for the purpose of determining the type value.
        most_common_non_joker = most_common_letter(hand.replace("J", ""))
        hand = hand.replace("J", most_common_non_joker)
    counts = sorted(np.unique(list(hand), return_counts=True)[1])[::-1]
    type_value = TYPE_RANKS.index(tuple(counts))
    return 16**5 * type_value + lex_value


def most_common_letter(string: str) -> str:
    """
    Return the most common letter in a string.
    """
    return max(string, key=string.count)


if __name__ == "__main__":
    run_aoc(run_part1, run_part2)
