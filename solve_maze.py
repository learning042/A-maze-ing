from maze import Maze
from cell import DIRECTIONS
from tuple_op import subtract_tuples
from typing import Generator


def solve_maze(maze: Maze) -> Generator[None, None, None]:
    maze.reset_path()
    maze.turn_all_cells_unvisited()
    start = maze.get_cell(*maze.start)
    end = maze.get_cell(*maze.end)
    start.mark_visited()
    queue = [maze.get_cell(*maze.start)]
    while queue:
        current = queue.pop(0)
        if current == end:
            return
        neighbors = maze.return_available_moves(current)
        for neighbor in neighbors:
            neighbor.mark_visited()
            neighbor.parent = current
            queue.append(neighbor)
            yield


def get_path(maze: Maze) -> str:
    path = ""
    curr = maze.get_cell(*maze.end)
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
    return path


if __name__ == "__main__":
    from maze_gen import DFSGenerator
    g = DFSGenerator()
    maze = g.creator(10, 10, (9, 9))
    for _ in solve_maze(maze):
        continue
    print(maze.get_graphical_view())
    print(get_path(maze))
    
