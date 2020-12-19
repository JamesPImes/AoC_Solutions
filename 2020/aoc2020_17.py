
import aoctools

INACTIVE = '.'
ACTIVE = '#'


class Cell:
    def __init__(self, cur):
        self.cur = cur
        self.next = cur

    @property
    def is_active(self):
        return self.cur == ACTIVE

    def end_of_round(self):
        self.cur = self.next

    def turn_on(self):
        if self.cur == INACTIVE:
            self.next = ACTIVE

    def turn_off(self):
        if self.cur == ACTIVE:
            self.next = INACTIVE


class Space:
    def __init__(self, dim=3):
        """
        :param dim: How many dimensions this space exists in (3 or 4).
        """
        self.cells = {}
        self.x_rge = (0, 0)
        self.y_rge = (0, 0)
        self.z_rge = (0, 0)
        self.w_rge = (0, 0)
        self.dim = dim

    def new_cell(self, xyz, status=INACTIVE):
        """
        Create a new Cell at coord `xyz`, and update the grid ranges,
        as appropriate.
        """
        self.cells.setdefault(xyz, Cell(status))
        if self.dim == 4:
            x, y, z, w = xyz
        else:
            x, y, z = xyz
            w = 0

        # Update `self.x_rge`, `.y_rge`, `.z_rge`, and `.w_rge`, as needed
        for val, rge in [(x, 'x_rge'), (y, 'y_rge'), (z, 'z_rge'), (w, 'w_rge')]:
            mn, mx = getattr(self, rge)
            if val < mn:
                setattr(self, rge, (val, mx))
            elif val > mx:
                setattr(self, rge, (mn, val))
        return self.cells[xyz]

    def expand(self):
        """
        Expand the currently known universe by 1 unit in all directions.
        """
        for k in self.perimeter_coords():
            for j in self.adjacent_coords(k):
                # By pinging each adjacent coord with `.new_cell()`, it
                # initializes it, if it doesn't already exist. (If it
                # DOES already exist, no new cell will be created.)
                #
                # TODO: This is inefficient, in that it pings many cells
                #  multiple times, and pings cells facing toward the
                #  center. This would probably run a lot faster if I
                #  wrote a method to ping only the outside adjacent cells.
                self.new_cell(j)

    def perimeter_coords(self):
        """
        Return a list of coords of the outermost (known) cells in our
        space.
        """
        x_mn, x_mx = self.x_rge
        y_mn, y_mx = self.y_rge
        z_mn, z_mx = self.z_rge

        # TODO: There must be a more efficient (and less repetitive) way
        #  to do this.
        if self.dim == 4:
            w_mn, w_mx = self.w_rge
            perim = [
                (x, y, z, w)
                for x in self.x_rge
                for y in range(y_mn, y_mx + 1)
                for z in range(z_mn, z_mx + 1)
                for w in range(w_mn, w_mx + 1)
            ]
            perim.extend([
                (x, y, z, w)
                for x in range(x_mn, x_mx + 1)
                for y in self.y_rge
                for z in range(z_mn, z_mx + 1)
                for w in range(w_mn, w_mx + 1)
            ])
            perim.extend([
                (x, y, z, w)
                for x in range(x_mn, x_mx + 1)
                for y in range(y_mn, y_mx + 1)
                for z in self.z_rge
                for w in range(w_mn, w_mx + 1)
            ])
            perim.extend([
                (x, y, z, w)
                for x in range(x_mn, x_mx + 1)
                for y in range(y_mn, y_mx + 1)
                for z in range(z_mn, z_mx + 1)
                for w in self.w_rge
            ])

        else:
            perim = [
                (x, y, z)
                for x in self.x_rge
                for y in range(y_mn, y_mx + 1)
                for z in range(z_mn, z_mx + 1)
            ]
            perim.extend([
                (x, y, z)
                for x in range(x_mn, x_mx + 1)
                for y in self.y_rge
                for z in range(z_mn, z_mx + 1)
            ])
            perim.extend([
                (x, y, z)
                for x in range(x_mn, x_mx + 1)
                for y in range(y_mn, y_mx + 1)
                for z in self.z_rge
            ])

        # Get rid of duplicates by converting to a set.
        return set(perim)

    def get_cell(self, xyz):
        """
        Return the Cell at coord `xyz`. If it does not exist, initialize
        it first (as inactive) and store it, then return it.
        """
        if xyz in self.cells.keys():
            return self.cells[xyz]
        return self.new_cell(xyz, INACTIVE)

    def adjacent_coords(self, xyz: tuple):
        """
        Get a list of coords of all cells adjacent to coord `xyz`.
        """
        if self.dim == 4:
            x, y, z, w = xyz
            adjacent = [
                (i, j, k, l)
                for i in range(x - 1, x + 2)
                for j in range(y - 1, y + 2)
                for k in range(z - 1, z + 2)
                for l in range(w - 1, w + 2)
            ]
        else:
            x, y, z = xyz
            adjacent = [
                (i, j, k)
                for i in range(x - 1, x + 2)
                for j in range(y - 1, y + 2)
                for k in range(z - 1, z + 2)
            ]
        # Remove our center cell
        adjacent.remove(xyz)
        return adjacent

    def count_adjacent_act(self, xyz: tuple):
        adjacent = self.adjacent_coords(xyz)

        act_count = 0
        for coord in adjacent:
            act_count += 1 if self.get_cell(coord).is_active else 0

        return act_count

    @property
    def all_coords(self):
        """
        Return a list of all coords at which a Cell has been
        initialized.
        """
        return list(self.cells.keys())

    def new_round(self):
        self.expand()
        for xyz in self.all_coords:
            cell = self.cells[xyz]

            # How many currently active cells within range.
            act_count = self.count_adjacent_act(xyz)

            # Rules for turning on and off, per puzzle instructions
            if cell.is_active and act_count not in [2, 3]:
                # print(cell.is_active, act_count)
                cell.turn_off()
            if (not cell.is_active) and act_count == 3:
                cell.turn_on()

        for cell in self.cells.values():
            cell.end_of_round()

    @property
    def total_active(self):
        tot = 0
        for cell in self.cells.values():
            if cell.is_active:
                tot += 1
        return tot


def gen_space(raw, dim=3):
    space = Space(dim=dim)
    rows = raw.split('\n')
    y = 0
    z = 0
    w = 0
    while y < len(rows):
        row = rows[y]
        x = 0
        while x < len(row):
            if dim == 4:
                space.new_cell((x, y, z, w), status=row[x])
            else:
                space.new_cell((x, y, z), status=row[x])
            x += 1
        y += 1
    return space


def part1(raw):
    print("Running part 1...")
    space = gen_space(raw, dim=3)
    end_round = 6
    for i in range(end_round):
        space.new_round()

    return space.total_active


def part2(raw):
    print("Running part 2...")
    space = gen_space(raw, dim=4)
    end_round = 6
    for i in range(end_round):
        space.new_round()

    return space.total_active


puz_in = aoctools.puzzle_input(2020, 17)
test_data = '''.#.
..#
###'''

aoctools.test(1, part1, test_data, 112)
aoctools.test(2, part2, test_data, 848)

aoctools.submit(1, part1, puz_in)
aoctools.submit(2, part2, puz_in)
