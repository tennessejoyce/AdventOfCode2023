import unittest
from Tennesse_Day3 import GearCounter, EngineCounter


class GearCounterTestCase(unittest.TestCase):
    def test_gear_counter(self):
        counter = GearCounter()

        # Test adding values and connecting asterisks
        counter.add(1)
        counter.add(2)
        counter.connect({(0, 0)})
        counter.finish_part()

        counter.add(3)
        counter.connect({(0, 0), (1, 0)})
        counter.add(4)
        counter.connect({(2, 0)})
        counter.finish_part()

        counter.add(5)
        counter.finish_part()

        # Test the expected part numbers by asterisk
        expected_part_numbers = {(0, 0): [12, 34], (1, 0): [34], (2, 0): [34]}
        self.assertEqual(counter.part_numbers_by_asterisk, expected_part_numbers)


class EngineCounterTestCase(unittest.TestCase):
    def test_engine_counter(self):
        counter = EngineCounter()

        # Test adding values and marking as valid
        counter.add(1)
        counter.add(2)
        counter.mark_valid()
        counter.finish_part()

        counter.add(3)
        counter.mark_valid()
        counter.add(4)
        counter.finish_part()

        counter.add(5)
        counter.finish_part()

        # Test the expected part numbers
        expected_part_numbers = [12, 34]
        self.assertEqual(counter.part_numbers, expected_part_numbers)


if __name__ == "__main__":
    unittest.main()
