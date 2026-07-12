# https://adventofcode.com/2024/day/16

# Find path through maze, 1000 pt extra for 90 degree turn

# Hints from https://github.com/mgtezak/Advent_of_Code/blob/master/2024/16/p1.py

from heapq import heappop, heappush
import pygame
import logging
import coloredlogs
import cProfile

# Create a logger object.
coloredlogs.install(level='INFO',
                    fmt='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
logger = logging.getLogger(__name__)

# Game settings
SCREEN_SIZE = 1500
SCALE = 64
FPS = 200

# Direction modifier
DIRECTIONS = [
    (0, -1),    # N
    (1, 0),     # E
    (0, 1),     # S
    (-1, 0),    # W
]


def read_puzzle(filename: str) -> tuple[list, list]:
    """Reads puzzle input from filename

    Args:
        filename (str): filename

    Returns:
        tuple[list]: maze
    """

    puzzle = []

    with open(filename) as f:
        while line := f.readline():
            puzzle.append([c for c in line.replace('\n', '')])

    return puzzle


def find_location(maze: list[str], item: str) -> tuple[int, int]:
    """Finds something in the maze

    Args:
        maze (list[str]): Puzzle input
        item (str): Item to look for

    Returns:
        tuple[int, int]: Location of item
    """

    for y, line in enumerate(maze):
        for x, col in enumerate(line):
            if col == item:
                return (x, y)


def draw_map(screen: pygame.display, font,
             maze: list,
             visited: set,
             SCALE: int) -> None:
    """Draws the puzzle on the screen

    Args:
        screen (pygame.display): _description_
        font (_type_): _description_
        maze (list): _description_
        visited (set): _description_
        SCALE (int): _description_
    """

    logger.debug('Updating screen')

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw pathway (cells and direction)
    visited_coordinates = set()
    for dir, x, y in visited:
        if maze[y][x] == '.':
            # Do this only for .

            # Draw direction glyph ONCE
            if (x, y) not in visited_coordinates:
                # Store already drawn cells
                visited_coordinates.add((x, y))

                # Check which direction to draw
                if dir == 0:    # (0, -1):
                    c = '^'
                elif dir == 1:  # (1, 0):
                    c = '>'
                elif dir == 2:  # (0, 1):
                    c = 'v'
                elif dir == 3:  # (-1, 0):
                    c = '<'
                else:
                    logger.critical("Unknown direction")
                    exit(-1)

                text = font.render(c, True, (127, 255, 127))
                screen.blit(text, (SCALE * x, SCALE * y))

    # Draw rest of the maze;
    # expand into both x y coordinates and
    # maze cell content
    for i, line in enumerate(maze):
        for ii, c in enumerate(line):
            color = (63, 127, 63)

            # "Fancy" coloring here
            if c in 'SE':
                # For start and end position bright one
                color = (196, 255, 196)

            if c == '.':
                if (ii, i) in visited_coordinates:
                    continue
                else:
                    c = '·'
                    color = (127, 255, 127)

            text = font.render(c, True, color)
            screen.blit(text, (SCALE * ii, SCALE * i))

    pygame.display.flip()


def quick_draw_map(screen: pygame.display, font,
                   maze: list,
                   visited: set,
                   SCALE: int) -> None:
    """Draws the puzzle on the screen

    Args:
        screen (pygame.display): _description_
        font (_type_): _description_
        maze (list): _description_
        visited (set): _description_
        SCALE (int): _description_
    """

    logger.debug('Updating screen')

    # Clear screen
    # screen.fill((0, 0, 0))

    # Draw pathway (cells and direction)
    visited_coordinates = set()
    for dir, x, y in visited:
        if maze[y][x] == '.':
            # Do this only for .

            # Draw direction glyph ONCE
            if (x, y) not in visited_coordinates:
                # Store already drawn cells
                visited_coordinates.add((x, y))

                # Check which direction to draw
                if dir == 0:    # (0, -1):
                    c = '^'
                elif dir == 1:  # (1, 0):
                    c = '>'
                elif dir == 2:  # (0, 1):
                    c = 'v'
                elif dir == 3:  # (-1, 0):
                    c = '<'
                else:
                    logger.critical("Unknown direction")
                    exit(-1)

                text = font.render(c, True, (127, 255, 127))
                screen.blit(text, (SCALE * x, SCALE * y))
                pygame.display.flip()

    return None

    # Draw rest of the maze;
    # expand into both x y coordinates and
    # maze cell content
    for i, line in enumerate(maze):
        for ii, c in enumerate(line):
            color = (63, 127, 63)

            # "Fancy" coloring here
            if c in 'SE':
                # For start and end position bright one
                color = (196, 255, 196)

            if c == '.':
                if (ii, i) in visited_coordinates:
                    continue
                else:
                    c = '·'
                    color = (127, 255, 127)

            text = font.render(c, True, color)
            screen.blit(text, (SCALE * ii, SCALE * i))

    pygame.display.flip()


def part_a(filename: str, SHOW: bool = False) -> int:
    # Read puzzle
    maze = read_puzzle(filename)

    # Redefine SCALE to fit maze on screen
    SCALE = SCREEN_SIZE // len(maze[0])
    logger.info(f'Setting {SCALE=}')

    # Set up pygame
    pygame.init()
    timert = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.SysFont('freemono', size=SCALE)

    size_x = SCALE * len(maze[0])
    size_y = SCALE * len(maze)

    if SHOW:
        screen = pygame.display.set_mode([size_x, size_y])

    # Find start and end
    current_position = find_location(maze, 'S')
    end_position = find_location(maze, 'E')

    logger.info(f'Start: {current_position}')
    logger.info(f'End: {end_position}')

    # Store possibilities in _heap_:
    #       score, direction (1=East), x and y
    heap = [(0, 1, *current_position)]

    # Keep track of already visited positions
    visited = set()

    # Draw map on screen
    if SHOW:
        draw_map(screen, font, maze, visited, SCALE)

    # Start looping over the maze
    i = 0
    while heap:
        # Draw map on screen
        if SHOW:
            i = (i + 1) % 1000
            if i == 0:
                quick_draw_map(screen, font, maze, visited, SCALE)

        # Get item from the heap (err... this one has the lowest score?)
        score, dir, x, y = heappop(heap)
        logger.debug(f'{score=}, {dir=}, {x=}, {y=}')

        # Check for end position
        if (x, y) == end_position:
            logging.info('Reached the exit, exiting...')
            # Get out of while loop
            break

        # Check if we already visited here
        if (dir, x, y) in visited:
            # Jump to start of while loop
            logger.debug('Already visited, next...')
            continue

        # Process current position
        # - Add dir/pos to visited positions
        visited.add((dir, x, y))

        # Check straight ahead
        new_x = x + DIRECTIONS[dir][0]
        new_y = y + DIRECTIONS[dir][1]
        logger.debug(f'Maze: {maze[y][x]=}')
        if maze[y][x] in 'S.' and (dir, new_x, new_y) not in visited:
            logger.debug(f'Adding {dir}, {new_x}, {new_y}')
            heappush(heap, (score + 1, dir, new_x, new_y))

        # Prepare going left (stepping into direction - 1)
        # N E S W (go 1 back, loop around 4)
        left = (dir - 1) % 4
        if (left, x, y) not in visited:
            heappush(heap, (score + 1000, left, x, y))

        # Same but going right
        right = (dir + 1) % 4
        if (right, x, y) not in visited:
            heappush(heap, (score + 1000, right, x, y))

        # Check on pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        # Draw on screen if selected
        if SHOW:
            logger.debug('FPS')
            timert.tick(FPS)

    # Show score
    logging.info(f'Score: {score}')

    # Keep game screen open
    running = True
    while running and SHOW:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        timert.tick(FPS)

    # Stop pygame
    pygame.quit()

    return score


def stub():
    part_a('16/input.txt', SHOW=True)


if __name__ == "__main__":
    cProfile.run("stub()")
