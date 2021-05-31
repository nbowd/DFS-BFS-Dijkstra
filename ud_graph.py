# Course: 
# Author: 
# Assignment: 
# Description:

from collections import deque
import heapq as heap

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
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
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
        Add new vertex to the graph
        """
        if v in self.adj_list:
            return
        self.adj_list[v] = []
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u == v:
            return
        if u not in self.adj_list:
            self.add_vertex(u)
        if v not in self.adj_list:
            self.add_vertex(v)

        if u not in self.adj_list[v]:
            self.adj_list[v].append(u)
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
        

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        if u == v:
            return

        if u in self.adj_list:
            if v in self.adj_list[u]:
                self.adj_list[u].remove(v)
        if v in self.adj_list:
            if u in self.adj_list[v]:
                self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if v in self.adj_list:
            edges = self.adj_list.pop(v)
            for edge in edges:
                self.adj_list[edge].remove(v)

        

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        return [*self.adj_list]

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        result = []
        for vertex in self.adj_list:
            for edge in self.adj_list[vertex]:
                if (edge,vertex) not in result:
                    result.append((vertex, edge))
     
        return result
        

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        result = True
        path_size = len(path)
        if path_size == 0:
            return result
        if path_size == 1:
            if path[0] not in self.adj_list:
                result = False
        for i in range(path_size-1):
            if path[i] not in self.adj_list:
                return False
            if path[i+1] not in self.adj_list[path[i]]:
                result = False
        return result


    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        result = []
        if v_start not in self.adj_list:
            return result

        next_vertex = []
        next_vertex.append(v_start)
        vertex = v_start

        while len(next_vertex) != 0:
                
            edges = self.adj_list[vertex]

            if vertex not in result:
                result.append(vertex)

            if vertex == v_end:
                return result

            edges.sort()
            old_vertex = vertex
            for edge in edges:
                if edge not in result:
                    next_vertex.append(vertex)
                    vertex = edge
                    break
            if vertex == old_vertex:
                vertex = next_vertex.pop()
   
            
        return result

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        result = []
        if v_start not in self.adj_list:
            return result

        next_vertex = deque()
        next_vertex.append(v_start) 

        while len(next_vertex) != 0:
            vertex = next_vertex.popleft()
            edges = self.adj_list[vertex]

            if vertex not in result:
                result.append(vertex)

            if vertex == v_end:
                return result 

            edges.sort()
            for item in edges:
                if item not in result:
                    next_vertex.append(item)
            
        return result        

    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """
        count = 0
        vertices = self.get_vertices()
      
        
        while len(vertices) > 0:
            vertex = vertices[0]
            if len(self.adj_list[vertex]) == 0:
                count += 1
                vertices.remove(vertex)
                continue
            connection = self.dfs(vertex)
            for component in connection:
                vertices.remove(component)
            count += 1

        return count


    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        cycle = False

        def cycle_dfs(v_start):
            result = []
            cycle = False
            backtrack = False
            if v_start not in self.adj_list:
                return cycle, result

            next_vertex = []
            next_vertex.append(v_start)
            vertex = v_start

            while len(next_vertex) != 0:
                edges = self.adj_list[vertex]

                if vertex not in result:
                    result.append(vertex)
                else:
                    if not backtrack:
                        if vertex != result[-1] and vertex != result[-2]:
                            cycle = True 

                edges.sort()
                old_vertex = vertex
                for edge in edges:
                    if edge not in result:
                        next_vertex.append(vertex)
                        vertex = edge
                        backtrack = False
                        break
                if vertex == old_vertex:
                    vertex = next_vertex.pop()
                    backtrack = True
    
                
            return cycle, result       

        vertices = self.get_vertices()
      
        while len(vertices) > 0:
            vertex = vertices[0]
            if len(self.adj_list[vertex]) == 0:
                vertices.remove(vertex)
                continue
            cycle_result = cycle_dfs(vertex)
            contains, connection = cycle_result
            if contains:
                cycle = True

            for component in connection:
                vertices.remove(component)

        return cycle


if __name__ == '__main__':

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = UndirectedGraph()
    # print(g)

    # for v in 'ABCDE':
    #     g.add_vertex(v)
    # print(g)

    # g.add_vertex('A')
    # print(g)

    # for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
    #     g.add_edge(u, v)
    # print(g)


    # print("\nPDF - method remove_edge() / remove_vertex example 1")
    # print("----------------------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    # g.remove_vertex('DOES NOT EXIST')
    # g.remove_edge('A', 'B')
    # g.remove_edge('X', 'B')
    # print(g)
    # g.remove_vertex('D')
    # print(g)


    # print("\nPDF - method get_vertices() / get_edges() example 1")
    # print("---------------------------------------------------")
    # g = UndirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    # print(g.get_edges(), g.get_vertices(), sep='\n')


    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    # test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    # for path in test_cases:
    #     print(list(path), g.is_valid_path(list(path)))


    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = ['AJ', 'AD', 'AB', 'AC', 'JA','JD', 'JK', 'EB', 'BE', 'BA', 'DA', 'DJ', 'DK', 'FI', 'IF', 'CA', 'KD', 'KJ']
    # g = UndirectedGraph(edges)
    # test_cases = 'ABCDEGH'
    # print(g.dfs('A'))

    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = 'ABCDEGH'
    # for case in test_cases:
    #     print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    # print('-----')
    # for i in range(1, len(test_cases)):
    #     v1, v2 = test_cases[i], test_cases[-1 - i]
    #     print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    # print("\nPDF - method count_connected_components() example 1")
    # print("---------------------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = (
    #     'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #     'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #     'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #     'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    # for case in test_cases:
    #     command, edge = case.split()
    #     u, v = edge
    #     g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    #     print(g.count_connected_components(), end=' ')
    # print()


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
