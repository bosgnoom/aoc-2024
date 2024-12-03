import csv


def read_file(filename):
    with open(filename) as f:
        reader = csv.reader(f, delimiter=' ')

        lines = [line for line in reader]

    # convert into int
    lines2 = [[int(j) for j in line] for line in lines]

    return lines2


def calc_differences(row, print_before=''):
    diff = []

    for i in range(len(row) - 1):
        diff.append(row[i + 1] - row[i])

    print(f'{print_before}{row} --> {diff} -->', end=' ')

    return diff


def check_differences(row):
    # Check for sign first: all above or below zero
    # Next step: check for maximum difference
    return (((all([r < 0 for r in row])) or (all([r > 0 for r in row])))
            and (all([abs(r) <= 3 for r in row])))


def opdracht_a(filename):
    lines = read_file(filename)

    scores = []
    for row in lines:
        diffs = calc_differences(row)
        score = check_differences(diffs)

        if score:
            print("Safe")
        else:
            print("Unsafe")

        scores.append(score)

    print(f'\nTotal score: {sum(scores)}')

    return sum(scores)


if __name__ == "__main__":
    assert opdracht_a('2/puzzle_input.txt') == 356
