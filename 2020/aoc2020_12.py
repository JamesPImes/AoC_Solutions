
import aoctools


class Ship:
    """
    A vessel at sea during a horrible storm.
    """

    cardinals = {
        'E': 0,
        'S': 90,
        'W': 180,
        'N': 270
    }

    def __init__(self, wp=None):
        """
        NOTE: Must provide a Waypoint object (`wp`) for Part 2. Not
        needed for a Ship operating under Part 1 rules.
        """
        self.cur_dir = 0
        self.ew = 0
        self.ns = 0
        self.wp = wp

    def move(self, distance, direction=None):
        """
        Move the Ship a specific `distance`. If `direction` is specified
        (either as an int in increments of 90, with 0 being East, 90
        being South, etc.; or as 'E', 'S', 'W', 'N'), the ship will move
        that direction without changing the direction it 'wants' to go
        (i.e. its `.cur_dir`). If unspecified, it will move forward in
        its currently stored direction (`.cur_dir`).
        """
        if direction is None:
            direction = self.cur_dir
        elif direction in self.cardinals.keys():
            direction = Ship.cardinals[direction]

        if direction in [90, 180]:
            distance *= -1

        if direction in [0, 180]:
            self.ew += distance
        else:
            self.ns += distance

    def turn(self, lr='R', degrees=0):
        """
        Rotate the Ship left or right (`lr`) by `degrees` (an int, in
        increments of 90).
        """
        if lr == 'L':
            degrees *= -1
        self.cur_dir = (self.cur_dir + degrees) % 360

    def read_instruct_part1(self, line):
        """
        Read instructions per Part 1 interpretation, i.e. each
        instruction is handled internally (move N/S/E/W or turn
        according to the position of the Ship itself).
        """
        inst, num = line[0], int(line[1:])
        if inst in Ship.cardinals.keys():
            self.move(distance=num, direction=inst)
        elif inst in ['L', 'R']:
            self.turn(lr=inst, degrees=num)
        else:
            self.move(distance=num)

    def read_instruct_part2(self, line):
        """
        Read instructions per Part 2 interpretation, i.e. cardinals
        and turns are actually instructions for our Waypoint, and only
        'forward' ('F') is meant for this Ship (in relation to our
        Waypoint).
        """
        inst, num = line[0], int(line[1:])
        if inst in Ship.cardinals.keys():
            self.wp.move(distance=num, direction=inst)
        elif inst in ['L', 'R']:
            self.wp.turn(lr=inst, degrees=num)
        else:
            self.chase_wp(n=num)

    @property
    def manhattan(self):
        """
        Return the current 'Manhattan distance'.
        """
        return abs(self.ew) + abs(self.ns)

    def chase_wp(self, wp=None, n=0):
        """
        Move `n` times to the Waypoint `wp` (which moves relative to
        this Ship).
        """
        if wp is None:
            wp = self.wp

        self.ew += (wp.ew_delta * n)
        self.ns += (wp.ns_delta * n)


class Waypoint:
    """
    A beacon of hope, whose (0, 0) coord is a Ship trying to navigate to
    it.
    """

    def __init__(self, coord=(10, 1)):
        self.ew_delta = coord[0]
        self.ns_delta = coord[1]

    def move(self, distance, direction=0):
        if direction in ['S', 'W']:
            distance *= -1

        if direction in ['N', 'S']:
            self.ns_delta += distance
        elif direction in ['E', 'W']:
            self.ew_delta += distance

    def turn(self, lr='R', degrees=0):
        """
        Rotate this Waypoint around (0,0), in increments of 90 degrees.
        """

        # Just in case our dataset contains any rotations > 1.
        degrees %= 360

        # Convert counter-clockwise rotations to clockwise
        if lr == 'L':
            degrees = (360 - degrees) % 360

        # We'll rotate this many 90-degree increments
        if degrees % 90 != 0:
            raise ValueError('Works only for 90-degree increments.')

        for _ in range(degrees//90):
            # Rotate a quarter-turn for every 90 degrees
            self.ew_delta, self.ns_delta = self.ns_delta, -self.ew_delta


def part1(raw):
    instructs = raw.split('\n')
    ship = Ship()
    for inst in instructs:
        ship.read_instruct_part1(inst)

    return ship.manhattan


def part2(raw):
    instructs = raw.split('\n')
    wp = Waypoint(coord=(10, 1))
    ship = Ship(wp=wp)
    for inst in instructs:
        ship.read_instruct_part2(inst)

    return ship.manhattan


puz_in = aoctools.puzzle_input(2020, 12)
test_data = '''F10
N3
F7
R90
F11'''

aoctools.test(1, part1, test_data, 25)
aoctools.test(2, part2, test_data, 286)

aoctools.submit(1, part1, puz_in)
aoctools.submit(2, part2, puz_in)
