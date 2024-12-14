from functools import cache
import coloredlogs
import logging
logger = logging.getLogger(__name__)

coloredlogs.install(level='INFO', logger=logger)


def read_puzzle(puzzle: str) -> list[int]:
    return [int(a) for a in puzzle.split(' ')]


@cache
def update_stone(stone: int) -> list[int]:
    stone_str = str(stone)
    stone_len = len(stone_str)
    logger.debug(f'Stone: {stone} ', end='')

    if (stone == 0):
        # If 0, replace by 1
        logger.debug('Found 0, return 1')
        return [1]
    elif (stone_len % 2 == 0):
        # For even lengths, replace by two stones
        # left half first, right half next
        half = stone_len // 2
        splitted = [int(stone_str[0:half]), int(stone_str[half:])]
        logger.debug(f'Found even length, splitting stone into: {splitted}')
        return splitted
    else:
        # No rules apply, return stone * 2024
        logger.debug('No rules apply, returning 2024 * stone')
        return [stone * 2024]

    return -1


def main():
    # Note to self: bruteforce edition, will take too long
    # for n=75

    # puzzle = read_puzzle('0 1 10 99 999')
    # 1 2024 1 0 9 9 2021976

    puzzle = read_puzzle('125 17')

    # Initial arrangement:
    # 125 17

    # After 1 blink:
    # 253000 1 7

    # After 2 blinks:
    # 253 0 2024 14168

    # After 3 blinks:
    # 512072 1 20 24 28676032

    # After 4 blinks:
    # 512 72 2024 2 0 2 4 2867 6032

    # After 5 blinks:
    # 1036288 7 2 20 24 4048 1 4048 8096 28 67 60 32

    # After 6 blinks:
    # 2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2

    # Real input
    puzzle = read_puzzle('5 62914 65 972 0 805922 6521 1639064')

    row = puzzle
    # print(row)
    result = []

    for blink in range(25):
        logger.info(f'Starting {blink}')

        result = []
        for stone in row:
            result += update_stone(stone)

        row = result

        # logger.info(f'{blink=}, length={len(result)}, unique={
        #             len(set(result))}, so {len(set(result)) / len(result):%}')
    logger.info(result)
    logger.info(len(row))

    return len(result)


if __name__ == "__main__":
    main()  # 199753
