
import aoctools

puz_in = aoctools.puzzle_input(2020, 1)

test_data = '''1721
979
366
299
675
1456'''


def process_raw(raw):
    return [int(n) for n in raw.split('\n')]


def part1(raw):
    target = 2020
    nums = process_raw(raw)
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return nums[i] * nums[j]


def part2(raw):
    target = 2020
    nums = process_raw(raw)
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            for k in range(j + 1, len(nums)):
                if nums[i] + nums[j] + nums[k] == target:
                    return nums[i] * nums[j] * nums[k]


aoctools.test(1, part1, test_data, 514579)
aoctools.test(2, part2, test_data, 241861950)

print(f"Part 1 Answer: {part1(puz_in)}")
print(f"Part 2 Answer: {part2(puz_in)}")
input()
