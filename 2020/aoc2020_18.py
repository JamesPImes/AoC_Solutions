
import aoctools
import re

# For identifying '+' operations -- eg., '5+10'
ADD = re.compile(r'\d+\+\d+')

# For identifying '*' operations -- eg., '5*10'
MULTI = re.compile(r'\d+\*\d+')

# For identifying either '+' or '*' operations -- eg., '5+10'   OR   '5*10'
ADDMULTI = re.compile(r'\d+[\+\*]\d+')

LP = re.compile(r'\(')  # '('
RP = re.compile(r'\)')  # ')'


def eval_lr(line, part=1):
    """
    Recursively evaluate this line, parsing within parentheses until
    none remain, and then parsing '+' and '*' according to the rules of
    the puzzle (which are different for `part` 1 vs. 2).
    :param line: A raw line from the puzzle input.
    :param part: Whether we're solving under the Part 1 rules ('+' and
    '*' are evaluated left-to-right) or Part 2 rules (all '+' first,
    then all '*').
    :return: The evaluation of this line (an integer).
    """
    line = line.replace(' ', '')

    # First parse within parentheses
    lp_i = 0  # left-parenthesis index
    while True:
        # Find ')'
        mo_r = RP.search(line, pos=lp_i)
        if mo_r is None:
            break
        rp_i = mo_r.start()  # right-parenthesis index
        while True:
            # Find the '(' closest to our already-matched ')'
            mo_l = LP.search(line[:rp_i], pos=lp_i)
            if mo_l is None:
                break
            lp_i = mo_l.end()

        # Evaluate this portion of the line, and put the result back in line.
        v = eval_lr(line[lp_i:rp_i], part=part)
        line = line[:lp_i - 1] + str(v) + line[rp_i + 1:]

        # Reset our left-parenthesis index and look for more parentheses.
        lp_i = 0

    # Then parse '+' and '*' (left-to-right for part 1; '+' then '*' for part 2)
    orig = None
    while True:
        if orig == line:
            break

        orig = line

        # Default to part 1, where addition and multiplication are evaluated
        # at the same precedence -- just left-to-right as they occur.
        patterns = [ADDMULTI]
        if part == 2:
            # For part 2, we first do all addition, then all multiplication, so
            # we use separate regex patterns.
            patterns = [ADD, MULTI]
        for pattern in patterns:
            while True:
                mo = pattern.search(line)
                if mo is None:
                    break
                v = eval(mo[0])
                line = line[:mo.start()] + str(v) + line[mo.end():]

    return int(line)


def part1(raw):
    lines = raw.split('\n')
    total = 0
    for line in lines:
        total += eval_lr(line)
    return total


def part2(raw):
    lines = raw.split('\n')
    total = 0
    for line in lines:
        total += eval_lr(line, part=2)
    return total


puz_in = aoctools.puzzle_input(2020, 18)
test_data1 = '1 + 2 * 3 + 4 * 5 + 6'
test_data1a = '2 * 3 + (4 * 5)'
test_data1b = '5 + (8 * 3 + 9 + 3 * 4 * 3)'
test_data1c = '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'
test_data1d = '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'
test_data2 = '1 + (2 * 3) + (4 * (5 + 6))'
test_data2a = '2 * 3 + (4 * 5)'
test_data2b = '5 + (8 * 3 + 9 + 3 * 4 * 3)'
test_data2c = '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'
test_data2d = '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'

aoctools.test('1', part1, test_data1, 71)
aoctools.test('1a', part1, test_data1a, 26)
aoctools.test('1b', part1, test_data1b, 437)
aoctools.test('1c', part1, test_data1c, 12240)
aoctools.test('1d', part1, test_data1d, 13632)

aoctools.test('2', part2, test_data2, 51)
aoctools.test('2a', part2, test_data2a, 46)
aoctools.test('2b', part2, test_data2b, 1445)
aoctools.test('2c', part2, test_data2c, 669060)
aoctools.test('2d', part2, test_data2d, 23340)

aoctools.submit(1, part1, puz_in)
aoctools.submit(2, part2, puz_in)
