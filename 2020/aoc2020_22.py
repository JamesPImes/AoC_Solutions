
import aoctools


def parse_raw(raw):
    players_raw = raw.split('\n\n')
    starting_hands = {}
    for ph in players_raw:
        p, c = ph.split(':\n')
        player = int(p.replace('Player ', ''))
        starting_hands[player] = [int(x) for x in c.split('\n')]

    return starting_hands


def new_turn(hands):
    p1, p2 = hands[1].pop(0), hands[2].pop(0)
    assert p1 != p2
    if p1 > p2:
        hands[1].extend([p1, p2])
    else:
        hands[2].extend([p2, p1])


def score_hand(hand):
    score = 0
    total_cards = len(hand)
    for i in range(total_cards):
        score += hand[i] * (total_cards - i)
    return score


def part1(raw):
    hands = parse_raw(raw)
    total_cards = len(hands[1]) + len(hands[2])

    while total_cards not in [len(hands[1]), len(hands[2])]:
        new_turn(hands)
    return max([score_hand(hands[1]), score_hand(hands[2])])


puz_in = aoctools.puzzle_input(2020, 22)
test_data = '''Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10'''

aoctools.test(1, part1, test_data, 306)
# aoctools.test(2, part2, test_data, 0)

aoctools.submit(1, part1, puz_in)
# aoctools.submit(2, part2, puz_in)
