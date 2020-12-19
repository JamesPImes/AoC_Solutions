
import aoctools


def solution(raw, end_after=2020):
    start_nums = [int(x) for x in raw.split(',')]

    # We'll store only the last two times each number was said.
    nums_lasts = {}

    first_pass = len(start_nums)
    if first_pass > end_after:
        first_pass = end_after

    most_recent = None
    for i in range(first_pass):
        say = most_recent = start_nums[i]
        nums_lasts.setdefault(say, [i, i])
        i += 1

    for i in range(first_pass, end_after):
        a, b = nums_lasts[most_recent]
        say = b - a
        nums_lasts.setdefault(say, [i, i])

        # Update the last two times `say` was spoken
        nums_lasts[say] = [nums_lasts[say][-1], i]
        i += 1
        most_recent = say

    return most_recent


def part1(raw):
    return solution(raw, end_after=2020)


def part2(raw):
    import datetime
    print(f"Part 2 started at {datetime.datetime.now()}...")
    answer = solution(raw, end_after=30000000)
    print(f"Part 2 finished at {datetime.datetime.now()}.")
    return answer


puz_in = aoctools.puzzle_input(2020, 15)
test_data = '0,3,6'

aoctools.test(1, part1, test_data, 436)

aoctools.submit(1, part1, puz_in)
aoctools.submit(2, part2, puz_in)
