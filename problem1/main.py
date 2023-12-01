import logging
import re

logging.basicConfig(level=logging.INFO)

DIGITS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def main():
    # Load the input
    with open(r"problem1\input.txt", "r", encoding="utf-8") as f:
        inputs = f.readlines()
    # inputs = list(inputs)[:20]

    calibration_values = [get_calibration_value2(line) for line in inputs]
    logging.info(inputs)
    logging.info(calibration_values)
    logging.info(sum(calibration_values))


def get_calibration_value1(line):
    matches = re.findall("(\d)", line)
    logging.debug(f"{line}: {matches}")
    if len(matches) < 1:
        raise ValueError(f"Could not find two numbers in {line}")
    return int(matches[0] + matches[-1])


def get_calibration_value2(line):
    matches = find_all_overlapping("(" + "|".join(DIGITS) + "|\d)", line)
    logging.debug(f"{line}: {matches}")
    if len(matches) < 1:
        raise ValueError(f"Could not find two numbers in {line}")
    return 10 * to_int(matches[0]) + to_int(matches[-1])


def to_int(digit):
    if digit.isdigit():
        return int(digit)
    else:
        return DIGITS.index(digit) + 1


def find_all_overlapping(pattern, string):
    pattern = "(?=(" + pattern + "))"
    return [match.group(1) for match in re.finditer(pattern, string)]


if __name__ == "__main__":
    main()
