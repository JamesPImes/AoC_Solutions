
import aoctools
import math

# ---------------------------------------------------------------------
# This is not yet a working solution**. It will construct rows and sort
# the rows into the correct grid ONLY if there are no tiles with a side
# that matches multiple other tiles (e.g., the test data). I need to
# design a solution that:
#   a) [DONE] Determines when the remaining tiles cannot be formed into
#       rows;
#   b) Figures out which prior row(s) to break apart to continue trying
#       to solve. The issue must(?) be either end (or both ends) of the
#       last-formed row.
#   c) Preclude the same broken row from forming again (to prevent a
#       loop), but allow other non-broken rows to reform.
#
# There are also lots of edge cases that would probably not be captured
# by my current approach (e.g., a single tile with two identical sides
# -- which is the motivation behind the partially-implemented
# cached_transforms` idea).
#
# **I mean, there is a VERY dumb tweak to my solution to make it "work"
# for part 1:
#   a) In `Grid.make_rows()`, first randomly sort the list of tile
#       names before trying to construct any rows.
#   b) Repeatedly call `.make_rows()` until chance smiles upon us and
#       gives us a random order that will successfully generate rows.
# This is, as I say, dumb (and very slow).  But it DID get me the
# correct answer:  18449208814679
#
# ... after it generated these rows:
# ['2339', '3539', '2011', '3329', '3637', '3041', '1039', '2237', '3049', '3433', '1123', '2207']
# ['2267', '1619', '3001', '2531', '3109', '1721', '3793', '3089', '2963', '3931', '2749', '1481']
# ['1291', '3557', '2767', '3671', '3407', '1093', '2663', '1307', '2423', '2837', '1091', '1609']
# ['2083', '2927', '3779', '1823', '1471', '3331', '2239', '1733', '1319', '1429', '1933', '1907']
# ['1499', '3697', '3499', '2903', '3061', '2027', '3271', '2801', '1997', '2843', '1439', '2879']
# ['2659', '3863', '1277', '3469', '2677', '1871', '1097', '1031', '2297', '3259', '1087', '1973']
# ['3119', '1951', '2753', '3929', '1201', '1193', '3347', '1511', '2377', '2791', '1613', '1163']
# ['2473', '1051', '2591', '2539', '3253', '1459', '2477', '2657', '2137', '2311', '3673', '1171']
# ['3659', '2819', '2521', '3769', '2707', '2999', '1567', '1019', '1847', '3191', '1709', '3067']
# ['1129', '3593', '2789', '3733', '2551', '3467', '1559', '1913', '1451', '3821', '2251', '3023']
# ['1361', '1223', '1249', '3739', '1999', '1747', '3623', '2069', '1187', '1987', '3559', '2803']
# ['2111', '2579', '1399', '3343', '2371', '2383', '1571', '3121', '1063', '1663', '1783', '1693']
# ---------------------------------------------------------------------


class Grid:
    def __init__(self, raw):
        self.tiles = {}

        self.parse_tiles(raw)
        self.w = self.h = int(math.sqrt(len(self.tiles)))

        # Per puzzle instructions, we should have only a square number
        # of tiles; just make sure we didn't lop off something...
        assert self.w * self.h == len(self.tiles)

    def parse_tiles(self, raw):
        tiles_raw = raw.split('\n\n')
        for tile in tiles_raw:
            nt = Tile(tile)
            self.tiles[nt.name] = nt

        return self.tiles

    def rotate_clean(self, clean):
        """
        :param clean: An list of rows, already ordered in such a way
        that they fit together. (Represents a semi-grid, construction in
        progress.)
        :return: The clean semi-grid, its contents having been rotated.
        """
        clean.reverse()
        for row in clean:
            self.rotate_row(row)
        return clean

    def rotate_row(self, row):
        """
        :param row: A list of tile names.
        :return: The row, rotated 180 degrees.
        """
        row.reverse()
        for tile_name in row:
            self.tiles[tile_name].rotate(2)
        return row

    def flip_row_ew(self, row):
        """
        :param row: A list of tile names.
        :return: The row, flipped East/West.
        """
        row.reverse()
        for tile_name in row:
            self.tiles[tile_name].flip_ew()
        return row

    def flip_row_ns(self, row):
        """
        :param row: A list of tile names.
        :return: The row, flipped North/South.
        """
        for tile_name in row:
            self.tiles[tile_name].flip_ns()
        return row

    def arrange_rows(self, rows):

        def attach_up(construction, row2):
            row1 = construction[0]
            pairs = zip(row1, row2)
            for t1, t2 in pairs:
                t1, t2 = self.tiles[t1], self.tiles[t2]
                if not t1.match_sides(t2, t1_side='N', transforms=['']):
                    return False
            construction.insert(0, row2)
            return True

        def attach_down(construction, row2):
            row1 = construction[-1]
            pairs = zip(row1, row2)
            for t1, t2 in pairs:
                t1, t2 = self.tiles[t1], self.tiles[t2]
                if not t1.match_sides(t2, t1_side='S', transforms=['']):
                    return False
            construction.append(row2)
            return True

        constructor = []
        used_row_indexes = []
        i = 0

        while True:
            # print(i)
            if len(constructor) == self.h:
                break
            elif i == len(rows):
                print(f"FAIL: {constructor}")
                input()
                return None

            print(i)
            cand_row = rows[i]
            if i in used_row_indexes:
                i += 1
                continue
            if len(constructor) == 0:
                constructor.append(cand_row)
                i += 1
                continue

            tforms = ['', 'R2', 'R2,NS', 'R2', 'R2,NS,EW', 'R2']
            for tf in tforms:
                commands = tf.split(',')
                for cmd in commands:
                    if cmd == 'R2':
                        self.rotate_row(cand_row)
                    elif cmd == 'NS':
                        self.flip_row_ns(cand_row)
                    elif cmd == 'EW':
                        self.flip_row_ew(cand_row)
                if attach_up(constructor, cand_row):
                    used_row_indexes.append(i)
                    i = 0
                    break
                elif attach_down(constructor, cand_row):
                    used_row_indexes.append(i)
                    i = 0
                    break
            i += 1
        print("Success! -------------- ")
        for r in constructor:
            print(r)
        print("Success! -------------- ")
        return constructor

    def make_rows(self):
        rows = []
        av_tiles = list(self.tiles.keys())
        av_tiles.sort()

        # ALERT: Bodgetown, USA. Population: The next two lines of code.
        import random
        av_tiles.sort(key=lambda x: random.randint(0, 1000))

        while True:
            print(f"Row {len(rows) + 1}...")
            row = self.make_row(av_tiles)
            if row is not None:
                rows.append(row)
                print(rows)
                # av_tiles = list(set(av_tiles) - set(row))
                # av_tiles.sort()
                av_tiles = [t for t in av_tiles if t not in row]
            else:
                print("Cannot make more rows.")
                print(f"remain: {av_tiles}")
                for t in self.tiles.values():
                    t.locked = False
                    t.cached_transforms = None
                return -1
            if len(av_tiles) == 0:
                break
        print("Success! -------------- (Unordered rows)")
        for r in rows:
            print(r)
        print("Success! -------------- (Unordered rows)")
        return rows

    def make_row(self, available_tiles: list):
        """
        :param available_tiles: A list of tile names that are available
        to use.
        :return: If successful, returns a list of tile names that
        connect; otherwise returns None.
        """

        def attach_to_right(row, t2, use_cached=False):
            try:
                t1 = self.tiles[row[-1]]
            except IndexError:
                return False
            transforms = None
            if use_cached:
                transforms = t2.cached_transforms
            if t1.match_sides(t2, t1_side='E', transforms=transforms):
                row.append(t2.name)
                return True
            return False

        def attach_to_left(row, t2, use_cached=False):
            try:
                t1 = self.tiles[row[0]]
            except IndexError:
                return False
            transforms = None
            if use_cached:
                transforms = t2.cached_transforms
            if t1.match_sides(t2, t1_side='W', transforms=transforms):
                row.insert(0, t2.name)
                return True
            return False

        c_row = []  # candidate row
        used_tile_indexes = []
        # TODO: Possible optimization: Cache apparent partial rows that
        #  had to be removed from the grid. (ASSUMING that the puzzle
        #  input has tiles whose sides might match to multiple others.)
        i = 0

        while True:
            # print(i)
            if len(c_row) == self.w:
                return c_row
            elif i == len(available_tiles):
                print(f"FAIL: {c_row}")
                return None
            if i in used_tile_indexes:
                i += 1
                continue
            cand_tile = available_tiles[i]
            if len(c_row) == 0:
                c_row.append(cand_tile)
                used_tile_indexes.append(i)
                i += 1
                continue

            t2 = self.tiles[cand_tile]

            # Try attaching right, then left
            if attach_to_right(c_row, t2):
                used_tile_indexes.append(i)
                i = 0
                continue
            elif attach_to_left(c_row, t2):
                used_tile_indexes.append(i)
                i = 0
                continue
            i += 1


class Tile:
    def __init__(self, raw_tile: str):
        name, face = raw_tile.split(':\n')
        self.name = name.replace('Tile ', '')

        # Tile face represented as nested list; `face[y][x]` for (x, y) value
        self.face = [[x for x in row] for row in face.split('\n')]

        self.w = len(self.face[0])
        self.h = len(self.face)
        self.locked = False
        self.cached_transforms = None

    @property
    def side_W(self):
        return [self.face[y][0] for y in range(self.h)]

    @property
    def side_E(self):
        return [self.face[y][self.w - 1] for y in range(self.h)]

    @property
    def side_N(self):
        return [self.face[0][x] for x in range(self.w)]

    @property
    def side_S(self):
        return [self.face[self.h - 1][x] for x in range(self.w)]

    @property
    def sides_EW(self):
        """Return a list of the left and right sides of this tile."""

        # Left/Right sides
        return [
            [self.face[y][x]
            for y in range(self.h)]
            for x in [0, self.w - 1]
        ]

        # Include the Top/Bottom sides

    @property
    def sides_NS(self):
        """Return a list of the top and bottom sides of this tile."""
        return [
            [self.face[y][x]
             for x in range(self.w)]
            for y in [0, self.h - 1]
        ]

    @property
    def sides(self):
        """
        Return a list of all sides of this tile: [W, N, E, S]
        """
        return [self.side_W, self.side_N, self.side_E, self.side_S]

    def rotate(self, n=1):
        """Rotate the face 90 degrees clockwise `n` times."""
        for _ in range(n % 4):
            rot = []
            for x in range(self.w):
                rot.append([])
                for y in range(self.h - 1, -1, -1):
                    rot[-1].append(self.face[y][x])

            self.face = rot

    def flip_ew(self):
        """Flip the face left/right."""
        for row in self.face:
            row.reverse()

    def flip_ns(self):
        """Flip the face up/down."""
        self.face.reverse()

    def find_matches(self, consider: dict):
        """
        Find all possible matches (of any side to any other side) within
        the consideration set `consider`.
        """
        pass

    def match_sides(self, t2, t1_side=None, transforms=None):
        """
        :param t2: A tile to compare to the sides of `self`.
        :param t1_side: The name of the side of our tile to which to try
        to attach `t2` -- either 'W', 'N', 'E', or 'S'.
        :param transforms: The specific transformations (in order) to
        consider for `t2`. If not specified, will use the
        transformations that it has cached; and if there are none there,
        will use all transformations.
        :return: Returns the name of the side of the `t2` Tile that
        connects to our Tile ('W', 'N', 'E', or 'S'). Returns None if
        there was no appropriate match.
        """

        # Which side of `t1` (i.e. self) matches to which side of `t2`
        matchups = {
            'W': 'E',
            'E': 'W',
            'N': 'S',
            'S': 'N'
        }

        # Side name -> the function to get that side value
        get_side = {
            'W': lambda x: x.side_W,
            'E': lambda x: x.side_E,
            'N': lambda x: x.side_N,
            'S': lambda x: x.side_S
        }

        if t1_side is None:
            t1_side = 'E'

        name1 = t1_side
        t1_side = get_side[name1](self)
        name2 = matchups[name1]

        # Possible transformations for `t2` Tile.
        # All basic rotations, including no rotation ('R1' -> rotate 1)
        tforms = ['', 'R1', 'R1', 'R1']

        # Up/Down flip, then all sides ('NS' -> flip_ns)
        tforms.extend(['R1,NS', 'R1', 'R1', 'R1'])

        # Left/Right flip, then all sides ('EW' -> flip_ew)
        tforms.extend(['R1,NS,EW', 'R1', 'R1', 'R1'])

        if transforms is None and t2.cached_transforms is not None:
            tforms = t2.cached_transforms

        # For breaking the loop when checking a locked tile.
        # TODO: Better flow control for this loop.
        keep_running = True
        while len(tforms) > 0 and keep_running:
            if not t2.locked:
                # Only if `t2` Tile is unlocked do we want to transform it
                tf = tforms.pop(0)
                if len(tforms) == 0:
                    t2.cached_transforms = None
            else:
                tf = ''
                keep_running = False
            commands = tf.split(',')
            for cmd in commands:
                if cmd == 'R1':
                    t2.rotate()
                elif cmd == 'NS':
                    t2.flip_ns()
                elif cmd == 'EW':
                    t2.flip_ew()
            t2_side = get_side[name2](t2)

            if t1_side == t2_side:
                # Cache our unused transformations with `t2` and
                # return the matched side. (We'll use the remaining
                # transformations on `t2` if it needs to be detached
                # and retried later on.)
                t2.cached_transforms = tforms

                # Do not transform the `t2` Tile again, until unlocked
                t2.locked = True

                return name2

        return None

    def print(self):
        fc = self.face
        w = self.w
        h = self.h
        print('\n'.join([''.join([fc[y][x] for x in range(w)]) for y in range(h)]))


def part1(raw):
    grid = Grid(raw)
    rows = -1
    while rows == -1:
        rows = grid.make_rows()
    arr = grid.arrange_rows(rows)
    return int(arr[0][0]) * int(arr[0][-1]) * int(arr[-1][0]) * int(arr[-1][-1])


puz_in = aoctools.puzzle_input(2020, 20)
test_data = '''Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...'''

aoctools.test(1, part1, test_data, 20899048083289)

aoctools.submit(1, part1, puz_in)

input()
