
import aoctools


def rotate_to_val(a_list: list, target=1):
    """
    'Rotate' our list until the `target` value is at index 0. Returns a
    new list.
    """
    return rotate_by_n(a_list, a_list.index(target))


def rotate_by_n(a_list: list, n=1):
    """
    'Rotate' our list clockwise by `n` notches. Returns a new list.
    """
    return a_list[n:] + a_list[:n]


def new_round(cups: list):
    hold_cups, remaining_cups = cups[1:4], cups[:1] + cups[4:]

    destination = cups[0] - 1
    while True:
        if destination < min(remaining_cups):
            destination = max(remaining_cups)
        try:
            i = remaining_cups.index(destination)
            break
        except ValueError:
            destination -= 1

    cups = remaining_cups[:i + 1] + hold_cups + remaining_cups[i + 1:]

    # Rotate by 1 to set up the next round.
    cups = rotate_by_n(cups, 1)
    return cups


def part1(raw, rounds=100):
    cups = [int(x) for x in list(raw)]

    for _ in range(rounds):
        cups = new_round(cups)

    cups = rotate_to_val(cups, 1)

    return ''.join([str(c) for c in cups[1:]])


puz_in = aoctools.puzzle_input(2020, 23)
test_data = '''389125467'''

aoctools.test(1, part1, test_data, '67384529')
# aoctools.test(2, part2, test_data, 0)

aoctools.submit(1, part1, puz_in)
# aoctools.submit(2, part2, puz_in)
