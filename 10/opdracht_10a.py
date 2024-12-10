import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Read input file as numpy array
field = np.genfromtxt("10/input.txt", dtype=int, delimiter=1)

# Add a round of -1, so we don't get into trouble when looking around edge
# values
field = np.pad(field, 1, constant_values=-1)


# Ruud will like this: networkx
G = nx.DiGraph()

# Store nodes with 0 (startingpoints)
startnodes = []

# look up down left right
directions = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])

# Loop over input
for y in range(1, field.shape[0] - 1):
    for x in range(1, field.shape[1] - 1):
        # Add each node step by step
        G.add_node(f"{y},{x}")

        # Is this node a starting node?
        if field[y, x] == 0:
            startnodes.append(f"{y},{x}")

        # Look for sequental fields (difference is 1), add edge
        for direction in directions:
            if field[tuple(direction + [y, x])] - field[y, x] == 1:
                G.add_edge(f"{y},{x}",
                           f"{y + direction[0]},{x + direction[1]}")

sum1 = 0
sum2 = 0

for startnode in startnodes:
    for endnode in filter(
        lambda a: a[1] == 9,
        nx.single_source_shortest_path_length(G, startnode).items(),
    ):
        sum1 += 1
        sum2 += len(list(nx.all_simple_paths(G, startnode, endnode)))
print(sum1, sum2)

fig, ax = plt.figure()

nx.draw(G)
