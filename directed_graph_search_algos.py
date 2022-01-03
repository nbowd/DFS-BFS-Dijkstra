# Author: Nicholas Bowden
# Description: Contains DFS/BFS/Dijkstra's search methods for Directed Graph as well as: add_vertex(), add_edge()remove_edge(), get_vertices(), 
#  get_edges()is_valid_path(), dfs(), ​bfs()has_cycle(), dijkstra(). More can be found on the docstring of each method and examples can be found in the included pdf.

from collections import deque
import heapq


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds a vertex to the graph. 
        
        Initializes a list with 0's to represent each of the existing vertices.
        Loops through each list and adds a 0 to account for the newly added vertex.
        Returns the current vertex count.
        """
        self.adj_matrix.append([0 for x in range(self.v_count)])
        self.v_count += 1

        for row in self.adj_matrix:
            row.append(0)
        
        return self.v_count
            
    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Create an edge between to vertices using source, destination, and weight.

        If any of the inputs are invalid, the edge is not added.
        Otherwise, assigns the passed weight to the matrix.
        """
        # Invalid, src OR dst are out of range, 
        if not 0 <= src < self.v_count or not 0 <= dst < self.v_count:
            return
        
        # Invalid, src and dst are the same node
        if src == dst:
            return
        
        # Invalid, negative weight
        if weight < 0:
            return

        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes an edge between two vertices using source, destination, and weight.

        If any of the inputs are invalid, an edge is not removed.
        Otherwise resets the weight of that edge to 0.
        """
        # Invalid, src OR dst out of range
        if not 0 <= src < self.v_count or not 0 <= dst < self.v_count:
            return
        
        # Invalid, src and dst are same vertex
        if src == dst:
            return 

        self.adj_matrix[src][dst] = 0


    def get_vertices(self) -> []:
        """
        Returns current vertices in a list.

        Index names start at 0.
        """
        return [i for i in range(self.v_count)]

    def get_edges(self) -> []:
        """
        Returns a list containing the current edges with their weights.

        Loops through each cell in the matrix and if that cell is not 0, 
        its location and value gets added to the result.
        """
        result = []

        for src in range(self.v_count):
            for dst in range(self.v_count):
                weight = self.adj_matrix[src][dst]
                if weight != 0:
                    result.append((src, dst, weight))

        return result

    def is_valid_path(self, path: []) -> bool:
        """
        Returns True if the passed list contains a valid path, Otherwise returns False.

        Loops through and checks if each vertex has a weighted edge to the next in the list.
        If at any point there isn't an edge then it is an invalid path.
        """
        size = len(path)
        
        # Empty Path
        if size == 0:
            return True

        # Single vertex
        if size == 1:
            if path[0] < self.v_count:
                return True
            return False

        src = path[0]
        dst = path[1]

        # Returns false if there is ever a non weighted edge between two path vertices.
        for i in range(2, size):
            if self.adj_matrix[src][dst] == 0:
                return False
            src = dst
            dst = path[i]
        
        # Accounts for path size 2
        if self.adj_matrix[src][dst] == 0:
            return False

        return True
            
    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during this recursive DFS search. 

        Can be used to find a specific node by using v_end, or find all connected nodes without.
        Runs until all vertices are visited or v_end has been visited. 
        Marks current node as visited, then loops through each column in the row list.
        A recursive call is made at that vertex for each weighted edge in that list 
        """
        visited = []

        if v_start not in self.get_vertices():
            return visited

        def rec_dfs(visited, v, v_end=None):
            """Recursively checks for weighted edges to unvisited nodes."""
            if v_end:
                if v_end not in visited: # Runs until v_end is visited
                    visited.append(v) 
            elif v_end is None:  # Runs until all adjacent nodes are visited
                visited.append(v)

            # Loops through each adjacent vertex, recurring for each
            for adj in range(len(self.adj_matrix[v])):
                if v_end and v_end in visited:
                    break
                elif self.adj_matrix[v][adj] != 0 and adj not in visited:
                    rec_dfs(visited, adj, v_end)
                
        rec_dfs(visited, v_start, v_end)
      
        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search.

        Uses a queue to keep track of unvisited vertices, runs until the queue is empty, indicating 
        every connected node has been visited. 
        Can be used to search from node to node with the presence of v_end or to find all connected nodes without.

        Takes the vertex at the front of the queue and gets it's adjacent matrix row list. Then
        the vertex is added to the result list if its not a duplicate.
        Loops through the row list, for each weighted edge found that vertex is added to the queue if it's not a duplicate.
        Ends when v_end is added to the result list or when the queue is empty indicating that all of the connected
        nodes have been visited.
        """
        visited = []
        
        # Invalid starting node
        if v_start not in self.get_vertices():
            return visited

        next_vertex = deque()
        next_vertex.append(v_start) 

        # Runs until v_end is found or queue is empty
        while len(next_vertex) != 0:
            vertex = next_vertex.popleft()  # dequeue 
            edges = self.adj_matrix[vertex]

            # Marks as visitied
            if vertex not in visited:  
                visited.append(vertex)

            # Ends loop
            if vertex == v_end:  
                return visited 

            for dst in range(len(edges)):
                if self.adj_matrix[vertex][dst] != 0 and dst not in visited:  # Unvisited weighted edge
                    next_vertex.append(dst)  # enqueue if not duplicate
            
        return visited  

    def has_cycle(self):
        """
        Returns True if graph has a cycle and False if not using a recursive DFS method. 

        Keeps a list of visited vertices and a stack to keep track of which path it is on
        Iterates through each vertex in the graph, skipping the already visited and empty (no weighted edges) vertices.

        When a weighted edge is found, marks current node as visited and also marks it on the path stack. 
        Iterates through each weighted edge and making recursive calls for each. This if an adjacent node has 
        already been marked in the path stack, if so then a cycle has been found. If not, then before each recursive call finishes
        it unmarks the current node from the path stack and continues with the next node with path options. 
        """
        vertices = self.get_vertices()
        visited = [False for i in range(len(vertices))]
        path = [False for i in range(len(vertices))]  
        cycle = False

        def rec_dfs(visited, path, v):
            """Recursively checks for a cycle"""
            # Mark current node as visited
            visited[v] = True
            path[v] = True

            # Adjacent vertices
            for adj in range(len(self.adj_matrix[v])):
                if self.adj_matrix[v][adj] != 0:
                    if not visited[adj]:
                        if rec_dfs(visited, path, adj): # Recur to check cycle
                            return True 
                    elif path[adj]:  # Base case, adjacent node already visited during this path. Cycle found
                        return True

            # Back track. Erases from list to check other options
            path[v] = False
            # No back edge
            return False     

        for vertex in vertices:
            # Skips visited nodes, looking for unvisited chains
            if visited[vertex]:
                continue
            
            # No weighted edges
            empty = False
            for i in range(len(self.adj_matrix[vertex])):
                if empty:
                    break
                if self.adj_matrix[vertex][i] != 0:
                    empty = True

            # Returns True if cycle is found, continues otherwise
            if rec_dfs(visited, path, vertex):
                cycle = True
                break 

        return cycle     

    def dijkstra(self, src: int) -> []:
        """
        Finds the closes distance to each node in the list using dijkstra's algorithm.

        Uses heapq to structure the priority queue for distance and node connections.
        Creates a visited dictionary with the value of infinity set for each vertex.
        
        The source node is added to the priority queue with distance(priority) 0.
        Iterates until the queue has been emptied, checking and updating the visited 
        dictionary to only save the shortest distances to each vertex. Unpacks and returns
        the visited values for the result.
        """
        # Initialize empty dictionary represented visited vertices
        vertices = self.get_vertices()
        visited = {vert: float('inf') for vert in vertices}

        # Initialize priority queue and boilerplate methods from heapq documentation
        pq = []  # heap
        def add_task(task, priority=0):
            """Add a new task or update the priority of an existing task"""
            entry = [priority, task]
            heapq.heappush(pq, entry)

        def pop_task():
            """Remove and return the lowest priority task. Raise KeyError if empty."""
            while pq:
                priority, task = heapq.heappop(pq)  
                return task, priority
            raise KeyError('pop from an empty priority queue')

        # Add source vertex with distance(priority) 0
        add_task(src, 0)
        while len(pq) > 0:
            try:
                closest =  pop_task()
            except(KeyError): 
                break
            vertex = closest[0]  # splits returned tuple
            distance = closest[-1]
            
            # if current path distance is less than saved distance at this vertex
            if int(distance) < visited[vertex]: 
                visited[vertex] = distance  # updates distance(priority)
                for c in range(len(self.adj_matrix[vertex])):

                    # Found weighted edge for path
                    if self.adj_matrix[vertex][c] != 0:
                        add_task(c, distance + self.adj_matrix[vertex][c])
            
        return [*visited.values()]  # unpacks just the values

if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]

    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(3,8,20), (3, 9, 3), (5, 2, 11), (5, 6, 15),
             (7, 2, 9), (8, 0, 4), (8, 1, 11), (9,12,17),
             (10,3,9), (10,5,5), (12,1,13), (12,7,8)]
    g = DirectedGraph(edges)
    print(g.dijkstra(3))
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')

    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
