from opdracht_1a import import_file
from collections import Counter


def calc_similarity(a,b):
    counts = Counter(b)

    sims = []
    for i in a:
        score = i * counts[i]
        print(i, counts[i], score)
        sims.append(score)

    return sum(sims)



def test_opdracht_1b():
    # Read file input
    a, b = import_file('1/example_a.txt')

    # Calculate similarity score
    sim = calc_similarity(a,b)

    assert sim == 31


if __name__ == "__main__":
    a, b = import_file('1/puzzle_input.txt')
    print(calc_similarity(a,b))
