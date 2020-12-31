
# ---------------------------------------------------------------------
# For the other Conway puzzles in AoC 2020 (Days 11 and 17), I created a
# class for cells and another class for the grid they exist on. For this
# puzzle, I wanted to try a simpler solution, and just used a new dict
# for the grid for each round, keyed by each tile's coord.
# ---------------------------------------------------------------------

import aoctools
import re

TILE_RE = re.compile(r"se|sw|ne|nw|e|w")

# We use a coord system for our hexagonal layout. Beginning at reference
# coord (0, 0), a step to the SE, SW, NE, or NW will change x and y each
# by 1 (+ or -, depending on the direction). Stepping E or W will leave
# the y value as it is, and change x by +2 (E) or -2 (W).
DIRECTS = {
        'se': lambda x, y: (x + 1, y - 1),
        'sw': lambda x, y: (x - 1, y - 1),
        'ne': lambda x, y: (x + 1, y + 1),
        'nw': lambda x, y: (x - 1, y + 1),
        'e': lambda x, y: (x + 2, y),
        'w': lambda x, y: (x - 2, y)
    }


def parse_directions(direct):
    """
    Parse a raw line of un-delimited directions into a list of its
    components.
    """
    d = []
    i = 0
    while i < len(direct):
        mo = TILE_RE.search(direct, pos=i)
        d.append(mo[0])
        i = mo.end()
    return d


def generate_initial_tiles(raw):
    raw_directions = raw.split('\n')

    # A dict, keyed by coord. Value of 0 means a white tile; 1 is black tile
    tiles = {}

    for direction in raw_directions:
        x, y = 0, 0
        parsed = parse_directions(direction)
        for step in parsed:
            x, y = DIRECTS[step](x, y)
        tiles.setdefault((x, y), 0)
        # Flip the tile at that coord.
        tiles[(x, y)] = (tiles[(x, y)] + 1) % 2

    # It would be somewhat more optimal not to step to each one, but to
    # just take the sum of all SE, of all SW, of all NE, etc. Since we
    # only care about the tile that gets 'stepped on' last, it doesn't
    # matter how we get there -- only its coord. This solution works
    # fast, though, so not worth redoing it for minimal improvement.

    return tiles


def conway_round(cells: dict):
    new_round = {}

    def count_adjacent(x, y):
        total_black = 0
        for func in DIRECTS.values():
            adj_coord = func(x, y)
            total_black += cells.get(adj_coord, 0)
        return total_black

    # Expand our known hex-grid by 1 tile in all directions (as needed),
    # for each outer tile that is black.
    to_add = set()
    for c, v in cells.items():
        if v == 0:
            # Don't expand if this tile is white (a modest optimization
            # that is legal for our specific Conway ruleset due to the
            # fact that white tiles surrounded by only white tiles won't
            # change).
            continue
        x, y = c
        for func in DIRECTS.values():
            adj_coord = func(x, y)
            to_add.add(adj_coord)
    for adj_coord in to_add:
        cells.setdefault(adj_coord, 0)

    # Apply our Conway rules to each cell.
    for c, v in cells.items():
        x, y = c
        black_count = count_adjacent(x, y)
        if v == 0 and black_count == 2:
            v = 1
        elif v == 1 and black_count not in [1, 2]:
            v = 0
        new_round[c] = v

    return new_round


def part1(raw):
    tiles = generate_initial_tiles(raw)

    return sum(tiles.values())


def part2(raw, rounds=100):
    tiles = generate_initial_tiles(raw)

    for _ in range(rounds):
        tiles = conway_round(tiles)

    return sum(tiles.values())


puz_in = aoctools.puzzle_input(2020, 24)
test_data = '''sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew'''

aoctools.test(1, part1, test_data, 10)
aoctools.test(2, lambda x: part2(x, 1), test_data, 15)
aoctools.test(2, lambda x: part2(x, 2), test_data, 12)
aoctools.test(2, lambda x: part2(x, 3), test_data, 25)
aoctools.test(2, lambda x: part2(x, 5), test_data, 23)
aoctools.test(2, lambda x: part2(x, 10), test_data, 37)
aoctools.test(2, lambda x: part2(x, 100), test_data, 2208)

aoctools.submit(1, part1, puz_in)
aoctools.submit(2, part2, puz_in)
