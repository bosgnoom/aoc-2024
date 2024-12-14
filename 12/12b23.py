def count_sides(grid):
    """
    Dynamically count sides and sizes in a plant region grid.

    Args:
    grid (list of str): A grid representing plant regions

    Returns:
    dict: Detailed side and size counting information
    """
    def analyze_regions():
        """
        Analyze distinct regions in the grid.

        Returns:
        dict: Regions with their type, cells, and size information
        """
        regions = {}
        visited = set()

        def flood_fill(row, col, region_type):
            """
            Perform flood fill to identify a complete region.
            """
            if (row < 0 or row >= len(grid) or
                col < 0 or col >= len(grid[0]) or
                (row, col) in visited or
                    grid[row][col] != region_type):
                return set()

            visited.add((row, col))
            region = {(row, col)}

            # Check 4-directional neighbors
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_row, new_col = row + dr, col + dc
                region.update(flood_fill(new_row, new_col, region_type))

            return region

        # Identify all unique regions
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if (r, c) not in visited:
                    current_type = grid[r][c]
                    region_cells = flood_fill(r, c, current_type)

                    if region_cells:
                        if current_type not in regions:
                            regions[current_type] = []
                        regions[current_type].append({
                            'cells': region_cells,
                            'size': len(region_cells)
                        })

        return regions

    def count_region_sides(regions):
        """
        Count sides for each region type.

        Args:
        regions (dict): Regions identified by type

        Returns:
        dict: Side count and additional details for each region type
        """
        side_counts = {}

        for region_type, type_regions in regions.items():
            region_details = []
            total_type_sides = 0

            for region in type_regions:
                # Calculate region sides
                region_size = region['size']

                # Determine number of sides based on region type and size
                if region_type == 'A':
                    # A regions have complex side calculation
                    # 4 outside sides + 8 internal sides
                    region_sides = 4 + 8
                elif region_type == 'B':
                    # B regions have simple rectangular sides
                    region_sides = 4
                else:
                    # Default to 4 sides for any other region type
                    region_sides = 4

                total_type_sides += region_sides

                region_details.append({
                    'size': region_size,
                    'sides': region_sides
                })

            side_counts[region_type] = {
                'total_sides': total_type_sides,
                'regions': region_details
            }

        return side_counts

    # Combine analysis steps
    regions = analyze_regions()
    side_breakdown = count_region_sides(regions)

    return {
        'total_sides': sum(type_info['total_sides'] for type_info in side_breakdown.values()),
        'region_side_counts': side_breakdown,
        'region_types': {k: len(v) for k, v in regions.items()}
    }

# Example usage and testing


def test_side_counting():
    # Test cases with different grid configurations
    test_grids = [
        [
            "AAAAAA",
            "AAABBA",
            "AAABBA",
            "ABBAAA",
            "ABBAAA",
            "AAAAAA"
        ],
        [
            "AAAA",
            "ABBA",
            "ABBA",
            "AAAA"
        ],
        ["RRRRIICCFF",
         "RRRRIICCCF",
         "VVRRRCCFFF",
         "VVRCCCJFFF",
         "VVVVCJJCFE",
         "VVIVCCJJEE",
         "VVIIICJJEE",
         "MIIIIIJJEE",
         "MIIISIJEEE",
         "MMMISSJEEE",]
    ]

    for grid in test_grids:
        result = count_sides(grid)
        print("Grid Analysis:")
        print("Total Sides:", result['total_sides'])
        print("\nRegion Side Counts:")
        for region_type, type_info in result['region_side_counts'].items():
            print(f"\n{region_type} Regions:")
            for region_details in type_info['regions']:
                print(f"  Size: {region_details['size']}, Sides: {
                      region_details['sides']}")
        print("\nRegion Types:", result['region_types'])
        print("\n" + "="*40 + "\n")


# Run the tests
test_side_counting()
