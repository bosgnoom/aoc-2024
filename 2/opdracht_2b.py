from opdracht_2a import read_file, calc_differences, check_differences


def check_differences_damperer(row):
    # Check complete row first
    if check_differences(calc_differences(row)):
        return True
    else:
        # Check each row by removing the n-th item
        print('Subsequent checking', end='')
        for n in range(len(row)):
            # Create a copy, otherwise the original row is lost
            row2 = row.copy()
            row2.pop(n)
            if check_differences(calc_differences(row2, print_before='\n   ')):
                return True

    # If loop is complete, none of the variations match, so return False here
    return False


def opdracht_b(filename):
    lines = read_file(filename)

    scores = []
    for row in lines:
        score = check_differences_damperer(row)

        if score:
            print("Safe")
        else:
            print("Unsafe")
        scores.append(score)

    print(f'\nTotal score: {sum(scores)}')

    return sum(scores)


if __name__ == "__main__":
    assert opdracht_b('2/puzzle_input.txt') == 413
