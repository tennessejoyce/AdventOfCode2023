import logging
import re

logging.basicConfig(level=logging.INFO)


def main():
    # Load the input
    with open(r"problem1\test_input.txt", "r") as f:
        inputs = f.readlines()

    calibration_values = [get_calibration_value(line) for line in inputs]
    print(inputs)
    print(calibration_values)
    print(sum(calibration_values))


def get_calibration_value(line):
    return len(line)


if __name__ == "__main__":
    main()
