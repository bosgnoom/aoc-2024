import csv
import pprint

def import_file(filename):
    # Read file
    with open(filename) as f:
        lines = [ line.split('   ') for line in f ]

    # Convert into integers
    lines = [(int(a), int(b)) for a,b in lines]

    # Convert list of tuples into two lists
    return zip(*lines)


def calc_differences(a,b):
    diffs = []
    for a,b in zip(sorted(a), sorted(b)):
        diffs.append(abs(a-b))

    return diffs


def test_example():
    a, b = import_file('1/example_a.txt')
    test_diffs = calc_differences(a,b)
    print(test_diffs)
    assert sum(test_diffs) == 11


if __name__ == '__main__':
    a,b = import_file('1/puzzle_input.txt')
    
    diffs = calc_differences(a, b)

    print(f'Sum of differences: {sum(diffs)}')