# A state has a number of cities clusters in which the cities are connected by a network of roads.
# These roads are bidirectional. i.e traffic can move in either direction.
# There are no connections between the clusters. With in a cluster, assume that 2 cities are connected by one road at most.
# Write an algorithm to determin the total number of clusters of internally connected cities for one such network of cities and roads.

# Input:
# The first line of input consisists of 2 space-separated integers - matInput_row and matInput_col, representing the number of cities in the state(N)
# and number of connections with each city(M)
# The next N lines consist of M space-separated integers, representing the matrix. Entry (i j) of the matrix is 1 if the ith city and the jth city are connected by a road.
# Otherwise, it is 0.

# Output:
# Print an integer representing the total number of clusters of internally connected cities for one such network of cities and roads.
# Constraints:
# The elements of the matrix are either 0 or 1.

# Example:
# Input:
# 5 5
# 0 0 0 0 0
# 0 0 1 0 0
# 0 1 0 1 0
# 0 0 1 0 0
# 0 0 0 0 0
# Output:
# 3

# Explanation:
# Number of cities = 5 and total connecting cities = 4 (represented by 1), so total number of connected clusters = 3.
# So the output is 3.


def countClusters(matInput):
    # number of cities
    n = len(matInput)
    # visited cities
    visited = [False] * n

    def dfs(city):
        visited[city] = True
        for i in range(n):
            if matInput[city][i] == 1 and not visited[i]:
                dfs(i)



    # count clusters
    counter = 0
    for i in range(n):
        if not visited[i]:
            dfs(i)
            counter += 1

    return counter




if __name__ == "__main__":

    matInput_row = 5
    matInput_col = 5
    matInput = [
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    print(countClusters(matInput))
    
