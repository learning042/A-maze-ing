from maze import Maze
from cell import Cell
from math import sqrt
import random

NORTH = (0, -1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)


def sum_tuples(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
    """Add the coordinates of one tuple to the other."""
    return (p1[0] + p2[0], p1[1] + p2[1])


def calculate_distance(p1: tuple[int, int], p2: tuple[int, int] = (0, 0)) -> float:
    """
    Calculate the distance between two points. 
    If p2 is not specified It is considered
    the distance between p1 and the origin
    """
    return (
        sqrt(
            (p1[0] - p2[0]) ** 2 +
            (p1[1] - p2[1]) ** 2
            )
        )


class Cursor:
    def __init__(self, row: int, column: int) -> None:
        self._position = (row, column)

    def move(self, direction: tuple[int, int]) -> None:
        """Move in a specific direction one unit"""
        if round(calculate_distance(direction)) != 1:
            raise ValueError("Invalid 'direction' value. It should be an unit \"vector\"(tuple).")
        self._position = sum_tuples(self._position, direction)

    def return_available_cells_around(self, maze: Maze) -> list[Cell] | None:
        """Return the available(not visited and possible to visit) cells around the cursor."""
        not_visited: list[tuple[int, int]] | None = []
        maze.mark_visited(*self._position)
        for direction in (NORTH, EAST, SOUTH, WEST):
            cell_position = sum_tuples(self._position, direction)
            if cell_position[0] < 0 or cell_position[1] < 0:
                continue
            cell = maze.grid[cell_position[0]][cell_position[1]]
            if cell.visited or cell.is_42:
                continue
            not_visited.append(cell)
        #nv = [n.position() for n in not_visited]
        #print(f"not_visited {nv}")
        return not_visited

    def move_random_available(self, maze: Maze) -> None:
        """Move to a random visited cell that is beside the current position"""
        cells = self.return_available_cells_around(maze)
        if not len(cells):
            return
        cell = random.choice(cells)
        self._position = cell.position()
        maze.mark_visited(*self._position)
    
    def get_position(self) -> tuple[int, int]:
        return self._position


if __name__ == "__main__":
    maze = Maze(40, 40)
    cursor = Cursor(0, 0)
    print(cursor.get_position())
    for _ in range(40):
        cursor.move_random_available(maze)
        print(cursor.get_position())
