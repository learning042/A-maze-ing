from maze import Maze
from math import sqrt


def add_position(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
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
    def __init__(self, position: tuple[int, int]) -> None:
        self._position = position

    def move(self, direction: tuple[int, int]) -> None:
        """Move in a specific direction one unit"""
        if round(calculate_distance(direction)) != 1:
            raise ValueError("Invalid 'direction' value. It should be an unit \"vector\"(tuple).")
        self._position = add_position(self._position, direction)

    def return_available_cells_around(self, maze: Maze) -> list[tuple[int, int]] | None:
        """Return the available cells around the cursor."""
        visited: list[tuple[int, int]] | None = []
        ... 

    def move_to_visited(self, maze: Maze) -> None:
        """Move to a random visited cell that is beside the current position"""
        ...

    def get_position(self) -> tuple[int, int]:
        return self._position


if __name__ == "__main__":
    cursor = Cursor((1,1))
    print(cursor.get_position())
    NORTH = (0, -1)
    cursor.move(NORTH)
    print(cursor.get_position())
    print(calculate_distance((0, 1)))
