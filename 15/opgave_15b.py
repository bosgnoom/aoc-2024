# https://adventofcode.com/2024/day/15

import pygame
import logging
import coloredlogs

coloredlogs.install(level=logging.DEBUG)

# Game settings
SCALE = 64
FPS = 1


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


def preprocess_map(puzzle: list[str]) -> list[str]:
    """Expand puzzle

    Args:
        puzzle (list[str]): Map

    Returns:
        list[str]: Expanded map
    """

    new_puzzle = []

    for line in puzzle:
        new_line = []
        for c in line:
            if c == '#':
                new_line += ['#', '#']
            elif c == 'O':
                new_line += ['[', ']']
            elif c == '.':
                new_line += ['.', '.']
            elif c == '@':
                new_line += ['@', '.']
            else:
                logging.error('Unknown character in map: {c}')
        new_puzzle.append(new_line)

    return new_puzzle


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


def draw_map(screen: pygame.display,
             font: pygame.font,
             map: list[list],
             robot: tuple[int, int]) -> None:
    """Draws the puzzle on the screen

    Args:
        screen (pygame.display): Pygame screen
        font (pygame.font): Font in use
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
                c = '⚙︎'  # lol unicode kinda works!
            elif c == 'O':
                color = (127, 255, 127)
            elif c == '.':
                color = (64, 255, 64)
                c = '·'
            else:
                color = (32, 127, 32)

            text = font.render(c, True, color)
            screen.blit(text, (SCALE*ii, SCALE*i))


def indicate_map(screen, font, puzzle, position: tuple) -> None:
    """Changes color of O's on map which are evaluated whether a move is possible

    Args:
        screen (pygame.display): Screen
        position (tuple): Position of O (x,y)
    """
    x, y = position
    c = puzzle[y][x]
    text = font.render(c, True, (63, 127, 255))
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
            if c == '[':
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
    puzzle = preprocess_map(puzzle)

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

        # Have an empty waiting list for possible moves (when '[]' is encountered)
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

            # Checks for the NEW position
            if directions[step] in '<>':
                if puzzle[y][x] == '#':
                    # Is a wall
                    logger.debug(f'Found wall at {x}, {y}. No movement possible, next step {step}/{len(directions)-1}')
                    step += 1

                    break

                elif puzzle[y][x] == '.':
                    # Performs left and right movement (easy part)

                    logger.debug(f'Found empty position at {x}, {y}. Updating left/right positions...')
                    waiting_list.append((x, y))

                    # How long the waiting list is
                    while len(waiting_list) > 1:
                        # Yes, so update multiple items (i.e. the []'s)
                        pos = waiting_list.pop()
                        x, y = pos

                        logger.debug(f'Found {pos} in waiting list')

                        if directions[step] == '<':
                            # Left movement
                            puzzle[y][x] = puzzle[y][x+1]

                        if directions[step] == '>':
                            # Right movement
                            puzzle[y][x] = puzzle[y][x-1]

                    # Now update robot position
                    x, y = waiting_list[0]
                    logger.debug(f'Last one in waiting list: {x}, {y}')
                    puzzle[y][x] = '.'
                    robot = (x, y)

                    # Prepare for next step
                    step += 1

                    break

                elif puzzle[y][x] in '[]':
                    # Found a piece of a box in left/right movement (still easy part)

                    logger.debug('Found box, checking further...')

                    # Add this position to the waiting list
                    waiting_list.append((x, y))

                    # Show on the map what we're evaluating
                    if SHOW:
                        indicate_map(screen, font, puzzle, (x, y))
                        timert.tick(FPS)

                    logger.debug(f'{robot} {waiting_list}')
            else:
                # Up/down movement

                if puzzle[y][x] == '.':
                    # Performs up/down movement
                    # Needs work, only robot moves now...
                    logger.debug(f'Found empty position at {x}, {y}. Updating up/down positions...')
                    if directions[step] == '^':
                        # Up movement
                        puzzle[y][x] = puzzle[y-1][x]

                    if directions[step] == 'v':
                        # Down movement
                        puzzle[y][x] = puzzle[y+1][x]

                    puzzle[y][x] = '.'
                    robot = (x, y)

                    # Prepare for next step
                    step += 1

                    break

                elif puzzle[y][x] in '[]':
                    # Found a piece of a box in up/down movement (hard part)

                    logger.debug('Found box, checking further...')

                    # Add positions to the waiting list
                    if puzzle[y][x] == '[':
                        waiting_list.append([(x, y), (x+1, y)])
                    else:
                        waiting_list.append([(x, y), (x-1, y)])

                    # Show on the map what we're evaluating
                    if SHOW:
                        for i in waiting_list[-1]:
                            indicate_map(screen, font, puzzle, i)
                        timert.tick(FPS)

                    last_loop = True
                    while last_loop:
                        logger.info(f'last loop, checking: {waiting_list[-1]}')

                        check_list = []

                        for i in waiting_list[-1]:
                            xx, yy = i
                            logger.info(f'Checking on {i}: {puzzle[yy][xx]}')

                            # check direction
                            if directions[step] == '^':
                                yy = yy - 1
                            else:
                                yy = yy + 1

                            # check end of move
                            if puzzle[yy][xx] == '#':
                                # No move possible, exit
                                logger.debug('Found #, no move possible')

                                # Reset all things
                                waiting_list = []
                                last_loop = False
                                step = step + 1

                                break

                            # else left box
                            elif puzzle[yy][xx] == '[':
                                check_list.append((xx, yy))
                                check_list.append((xx+1, yy))

                            # or right box
                            elif puzzle[y][x] == ']':
                                check_list.append((xx, yy))
                                check_list.append((xx-1, yy))

                        # REmove duplicates from check_list:
                        check_list = list(set(check_list))

                        logger.info(f'After checking {check_list=}')

                        if check_list:
                            # Check whether all current in last waiting list are .
                            all_dots = True
                            logger.info(f'all dots check {check_list=}')

                            for i in check_list:
                                xx, yy = i
                                if puzzle[yy][xx] != '.':
                                    all_dots = False

                            if all_dots:
                                logging.info("All dots! Clear to go!")
                                last_loop = False
                                # TODO: update positions and exit this while loop

                                while len(waiting_list) > 0:
                                    # Yes, so update multiple items (i.e. the []'s)
                                    posis = waiting_list.pop()
                                    for pos in posis:
                                        logger.debug(f'Moving {pos=}')
                                        xx, yy = pos

                                        logger.debug(f'Found {pos} in waiting list')

                                        if directions[step] == '^':
                                            # Up movement
                                            puzzle[yy-1][xx] = puzzle[yy][xx]

                                        if directions[step] == 'v':
                                            # Down movement
                                            puzzle[yy+1][xx] = puzzle[yy][xx]

                                            if SHOW:
                                                # Draw map on screen
                                                draw_map(screen, font, puzzle, robot)

                                                # Update display
                                                pygame.display.flip()

                                # Now update robot position
                                # x, y = waiting_list[0]
                                # logger.debug(f'Last one in waiting list: {x}, {y}')
                                # puzzle[y][x] = '.'
                                if directions[step] == '^':
                                    # Up movement
                                    robot = (x, y-1)

                                elif directions[step] == 'v':
                                    # Down movement
                                    robot = (x, y+1)

                                # Prepare for next step
                                step += 1

                                last_loop = False

                                break

                            else:
                                logging.info("not all dots, adding checklist to waiting list")
                                waiting_list.append(check_list)

                                logger.critical(f'{check_list=}')
                                logger.critical(f'{waiting_list=}')
                        else:
                            # TODO: update positions in waiting list
                            logger.critical("Updating positions here!")

                        # Show on the map what we're evaluating
                        if SHOW:
                            for i in waiting_list[-1]:
                                indicate_map(screen, font, puzzle, i)
                            timert.tick(FPS)

                    logger.debug(f'{robot} {waiting_list}')

        # Wait a bit and continue
        if SHOW:
            timert.tick(FPS)

    logger.info('\nAll steps complete!')

    if SHOW:
        # Draw map on screen
        draw_map(screen, font, puzzle, robot)

        # Update display
        pygame.display.flip()

    # Calculate score
    print(f'Score: {calc_score(puzzle)}')

    return calc_score(puzzle)


if __name__ == "__main__":

    main('15/ex3.txt')

    # Keep game screen open
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Stop pygame
    pygame.quit()
