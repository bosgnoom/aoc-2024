import pytest
import itertools


def read_puzzle(filename: str) -> list[str]:
    """Reads puzzle from disk

    Args:
        filename (str): filename

    Returns:
        list[list]: puzzle, each list is [answer n1 n2 n3 ... nn]
    """

    # Read file
    with open(filename) as f:
        lines = f.read()

    # Split by newline
    lines = (lines.split('\n'))

    return lines


def find_antennae(grid: list[str]) -> list:
    """Locates the unique antennae in the grid

    Args:
        grid (list[str]): Our map

    Returns:
        list: list of chars and numbers
    """
    all_chars = ''.join(grid)

    return [a for a in set(all_chars) if a.isalnum()]


def find_coords(grid: list[str], ant: str) -> list[tuple]:
    """Finds coordinates of an antenna

    Args:
        grid (list[str]): Our map
        ant (str): Antenna

    Returns:
        list: List of (row, col) coordinates of antenna
    """
    coords = []

    # Loop over the grid
    for r, row in enumerate(grid):
        # Find (even multiple 'ant's on a single row)
        col_indexes = [r for r, x in enumerate(row) if x == ant]
        for c in col_indexes:
            coords.append((r, c))

    return coords


def find_antinodes(grid: list[str], coords: list[tuple]) -> list[tuple]:
    """Finds coordinates of the antinodes

    Args:
        grid (list[str]): Our map
        coords (list[tuple]): Coordinates of two antennae

    Returns:
        list[tuple]: List of coordinates of the antinode if within grid
    """

    # Store antinodes
    result = []

    # Find antinodes here
    for coord in itertools.combinations(coords, 2):
        print(coord)

        # Unpack coordinates
        r1, c1 = coord[0]
        r2, c2 = coord[1]

        # calculate dx, dy
        dr = r1 - r2
        dc = c1 - c2

        # print(dr, dc)

        # calculate new coords
        r3 = r1 + dr
        c3 = c1 + dc

        r4 = r2 - dr
        c4 = c2 - dc

        print(r3, c3)
        print(r4, c4)

        try:
            if ((r3 >= 0) and (r3 <= len(grid))
                    and (c3 >= 0) and (c3 <= len(grid[0]))
                    and (grid[r3][c3] == '#')
                ):
                print(f'Antinode found at {r3, c3}')
                result.append((r3, c3))
            if ((r4 >= 0) and (r4 <= len(grid))
                    and (c4 >= 0) and (c4 <= len(grid[0]))
                    and (grid[r4][c4] == '#')
                ):
                print(f'Antinode found at {r4, c4}')
                result.append((r4, c4))
        except IndexError as e:
            print('Out of grid, bummer, why???')
            print(r3, c3, r4, c4)

    # Return found antinodes
    return result


def main():

    grid = read_puzzle('8/ex4.txt')

    total = 0
    for a in find_antennae(grid):

        coords = find_coords(grid, a)

        ret = find_antinodes(grid, coords)

        print(ret)

        total += len(ret)
    print(f'\n-----------------\nTotal: {total}')


if __name__ == "__main__":
    main()
