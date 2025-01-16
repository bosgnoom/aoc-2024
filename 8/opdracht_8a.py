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
        print(f'Checking coords: {coord}')

        # Unpack coordinates
        r1, c1 = coord[0]
        r2, c2 = coord[1]

        # calculate dx, dy
        dr = r1 - r2
        dc = c1 - c2

        # New coord
        r3 = r1 + dr
        c3 = c1 + dc

        r4 = r2 - dr
        c4 = c2 - dc

        # Check whether within grid
        if ((0 <= r3 < len(grid))
                and (0 <= c3 < len(grid[0]))):
            print(f'    Antinode found at {r3, c3}')
            result.append((r3, c3))

        if ((0 <= r4 < len(grid))
                and (0 <= c4 < len(grid[0]))):
            print(f'    Antinode found at {r4, c4}')
            result.append((r4, c4))

    # Return found antinodes
    return result


def find_antinodes_2(grid: list[str], coords: list[tuple]) -> list[tuple]:
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
        print(f'Checking coords: {coord}')

        # Unpack coordinates
        r1, c1 = coord[0]
        r2, c2 = coord[1]

        # calculate dx, dy
        dr = r1 - r2
        dc = c1 - c2

        # Calculate ALONG the line of the two coordinates,
        # Taking the entire size of the grid as range, so we
        # won't end up too short
        for n in range(50):
            # calculate new coords, "up" and "down"
            r3 = r1 + (n * dr)
            c3 = c1 + (n * dc)

            r4 = r2 - (n * dr)
            c4 = c2 - (n * dc)

            if ((0 <= r3 < len(grid))
                    and 0 <= c3 < len(grid[0])):
                print(f'    Antinode found at {r3, c3}')
                result.append((r3, c3))
            if ((r4 >= 0) and (r4 < len(grid))
                and (c4 >= 0) and (c4 < len(grid[0]))
                and True  # (grid[r4][c4] == '.')
                ):
                print(f'    Antinode found at {r4, c4}')
                result.append((r4, c4))

    # Return found antinodes
    return result


def main(filename):
    grid = read_puzzle(filename)

    total = []

    for a in find_antennae(grid):

        coords = find_coords(grid, a)
        result = find_antinodes(grid, coords)
        total += result

    print('\n-----------------')
    print(f'Amount: {len(set(total))}')

    return total


def main2(filename):
    grid = read_puzzle(filename)

    total = []

    for a in find_antennae(grid):

        coords = find_coords(grid, a)
        result = find_antinodes_2(grid, coords)
        total += result

    print('\n-----------------')
    print(f'Amount: {len(set(total))}')

    return total


if __name__ == "__main__":
    # 311 is too low
    # 323 too high
    assert len(set(main('8/input.txt'))) == 318

    assert len(set(main2('8/input.txt'))) == 1126
