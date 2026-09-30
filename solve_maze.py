from maze import Maze
from cell import Cell

def solve_maze(maze: Maze) -> Cell | None:
    #1- SAVE current -> queue
    #2- TAKE the first and EXPLORE the neighbors
    #3- SAVE
    #4- Repeat the process for each way
    start = maze.get_cell(*maze.start)
    end = maze.get_cell(*maze.end)
    start.mark_visited()
    queue = [maze.get_cell(*maze.start)]
    while queue:
        current = queue.pop(0)
        if current == end:
            return current
        neighbors = maze.return_available_neighbors(current)
        for neighbor in neighbors:
            neighbor.mark_visited()
            neighbor.parent = current
            queue.append(neighbor)
    return None
        
