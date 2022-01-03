# Author: Nicholas Bowden
# Description: A modified version of Dijkstra's algorithm to find a valid path through a maze. 
# The maze input should consist of a nested list where open spaces are empty and walls are represented with '#'

import heapq

def solve_puzzle(board, source, destination):
    if source == destination: return [source] 

    max_x = len(board)
    max_y = len(board[0])

    shortest_path = None
    distances = {(r,c): float('inf') for r in range(max_x) for c in range(max_y)}
    distances[source] = 0

    # Format: Distance from source, source node, current path
    priority_queue = [(0, source,[source])]

    while len(priority_queue) > 0:
        current_distance, (x,y), path = heapq.heappop(priority_queue)

        # Only process each node once, the first time it is removed from the priority queue
        if current_distance > distances[(x,y)]:
            continue
        
        for x_change, y_change in [(0,1), (1,0), (-1,0), (0,-1)]: # Potential moves: Up, right, down, left
            nx = x + x_change
            ny = y + y_change
            if not 0 <= nx <max_x or not 0<=ny<max_y: continue # Checks for invalid neighbor
            if board[nx][ny] == '#': continue # Checks for wall cell
            
            distance = current_distance + 1

            # If we found a new minimum value for a path then we will update the dict and explore that path
            if distance < distances[(nx,ny)]:
                distances[(nx,ny)] = distance
                heapq.heappush(priority_queue, (distance, (nx,ny), path + [(nx,ny)]))

                # Neighbor is destination and path is shorter, update shortest_path
                if (nx,ny) == destination: 
                    shortest_path = path+[destination] 

    return shortest_path  
