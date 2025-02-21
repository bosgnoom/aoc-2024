# https://adventofcode.com/2024/day/15

import pygame
import logging
import coloredlogs

coloredlogs.install(level=logging.INFO)

# Game settings
SCALE = 24
FPS = 100


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
        tuple, list[str]: Position (x, y) of robot and updated map 
    """
    for y, line in enumerate(map):
        for x, col in enumerate(line):
            if col == '@':
                # Robot found, returning position
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
            elif c in '[O]':
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
    if c == '.':
        c = '·'
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


def calc_pos(robot, offset):
    """Calculate new position for robot

    Args:
        robot (_type_): _description_
        offset (_type_): _description_
    """

    return (robot[0] + offset[0], robot[1] + offset[1])


def main_b(filename: str, SHOW=True) -> int:
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
    puzzle_raw, directions = read_puzzle(filename)
    puzzle = preprocess_map(puzzle_raw)

    # Find robot
    robot, puzzle = find_robot(puzzle)
    logger.info(f'Found robot at: {robot}')

    # Debugging info
    logger.debug(directions)
    size_x = SCALE * len(puzzle[0])
    size_y = SCALE * len(puzzle)

    # Set up pygame screen. Perhaps TODO: use fancy way to set the SCALE
    # By e.g. 1024 // length of puzzle or something like that.
    # Gives big SCALE for small puzzle, small SCALE for large puzzle (with min/max somewhere)
    if SHOW:
        screen = pygame.display.set_mode([size_x, size_y])

    # For where to look depening on direction and found box edge
    OFFSETS = {
        "<": (-1, 0),
        ">": (1, 0),
        "^": (0, -1),
        "v": (0, 1),

        "[": (1, 0),  # if found [ look to the right
        "]": (-1, 0),  # else look to the left for a ]
    }

    # Loop over all the steps in directions
    for move in directions:
        # First, check if pygame wants to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if SHOW:
            # Draw map on screen
            draw_map(screen, font, puzzle, robot)

            # Update display
            pygame.display.flip()

        # Calculate possible new position of robot
        offset = OFFSETS[move]
        x, y = calc_pos(robot, offset)
        logger.info(f'Robot: {robot}, move: {move}')

        # Check new position, this is either a block, a wall or an empty space
        if puzzle[y][x] in "[]":
            # Encountered a block

            # Check move
            if move in "<>":
                # For the "easy" part: left/right movement is similar to assignment A

                # Store new position in a list
                check_list = [(x, y)]

                # Continue checking in the `move` direction
                while puzzle[y][x] in "[]":
                    # if SHOW:
                    #     indicate_map(screen, font, puzzle, (x, y))
                    #     timert.tick(FPS)

                    x, y = calc_pos((x, y), offset)
                    check_list.append((x, y))

                # if SHOW:
                #     indicate_map(screen, font, puzzle, (x, y))
                #     timert.tick(FPS)

                # Hit something else than a box; either a wall or a free position
                if puzzle[y][x] == '#':
                    continue
                elif puzzle[y][x] == '.':
                    # Free position, update puzzle
                    logging.debug(f'Found empty position, {check_list=}')

                    # Move boxes step by step
                    while len(check_list) > 1:
                        x1, y1 = check_list.pop()   # Get the last one
                        x2, y2 = check_list[-1]     # And next-to-last one
                        puzzle[y1][x1] = puzzle[y2][x2]   # Update box info

                    # Last position is now free for the robot
                    puzzle[y2][x2] = '.'
                    robot = (x2, y2)

                else:
                    logger.critical(f'Error in puzzle: {puzzle[y][x]}')

            elif move in "^v":
                # The hard part: up/down will move in at least 2 columns https://github.com/xavdid/advent-of-code/blob/main/solutions/2024/day_15/solution.py

                # Add found box piece and corresponding one to check_list
                x2, y2 = calc_pos((x, y), OFFSETS[puzzle[y][x]])
                check_list = [[(x, y), (x2, y2)]]

                # Show on screen
                # if SHOW:
                #     for cell in check_list[0]:
                #         indicate_map(screen, font, puzzle, cell)
                #         timert.tick(FPS)

                logger.debug(f'Up down starting, {check_list=}')

                # Boolean to store whether move is possible
                move_possible = True

                # Now loop over the puzzle checking up/downwards for further boxes
                while True:
                    # Switch to a set to prevent storing double items
                    logger.debug(check_list[-1])
                    next_row = {calc_pos(cell, offset) for cell in check_list[-1]}
                    logger.debug(f'{next_row=}')

                    # Check for boxes above/below current
                    new_boxes = {calc_pos((xx, yy), OFFSETS[puzzle[yy][xx]])
                                 for xx, yy in next_row
                                 if puzzle[yy][xx] in "[]"}
                    logger.debug(f'{new_boxes=}')

                    next_row.update(new_boxes)
                    logger.debug(f'{next_row=}')

                    # Show on screen
                    # if SHOW:
                    #     for cell in next_row:
                    #         indicate_map(screen, font, puzzle, cell)
                    #         timert.tick(FPS)

                    # Check whether the new cells are indeed boxes,
                    for xx, yy in next_row:
                        logger.debug(puzzle[yy][xx])
                        if puzzle[yy][xx] == "#":
                            # WE've hit a wall, stopping here
                            logger.debug("Hit a wall, aborting move")
                            move_possible = False
                            # Escape from while loop
                            break

                    # if so, add them to the check_list
                    new_boxes = [(xx, yy) for xx, yy in next_row if puzzle[yy][xx] in "[]"]
                    logger.debug(f'{new_boxes=}')
                    if new_boxes:
                        check_list.append(new_boxes)
                    else:
                        # Empty new_boxes, so we can move!
                        # Exit while loop using break
                        logger.debug('No new boxes found, <break>')
                        break

                if move_possible:
                    logger.debug('Updating puzzle')
                    # Loop over all rows, starting with the last one
                    for row in check_list[::-1]:
                        for cell in row:
                            # For each cell in the row,
                            # Calculate new position
                            x2, y2 = calc_pos(cell, offset)

                            # Get old position
                            x1, y1 = cell

                            # Update new position data with old position one
                            puzzle[y2][x2] = puzzle[y1][x1]

                            # Clear old position
                            puzzle[y1][x1] = '.'

                            # Show on screen
                            # if SHOW:
                            #     indicate_map(screen, font, puzzle, cell)
                            #     timert.tick(FPS)

                    # Finally, set robot to new position
                    robot = (x, y)
                else:
                    logger.debug('No move possible')

            else:
                logger.critical(f'Illegal move: {move}')
                exit(-1)

        elif puzzle[y][x] == "#":
            # Hit a wall, process next move
            # Go back to the top of the for loop,
            # Speeds up animation, otherwise use _pass_ here
            continue

        elif puzzle[y][x] == '.':
            # Ok to move, update robot position
            robot = (x, y)

        else:
            # This should not be happening, exiting!
            logger.critical(f'Unknown item in puzzle map: {puzzle[y][x]}')
            exit(-1)

        # Wait a bit and continue
        if SHOW:
            logger.debug('FPS')
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

    main_b('15/input.txt')  # 1535509

    # Keep game screen open
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Stop pygame
    pygame.quit()
