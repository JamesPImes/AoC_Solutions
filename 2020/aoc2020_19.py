
# ----------------------------------------------------------------------
# This is a somewhat wonky solution. *Actually* defining the regexes
# recursively would be a much better solution, although I don't know how
# to implement that in native Python (apparently the 3rd-party `regex`
# module has this functionality).
#
# In any case, this solution works for the puzzle input:
#
# Part 1 solution should in theory work for inputs of any length --
# because without recursion, there is a finite length allowed by the
# defined rules, so any messages longer than the maximum-length allowed
# by the rules would just be found to be invalid (by definition,
# obviously).
#
# In theory, the Part 2 solution should (I think) ALSO work on any
# length of input because I set the number of simulated recursions to be
# determined dynamically by the longest message in the input (i.e. the
# longer the message, the more 'recursions' we do). But if the dataset
# contained any extra-long messages, it might cause this to run
# impractically slowly / resource-intensively.
# ----------------------------------------------------------------------

import aoctools
import re


def parse_rules(raw_rules):
    """
    Parse raw puzzle input (limited to the rules portion only) into a
    dict, keyed by the number (left of ':' in input) whose value is the
    definition (right of ':').
    """
    rules = raw_rules.split('\n')
    return {r[0]: r[1].strip('"') for r in [s.split(': ') for s in rules]}


def brute_define(rule: tuple, rules: dict):
    """
    Get the full unpacked definition (i.e. 'a' and 'b' allowed, but no
    numbers) for this rule, using a brute-strength algorithm.
    """

    # TODO: There must be a cleaner / simpler way to do this recursively...

    rule_num, definition = rule
    while True:
        # Search for the first number
        mo = re.search(r'\d+', definition)
        if mo is None:
            # If no numbers found, this definition is fully unpacked.
            break

        # Replace that number with its respective definition. For
        # definitions that are a bare 'a' or 'b', do not add paren.
        # Otherwise, maintain explicit grouping by couching in parens.
        num = mo[0]
        pat = r"\b" + num + r"\b"
        sub_in = rules[num]
        if rules[num] not in ['a', 'b']:
            sub_in = '(' + sub_in + ')'
        definition = re.sub(pat, f"{sub_in}", definition)

    return definition


def get_pattern(n: int, rules: dict):
    pat = r'\b' + brute_define((str(n), rules[str(n)]), rules) + r'\b'
    pat = pat.replace(' ', '')
    return pat


def part1(raw):
    rules_raw, messages_raw = raw.split('\n\n')
    rules = parse_rules(rules_raw)
    messages = messages_raw.split('\n')

    re_pattern = get_pattern(0, rules)

    ok = 0
    for message in messages:
        if re.search(re_pattern, message) is not None:
            ok += 1

    return ok


def part2(raw):
    # The same brute-strength solution as for part 1, but with a
    # 'simulated' recursion for rules 8 and 11 (that should work for
    # a dataset with a known maximum length, but would NOT work with
    # a dataset with unknown length -- or at least, would be very
    # inefficient, if it worked at all...)

    rules_raw, messages_raw = raw.split('\n\n')
    rules = parse_rules(rules_raw)
    messages = messages_raw.split('\n')
    longest_message = max([len(msg) for msg in messages])

    # Redefine Rules 8 and 11 per puzzle instructions
    rules['8'] = "42 | 42 8"
    rules['11'] = "42 31 | 42 11 31"

    # *Simulate* recursively defining rules 8 and 11 (but stopping after
    # we've done one step of depth per character in the longest message),
    # without *actually* recursively defining it.
    for _ in range(longest_message):
        rules['8'] = re.sub(r"8", '(42 | 42 8)', rules['8'])
        rules['11'] = re.sub(r"11", '(42 31 | 42 11 31)', rules['11'])

    # Now delete any remaining 8's and 11's in these rules, to avoid an
    # infinite loop when we call `get_pattern()`.
    rules['8'] = re.sub(r" 8\)", ")", rules['8'])
    rules['11'] = re.sub(r" 11 ", " ", rules['11'])

    re_pattern = get_pattern(0, rules)

    ok = 0
    for message in messages:
        if re.search(re_pattern, message) is not None:
            ok += 1

    return ok


puz_in = aoctools.puzzle_input(2020, 19)

test_data = '''0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb'''

test_data2 = '''42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba'''

aoctools.test(1, part1, test_data, 2)
aoctools.test(2, part2, test_data2, 12)

aoctools.submit(1, part1, puz_in)
aoctools.submit(2, part2, puz_in)
