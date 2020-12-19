
import aoctools

puz_in = aoctools.puzzle_input(2020, 3)

test_data = '''..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#'''

TREE = '#'


def trees_hit(rows, right=1, down=1):
    hits = 0
    width = len(rows[0])
    i = 0
    x = 0
    while i < len(rows):
        row = rows[i]
        if row[x] == TREE:
            hits += 1
        i += down
        x = (x + right) % width
    return hits


def part1(raw):
    rows = raw.split('\n')
    return trees_hit(rows, right=3, down=1)


def part2(raw):
    rows = raw.split('\n')
    hits = []
    for slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        hits.append(trees_hit(rows, right=slope[0], down=slope[1]))
    prod = 1
    for hit in hits:
        prod *= hit
    return prod


aoctools.test(1, part1, test_data, 7)
aoctools.test(2, part2, test_data, 336)

print(f"Part 1 Answer: {part1(puz_in)}")
print(f"Part 2 Answer: {part2(puz_in)}")
input()
