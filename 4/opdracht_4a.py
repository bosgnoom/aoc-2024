def count_word_occurrences(grid: list[list], word: str) -> int:
    """Count word occurrences

    By searching for the _word_ in all directions

    :param grid: Word puzzle
    :type grid: list of list
    :param word: word we're looking for
    :type word: str
    :return: count of words
    :rtype: int
    """
    rows, cols = len(grid), len(grid[0])
    word_len = len(word)
    directions = [
        (0, 1),  # Right
        (1, 0),  # Down
        (1, 1),  # Down-right diagonal
        (1, -1),  # Down-left diagonal
        (0, -1),  # Left
        (-1, 0),  # Up
        (-1, -1),  # Up-left diagonal
        (-1, 1)  # Up-right diagonal
    ]

    def is_valid(x: int, y: int) -> bool:
        return 0 <= x < rows and 0 <= y < cols

    def search_from(x: int, y: int, dx: int, dy: int) -> bool:
        """Search for the word starting from (x, y) in direction (dx, dy)."""
        for i in range(word_len):
            nx, ny = x + i * dx, y + i * dy
            if not is_valid(nx, ny) or grid[nx][ny] != word[i]:
                return False
        return True

    count = 0
    for i in range(rows):
        for j in range(cols):
            for dx, dy in directions:
                if search_from(i, j, dx, dy):
                    count += 1
    return count


def read_puzzle(filename: str) -> list[list]:
    """Reads puzzle input from file

    :param filename: _description_
    :type filename: str
    :return: _description_
    :rtype: list[list]
    """
    with open(filename) as f:
        lines = f.readlines()

    grid = []
    for line in lines:
        row = []
        for lin in line:
            if lin != '\n':
                row.append(lin)
        grid.append(row)

    return grid


def opdracht_4a() -> None:
    grid = read_puzzle('4/input.txt')
    word = "XMAS"
    result = count_word_occurrences(grid, word)
    print(f'Total word count: {result}')
    return result


if __name__ == "__main__":
    assert opdracht_4a() == 2458
