from cell import Cell
from tuple_op import sum_tuples, subtract_tuples
from typing import Any, TextIO, IO
import sys
import os
from contextlib import nullcontext
from cursor import sum_tuples


NORTH = (0, -1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)


class Maze:
    """Defines the maze"""
    def __init__(self, width: int, height: int, start: tuple[int, int] = (0, 0)) -> None:
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
        self.start = start
        self.mark_visited(*self.start)

    def show(
    self,
    attribute: str,
    filename: str = "sys.stdout",
    clear: bool = False,
    append: bool = False
 ) -> None:
        mode = "a" if append else "w"
        context: IO[str] | nullcontext = nullcontext(sys.stdout)
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
                    print(value, file=f, end=" ")
                print(file=f)

    def mark_visited(self, row: int, column: int) -> None:
        cell = self.grid[row][column]
        cell.mark_visited()

    def return_available_cells_around(self, row: int, column: int) -> list[Cell]:
        """Return the available(not visited and possible to visit) cells around the cursor."""
        position = (row, column)
        not_visited: list[Cell] = []
        for direction in (NORTH, EAST, SOUTH, WEST):
            cell_position = sum_tuples(position, direction)
            if cell_position[0] < 0 or cell_position[1] < 0:
                continue
            cell = self.grid[cell_position[0]][cell_position[1]]
            if not cell.visited and not cell.is_42:
                not_visited.append(cell)
        #nv = [n.position() for n in not_visited]
        #print(f"not_visited {nv}")
        return not_visited

    def get_cell(self, row: int, column: int) -> Cell:
        return self.grid[row][column]

    def break_walls(self, head_pos: tuple[int, int], tail_pos: tuple[int, int]) -> None:
        head = self.get_cell(*head_pos)
        tail = self.get_cell(*tail_pos)
        head.break_wall(subtract_tuples(head_pos, tail_pos))
        tail.break_wall(subtract_tuples(tail_pos, head_pos))

    def print_maze(self) -> None:
        for row in self.grid:
            for cell in row:
                if cell.north:
                    print("###", end="")
            print("#")
            for cell in row:
                if cell.west:
                    print("#", end="")
                else:
                    print(" ", end="")
                print("  ", end="")
            print("#")
        for _ in range(self.width):
            print("###", end="")
        print("#")

            


                



def main() -> None:
    maze = Maze(20, 15)
    #around = maze.grid
    #for lista in around:
    #    for cell in lista:
    #        print(cell.position())
    maze.show("position")
    around = maze.return_available_cells_around(5, 2)
    for cell in around:
        print(cell.position())
    head = maze.get_cell(5, 1)
    tail = maze.get_cell(5, 2)
    print(head.north)
    print(tail.south)
    maze.break_walls((5, 1), (5, 2))
    print(head.north)
    print(tail.south)
    maze.print_maze()


if __name__ == "__main__":
    main()
