from maze import Maze
from cell import DIRECTIONS
from tuple_op import subtract_tuples


def solve_maze(maze: Maze) -> str:
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
        delta = subtract_tuples(curr.position(), curr.parent.position())
        path += next(
                k[0].capitalize()
                for k, v in DIRECTIONS.items()
                if v == delta
                )
        curr = curr.parent
        curr.in_path = True
    path = path[::-1]
    maze.turn_all_cells_unvisited()
    return path
