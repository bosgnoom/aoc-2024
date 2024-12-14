def get_neighbors(x, y, grid):
    # Directions are (right, down, left, up)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            neighbors.append((nx, ny))
    return neighbors


def dfs(x, y, grid, visited, plant_type):
    stack = [(x, y)]
    region = []
    while stack:
        cx, cy = stack.pop()
        if visited[cx][cy]:
            continue
        visited[cx][cy] = True
        region.append((cx, cy))
        for nx, ny in get_neighbors(cx, cy, grid):
            if grid[nx][ny] == plant_type and not visited[nx][ny]:
                stack.append((nx, ny))
    return region


def calculate_region_properties(region, grid):
    area = len(region)
    perimeter = 0
    sides = 0
    for x, y in region:
        # Count perimeter and sides for each plot in the region
        for nx, ny in get_neighbors(x, y, grid):
            if grid[nx][ny] != grid[x][y]:
                perimeter += 1
            if (nx == 0 or ny == 0 or nx == len(grid) - 1 or ny == len(grid[0]) - 1 or grid[nx][ny] != grid[x][y]):
                sides += 1
    return area, perimeter, sides


def calculate_total_price(grid):
    visited = [[False] * len(grid[0]) for _ in range(len(grid))]
    region_properties = []

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if not visited[i][j]:
                plant_type = grid[i][j]
                region = dfs(i, j, grid, visited, plant_type)
                area, perimeter, sides = calculate_region_properties(
                    region, grid)
                region_properties.append((plant_type, area, perimeter, sides))

    # Calculate the price for each region (area * sides)
    total_price = 0
    for _, area, _, sides in region_properties:
        total_price += area * sides

    return region_properties, total_price


# Example 1: Test the function with the first map
grid1 = [
    ['A', 'A', 'A', 'A'],
    ['B', 'B', 'C', 'D'],
    ['B', 'B', 'C', 'C'],
    ['E', 'E', 'E', 'C']
]

region_properties1, total_price1 = calculate_total_price(grid1)
print("Region Properties (Area, Perimeter, Sides):")
for plant, area, perimeter, sides in region_properties1:
    print(f"Plant {plant}: Area={area}, Perimeter={perimeter}, Sides={sides}")
print(f"Total Price: {total_price1}")

# Example 2: Test with the second map (for the X and O regions)
grid2 = [
    ['O', 'O', 'O', 'O', 'O'],
    ['O', 'X', 'O', 'X', 'O'],
    ['O', 'O', 'O', 'O', 'O'],
    ['O', 'X', 'O', 'X', 'O'],
    ['O', 'O', 'O', 'O', 'O']
]

region_properties2, total_price2 = calculate_total_price(grid2)
print("\nRegion Properties (Area, Perimeter, Sides):")
for plant, area, perimeter, sides in region_properties2:
    print(f"Plant {plant}: Area={area}, Perimeter={perimeter}, Sides={sides}")
print(f"Total Price: {total_price2}")
