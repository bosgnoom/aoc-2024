import itertools


def read_puzzle(filename: str) -> list[list]:
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

    # Convert 3267: 81 40 27 into 3267 81 40 27
    # Converting all str into int
    puzzle = []
    for line in lines:
        puzzle.append([int(a) for a in line.replace(':', '').split(' ')])

    return puzzle


def calculate_row(row: list, operations: str = '+*') -> int:
    """Calculates score per calculation row,


    Args:
        row (list): list of answer and numbers, like 3267 81 40 27
        operations (str, optional): which operations to perform. Defaults to '+*'.

    Returns:
        int: answer if this can be calculated from numbers and operations, else 0
    """
    answer = row[0]
    numbers = row[1:]

    # Use itertools to make all possible combinations (product)
    for i in itertools.product(operations, repeat=len(numbers)-1):
        # Start with first number
        subtotal = numbers[0]

        # Use operation and next number, repeat for remaining numbers
        for n, j in enumerate(i):
            if j == '+':
                subtotal = subtotal + numbers[n+1]
            if j == '*':
                subtotal = subtotal * numbers[n+1]
            # This one is new in assignment b
            if j == '|':
                subtotal = int(str(subtotal)+str(numbers[n+1]))

        # Now check for correct answer, break if possible
        if subtotal == answer:
            print(i, numbers, subtotal, answer, 'OK')
            return answer

    return 0


def main(filename: str, operations: str = None) -> None:
    """Runs puzzle

    Args:
        filename (str): Puzzle input
        operations (str): operations to perform
    """
    puzzle = read_puzzle(filename)

    result = 0
    for row in puzzle:
        if operations is None:
            result += calculate_row(row)
        else:
            result += calculate_row(row, operations)

    print(f'Calibration result: {result}')

    return result


if __name__ == '__main__':
    opdracht_a = main('7/input.txt')
    opdracht_b = main('7/input.txt', operations='*+|')

    print('==========')
    print(f'Calibration factor A: {opdracht_a}')
    print(f'Calibration factor B: {opdracht_b}')
