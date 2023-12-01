import logging
import functools

logging.basicConfig(level=logging.INFO)


def main():
    # Load the input
    inputs = []
    with open(r"problem1\input.txt", "r") as f:
        for line in f.readlines():
            if len(line) > 1:
                inputs.append(eval(line))

    # Part 1
    index_sum = 0
    for i, (left_input, right_input) in enumerate(zip(inputs[::2], inputs[1::2])):
        i = i + 1
        if _compare(left_input, right_input) <= 0:
            index_sum += i
            logging.info(f"{i} is in right order.")
    logging.info(f"Index sum: {index_sum}")

    # Part 2
    inputs += [[[2]], [[6]]]
    sorted_packets = sorted(inputs, key=functools.cmp_to_key(_compare))
    logging.info(sorted_packets)
    div1 = sorted_packets.index([[2]]) + 1
    div2 = sorted_packets.index([[6]]) + 1
    logging.info(f"Dividers are at {div1} and {div2}, decoder key is {div1 * div2}.")


def _compare(item1, item2):
    logging.debug(f"- Compare {item1} vs. {item2}")
    if isinstance(item1, int) and isinstance(item2, int):
        if item1 < item2:
            logging.debug(f"Left side is smaller, so inputs are in the right order")
            return -1
        elif item1 > item2:
            logging.debug(
                f"Right side is smaller, so inputs are not in the right order"
            )
            return 1
        else:
            return 0
    # Cast to lists, if they aren't already.
    if isinstance(item1, int):
        item1 = [item1]
    if isinstance(item2, int):
        item2 = [item2]
    # Handle lists recursively
    for x, y in zip(item1, item2):
        order = _compare(x, y)
        if order != 0:
            return order
    # If the shared portion of the lists are identical, look at
    # the lengths to make the decision.
    return _compare(len(item1), len(item2))


if __name__ == "__main__":
    main()
