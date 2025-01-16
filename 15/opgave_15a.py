# https://adventofcode.com/2024/day/15

import pygame
import logging

logging.basicConfig(level=logging.ERROR)

# Game settings
SCALE = 40
FPS = 240


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


def find_robot(map: list[str]) -> tuple[tuple[int, int], list[str]]:
    """Finds the robot in the puzzle

    Args:
        map (list[str]): Puzzle map

    Returns:
        tuple, list[str]: Position (x, y) of robot and updated map (removed @)
    """
    for y, line in enumerate(map):
        for x, col in enumerate(line):
            if col == '@':
                # Reset robot position to empty
                map[y][x] = '.'

                return (x, y), map


def draw_map(screen: pygame.display, font, map: list, robot: tuple[int, int]) -> None:
    """Draws the puzzle on the screen

    Args:
        screen (pygame.display): Pygame screen
        map (list): Puzzle state
        robot (tuple): Position of robot (x,y)
    """
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

            text = font.render(c, True, color)
            screen.blit(text, (SCALE*ii, SCALE*i))


def indicate_map(screen, font, position: tuple) -> None:
    """Changes color of O's on map which are evaluated whether a move is possible

    Args:
        screen (pygame.display): Screen
        position (tuple): Position of O (x,y)
    """
    x, y = position
    text = font.render("O", True, (63, 127, 255))
    screen.blit(text, (SCALE * x, SCALE * y))
    pygame.display.flip()


def calc_score(puzzle: list[str]) -> int:
    """Calculates the total GPS score

    Args:
        puzzle (list[str]): Puzzle

    Returns:
        int: Sum of GPS scores
    """
    score = 0
    for y, line in enumerate(puzzle):
        for x, c in enumerate(line):
            if c == 'O':
                score += 100*y + x

    return score


def main(filename: str, SHOW=True) -> int:
    """Runs a gamefile

    Args:
        filename (str): Game input

    Returns:
        int: GPS score
    """
    logger = logging.getLogger()

    # Set up pygame
    pygame.init()
    timert = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.SysFont('freemono', size=SCALE)

    # Read puzzle
    puzzle, directions = read_puzzle(filename)

    # Find robot
    robot, puzzle = find_robot(puzzle)
    x, y = robot
    logger.info(f'Found robot at: {x}, {y}')

    # Debugging info
    logger.debug(directions)
    size_x = SCALE * len(puzzle[0])
    size_y = SCALE * len(puzzle)

    # Set up pygame screen. Perhaps TODO: use fancy way to set the SCALE
    # By e.g. 1024 // length of puzzle or something like that.
    # Gives big SCALE for small puzzle, small SCALE for large puzzle (with min/max somewhere)
    if SHOW:
        screen = pygame.display.set_mode([size_x, size_y])

    # Keep track of which direction step we're at
    step = 0

    # Exit pygame loop?
    running = True

    # Game loop
    while running and (step < len(directions)):
        # First, check if pygame wants to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

        if SHOW:
            # Draw map on screen
            draw_map(screen, font, puzzle, robot)

            # Update display
            pygame.display.flip()

        # Update map for given direction
        # Get robot position
        x, y = robot

        # Use a loop to find out whether the robot can move:
        # - For a #: hit wall, nope, no movement
        # - For a O: add cell to "waiting list", will push if ends with '.' else end move
        # - For a .: yes, move possible
        logger.info(f'{step} Robot at {x},{y}, dir={directions[step]}')

        # Have an empty waiting list for possible moves (when 'O' is encountered)
        waiting_list = []

        # While loop to determine new position
        while True:
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

            # Checks for NEW position
            if puzzle[y][x] == '#':
                logger.debug(f'Found wall at {x}, {y}. No movement possible, next step {step}/{len(directions)}')
                step += 1

                break

            elif puzzle[y][x] == '.':
                logger.debug(f'Found empty position at {x}, {y}. Updating positions...')
                waiting_list.append((x, y))

                # How long the waiting list is
                while len(waiting_list) > 1:
                    # Yes, so update multiple items (i.e. the O's)
                    pos = waiting_list.pop()
                    logger.debug(f'Found {pos} in waiting list')
                    x, y = pos
                    puzzle[y][x] = 'O'

                # Now update robot position
                x, y = waiting_list[0]
                logger.debug(f'Last one in waiting list: {x}, {y}')
                puzzle[y][x] = '.'
                robot = (x, y)

                # Prepare for next step
                step += 1

                break

            elif puzzle[y][x] == 'O':
                logger.debug('Found a box, checking further options...')

                # Add this position to the waiting list
                waiting_list.append((x, y))

                # Show on the map what we're evaluating
                if SHOW:
                    indicate_map(screen, font, (x, y))

                logger.debug(f'{robot} {waiting_list}')

        # Wait a bit and continue
        if SHOW:
            timert.tick(FPS)

    logger.info('\nAll steps complete!')

    if SHOW:
        # Draw map on screen
        draw_map(screen, puzzle, robot)

        # Update display
        pygame.display.flip()

    # Calculate score
    print(f'Score: {calc_score(puzzle)}')

    return calc_score(puzzle)


if __name__ == "__main__":

    assert main('15/input.txt') == 1526673

    # Keep game screen open
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Stop pygame
    pygame.quit()
