
import aoctools
import re

FIELD_RE = re.compile(r'(.*): (\d+)-(\d+) or (\d+)-(\d+)')


def parse_source(raw):

    def unpack_field_raw(line):
        """
        Parse a 'field' line into the field name and its ranges (a list
        of 2-tuples).
        Example:  'departure location: 29-458 or 484-956'
        --> 'departure location', [(29, 458), (484, 956)]
        """
        mo = FIELD_RE.search(line)
        return mo[1], [(int(mo[2]), int(mo[3])), (int(mo[4]), int(mo[5]))]

    fields_raw, my_tix_raw, csv_raw = raw.split('\n\n')

    fields = {}
    for line in fields_raw.split('\n'):
        field, ranges = unpack_field_raw(line)
        fields[field] = ranges

    my_tix = [
        int(x) for x in my_tix_raw.replace('your ticket:\n', '').split(',')
    ]

    csv_raw = csv_raw.replace('nearby tickets:\n', '')
    csv_rows = [
        [int(x) for x in line.split(',')] for line in csv_raw.split('\n')
    ]

    return {'fields': fields, 'my_tix': my_tix, 'csv_rows': csv_rows}


def within(num, rge: tuple):
    """Whether `num` is within the specified range (inclusive of the min
    and max)."""
    return rge[0] <= num <= rge[1]


def invalid_nums(nums, fields):
    valid = {}
    for num in nums:
        valid[num] = 0
        for rge in fields.values():
            valid[num] += 1 if within(num, rge[0]) or within(num, rge[1]) else 0

    invalid = [num for num, v in valid.items() if v == 0]
    return invalid


def find_invalid(data):
    fds = data['fields']
    csv_rows = data['csv_rows']
    invalid = []
    for row in csv_rows:
        invalid.extend(invalid_nums(row, fds))

    return invalid


def discard_invalid(data):
    fds = data['fields']
    csv_rows = data['csv_rows']
    valid = []
    for row in csv_rows:
        if len(invalid_nums(row, fds)) == 0:
            valid.append(row)

    data['csv_rows'] = valid


def deduce_order(data):
    """
    Determine the order of all field names, and return an appropriately
    sorted list of them.
    """
    fields = data['fields']
    fd_names = list(fields.keys())
    csv_rows = data['csv_rows']

    # Get columns from the csv row data.
    cols = []
    for i in range(len(csv_rows[0])):
        col = [num for num in [row[i] for row in csv_rows]]
        cols.append(col)

    # Determine which positions in line each `field` can possibly be, by
    # checking for each field type, if the column contains only would-be
    # legal numbers; repeating for each column
    field_index_candidate = {}
    for fd in fd_names:
        field_index_candidate[fd] = []
        temp_fd_dict = {fd: fields[fd]}
        for i in range(len(cols)):
            if len(invalid_nums(cols[i], temp_fd_dict)) == 0:
                field_index_candidate[fd].append(i)

    # Determine which permutation uses every position
    determined_positions = {}
    cull_ind = None
    while len(field_index_candidate.keys()) > 0:
        for field, posits in field_index_candidate.items():
            if len(posits) == 1:
                ind = posits[0]
                determined_positions[field] = ind
                field_index_candidate.pop(field)
                cull_ind = ind
                break

        for field, posits in field_index_candidate.items():
            # Cull this index from all other fields' candidate indexes
            try:
                posits.remove(cull_ind)
            except ValueError:
                pass
            field_index_candidate[field] = posits

    # Sort the dict keys by their position, and return a list of field names
    srt = sorted(determined_positions.items(), key=lambda fd_i: fd_i[1])
    return [fd_i[0] for fd_i in srt]


def part1(raw):
    """
    Get the sum of those numbers that are plainly invalid (i.e. would
    not be valid for any field).
    """
    data = parse_source(raw)
    return sum(find_invalid(data))


def part2(raw):
    """
    Get the product of those values whose field name starts with
    'departure'.
    """
    data = parse_source(raw)
    discard_invalid(data)
    ordered_fields = deduce_order(data)
    my_ticket = dict(zip(ordered_fields, data['my_tix']))
    prod = 1
    for k, v in my_ticket.items():
        if k.startswith('departure'):
            prod *= v
    return prod


puz_in = aoctools.puzzle_input(2020, 16)

test_data1 = '''class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12'''

# test_data2 = '''class: 0-1 or 4-19
# row: 0-5 or 8-19
# seat: 0-13 or 16-19
#
# your ticket:
# 11,12,13
#
# nearby tickets:
# 3,9,18
# 15,1,5
# 5,14,9'''


aoctools.test(1, part1, test_data1, 71)

aoctools.submit(1, part1, puz_in)
aoctools.submit(2, part2, puz_in)
