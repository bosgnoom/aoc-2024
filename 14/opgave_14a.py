import re
import numpy as np
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')


def read_puzzle(filename: str) -> list[dict]:
    """Reads puzzle from file and converts into input data

    Args:
        filename (str): filename

    Returns:
        list[dict]: like {p=0,4 v=3,-3}
    """

    with open(filename) as f:
        lines = [a for a in f.read().split('\n') if len(a) > 1]

    puzzle = []
    for i, line in enumerate(lines):
        numbers = re.findall(r'(-?\d+)', line)

        px, py, vx, vy = numbers

        puzzle.append({'p': (int(px), int(py)),
                       'v': (int(vx), int(vy))})

    return puzzle


def process_map(puzzle: list[dict], shape: tuple[int, int]) -> int:
    """Prints out the puzzle onto shape (wide, tall)

    Args:
        puzzle (list[dict]): puzzle data
        shape (tuple[int, int]): shape of map

    Returns:
        int: Safety score
    """
    cols, rows = shape

    # np.zeros in shape(rows, cols)
    map = np.zeros(shape=(rows, cols), dtype=int)

    # Fill map with robots
    for robot in puzzle:
        x, y = robot['p']
        map[y, x] += 1

    # Concat and print
    for row in map:
        logging.debug(''.join([str(int(x)) if x > 0 else '.' for x in row]))

    # Look up quadrants
    cols, rows = shape
    slice_c = cols // 2
    rows_c = rows // 2

    q1 = np.sum(map[:rows_c, :slice_c])
    q2 = np.sum(map[:rows_c, -slice_c:])
    q3 = np.sum(map[-rows_c:, :slice_c])
    q4 = np.sum(map[-rows_c:, -slice_c:])

    # Multiply to get to calculate safety factor
    result = np.prod([q1, q2, q3, q4])
    logging.info(f'\nSafety score: {q1}*{q2}*{q3}*{q4} = {result}')

    return result


def update_positions(puzzle: list[dict], shape: tuple) -> list[dict]:
    """Update position using given velocity

    Args:
        puzzle (list[dict]): List of robots
        shape (tuple): size of map

    Returns:
        list[dict]: New list of robots
    """

    updated_puzzle = []
    for robot in puzzle:
        # Get robot position and direction
        x, y = robot['p']
        dx, dy = robot['v']

        # Get map size
        rows, cols = shape

        # Update position
        logging.debug(f'Old pos: {x=}, {y=}, {robot['v']=}')
        x += dx
        y += dy
        logging.debug(f'New pos: {x=}, {y=}')

        # Update on out-of-bounds
        if y < 0:
            y += cols

        if y >= cols:
            y = y - cols

        if x < 0:
            x += rows

        if x >= rows:
            x = x-rows

        logging.debug(f'New pos: {x=}, {y=}')

        robot['p'] = (x, y)

        updated_puzzle.append(robot)

    return updated_puzzle


def main(filename, size):
    # Puzzle stores positions and velocities
    puzzle = read_puzzle(filename)

    result = 0

    process_map(puzzle, size)
    for i in range(100):
        puzzle = update_positions(puzzle, size)
        result = process_map(puzzle, size)

    return result


if __name__ == "__main__":
    # puzzle = [{'p': (2, 4), 'v': (2, -3)}]
    # puzzle = (read_puzzle('14/ex1.txt'))
    # main('14/ex1.txt', (11, 7))   # 12
    main('14/input.txt', (101, 103))  # 230172768
