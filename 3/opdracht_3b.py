import re
from opdracht_3a import read_puzzle


def process_memory(line):
    # Split the input line into instructions
    instructions = re.findall(
        r"(do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\))", line)

    enabled = True  # By default, mul instructions are enabled
    total_sum = 0   # Sum of enabled mul results

    for instr in instructions:
        print(f'{str(instr):<35}', end=' ')
        if instr[0] == "do()":
            print("enabling multiplication", end=' ')
            enabled = True  # Re-enable mul
        elif instr[0] == "don't()":
            print("disabling multiplication", end=' ')
            enabled = False  # Disable mul
        elif ("mul" in instr[0]) and (enabled):
            # Calculate the product of enabled mul
            print(f'{instr[1]} * {instr[2]} = {int(instr[1])
                  * int(instr[2])}', end=' ')
            total_sum += (int(instr[1]) * int(instr[2]))

        print(f'Total sum: {total_sum}')

    return total_sum


if __name__ == "__main__":
    puzzle = read_puzzle('3/input.txt')

    # transform puzzle into one big line (this is where you f-ed up)
    puzzle = ''.join(puzzle)
    result = process_memory(puzzle)

    print(f'Grand total: {result}')

    # To be honest, it took me a couple of times...
    assert result < 118168040, "This one is too high!"
    assert result < 70553436, "This one is too high!"
    assert result < 96384317, "This one is too high!"
    assert result == 67269798, "nOK"
