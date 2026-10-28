from maze import Maze
from cell import DIRECTIONS
from tuple_op import subtract_tuples


def solve_maze(maze: Maze) -> str:
    #1- SAVE current -> queue
    #2- TAKE the first and EXPLORE the neighbors
    #3- SAVE
    #4- Repeat the process for each way
    maze.reset_path()
    start = maze.get_cell(*maze.start)
    end = maze.get_cell(*maze.end)
    start.mark_visited()
    queue = [maze.get_cell(*maze.start)]
    while queue:
        current = queue.pop(0)
        if current == end:
            break
        neighbors = maze.return_available_moves(current)
        for neighbor in neighbors:
            neighbor.mark_visited()
            neighbor.parent = current
            queue.append(neighbor)
    path = ""
    curr = end
    curr.in_path = True
    while curr.parent is not None:
        path += (next(k[0].capitalize() for k in DIRECTIONS.keys() if DIRECTIONS[k] == subtract_tuples(curr.position(), curr.parent.position())))
        curr = curr.parent
        curr.in_path = True
    path = path[::-1]
    maze.turn_all_cells_unvisited()
    return path
