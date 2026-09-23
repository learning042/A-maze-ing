from cell import Cell
from math import sqrt
from tuple_op import sum_tuples, subtract_tuples
import random

NORTH = (0, -1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)


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

    def get_position(self) -> tuple[int, int]:
        return self._position


if __name__ == "__main__":
    maze = Maze(40, 40)
    cursor = Cursor(0, 0)
    print(cursor.get_position())
    for _ in range(40):
        cursor.move_random_available(maze)
        print(cursor.get_position())
