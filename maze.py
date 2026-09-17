from cell import Cell
from typing import Any, TextIO, IO
import sys
import os
from contextlib import nullcontext


class Maze:
    """Defines the maze"""
    def __init__(self, width: int, height: int) -> None:
        """
        Instantiate a new maze.

        Args:
            width : width of the maze in cell-side unit
            height : height of the maze int cell-side unit
            grid : list of lists where each list has a cell object for each line
                        of the maze
        """
        self.width = width
        self.height = height
        self.grid = [[Cell(row, col) for col in range(width)] for row in range(height)]

    def show(
            self,
            attribute: str,
            filename: str = "sys.stdout",
            clear: bool = False,
            append: bool = False
         ) -> None:
        """
        Print the given cell attribute of each cell.
          
        Options:
            filename: Redirects to a given file if specified
            append : If it is True, the content will be appended to the file
            clear : If it is True, all the previous content in the file
                    will be deleted before adding the new content
        """

        mode = "a" if append else "w"
        context: IO[str] | nullcontext = nullcontext(filename)
        if filename != "sys.stdout":
            context = open(filename, mode)
        with context as f:
            if clear:
                f.seek(0)
                f.truncate()
            for row in self.grid:
                for cell in row:
                    value = getattr(cell, attribute)
                    if callable(value):
                        value = value()
                    print(value, file=f, end="")
                print(file=f)



def main() -> None:
    maze = Maze(5, 10)
    maze.show("hex", "hello.txt")
    maze.show("position", "hello.txt")


if __name__ == "__main__":
    main()
