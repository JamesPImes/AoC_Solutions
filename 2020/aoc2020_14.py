
import aoctools
import re

STR_LENGTH = 36
MASK_RE = re.compile(r'mask = ([X01]+)')
MEM_RE = re.compile(r'mem\[(\d+)] = (\d+)')


def unpack_mask(raw):
    mo = MASK_RE.search(raw)
    return mo[1]


def unpack_mem(raw):
    mo = MEM_RE.search(raw)
    return int(mo[1]), int(mo[2])


def dec_to_bin(n, length=None):
    """
    Convert a decimal integer to its binary equivalent; with leading 0's
    sufficient to return a string of at least `length`.
    """
    raw_bin = bin(n)[2:]
    if length is None:
        return raw_bin
    return f"{'0' * (length - len(raw_bin))}{raw_bin}"


def bin_to_dec(b):
    """
    Convert the binary representation of a number (entered as a string)
    to its decimal int equivalent.
    """
    return int(b, 2)


def part1(raw):

    def parse_mask(mask_raw):
        """
        Parse a string representation of a mask into a dict of indexes
        and values. (Part 1 rules)
        """
        mask = {}
        i = 0
        while i < len(mask_raw):
            ch = mask_raw[i]
            if ch in ['0', '1']:
                mask[i] = int(ch)
            i += 1

        return mask

    def apply_mask(n: int, mask: dict, length=STR_LENGTH):
        b = dec_to_bin(n, length=length)
        for k, v in mask.items():
            b = list(b)  # break apart the binary representation
            b[k] = str(v)  # replace the character at index `k`, per mask
            b = ''.join(b)  # rejoin the binary to a string
        return bin_to_dec(b)

    def write_to_memory(raw_instructions):
        mem = {}
        mask = {}
        for line in raw_instructions.split('\n'):
            if line.startswith('mask'):
                mask = unpack_mask(line)
                mask = parse_mask(mask)
            else:
                mem_loc, dec_val = unpack_mem(line)
                mem[mem_loc] = apply_mask(int(dec_val), mask)

        return mem

    mem = write_to_memory(raw)
    return sum(mem.values())


def part2(raw):

    def parse_mask(mask_raw):
        """
        Parse a string representation of a mask into a dict of indexes
        (dict keys) and corresponding functions (dict values). (Part 2
        rules.)
        """
        mask = {}
        i = 0
        while i < len(mask_raw):
            ch = mask_raw[i]
            if ch == '0':
                # Leave this char as is.
                mask[i] = lambda a: a
            elif ch == '1':
                # Turn this char into a 1
                mask[i] = lambda _: '1'
            else:
                # Turn this char into a 'X'
                mask[i] = lambda _: 'X'
            i += 1

        return mask

    def apply_mask(n: int, mask: dict, length=STR_LENGTH):
        b = dec_to_bin(n, length=length)
        for k, func in mask.items():
            b = list(b)
            ch = b[k]
            b[k] = func(ch)
            b = ''.join(b)
        return b

    def floating_permutations(bit_raw):
        """
        Get a list of all permutations of floating memory.
        """
        if isinstance(bit_raw, str):
            bit_raw = [bit_raw]

        new_perms = []
        for b in bit_raw:
            mo = re.search('X', b)
            if mo is None:
                new_perms.append(b)
                continue
            down_perms = [
                re.sub('X', '0', b, count=1),
                re.sub('X', '1', b, count=1)
            ]
            new_perms.extend(floating_permutations(down_perms))
        return new_perms

    def write_to_memory(raw_instructions):
        mem = {}
        mask = {}
        for line in raw_instructions.split('\n'):
            if line.startswith('mask'):
                mask = unpack_mask(line)
                mask = parse_mask(mask)
            else:
                mem_loc_raw, dec_val = unpack_mem(line)
                mem_loc = apply_mask(int(mem_loc_raw), mask)
                all_mem_locs = floating_permutations(mem_loc)
                for ml in all_mem_locs:
                    mem[ml] = int(dec_val)
        return mem

    mem = write_to_memory(raw)
    return sum(mem.values())


puz_in = aoctools.puzzle_input(2020, 14)

test_data1 = '''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0'''

test_data2 = '''mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1'''

aoctools.test(1, part1, test_data1, 165)
aoctools.test(2, part2, test_data2, 208)

aoctools.submit(1, part1, puz_in)
aoctools.submit(2, part2, puz_in)
