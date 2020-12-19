
import aoctools
import re

puz_in = aoctools.puzzle_input(2020, 4)

test_data1 = '''ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in'''
test_data2 = None

# REQ_FIELDS = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

# Eye-color options
ECL_OPTIONS = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
BYR_RGE = (1920, 2002)
IYR_RGE = (2010, 2020)
EYR_RGE = (2020, 2030)

VERIFIER_FUNCS = {
    'byr': lambda x: within(x, BYR_RGE),
    'iyr': lambda x: within(x, IYR_RGE),
    'eyr': lambda x: within(x, EYR_RGE),
    'ecl': lambda x: x in ECL_OPTIONS,
    'hcl': lambda x: len(x) == 7 and re.search(r"#[\dabcdef]{6}", x) is not None,
    'hgt': lambda x: hgt_verify(x),
    'pid': lambda x: len(x) == 9 and re.search(r'\d{9}', x) is not None
    }


def within(num, rge):
    """
    Check whether `num` is within the range represented by the 2-tuple
    `rge` (inclusive of min and max). If `num` cannot be converted to an
    int, will return False.
    """
    try:
        num = int(num)
    except ValueError:
        return False
    return rge[0] <= num <= rge[1]


def hgt_verify(val):
    if not val.endswith(('cm', 'in')):
        return False
    unit = val[-2:]
    num = val[:-2]
    try:
        num = int(num)
    except ValueError:
        return False

    rge = (150, 193) if unit == 'cm' else (59, 76)
    if not (rge[0] <= num <= rge[1]):
        return False
    return True


def raw_to_passports(raw):
    return raw.split('\n\n')


def parse_passport(pp):
    pp = pp.replace('\n', ' ')
    return pp.split(' ')


def parse_fieldval(fieldval):
    return fieldval.split(':')


def part1(raw):
    pps = raw_to_passports(raw)
    valid_pps = []
    for pp in pps:
        # Append each passport, unless we are unable to find at least one
        # required field.
        valid = True
        for field in VERIFIER_FUNCS.keys():
            if re.search(field + ":", pp) is None:
                valid = False
                break
        if valid:
            valid_pps.append(pp)
    return len(valid_pps)


def part2(raw):
    pps = raw_to_passports(raw)
    valid_pps = []
    required_fields = list(VERIFIER_FUNCS.keys())

    # Verify each passport
    for pp in pps:
        fieldvals = parse_passport(pp)
        verified_fields = {k: 0 for k in required_fields}
        for fv in fieldvals:
            field, val = fv.split(':')
            verified_fields.setdefault(field, 0)
            # Apply the verifier function to each field/val combo. If True,
            # track that this field has at least one valid entry within the
            # passport. Use `.get()` to return a default lambda to avoid
            # raising a KeyError.
            checker = VERIFIER_FUNCS.get(field, lambda x: None)
            if checker(val):
                verified_fields[field] += 1

        # Confirm we've hit all of our required fields.
        required_verified = 0
        for fd in required_fields:
            if verified_fields[fd] > 0:
                required_verified += 1
        if required_verified == len(required_fields):
            valid_pps.append(pp)

    return len(valid_pps)


aoctools.test(1, part1, test_data1, 2)

print(f"Part 1 Answer: {part1(puz_in)}")
print(f"Part 2 Answer: {part2(puz_in)}")
input()
