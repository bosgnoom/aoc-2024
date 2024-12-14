import re
import pprint
import numpy as np


def read_puzzle(filename: str) -> list[dict]:
    with open(filename) as f:
        lines = [a for a in f.read().split('\n') if len(a) > 1]

    puzzle = []
    for i, line in enumerate(lines):
        numbers = re.findall(r'(-?\d+)', line)

        py, px, vy, vx = numbers

        puzzle.append({'p': (int(px), int(py)),
                       'v': (int(vx), int(vy))})

    return puzzle


def print_map(puzzle, shape):

    cols, rows = shape

    map = np.zeros(shape=(rows, cols))

    for robot in puzzle:
        x, y = robot['p']
        map[x, y] += 1

    pprint.pprint(map)
    for cols in map:
        print(''.join([str(int(x)) if x > 0 else '.' for x in cols]))

    # Look up quadrants
    rows, cols = shape
    slice_c = cols // 2
    rows_c = rows // 2

    q1 = np.sum(map[:rows_c, :slice_c])
    q2 = np.sum(map[:rows_c, -slice_c:])
    q3 = np.sum(map[-rows_c:, :slice_c])
    q4 = np.sum(map[-rows_c:, -slice_c:])

    # print(q1, q2, q3, q4)
    # Multiply to get to calculate safety factor
    result = np.prod([q1, q2, q3, q4])
    # print(f'\n\nSafety score: {q1}*{q2}*{q3}*{q4} = {int(result)}')
    print()


def update_positions(puzzle, shape=(11, 7)):
    updated_puzzle = []
    for robot in puzzle:
        # Get robot position and direction
        x, y = robot['p']
        dx, dy = robot['v']

        # Get map size
        rows, cols = shape

        # Update position
        print(f'Old pos: {x=}, {y=}, {robot['v']=}')
        x += dx
        y += dy
        print(f'New pos: {x=}, {y=}')

        # Fix out of bounds
        if y < 0:
            y += rows

        if y >= rows:
            y = y - rows

        if x < 0:
            x += cols

        if x >= cols:
            x = x-cols

        print(f'New pos: {x=}, {y=}')

        robot['p'] = (x, y)

        updated_puzzle.append(robot)

    return updated_puzzle


# puzzle = (read_puzzle('14/ex1.txt'))

puzzle = [{'p': (2, 4), 'v': (2, -3)}]
(wide, tall) = (11, 7)

print_map(puzzle, (wide, tall))
for i in range(1):

    # shape 11 wide, 7 tall
    puzzle = update_positions(puzzle)
    print_map(puzzle, (wide, tall))
