
import aoctools

COMMANDS = {
        'acc': lambda index, n, a: (index + 1, a + n),
        'jmp': lambda index, n, a: (index + n, a),
        'nop': lambda index, n, a: (index + 1, a)
    }


def parse_line(line):
    cmd, n = line.split(' ')
    return cmd, int(n)


def part1(raw):
    """
    Find the accumulator value (`a`) immediately before executing any
    line of code a second time.
    """
    lines = raw.split('\n')
    i = 0
    a = 0
    executed = []
    while True:
        line = lines[i]
        if i in executed:
            return a
        executed.append(i)
        cmd, n = parse_line(line)
        i, a = COMMANDS[cmd](i, n, a)


def part2(raw):
    """
    Run the code successfully after changing exactly one 'nop' to 'jmp'
    or vice versa. Return the final accumulator value (`a`).
    """

    lines = raw.split('\n')
    total_lines = len(lines)
    possible_swaps = [
        j for j in range(len(lines)) if lines[j].startswith(('nop', 'jmp'))
    ]
    while True:
        swap_i = possible_swaps.pop(0)
        i = 0
        a = 0
        executed = []
        while True:
            line = lines[i]
            if i in executed:
                break
            executed.append(i)
            cmd, n = parse_line(line)
            if i == swap_i:
                cmd = 'jmp' if cmd == 'nop' else 'nop'
            i, a = COMMANDS[cmd](i, n, a)
            if i == total_lines:
                return a


puz_in = aoctools.puzzle_input(2020, 8)
test_data = '''nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6'''

aoctools.test(1, part1, test_data, 5)
aoctools.test(2, part2, test_data, 8)

aoctools.submit(1, part1, puz_in)
aoctools.submit(2, part2, puz_in)
