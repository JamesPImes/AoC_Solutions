
import aoctools

puz_in = aoctools.puzzle_input(2020, 5)


def find_seat(seat_code):
    """
    Find the (row, column) of a seat, based on the provided seat code.
    """
    # 128 possible rows, 8 possible columns
    rows = list(range(128))
    cols = list(range(8))

    row_codes = seat_code[:7]
    col_codes = seat_code[-3:]

    for char in row_codes:
        # divide available rows
        if char == 'B':
            # 'B' -> keep only the upper half
            rows = rows[len(rows)//2:]
        else:
            # 'F' -> keep only the lower half
            rows = rows[:-len(rows)//2]

    for char in col_codes:
        # divide available cols
        if char == 'R':
            # 'R' -> take the upper half (rightmost)
            cols = cols[len(cols)//2:]
        else:
            # 'L' -> take the lower half
            cols = cols[:-len(cols)//2]

    return rows[0], cols[0]


def seat_id(row_col):
    return row_col[0] * 8 + row_col[1]


def part1(raw):
    seat_codes = raw.split('\n')
    found_seats = []
    for sc in seat_codes:
        id = seat_id(find_seat(sc))
        found_seats.append(id)
    return max(found_seats)


def part2(raw):
    seat_codes = raw.split('\n')
    found_seats = []
    for sc in seat_codes:
        id = seat_id(find_seat(sc))
        found_seats.append(id)

    # Generate all possible seats
    rows = list(range(128))
    cols = list(range(8))
    seats = []
    for row in rows:
        for col in cols:
            seats.append(seat_id((row, col)))

    missing_seats = list(set(seats) - set(found_seats))

    # Find the first seat whose id is not 1 greater than the previous seat
    # (We can rule out the first seat, because we know from the puzzle
    # instructions that it does not exist.)
    last_seat = missing_seats.pop(0)
    while len(missing_seats) > 0:
        cand = missing_seats.pop(0)
        if cand != last_seat + 1:
            return cand
        last_seat = cand
    return None


aoctools.test('1a', find_seat, 'BFFFBBFRRR', (70, 7))
aoctools.test('1b', find_seat, 'FFFBBBFRRR', (14, 7))
aoctools.test('1c', find_seat, 'BBFFBBFRLL', (102, 4))

print(f"Part 1 Answer: {part1(puz_in)}")
print(f"Part 2 Answer: {part2(puz_in)}")
input()
