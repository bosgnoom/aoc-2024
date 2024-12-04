from opdracht_4a import read_puzzle


def check_subgrid(s: list[list]) -> int:
    # Check whether a cross is present in the subgrid (3x3)
    # Using template matching (the sloppy way)
    result = 0

    # M.S
    # .A.
    # M.S
    if ((s[0][0] == 'M') & (s[0][2] == 'S')
        & (s[1][1] == 'A')
            & (s[2][0] == 'M') & (s[2][2] == 'S')):
        result = 1

    # S.S
    # .A.
    # M.M
    if ((s[0][0] == 'S') & (s[0][2] == 'S')
        & (s[1][1] == 'A')
            & (s[2][0] == 'M') & (s[2][2] == 'M')):
        result = 1

    # M.M
    # .A.
    # S.S
    if ((s[0][0] == 'M') & (s[0][2] == 'M')
        & (s[1][1] == 'A')
            & (s[2][0] == 'S') & (s[2][2] == 'S')):
        result = 1

    # S.M
    # .A.
    # S.M
    if ((s[0][0] == 'S') & (s[0][2] == 'M')
        & (s[1][1] == 'A')
            & (s[2][0] == 'S') & (s[2][2] == 'M')):
        result = 1

    return result


def print_subgrid(s: list[list]) -> None:
    """Prints out the subgrid with only MAS letters"""
    for r in range(3):
        for c in range(3):
            if s[r][c] in "MAS":
                print(s[r][c], end='')
            else:
                print(".", end='')
        print()


def opdracht_4b(grid: list[list]) -> int:
    score = 0
    subgrid = []
    for col in range(len(grid[0]) - 2):
        for row in range(len(grid) - 2):
            subgrid = [[grid[row + 0][col], grid[row + 0][col + 1], grid[row + 0][col + 2]],  # noqa
                       [grid[row + 1][col], grid[row + 1][col + 1], grid[row + 1][col + 2]],  # noqa
                       [grid[row + 2][col], grid[row + 2][col + 1], grid[row + 2][col + 2],]  # noqa
                       ]
            score += check_subgrid(subgrid)

    print(f'Total score: {score}')
    return score


if __name__ == "__main__":
    grid = read_puzzle('4/input.txt')
    assert opdracht_4b(grid) == 1945
