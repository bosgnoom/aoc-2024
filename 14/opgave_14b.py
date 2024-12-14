from PIL import Image
import numpy as np
import logging
import coloredlogs

from opgave_14a import read_puzzle, process_map, update_positions

coloredlogs.install(level='INFO')


def save_bitmap(n, puzzle, shape):
    wide, tall = shape

    map = np.zeros(shape=(tall, wide), dtype=int)

    for robot in puzzle:
        x, y = robot['p']
        map[y, x] += 1

    binary_image = (map > 0) * 255

    image = Image.fromarray(binary_image.astype(np.uint8))

    image.save(f'14/png/{n}.png')


def main2(filename, size):
    # Puzzle stores positions and velocities
    puzzle = read_puzzle(filename)

    process_map(puzzle, size)
    for i in range(10000):
        if i % 100 == 0:
            logging.info(i)
        puzzle = update_positions(puzzle, size)

        if 8080 < i < 8090:
            save_bitmap(i+1, puzzle, size)


if __name__ == "__main__":
    main2('14/input.txt', (101, 103))
    # See image 8086 + 1
