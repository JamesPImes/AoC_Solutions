
import aoctools

DEFAULT_SUBJECT_NUMBER = 7


def transform(val=1, subject_num=DEFAULT_SUBJECT_NUMBER, loop_size=1):
    for i in range(loop_size):
        val = (val * subject_num) % 20201227
    return val


def find_loop_size(public_key, subject_num=DEFAULT_SUBJECT_NUMBER):
    val = 1
    loop_size = 0
    while val != public_key:
        val = transform(val, subject_num, loop_size=1)
        loop_size += 1
    return loop_size


def part1(raw):
    pk_1, pk_2 = [int(x) for x in raw.split('\n')]
    ls_2 = find_loop_size(pk_2)
    encryption_key = transform(subject_num=pk_1, loop_size=ls_2)

    return encryption_key


puz_in = aoctools.puzzle_input(2020, 25)
test_data = '''5764801
17807724'''

aoctools.test(1, part1, test_data, 14897079)
# aoctools.test(2, part2, test_data, 000)
#
aoctools.submit(1, part1, puz_in)
# aoctools.submit(2, part2, puz_in)
