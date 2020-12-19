
import aoctools


class Cell:
    def __init__(self, cur):
        self.cur = cur
        self.next = cur

    @property
    def is_occupied(self):
        return self.cur == '#'

    def end_of_round(self):
        self.cur = self.next

    def fill(self):
        if self.cur != '.':
            self.next = '#'

    def empty(self):
        if self.cur != '.':
            self.next = 'L'


class Grid:

    def __init__(self):
        self.cells = []

    def cell_exists(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def count_occ(self, x, y, visibility=None):
        """
        Count how many occupied seats there are within the `visibility`
        of this
        """
        if visibility is None:
            # If not specified, we can see to the end of the grid.
            visibility = max(self.width, self.height)
        directions = [
            (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
        ]
        occupied = 0
        for direc in directions:
            d = 1
            while d <= visibility:
                targ_x, targ_y = x + direc[0] * d, y + direc[1] * d
                if not self.cell_exists(targ_x, targ_y):
                    # We've reached the end of the grid.
                    break
                cell = self.cells[targ_y][targ_x]
                if cell.cur == 'L':
                    # We see an empty seat.
                    break
                elif cell.cur == '#':
                    # We've reached the end of where we can see, and it's occupied.
                    occupied += 1
                    break
                d += 1

        return occupied

    @property
    def width(self):
        return len(self.cells[0])

    @property
    def height(self):
        return len(self.cells)

    def new_round(self, visibility=1, max_occupied=4):
        changed = 0
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[y][x]
                if cell.cur == '.':
                    continue

                occ_count = self.count_occ(x, y, visibility=visibility)

                if occ_count == 0 and cell.cur == 'L':
                    changed += 1
                    cell.fill()
                elif occ_count >= max_occupied and cell.cur == '#':
                    changed += 1
                    cell.empty()

        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[y][x]
                cell.end_of_round()

        return changed

    def print(self):
        s = ''
        for y in range(self.height):
            for x in range(len(self.cells[y])):
                s = f"{s}{self.cells[y][x].cur}"
            s = f"{s}\n"
        s.strip()
        print(s)

    @property
    def total_occupied(self):
        tot = 0
        for y in range(self.height):
            for x in range(len(self.cells[y])):
                cell = self.cells[y][x]
                if cell.is_occupied:
                    tot += 1
        return tot


def gen_grid(raw):
    grid = Grid()
    rows = raw.split('\n')
    y = 0
    while y < len(rows):
        grid.cells.append([])
        row = rows[y]
        x = 0
        while x < len(row):
            val = Cell(row[x])
            grid.cells[y].append(val)
            x += 1
        y += 1
    return grid


def part1(raw):
    print("Running part 1...")
    grid = gen_grid(raw)
    rounds = 0
    changed = 1
    while changed > 0:
        changed = grid.new_round(visibility=1, max_occupied=4)
        rounds += 1

    return grid.total_occupied


def part2(raw):
    print("Running part 2...")
    grid = gen_grid(raw)
    rounds = 0
    changed = 1

    while changed > 0:
        changed = grid.new_round(visibility=None, max_occupied=5)
        rounds += 1

    return grid.total_occupied

puz_in = aoctools.puzzle_input(2020, 11)
test_data = '''L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL'''

aoctools.test(1, part1, test_data, 37)
aoctools.test(2, part2, test_data, 26)

aoctools.submit(1, part1, puz_in)
aoctools.submit(2, part2, puz_in)
