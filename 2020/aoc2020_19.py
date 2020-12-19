
import aoctools
import re


def parse_rules(raw_rules):
    """
    Parse raw puzzle input (limited to the rules portion only) into a
    dict, keyed by the number (left of ':' in input) whose value is the
    definition (right of ':').
    """
    rules = raw_rules.split('\n')
    rules = [(r[0], r[1].strip('"')) for r in [s.split(': ') for s in rules]]
    return {k: v for k, v in rules}


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

aoctools.test(1, part1, test_data, 2)
# aoctools.test(2, part2, test_data, 000)

aoctools.submit(1, part1, puz_in)
# aoctools.submit(2, part2, puz_in)
