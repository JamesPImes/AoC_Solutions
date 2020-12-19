
import aoctools

JOLTAGE_BUFFER = 3


def get_joltages(raw):
    joltages = [int(x) for x in raw.split('\n')]

    # Add the outlet (with a joltage of 0) to the first position in our list
    joltages.insert(0, 0)
    joltages.sort()
    device_rating = max(joltages) + JOLTAGE_BUFFER
    joltages.append(device_rating)

    return joltages


def part1(raw):
    joltages = get_joltages(raw)

    one_jolt_difs = 0
    three_jolt_difs = 0
    current_joltage = 0

    for joltage in joltages:
        dif = joltage - current_joltage
        if dif == 1:
            one_jolt_difs += 1
        elif dif == 3:
            three_jolt_difs += 1
        current_joltage = joltage

    return one_jolt_difs * three_jolt_difs


def part2(raw):
    joltages = get_joltages(raw)

    # We'll count how many 'ways in' there are for each adapter
    # (smallest to largest), by adding the number of paths for each of
    # the adapters within the buffer range.

    paths_in = {}

    # 1 way in for our first adapter (the outlet itself).
    paths_in[0] = 1

    # For each subsequent adapter, check how many paths_in there are for
    # each number (`chk`) within the buffer range. E.g., assuming a
    # joltage_buffer of 3, then for 32, we'll check how many paths_in we
    # calculated for 31, 30, and 29; take the sum of all of those, and
    # that's how many paths_in there are for 32.  If 31, 30, or 29 did
    # not exist in our list of adapters, we add 0, since
    # `paths_in.get(..., 0)` returns 0 for keys that do not exist.
    for n in joltages[1:]:
        new_in = 0
        for chk in list(range(1, JOLTAGE_BUFFER + 1)):
            # For a `JOLTAGE_BUFFER` of 3, this is [1, 2, 3]
            # -- i.e. we're checking n-1, n-2, and n-3
            new_in += paths_in.get(n - chk, 0)
        paths_in[n] = new_in

    # Grab from the dict the value for the final element in `joltages`
    # (which is our device)
    return paths_in[(joltages[-1])]


puz_in = aoctools.puzzle_input(2020, 10)

test_data1 = '''16
10
15
5
1
11
7
19
6
12
4'''

test_data2 = '''28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3'''

aoctools.test('1a', part1, test_data1, 7*5)
aoctools.test('1b', part1, test_data2, 22*10)

aoctools.submit(1, part1, puz_in)
aoctools.submit(2, part2, puz_in)
