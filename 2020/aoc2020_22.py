
import aoctools


def parse_raw(raw):
    players_raw = raw.split('\n\n')
    starting_hands = {}
    for ph in players_raw:
        p, c = ph.split(':\n')
        player = int(p.replace('Player ', ''))
        starting_hands[player] = [int(x) for x in c.split('\n')]

    return starting_hands


def new_turn_part1(hands):
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


def new_game_part2(hands):
    winner = None
    card_orders = set()
    while winner is None:
        winner = new_round_part2(hands, card_orders)
    return winner


def new_round_part2(hands, card_orders):

    # Check if the cards have been in this order before. If so, player 1
    # wins the GAME.
    t1, t2 = tuple(hands[1]), tuple(hands[2])
    if (t1, t2) in card_orders:
        return 1

    # Keep track of this new order of cards.
    card_orders.add((t1, t2))

    # Draw top card
    p1, p2 = hands[1].pop(0), hands[2].pop(0)

    # Evaluate who won the round
    if len(hands[1]) >= p1 and len(hands[2]) >= p2:
        round_winner = recursive_combat(hands, p1, p2)
    elif p1 > p2:
        round_winner = 1
    else:
        round_winner = 2

    # Put the two cards back in the round winner's deck
    if round_winner == 1:
        hands[1].append(p1)
        hands[1].append(p2)
    else:
        hands[2].append(p2)
        hands[2].append(p1)

    # Check for a winner of the GAME (not the round).
    if len(hands[1]) == 0:
        return 2
    elif len(hands[2]) == 0:
        return 1
    else:
        return None


def recursive_combat(hands, p1, p2):
    # Copy the relevant portion of the hands.
    hands = {1: hands[1][:p1], 2: hands[2][:p2]}

    # Start a new game with those hands and return the winner.
    return new_game_part2(hands)


def part1(raw):
    hands = parse_raw(raw)

    while 0 not in [len(hands[1]), len(hands[2])]:
        new_turn_part1(hands)
    return max([score_hand(hands[1]), score_hand(hands[2])])


def part2(raw):
    hands = parse_raw(raw)
    new_game_part2(hands)
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
aoctools.test(2, part2, test_data, 291)

aoctools.submit(1, part1, puz_in)
aoctools.submit(2, part2, puz_in)
