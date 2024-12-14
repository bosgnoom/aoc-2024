from pulp import *
from itertools import zip_longest
import re
from gurobipy import Env


def grouper(iterable, n, *, incomplete='fill', fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks."
    # From: https://docs.python.org/3/library/itertools.html#itertools.zip_longest
    # grouper('ABCDEFG', 3, fillvalue='x') → ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') → ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') → ABC DEF
    iterators = [iter(iterable)] * n
    match incomplete:
        case 'fill':
            return zip_longest(*iterators, fillvalue=fillvalue)
        case 'strict':
            return zip(*iterators, strict=True)
        case 'ignore':
            return zip(*iterators)
        case _:
            raise ValueError('Expected fill, strict, or ignore')


def read_puzzle(filename: str, conversion: int = 0) -> list[dict]:

    with open(filename) as f:
        lines = f.readlines()

    puzzle = []
    for button_a, button_b, prize, _ in grouper(lines, 4):
        ax, ay = re.findall('X(.*), Y(.*)', button_a)[0]
        bx, by = re.findall('X(.*), Y(.*)', button_b)[0]
        x, y = re.findall('X=(.*), Y=(.*)', prize)[0]

        puzzle.append({'a': [int(ax), int(ay)],
                       'b': [int(bx), int(by)],
                       'prize': [int(x)+conversion, int(y)+conversion]})

    return puzzle


def solve(machine: dict) -> int:
    # unpack machine here

    ax, ay = machine['a']
    bx, by = machine['b']
    x, y = machine['prize']
    x += 10**13
    y += 10**13

    c1, c2, c3, c4, c5, c6 = ax, bx, x, ay, by, y
    # Solve for a and b
    b = (c1 * c6 - c4 * c3) / (c1 * c5 - c4 * c2)
    a = (c3 - c2 * b) / c1

    # Check if a and b are integers
    if a.is_integer() and b.is_integer():
        return a * 3 + b
    else:
        return 0


def main():

    machines = read_puzzle('13/input.txt')
    # pprint.pprint(machines)

    result = []

    for m in machines:
        result.append(solve(m))
    # solve(machines[1])

    print('\n\n\n')
    print(result)
    print(sum(result))


if __name__ == "__main__":
    main()
