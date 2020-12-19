
import aoctools
import re

MY_KIND = 'shiny gold'
RULE_INTERPRETER = re.compile(r"((\d)?\s?([\s\D]*) bags?[ .,]{1})")


class Luggage:

    def __init__(self, kind, universe=None):
        """
        :param kind: A string, representing which kind of Luggage this
        is (e.g., 'shiny gold').
        :param universe: A dict, representing which universe this
        Luggage belongs to (e.g., is it a test dataset, or the actual
        puzzle input). Thus, the dict stored as `self.universe` provides
        access to all other Luggage instances that belong to the same
        universe.
        """
        # `.rules` stores the quantity of each kind of sub-luggages
        # this Luggage must hold
        self.rules = {}
        self.universe = universe
        if universe is None:
            self.universe = {}

        # If this Luggage does not already exist in the universe, add it now.
        self.universe.setdefault(kind, self)

    def add_rule(self, kind, quantity):
        """
        Add to this Luggage object a rule specifying how many of each
        kind we must hold.
        """
        self.rules[kind] = quantity

    @property
    def deep_contents(self):
        """
        Get the required nested contents (a list of Luggage kinds,
        i.e. strings) of one of these Luggage kinds.
        """
        contents = []

        for kind in self.rules.keys():
            # Append to our list each kind one level below this Luggage
            # (i.e. the luggages specified in `.rules` for this Luggage)
            contents.append(kind)

            # Ask the Luggage one-level down what *it* in turn holds
            # (i.e. call this method recursively, for each subordinate
            # Luggage object kind).
            subcontents = self.universe[kind].deep_contents

            # And add those contents to our list too.
            contents.extend(subcontents)

        return contents

    @property
    def total_contents(self):
        """
        Get the total number of individual nested Luggage objects
        required for of one of these Luggage kinds.
        """

        # This method functions similarly to `deep_contents` (it gets
        # called recursively), but sums and returns integers, rather
        # than a list of strings.

        total = 0
        for kind, quantity in self.rules.items():
            # Add the contents of each sub-luggage, plus 1 for the
            # luggage itself, multiplied by however many of that kind
            # we need
            total += (self.universe[kind].total_contents + 1) * quantity
        return total

    def contains_deep(self, kind):
        """
        Return a bool, whether a Luggage of `kind` is required
        somewhere in the `.deep_contents` of this Luggage object.
        """
        return kind in self.deep_contents


def unpacker(mo):
    """
    Unpack a regex match into bag `kind` and `quantity` -- i.e. a
    match of '2 shiny orange bags' will return a tuple of
    (2, 'shiny orange').
    """
    quantity = mo[2]
    kind = mo[3]

    if quantity is not None:
        quantity = int(quantity)
    return quantity, kind


def parse_rule(line, universe: dict):
    """
    Parse a line into its component parts, adding luggages
    and defining rules as needed.
    """

    # Index for which character we're starting at within the `line`.
    # Starts at 0 (the start of the string) and moves to the end of each
    # regex match (so we're not searching the same

    i = 0
    matches = 0
    defined_luggage = None
    while True:
        mo = RULE_INTERPRETER.search(line, pos=i)
        if mo is None:
            break
        matches += 1

        # Move our index to the end of our most recent match
        i = mo.end()

        # Unpack each match into quantity and kind
        quantity, kind = unpacker(mo)

        # If our `universe` does not already contain a key for this
        # kind of luggage, initialize a new Luggage and add it to
        # the `universe`.
        universe.setdefault(kind, Luggage(kind, universe=universe))

        if matches == 1:
            # The first match represents the luggage for which we'll be
            # defining rules.
            defined_luggage = universe[kind]
        else:
            defined_luggage.add_rule(kind, quantity)


def populate(raw, universe=None):
    """
    Parse the rules and populate all Luggage objects. Returns a dict
    holding each kind of Luggage object within that universe.
    """
    if universe is None:
        universe = {}
    rules = raw.split('\n')
    for rule in rules:
        parse_rule(rule, universe)
    return universe


def part1(raw, universe=None):
    """
    How many Luggage types hold my kind of luggage at some level?
    :param raw: Raw puzzle input.
    :param universe: A dict representing the universe's rules for
    luggages.
    """
    if universe is None:
        universe = populate(raw)
    holding_my_kind = 0
    for kind, luggage_obj in universe.items():
        # Check each Luggage kind to see if it contains `MY_KIND` at
        # some level (however deep). If so, add 1 to `holding_my_kind`.
        if luggage_obj.contains_deep(MY_KIND):
            holding_my_kind += 1

    return holding_my_kind


def part2(raw, universe=None):
    """
    How many total individual bags must my luggage hold?
    """
    if universe is None:
        universe = populate(raw)
    return universe[MY_KIND].total_contents


test_data = '''light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.'''

puz_in = aoctools.puzzle_input(2020, 7)
TEST_UNIVERSE = {}
PUZZLE_UNIVERSE = {}

aoctools.test(1, part1, test_data, 4)
aoctools.test(2, part2, test_data, 32)

aoctools.submit(1, part1, puz_in)
aoctools.submit(2, part2, puz_in)
