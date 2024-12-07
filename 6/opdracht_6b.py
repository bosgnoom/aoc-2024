from collections import defaultdict
from multiprocessing import Pool
from functools import partial
from copy import deepcopy

from opdracht_6a import read_puzzle, find_elf


def find_empty_points(grid: list[list]) -> list:
    """Looks for positions where an item could be placed in the grid

    Args:
        grid (list[list]): Original grid

    Returns:
        list: List of tuples with coordinates
    """
    dots = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '.':
                dots.append((row, col))

    return dots


def modify_grid(grid: list[list], pos: tuple) -> list[list]:
    """Places an object in the grid on the given position,
    uses deepcopy to make sure that the original grid is not
    changed.

    Args:
        grid (list[list]): Original puzzle grid
        pos (tuple): row, col

    Returns:
        list[list]: Modified grid
    """
    row, col = pos
    grid2 = deepcopy(grid)
    grid2[row][col] = "#"

    return grid2


def walk_the_grid_many_times(grid: list[list], pos: tuple, dir: str) -> int:
    """Walk through the maze. Used for repeated runs through modified mazes

    Args:
        grid (list[list]): (modified) puzzle maze
        pos (tuple): row, col
        dir (str): direction of elf

    Returns:
        int: amount of visited places in the grid, returns 0 for loops
    """

    # Find limits of grid
    last_row = len(grid)-1
    last_col = len(grid[0])-1

    # Get current position
    row, col = pos

    # Store how often we are in a position
    memory = defaultdict(int)

    # Use dicts to determine where the elf is moving to
    direction_map = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    direction_change = {'^': '>', '>': 'v', 'v': '<', '<': '^'}

    # Let the elf walk in the grid,
    # break when exit reached or infinite loop
    while True:
        # Determine where the next step will lead the elf
        drow, dcol = direction_map[dir]

        # Did the elf found the exit?
        if not (0 <= row + drow <= last_row and 0 <= col + dcol <= last_col):
            break

        # Nope, let's mark the place
        grid[row][col] = 'X'

        # Has the elf been here before?
        memory[(row, col)] += 1
        if memory[(row, col)] > 256:
            # If many times, it's stuck in a loop, exit
            # 256 is arbitrary chosen, in the first assignment
            # the maximum was 128...
            return 0

        # If elf takes a step, will it encounter an obstacle?
        if grid[row + drow][col + dcol] == '#':
            dir = direction_change[dir]
        else:
            # Elf takes a step
            row += drow
            col += dcol

    # print('Exit found!')

    # Count the positions in the grid where we've been
    result = sum([row.count('X') for row in grid])

    # print(f'Amount of positions: {result}\n')

    # Find out what the busiest position was
    # mem = []
    # for k, v in memory:
    #     mem.append(v)
    # print(f'Busiest position: {max(mem)}')

    return result


def process_dot(dot: tuple, grid: list[list], pos: tuple, direction: str):
    """Helper function for multiprocessing

    Args:
        dot (tuple): Position of the grid to change
        grid (list[list]): Original grid
        pos (tuple): Position of the elf
        direction (str): Direction of the elf

    Returns:
        function: walk_the_grid_many_times with altered grid
    """
    # print(f'Testing dot {dot}')
    new_grid = modify_grid(grid, dot)
    return walk_the_grid_many_times(new_grid, pos, direction)


def opdracht_6b(filename: str) -> None:
    # Read in maze
    grid = read_puzzle(filename)

    # Find where the elf starts
    pos, direction = find_elf(grid)

    # Find empty spots in grid (.)
    empty_positions = find_empty_points(grid)

    # Let's bruteforce this one!
    print(f'Amount of empty spots: {len(empty_positions)}')

    # Loop over all possible positions where a . was in the grid
    loop_points = []

    # Partial function, so static input parameters can be passed
    partial_func = partial(process_dot, grid=grid,
                           pos=pos, direction=direction)

    # Doing the hard work here
    with Pool() as p:
        loop_points = p.map(partial_func, empty_positions)

    print(f'Loop points: {loop_points.count(0)}')

    return loop_points.count(0)


if __name__ == "__main__":
    assert opdracht_6b('6/input.txt') == 2188

    # For next time: let opdracht 6a return its path,
    # because that are the only ones where an additional
    # object will alter the path of the elf (initially)...
