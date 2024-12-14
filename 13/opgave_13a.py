from itertools import zip_longest
import re
import numpy as np


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
        # print(button_a, button_b, prize)
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

    a = np.array([[ax, bx], [ay, by]])
    b = np.array([x, y])
    ans = np.linalg.solve(a, b)

    check_x = ax * round(ans[0]) + bx * round(ans[1])
    check_y = ay * round(ans[0]) + by * round(ans[1])

    if (ans[0] < 1) or (ans[1] < 1):
        print('Lower than 0')
        return 0
    # print(f'{x=:6} {check_x=:6} dx={x-check_x:3} {y=:6} {check_y=:6} dy={y-check_y:3} {ans=}')   # noqa
    if (abs(x-check_x) < 1) and (abs(y-check_y) < 1):
        # if (ans[0].is_integer()) and (ans[1].is_integer()):
        # print(x, '=', check_x, y, '=', check_y, 'OK')
        print(f'{x=:6} {check_x=:6} dx={x-check_x:3} {y=:6} {check_y=:6} dy={y-check_y:3} {ans=} OK')   # noqa
        return int(3 * round(ans[0]) + round(ans[1]))
    else:
        # , y, '=', check_y, 'nOK')
        print(f'{x=:6} {check_x=:6} dx={x-check_x:3} {y=:6} {check_y=:6} dy={y-check_y:3} {ans=} nOK')   # noqa

        return 0


def main():

    # machines = read_puzzle('13/ex1.txt')
    machines = read_puzzle('13/input.txt')

    result = []

    for m in machines:
        result.append(solve(m))

    print('\n\n\n')
    # print(result)
    print(sum(result))  # 40369 for A, 72587986598368 for B


if __name__ == "__main__":
    main()
