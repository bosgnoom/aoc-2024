# https://adventofcode.com/2024/day/15

import pprint
import pygame
from time import sleep

SCALE = 80

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('freemono', size=SCALE)
timert = pygame.time.Clock()


def read_puzzle(filename: str) -> tuple[list, list]:
    """Reads puzzle input from filename

    Args:
        filename (str): filename

    Returns:
        tuple[list, list]: puzzle, directions
    """

    puzzle = []
    directions = []

    switch = True

    with open(filename) as f:
        while line := f.readline():
            if line == '\n':
                switch = False
            elif switch:
                # This is the map
                puzzle.append([c for c in line.replace('\n', '')])
            else:
                # After that, get directions
                directions.append(line.replace('\n', ''))

    return puzzle, ''.join(directions)


def find_robot(map):
    for y, line in enumerate(map):
        for x, col in enumerate(line):
            if col == '@':
                # Reset robot position to empty
                map[y][x] = '.'

                return (x, y), map


def draw_map(screen, map: list, robot) -> None:
    screen.fill((0, 0, 0))
    for i, line in enumerate(map):
        for ii, c in enumerate(line):
            # Add robot in its position
            if (ii, i) == robot:
                c = '@'

            # "Fancy" coloring here
            if c == '@':
                color = (255, 255, 255)
            elif c == 'O':
                color = (127, 255, 127)
            elif c == '.':
                color = (64, 255, 64)
            else:
                color = (32, 127, 32)

            text = font.render(c, False, color)
            screen.blit(text, (SCALE*ii, SCALE*i))


if __name__ == "__main__":
    # Read puzzle
    puzzle, directions = read_puzzle('15/ex1.txt')

    # Find robot
    robot, puzzle = find_robot(puzzle)
    x, y = robot
    print(f'Found robot at: {x}, {y}')

    # Debugging ingo
    pprint.pprint(directions)
    size_x = SCALE * len(puzzle[0])
    size_y = SCALE * len(puzzle)  # +(SCALE//2)

    print(size_x, size_y)

    # Set up pygame screen. Perhaps TODO: use fancy way to set the SCALE
    # By e.g. 1024 // length of puzzle or something like that.
    # Gives big SCALE for small puzzle, small SCALE for large puzzle (with min/max somewhere)
    screen = pygame.display.set_mode([size_x, size_y])

    # Keep track of which direction step we're at
    step = 0

    # Exit pygame loop?
    running = True

    # Game loop
    while running:
        # First, check if pygame wants to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw map on screen
        draw_map(screen, puzzle, robot)

        # Update display
        pygame.display.flip()

        # Update map for given direction
        # Get robot position
        x, y = robot

        # Use a loop to find out whether the robot can move:
        # - For a #: hit wall, nope, no movement
        # - For a O: ignore, will push
        # - For a .: yes, move possible
        print(f'{step=} Robot at {x},{y}, dir={directions[step]}')

        while ((puzzle[y][x] == '.') or (puzzle[y][x] == 'O')):
            # Update position
            if directions[step] == '<':
                # Left
                x = x - 1
            elif directions[step] == '>':
                # Right
                x = x + 1
            elif directions[step] == '^':
                # Up
                y = y - 1
            elif directions[step] == 'v':
                # Down
                y = y + 1
            else:
                # Should not happen, complain and quit
                print(f'Error for move {step}: {directions[step]}')
                exit(-1)

            if puzzle[y][x] == '#':
                print(f'Found wall at {x}, {y}. No movement possible, next step')
                step += 1
            elif puzzle[y][x] == '.':
                print(f'Found empty position at {x}, {y}. Updating map')
                robot = (x, y)
                print(f'{robot=}')
                break

        # Wait a bit and continue
        timert.tick(1)

    pygame.quit()
