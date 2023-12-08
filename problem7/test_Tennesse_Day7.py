import unittest
from Tennesse_Day7 import get_lex_value, get_type_value, Hand


class TestGetLexValue(unittest.TestCase):
    def test_lex_value(self):
        self.assertLess(get_lex_value(list("2AAAA")), get_lex_value(list("33332")))
        self.assertLess(get_lex_value(list("33332")), get_lex_value(list("44442")))


class TestGetTypeValue(unittest.TestCase):
    def test_type_value(self):
        self.assertEqual(get_type_value(list("AAAAA")), 6)
        self.assertEqual(get_type_value(list("AA8AA")), 5)
        self.assertEqual(get_type_value(list("23332")), 4)
        self.assertEqual(get_type_value(list("TTT98")), 3)
        self.assertEqual(get_type_value(list("23432")), 2)
        self.assertEqual(get_type_value(list("A23A4")), 1)
        self.assertEqual(get_type_value(list("23456")), 0)


class TestHand(unittest.TestCase):
    def test_lt(self):
        five_of_a_kind = Hand("AAAAA")
        four_of_a_kind = Hand("44442")
        full_house_low = Hand("33322")
        full_house_high = Hand("AAA33")

        four_of_a_kind_1 = Hand("33332")
        four_of_a_kind_2 = Hand("2AAAA")

        self.assertLess(four_of_a_kind, five_of_a_kind)
        self.assertLess(full_house_low, full_house_high)
        self.assertLess(four_of_a_kind_2, four_of_a_kind_1)


if __name__ == "__main__":
    unittest.main()
