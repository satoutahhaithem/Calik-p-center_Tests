import heapq
import sys
from ortools.sat.python import cp_model

def create_adjacency_matrix(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        
    # Read the size of the matrix and ignore the 'p' parameter
    size_info = list(map(int, lines[0].strip().split()))
    n = size_info[0]  # number of nodes
    e = size_info[1]  # number of edges
    p = size_info[2]  # additional parameter
    
    # Initialize adjacency matrix with zeros
    adj_matrix = [[0] * n for _ in range(n)]
    
    # Read the edges and weights
    for line in lines[1:]:
        i, j, weight = map(int, line.strip().split())
        # For undirected graph, set both adj_matrix[i-1][j-1] and adj_matrix[j-1][i-1] to weight
        adj_matrix[i-1][j-1] = weight
        adj_matrix[j-1][i-1] = weight
    
    return adj_matrix, n, e, p

def dijkstra(vertices, graph, sources):
    dist = [[float('inf')] * vertices for _ in range(len(sources))]
    pq = []
    for i, src in enumerate(sources):
        dist[i][src] = 0
        heapq.heappush(pq, (0, src, i))
    while pq:
        current_dist, u, src_index = heapq.heappop(pq)
        if current_dist > dist[src_index][u]:
            continue
        for v in range(vertices):
            if graph[u][v] > 0:
                new_dist = dist[src_index][u] + graph[u][v]
                if new_dist < dist[src_index][v]:
                    dist[src_index][v] = new_dist
                    heapq.heappush(pq, (new_dist, v, src_index))
    return dist

# Check if the filename argument is provided
if len(sys.argv) != 2:
    print("Usage: python3 max-sat_read_from_file.py <filename>")
    sys.exit(1)

# Get the filename from command-line arguments
filename = sys.argv[1]

# Create the adjacency matrix and get additional parameters
adj_matrix, n, e, p = create_adjacency_matrix(filename)

# Print the additional parameters
print(f"Number of nodes: {n}")
print(f"Number of edges: {e}")
print(f"Additional parameter (p): {p}")

# Compute shortest paths using Dijkstra's algorithm
sources = list(range(n))
graph = dijkstra(n, adj_matrix, sources)

# Extract unique distances
unique_distances = set()
for i in range(len(graph)):
    for j in range(len(graph[i])):
        if graph[i][j] != float('inf'):
            unique_distances.add(graph[i][j])
distinct_distances = sorted(list(unique_distances))

# OR-Tools model
model = cp_model.CpModel()

# Variables
y = [model.NewBoolVar(f'y_{j}') for j in range(n)]
z = [model.NewBoolVar(f'z_{k}') for k in range(len(distinct_distances))]

# Objective
model.Minimize(sum(distinct_distances[k] * z[k] for k in range(len(distinct_distances))))

# Constraints
for i in range(n):
    for k in range(len(distinct_distances)):
        model.Add(sum(y[j] for j in range(n) if graph[i][j] <= distinct_distances[k]) >= z[k])

model.Add(sum(y[j] for j in range(n)) <= p)
model.Add(sum(z[k] for k in range(len(distinct_distances))) == 1)

# Solve the model
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Display the solution
if status == cp_model.OPTIMAL:
    print("Objective value:", solver.ObjectiveValue())
    print("Solution status:", solver.StatusName(status))
    print("Values for y_j:")
    for j in range(n):
        print(f"y_{j+1} = {solver.Value(y[j])}")
    print("Values for z_k:")
    for k in range(len(distinct_distances)):
        print(f"z_{k+1} = {solver.Value(z[k])}")
else:
    print("No solution found")

print("rho values:", distinct_distances)
print("Shortest paths:")
for row in graph:
    print(row)
