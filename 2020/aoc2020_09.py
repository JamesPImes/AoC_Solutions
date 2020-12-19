
import aoctools


def two_add_up_to(nums, target) -> bool:
    """
    Check whether any two numbers in list `num` add up to `target`.
    :param nums: A list of ints.
    :param target: The required total.
    """
    i = 0
    nums.sort()
    clean_nums = []
    for num in nums:
        if num <= target:
            clean_nums.append(num)
    while i < len(clean_nums):
        for n in clean_nums[i + 1:]:
            if clean_nums[i] + n == target:
                return True
        i += 1
    return False


def find_contiguous_num_sum(nums, end, target):
    """
    Working back from `end`, look for contiguous numbers in `nums` to
    total `target`.
    """

    while True:
        cand_nums = []
        avail_nums = nums[:end]
        avail_nums.reverse()
        for n in avail_nums:
            cand_nums.append(n)
            total = sum(cand_nums)
            if total > target:
                end -= 1
                break
            elif total == target:
                return cand_nums


def bothparts(raw):
    """
    Part 1 - Find the first number in our sequence to not have two
    numbers within the prior 25 numbers to add up to it.
    Part 2 - Find a sequence occurring prior to the Part 1 answer that
    adds up to the Part 1 answer. Return the sum of the min and max of
    that sequence.
    """
    numbers = [int(x) for x in raw.split('\n')]
    total_candidates = 25
    i = total_candidates
    while True:
        target = numbers[i]
        avail = numbers[i - total_candidates: i]
        if not two_add_up_to(avail, target):
            break
        i += 1

    weak_nums = find_contiguous_num_sum(numbers, end=i, target=target)
    print(f"Part 1: {target}")
    print(f"Part 2: {min(weak_nums) + max(weak_nums)}")


puz_in = aoctools.puzzle_input(2020, 9)

bothparts(puz_in)
input()
