
INPUT_DIR = 'puzzle_inputs'


def puzzle_input(year, day, part=None):
    fp = f"..\\{INPUT_DIR}\\{year}\\{year}_{str(day).rjust(2, '0')}"
    if part is not None:
        fp = fp + str(part)
    fp = fp + ".txt"
    with open(fp, 'r') as file:
        raw = file.read().strip()

    return raw


def test(part, func, data, expected):
    try:
        answer = func(data)
        surplus = ' [PASS]'
        if answer != expected:
            surplus = f" ({expected} expected)"
        print(f"Part {part} Test: {answer}{surplus}")
    except Exception as e:
        import traceback
        print(f"Test {part} error: {e}!")
        traceback.print_exc()
        input()


def submit(part=1, func=None, data=None):
    if func is not None:
        try:
            answer = func(data)
            print(f"Part {part} Answer: {answer}")
        except Exception as e:
            import traceback
            print(f"Part {part} error: {e}!")
            traceback.print_exc()
            input()
    else:
        print(f"[Part {part}, not yet complete.]")
    if part == 2:
        input()


# import aoctools
#
# puz_in = aoctools.puzzle_input(0000, 00)
# test_data = '''  '''
#
# aoctools.test(1, part1, test_data, 000)
# aoctools.test(2, part2, test_data, 000)
#
# aoctools.submit(1, part1, puz_in)
# aoctools.submit(2, part2, puz_in)
