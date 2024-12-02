from opdracht_1a import import_file
from collections import Counter


def calc_similarity(a, b):
    counts = Counter(b)

    sims = []
    for i in a:
        score = i * counts[i]
        print(i, counts[i], score)
        sims.append(score)

    return sum(sims)


if __name__ == "__main__":
    a, b = import_file('1/puzzle_input.txt')
    print(calc_similarity(a, b))
