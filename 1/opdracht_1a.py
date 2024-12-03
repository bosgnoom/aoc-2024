def import_file(filename):
    # Read file
    with open(filename) as f:
        lines = [line.split('   ') for line in f]

    # Convert into integers
    lines = [(int(a), int(b)) for a, b in lines]

    # Convert list of tuples into two lists
    return zip(*lines)


def calc_differences(a, b):
    # Calculate the differences between two lists,
    # the lists are sorted first
    diffs = []
    for a, b in zip(sorted(a), sorted(b)):
        diffs.append(abs(a - b))

    return diffs


if __name__ == '__main__':
    a, b = import_file('1/puzzle_input.txt')

    diffs = calc_differences(a, b)

    print(f'Sum of differences: {sum(diffs)}')
