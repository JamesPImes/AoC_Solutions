
import aoctools


def part1(raw):
    """
    Determine the next bus to leave, after my 'earliest' time; and how
    long we have to wait for it (after 'earliest').  Return the product
    of the bus ID number and how many minutes we have to wait.
    """
    earliest, buses = raw.split('\n')
    earliest = int(earliest)
    rough_buses = [x if x == 'x' else int(x) for x in buses.split(',')]
    num_buses = [n for n in rough_buses if type(n) == int]

    next_departures_all = {}
    for bus in num_buses:
        next_departures_all[bus] = (earliest // bus) * bus + bus

    # Sort them all by their departure time into tuples (bus_id, depart_time)
    bus_time_pairs = sorted(next_departures_all.items(), key=lambda d: d[1])

    # Unpack the first-to-depart bus and its departure time.
    bus_id, depart_time = bus_time_pairs[0]

    return bus_id * (depart_time - earliest)


# TODO: Part 2


puz_in = aoctools.puzzle_input(2020, 13)
test_data = '''939
7,13,x,x,59,x,31,19'''

aoctools.test(1, part1, test_data, 295)

aoctools.submit(1, part1, puz_in)
aoctools.submit(2, None, None)
