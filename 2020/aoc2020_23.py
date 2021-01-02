
import aoctools


def new_round(links, current):
    h1 = links[current]
    h2 = links[h1]
    h3 = links[h2]
    links[current] = links[h3]

    destination_cup = current - 1
    while True:
        if destination_cup < 1:
            destination_cup = max(links.keys())
        if destination_cup not in [h1, h2, h3]:
            break
        destination_cup -= 1

    links[h3] = links[destination_cup]
    links[destination_cup] = h1
    return links[current]


def gen_pointers(cups: list):
    """
    Generate a dict of pointers from each cup to the next cup
    (clockwise).
    """
    points_to = {cups[i]: cups[i + 1] for i in range(len(cups) - 1)}

    # Circular, so link last item to first item.
    points_to[int(cups[-1])] = int(cups[0])

    return points_to


def part1(raw, rounds=100):
    cups = [int(x) for x in list(raw)]
    points_to = gen_pointers(cups)

    current_cup = cups[0]
    for _ in range(rounds):
        current_cup = new_round(points_to, current_cup)

    current_cup = points_to[1]
    final_order = f"{current_cup}"
    for _ in range(len(cups) - 2):
        current_cup = points_to[current_cup]
        final_order = f"{final_order}{current_cup}"

    return final_order


def part2(raw, rounds=10000000):
    total_cups = 1000000
    cups = [x + 1 if x >= len(raw) else int(raw[x]) for x in range(total_cups)]
    points_to = gen_pointers(cups)

    current_cup = cups[0]
    for _ in range(rounds):
        current_cup = new_round(points_to, current_cup)

    num_1 = points_to[1]
    num_2 = points_to[num_1]

    return num_1 * num_2


puz_in = aoctools.puzzle_input(2020, 23)
test_data = '''389125467'''

aoctools.test(1, part1, test_data, '67384529')
aoctools.test(2, part2, test_data, 149245887792)

aoctools.submit(1, part1, puz_in)
aoctools.submit(2, part2, puz_in)
