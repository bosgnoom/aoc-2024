import re


def read_puzzle(filename):
    with open(filename) as f:
        puzzle = f.readlines()

    return puzzle


def multiply(a, b):
    # Multiply numbers

    return a * b


def analyze_line(line):
    # Use regex to find multiplication(s) from line

    muls = re.findall(r'mul\(\d{1,3}\,\d{1,3}\)',
                      line)

    total = []
    for m in muls:
        numbers = (re.findall(r'\d+,\d+', m))
        a = int(numbers[0].split(',')[0])
        b = int(numbers[0].split(',')[1])
        print(f'{a} * {b} = {multiply(a, b)}')
        total.append(multiply(a, b))

    print('------------ +')

    print(f'Total: {sum(total)}')
    return sum(total)


def main():
    puzzle = read_puzzle('3/input.txt')

    grand_total = 0
    for line in puzzle:
        grand_total += analyze_line(line)

    print('\n\n')
    print(grand_total)

    assert grand_total == 188741603


if __name__ == "__main__":
    main()
