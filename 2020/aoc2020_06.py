
import aoctools


def get_groups(raw):
    """
    Convert the raw input into a nested list of groups. Each main-level
    element is a group. The deeper-level element is an individual
    within that group.
    """
    groups = raw.split('\n\n')
    clean_groups = []
    for group in groups:
        clean_groups.append(group.split('\n'))
    return clean_groups


def group_answers_part1(group: list):
    """
    Return a single string representing all of the unique answers given
    by at least one person in a group (per Part 1 rules).
    """
    grp_answers = set()
    for person in group:
        grp_answers = grp_answers.union(set(list(person)))
    return ''.join(grp_answers)


def part1(raw):
    groups = get_groups(raw)
    ans = 0
    for group in groups:
        ans += len(group_answers_part1(group))
    return ans


def group_answers_part2(group: list):
    """
    Return a single_string representing all of the unique answers given
    by EVERY person in a group (per Part 2 rules).
    """
    grp_answers = None
    for person in group:
        if grp_answers is None:
            grp_answers = set(list(person))
        grp_answers = grp_answers.intersection(set(list(person)))
    return ''.join(grp_answers)


def part2(raw):
    groups = get_groups(raw)
    ans = 0
    for group in groups:
        ans += len(group_answers_part2(group))
    return ans


puz_in = aoctools.puzzle_input(2020, 6)
test_data = '''abc

a
b
c

ab
ac

a
a
a
a

b'''

aoctools.test(1, part1, test_data, 11)
aoctools.test(2, part2, test_data, 6)

print(f"Part 1 Answer: {part1(puz_in)}")
print(f"Part 2 Answer: {part2(puz_in)}")
input()
