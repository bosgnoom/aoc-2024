from collections import defaultdict
import logging
import coloredlogs

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


def read_puzzle(puzzle: str) -> list[str]:
    """Converts puzzle into a list of strings

    Args:
        puzzle (str): puzzle

    Returns:
        list[str]: starting values
    """
    return [a for a in puzzle.split(' ')]


def main(puzzle: list[str], n: int) -> defaultdict:
    """Runs main loop

    Args:
        puzzle (list[str]): puzzle
        n (int): how often to blink

    Returns:
        defaultdict: scores per value
    """

    # Store the stones in a defaultdict, this one has always a zero
    # when there's no key
    stones = defaultdict(int)

    # Fill initial row of stones
    for i in puzzle:
        stones[i] += 1

    for blink in range(n):
        logger.info(f'{blink=}')

        # Add processed stones into a new dict
        new_stones = defaultdict(int)

        # Process all stones
        for stone, count in stones.items():
            logger.debug(f'{stone=}, {count=}')
            if stone == '0':
                # If 0 on stone, return 1
                new_stones['1'] += count

            elif len(stone) % 2 == 0:
                # If length is even, split stone in half
                half = len(stone) // 2

                # Do this for every same stone!
                new_stones[stone[:half]] += count
                new_stones[str(int(stone[half:]))] += count
            else:
                # Not any of above, return 2024*stone
                new_stones[str(int(stone) * 2024)] += count

        # Update the row of stones
        stones = new_stones

        # And show it
        logger.info(stones)

    result = sum(stones.values())
    logger.info(f'{result=}')

    return result, stones


if __name__ == "__main__":
    # puzzle = read_puzzle('0 1 10 99 999')
    puzzle = read_puzzle('125 17')
    # puzzle = read_puzzle('5 62914 65 972 0 805922 6521 1639064')
    length, stones = main(puzzle, 1)  # 199753

    assert length == 3
    assert stones == defaultdict(int, {'253000': 1, '1': 1,  '7': 1})
