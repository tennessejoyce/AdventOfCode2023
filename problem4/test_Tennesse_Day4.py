import unittest
from Tennesse_Day4 import ScratchCard


class TestScratchCard(unittest.TestCase):
    def test_from_row(self):
        row = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
        scratch_card = ScratchCard.from_row(row)
        self.assertEqual(scratch_card.card_number, 1)
        self.assertEqual(scratch_card.winning_numbers, {41, 48, 83, 86, 17})
        self.assertEqual(scratch_card.your_numbers, {83, 86, 6, 31, 17, 9, 48, 53})

    def test_get_score(self):
        scratch_card = ScratchCard(
            1, {41, 48, 83, 86, 17}, {83, 86, 6, 31, 17, 9, 48, 53}
        )
        self.assertEqual(scratch_card.get_score(), 8)

        scratch_card = ScratchCard.from_row(
            "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19"
        )
        self.assertEqual(scratch_card.get_score(), 2)


if __name__ == "__main__":
    unittest.main()
