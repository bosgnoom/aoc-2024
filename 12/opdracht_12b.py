from collections import deque


def calculate_price(map):
    rows = len(map)
    cols = len(map[0])
    visited = [[False] * cols for _ in range(rows)]

    def in_bounds(x, y):
        return 0 <= x < rows and 0 <= y < cols

    def bfs(x, y):
        queue = deque([(x, y)])
        visited[x][y] = True
        plant_type = map[x][y]
        area = 0
        sides = 0

        while queue:
            cx, cy = queue.popleft()
            area += 1
            # Check the 4 directions (up, down, left, right)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if not in_bounds(nx, ny):  # Edge of the map
                    sides += 1
                elif map[nx][ny] == plant_type and not visited[nx][ny]:
                    visited[nx][ny] = True
                    queue.append((nx, ny))
                elif map[nx][ny] != plant_type:  # Different plant type
                    sides += 1

        return area, sides

    total_price = 0

    for i in range(rows):
        for j in range(cols):
            if not visited[i][j]:
                # Start BFS for each unvisited garden plot
                area, sides = bfs(i, j)
                total_price += area * sides

    return total_price


# Example usage:

map1 = [
    "AAAA",
    "BBCD",
    "BBCC",
    "EEEC"
]

map2 = [
    "OOOOO",
    "OXOXO",
    "OOOOO",
    "OXOXO",
    "OOOOO"
]

map3 = [
    "EEEEE",
    "EXXXX",
    "EEEEE",
    "EXXXX",
    "EEEEE"
]

map4 = [
    "AAAAAA",
    "AAABBA",
    "AAABBA",
    "ABBAAA",
    "ABBAAA",
    "AAAAAA"
]

print("Total Price (Map 1):", calculate_price(map1))  # Expected: 80
print("Total Price (Map 2):", calculate_price(map2))  # Expected: 436
print("Total Price (Map 3):", calculate_price(map3))  # Expected: 236
print("Total Price (Map 4):", calculate_price(map4))  # Expected: 368
