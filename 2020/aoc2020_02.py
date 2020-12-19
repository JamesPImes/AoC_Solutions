
import aoctools
import re

puz_in = aoctools.puzzle_input(2020, 2)

test_data = '''1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc'''


def parse_line(line):
    """
    Parse a raw line (e.g., '2-9 c: ccccccccc') into a 4-tuple:
    (1st num <int>, 2nd num <int>, target char, target password)
    """
    mo = re.search(r"(\d+)-(\d+) (\w): (\w+)", line)
    return int(mo[1]), int(mo[2]), mo[3], mo[4]


def part1(raw):
    """
    '1-3 a:' means 'a' must occur between 1 and 3 times (inclusive).
    Right of the colon is the password to check.
    """
    valid_pws = []
    for line in raw.split('\n'):
        mn, mx, ch, pw = parse_line(line)
        if mn <= len(re.findall(ch, pw)) <= mx:
            valid_pws.append(pw)

    return len(valid_pws)


def part2(raw):
    valid_pws = []
    for line in raw.split('\n'):
        i1, i2, ch, pw = parse_line(line)
        matched = 0
        for i in [i1, i2]:
            try:
                # Note: ints in the input are 1-indexed, rather than 0-indexed
                matched += int(pw[i - 1] == ch)
            except IndexError:
                pass
        if matched == 1:
            valid_pws.append(pw)

    return len(valid_pws)


aoctools.test(1, part1, test_data, 2)
aoctools.test(1, part2, test_data, 1)

print(f"Part 1 Answer: {part1(puz_in)}")
print(f"Part 2 Answer: {part2(puz_in)}")
input()
