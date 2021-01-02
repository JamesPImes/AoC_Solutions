
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


def part2(raw):
    # NOTE: Implementation for this is my own, but the Reddit megathread
    # clued me into the principal at play here. Before this, I had a
    # brute-force solution that I'm pretty sure was logically correct
    # but would have taken about a month to compute.

    _, buses = raw.split('\n')
    buses = [x for x in buses.split(',')]
    offsets = {int(buses[i]): i for i in range(len(buses)) if buses[i] != 'x'}
    buses = [int(x) for x in buses if x != 'x']

    def check_solution(depart_time):
        for bus in buses:
            if (depart_time + offsets[bus]) % bus != 0:
                return False
        return True

    start = 0
    incrementer = buses[0]
    for i in range(len(buses) - 1):
        depart_time = start
        meetup_markers = []
        bus_1 = buses[i]
        bus_2 = buses[i + 1]
        while True:
            if (depart_time + offsets[bus_1]) % bus_1 == 0 and \
                    (depart_time + offsets[bus_2]) % bus_2 == 0:
                meetup_markers.append(depart_time)
            if len(meetup_markers) == 2:
                incrementer = meetup_markers[1] - meetup_markers[0]
                start = meetup_markers[0]
                break
            else:
                depart_time += incrementer

        if check_solution(depart_time=start):
            # In case we stumble onto a solution before checking all buses...
            return start

    while True:
        if check_solution(start):
            return start
        start += incrementer


puz_in = aoctools.puzzle_input(2020, 13)
test_data = '''939
7,13,x,x,59,x,31,19'''

aoctools.test(1, part1, test_data, 295)
aoctools.test(2, part2, test_data, 1068781)

aoctools.submit(1, part1, puz_in)
aoctools.submit(2, part2, puz_in)
