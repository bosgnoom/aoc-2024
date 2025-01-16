def print_puzzle(grid: list[list]) -> None:
    """Prints out the puzzle grid

    Args:
        grid (list[list]): Grid
    """
    for line in grid:
        print(''.join(line))

    print()


def read_puzzle(filename: str) -> list[list]:
    """Reads file with grid

    Args:
        filename (str): filename

    Returns:
        list[list]: grid
    """
    with open(filename) as f:
        lines = f.readlines()

    puzzle = []
    for line in lines:
        newline = [ch for ch in line if ch != '\n']
        puzzle.append(newline)

    return puzzle


def find_elf(grid: list[list]) -> tuple[tuple, str]:
    """Locates the elf in the grid,
    returns position and direction

    Args:
        grid (list[list]): Grid

    Returns:
        tuple[tuple, str]: position as (row, col) and direction
    """

    # Find starting position of elf
    # Row first
    row = 0
    while not any([e in grid[row] for e in '<>^v']):
        row += 1
    print(f'Found elf at row: {row}')

    # Now column and direction
    for dir in '<>^v':
        if dir in grid[row]:
            column = grid[row].index(dir)
            break

    print(f'Found elf at column: {column}')
    print(f'Found elf direction: {dir}')

    return (row, column), dir


def walk_the_grid(grid: list[list], pos: tuple, dir: str) -> int:
    """Walks the elf through the grid, counting positions where the elf has been

    Args:
        grid (list[list]): Grid
        pos (tuple): starting position of the elf
        dir (str): starting direction of the elf

    Returns:
        int: amount of tiles where the elf has been
    """

    # Find limits of grid
    last_row = len(grid)-1
    last_col = len(grid[0])-1

    # Get current position
    row, col = pos

    while True:
        # Check if move is possible given direction
        if dir == '^':
            if (row != 0) and (row != last_row):
                grid[row][col] = 'X'
                if grid[row-1][col] == '#':
                    dir = '>'
                else:
                    row = row - 1
            else:
                break

        if dir == '>':
            if (col != 0) and (col != last_col):
                grid[row][col] = 'X'
                if grid[row][col+1] == '#':
                    dir = 'v'
                else:
                    col = col + 1
            else:
                break

        if dir == 'v':
            if (row != 0) and (row != last_row):
                grid[row][col] = 'X'
                if grid[row+1][col] == '#':
                    dir = '<'
                else:
                    row = row + 1
            else:
                break

        if dir == '<':
            if (col != 0) and (col != last_col):
                grid[row][col] = 'X'
                if grid[row][col-1] == '#':
                    dir = '^'
                else:
                    col = col - 1
            else:
                break

        # During example, see how the elf walks
        # print_puzzle(grid)
        # time.sleep(0.01)

    grid[row][col] = 'X'
    print('Exit found!')

    print_puzzle(grid)

    # Count the positions in the grid where we've been
    result = 0
    for row in grid:
        result += row.count('X')

    print(f'Amount of positions: {result}')

    return result


def opdracht_6a(filename: str) -> int:
    """Runs assignment 6a

    Args:
        filename (str): puzzle input

    Returns:
        int: amount of visited tiles
    """
    grid = read_puzzle(filename)

    print_puzzle(grid)

    pos, direction = find_elf(grid)

    return walk_the_grid(grid, pos, direction)


if __name__ == "__main__":
    assert opdracht_6a('6/input.txt') == 5453
