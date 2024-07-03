from docplex.mp.model import Model
import heapq
import sys


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
# # Specify the filename
# filename = 'instances/pmed1.txt'

# Create the adjacency matrix and get additional parameters
adj_matrix, n, e, p = create_adjacency_matrix(filename)

# Print the additional parameters
print(f"Number of nodes: {n}")
print(f"Number of edges: {e}")
print(f"Additional parameter (p): {p}")

# Print the adjacency matrix
# print("Adjacency matrix:")
# for row in adj_matrix:
#     print(row)

# Compute shortest paths using Dijkstra's algorithm
sources = list(range(n))
graph = dijkstra(n, adj_matrix, sources)

# Print the shortest paths




# for row in graph:
#     print(row)
print("###########################################################################")

# Extract unique distances
unique_distances = set()
for i in range(len(graph)):
    for j in range(len(graph[i])):
        if graph[i][j] != 0:
            unique_distances.add(graph[i][j])
distinct_distances = sorted(list(unique_distances))
for i in range(len(graph)):
    for j in range(len(graph[i])):
        if graph[i][j] != 0:
            unique_distances.add(graph[i][j])
distinct_distances = sorted(list(unique_distances))

M = range(n)  # Indices for y_j
T = range(len(distinct_distances))  # Indices for z_k
N = range(n)  # Indices for i
rho = distinct_distances  # Costs for z_k
mdl = Model(name='p-center')

# Define decision variables
y = mdl.binary_var_list(M, name='y')
z = mdl.binary_var_list(T, name='z')

# Define the objective function
mdl.minimize(mdl.sum(rho[k] *z[k]  for k in T))

# Constraints
for i in N:
    for k in T:
        mdl.add_constraint(mdl.sum(y[j] for j in M if graph[i][j] <= rho[k] ) >= z[k])

mdl.add_constraint(mdl.sum(y[j] for j in M) <= p)
mdl.add_constraint(mdl.sum(z[k] for k in T) == 1)
mdl.context.cplex_parameters.threads = 1 

# Solve the model
solution = mdl.solve(log_output=False)
# Display the solution
if solution:
    print("##########ceplex###################")
    print("Objective value:", solution.objective_value)
    print("Solution status:", solution.solve_status)
    print("Values for y_j:")
    for j in M:
        print(f"y_{j+1} = {y[j].solution_value}")
    print("Values for z_k:")
    for k in T:
        print(f"z_{k+1} = {z[k].solution_value}")
        # print (z)
else:
    print("No solution found")


print ("rho values ", rho)
print("Shortest paths:")
for row in graph:
    print(row)
