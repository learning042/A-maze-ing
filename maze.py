from cell import Cell
from typing import Any, TextIO
import sys
from contextlib import nullcontext

class Maze:
    """Defines the maze"""
    def __init__(self, width: int, height: int) -> None:
        """
        Instantiate a new maze.

        Args:
            self.width : width of the maze in cell-side unit
            self.height : height of the maze int cell-side unit
            self.grid : list of lists where each list has a cell object for each line
                        of the maze
        """
        self.width = width
        self.height = height
        self.grid = [[Cell(row, col) for col in range(width)] for row in range(height)]

    def show(self, attribute: str, filename = "sys.stdout") -> None:
        """Print the cell attribute of each cell"""
        if filename != "sys.stdout":
            context = open(filename, "w")
        else:
            context = nullcontext(sys.stdout)

        with context as f:
            for row in self.grid:
                for cell in row:
                    value = getattr(cell, attribute)
                    if callable(value):
                        value = value()
                    print(value, file=f, end="")
                print(file=f)


def main() -> None:
    maze = Maze(5, 10)
    maze.show("hex")
    maze.show("show")


if __name__ == "__main__":
    main()
