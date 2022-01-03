# Author: Nicholas Bowden
# Description: Undirected graph methods implemented: add_vertex(), add_edge()remove_edge(), 
#   remove_vertex()get_vertices(), get_edges()is_valid_path(), dfs(), ​bfs()count_connected_components(), has_cycle()

from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph. 
        
        Does nothing if the vertex passed is already in the dictionary. 
        Initializes an empty list to store adjacent vertices.
        """
        if v in self.adj_list:
            return
        self.adj_list[v] = []
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph. 
        
        If either vertex is not already in the adjacency dictionary, it adds it to the dictionary.
        Adds each vertex to the others list.
        Does not allow duplicates to be added on any list.
        Does nothing if that same vertex is passed for both parameters.
        """
        # Same vertex passed
        if u == v:
            return
        
        # Adds a new vertex to adj_list if not in the dictionary
        if u not in self.adj_list:
            self.add_vertex(u)
        if v not in self.adj_list:
            self.add_vertex(v)

        # Adds opposite vertex to each list if not already present
        if u not in self.adj_list[v]:
            self.adj_list[v].append(u)
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
        

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph. 
        
        Checks if passed vertices are in the dictionary and then checks if the opposite 
        vertex is present in each vertices adjacency list and removes each occurrence if found.
        Does nothing if the same vertex is passed for both parameters.
        """
        # Same vertex passed
        if u == v:
            return
        
        # Checks if passed vertex is in the dictionary
        if u in self.adj_list:
            # Removes if found on opposite vertices list
            if v in self.adj_list[u]:
                self.adj_list[u].remove(v)
        
        # Same for the other vertex
        if v in self.adj_list:
            if u in self.adj_list[v]:
                self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges. 
        
        Pops the vertex off the dictionary, uses the list that was popped 
        to find all the adjacent vertices and remove the occurrence of the removed vertex.
        """
        if v in self.adj_list:
            edges = self.adj_list.pop(v)

            for edge in edges:
                self.adj_list[edge].remove(v)

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order).
        """
        return [*self.adj_list]

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order). Appends all the non repeating vertex,edge combonations.
        """
        result = []

        for vertex in self.adj_list:
            for edge in self.adj_list[vertex]:

                if (edge,vertex) not in result:  # prevents 'duplicates' 
                    result.append((vertex, edge))
     
        return result
        

    def is_valid_path(self, path: []) -> bool:
        """
        Return True if provided path is valid, False otherwise.

        Traverses through each value on the path, checking that the next path value is an adjacent node to the current value.
        """
        result = True
        path_size = len(path)
        
        # Empty path
        if path_size == 0:
            return result

        # Single value, verifies that it's valid
        if path_size == 1:
            if path[0] not in self.adj_list:
                result = False

        # Traverses through verifying that each step and the next are possible
        for i in range(path_size-1):
            if path[i] not in self.adj_list:  # Current node not in list
                return False
            if path[i+1] not in self.adj_list[path[i]]:  # Next node not adjacent to current node
                result = False

        return result


    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during this recursive DFS search. 
        
        Vertices are picked in alphabetical order.
        Can be used to find a specific node by using v_end, or find all connected nodes without.

        Starts at the passed node and saves it as visited, then takes the adjacency list and sorts.
        Iterating through that list, if v_end is found then it is added to visited and the 
        function stops. If v_end is not found or not present, the function continues looking for adjacent
        nodes that have not been visited yet. Once it has visited them all it returns the result.
        """
        visited = []

        # Invalid start
        if v_start not in self.get_vertices():
            return visited

        def rec_dfs(visited, v, v_end=None):
            """Recursive depth first search"""
            if v_end:
                if v_end not in visited: # Runs until v_end is visited
                    visited.append(v) 
            elif v_end is None:  # Runs until all adjacent nodes are visited
                visited.append(v)
    
            # Test cases require ascending lexicographical order
            self.adj_list[v].sort()

            # Loops through each adjacent vertex, recurring for each
            for adj in self.adj_list[v]:
                if v_end and v_end in visited:
                    break
                elif adj not in visited:
                    rec_dfs(visited, adj, v_end)
                
        rec_dfs(visited, v_start, v_end)
      
        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search. 

        Uses a queue to keep track of unvisited vertices, runs until the queue is empty, indicating 
        every connected node has been visited. 
        Can be used to search from node to node with the presence of v_end or to find all connected nodes without.

        Takes the vertex at the front of the queue and gets it's adjacent vertex list. This method then
        adds the vertex to the result list if its not a duplicate.
        Sorts the edges in alphabetical order, adds each vertex to the queue if it's not a duplicate.
        Ends when v_end is added to the result list or when the queue is empty indicating that all of the connected
        nodes have been visited.
        """
        visited = []
        
        # Invalid starting node
        if v_start not in self.adj_list:
            return visited

        next_vertex = deque()  # imported structure
        next_vertex.append(v_start) 

        # Runs until v_end is found or queue is empty
        while len(next_vertex) != 0:
            vertex = next_vertex.popleft()  # dequeue 
            edges = self.adj_list[vertex]

            # Marks as visitied
            if vertex not in visited:  
                visited.append(vertex)

            # Ends loop
            if vertex == v_end:  
                return visited 

            edges.sort()  # Alphabetical order
            for item in edges:
                if item not in visited:
                    next_vertex.append(item)  # enqueue if not duplicate
            
        return visited        

    def count_connected_components(self):
        """
        Return the number of connected componets in the graph.

        Gets a list of current vertices. Starts with the first vertex in the list and runs a dfs on it.
        The connected vertices are returned from that method then each of those connections are removed from
        the vertices list, leaving any unconnected nodes in the list. Increments the count for each removal of 
        an empty node or connected set found through dfs.
        """
        count = 0
        vertices = self.get_vertices()
      
        # Runs until vertices is empty
        while len(vertices) > 0:
            vertex = vertices[0]
            
            # Empty list, increment count
            if len(self.adj_list[vertex]) == 0:
                count += 1
                vertices.remove(vertex)
                continue

            # Remove nodes returned from dfs, increment count
            connection = self.dfs(vertex)
            for component in connection:
                vertices.remove(component)
            count += 1

        return count

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise.

        Creates a visited dictionary with a initial False value for each vertex.
        Loops through each one of the vertices, looking for unvisited nodes.

        If a node with an empty list is found, it's skipped over. 
        If a node has already been visited when encountered, it's skipped.

        Otherwise, using dfs, it recursively checks for cycles by saving
        the parent of the current node. When adjacent vertices are checked, if a vertex has 
        already been visited and it is NOT the current parent node, then a cycle has been found.
        """
        vertices = self.get_vertices()
        visited = {vert: False for vert in vertices}
        cycle = False

        def rec_dfs(visited, parent, v):
            # Mark current node as visited
            visited[v] = True

            # Adjacent vertices
            for adj in self.adj_list[v]:
        
                # if adj node hasn't been visited yet
                if not visited[adj]:
                    if rec_dfs(visited, v, adj): # Recur to check cycle
                        return True 
        
                # adj node has been visited AND is not the parent
                elif adj != parent:
                    return True # Back edge
        
            # No back edge
            return False     

        for vertex in vertices:
            # Skips empty lists
            if len(self.adj_list[vertex]) == 0:
                continue
            
            # Skips visited nodes, looking for unvisited chains
            if visited[vertex]:
                continue

            # Returns True if cycle is found, continues otherwise
            if rec_dfs(visited, None, vertex):
                cycle = True
                break 

        return cycle    

if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AJ', 'AD', 'AB', 'AC', 'JA','JD', 'JK', 'EB', 'BE', 'BA', 'DA', 'DJ', 'DK', 'FI', 'IF', 'CA', 'KD', 'KJ']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    print(g.dfs('A'))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
