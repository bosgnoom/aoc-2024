from collections import deque


def read_puzzle(filename: str) -> list[str]:
    with open(filename) as f:
        return [a for a in f.read().split('\n') if len(a) > 1]


def calculate_region_properties(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]

    def in_bounds(x, y):
        return 0 <= x < rows and 0 <= y < cols

    def bfs(start_x, start_y):
        queue = deque([(start_x, start_y)])
        visited[start_x][start_y] = True
        region_char = grid[start_x][start_y]
        area = 0
        perimeter = 0

        while queue:
            x, y = queue.popleft()
            area += 1

            # Check all four directions
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy

                if not in_bounds(nx, ny) or grid[nx][ny] != region_char:
                    perimeter += 1  # Add to perimeter if out of bounds or different character
                elif not visited[nx][ny]:
                    visited[nx][ny] = True
                    queue.append((nx, ny))

        return area, perimeter

    results = {}
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                region_char = grid[r][c]
                area, perimeter = bfs(r, c)
                if region_char not in results:
                    results[region_char] = []
                results[region_char].append((area, perimeter))

    return results


# Example input
garden_map = [
    "AAAA",
    "BBCD",
    "BBCC",
    "EEEC"
]

garden_map_2 = [
    "OOOOO",
    "OXOXO",
    "OOOOO",
    "OXOXO",
    "OOOOO",
]

garden_map = read_puzzle('12/input.txt')   # 1363682

print(garden_map)

# Convert input into a grid format
grid = [list(row) for row in garden_map]

# Calculate properties
region_properties = calculate_region_properties(grid)

# Display results
total_costs = 0
for region, properties in region_properties.items():
    print(f"Region {region}:")
    for area, perimeter in properties:
        price = area * perimeter
        total_costs += price
        print(f"  Area: {area}, Perimeter: {perimeter}, {price=}")

print(f"Total costs: {total_costs=}")  # total_costs=1363682
