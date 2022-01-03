# DFS-BFS-Dijkstra

DFS/BFS/Dijkstra's Search Algorithms for undirected and directed graphs in Python.
Modified Dijkstra's Algorithm for the maze solving function.

For an undirected graph there are methods to search use depth first search, breadth first search, as well as a method to detect cycles.
These methods are done using an adjacency list to represent the graph. Each vertex has a list of connected vertices.

For a directed graph there are the same methods as well as an additional method using Dijkstra's algorithm.
This will return the shortest path to each connected node.
These methods are done using an adjacency matrix to represent the edges. A value > 0 in the matrix represents a weighted edge between two vertices.

The maze solving function was achieved using a modified version of Dijkstra's using a priority queue. This allowed for only the most efficient path to be considered on the way to the exit. The shortest distances to each node are stored in a dictionary, with only the shortest path to each node being saved.
