from cell import Cell
from tuple_op import sum_tuples, subtract_tuples
from typing import Any, TextIO, IO
import sys
from contextlib import nullcontext


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

    def return_available_neighbors(self, cell: Cell) -> list[Cell]:
        """Return the available (not visited and possible to visit) cells around the cursor."""
        position = cell.position()
        not_visited: list[Cell] = []
        for direction in (NORTH, EAST, SOUTH, WEST):
            cell_position = sum_tuples(position, direction)
            if cell_position[0] < 0 or cell_position[1] < 0:
                continue
            try:
                cell = self.grid[cell_position[0]][cell_position[1]]
            except IndexError:
                continue
            if not cell.visited and not cell.is_42:
                not_visited.append(cell)
        #nv = [n.position() for n in not_visited]
        #print(f"not_visited {nv}")
        return not_visited

    def get_cell(self, row: int, column: int) -> Cell:
        return self.grid[row][column]

    def break_wall(self, curr_cell: Cell, next_cell: Cell) -> None:
        curr_pos = curr_cell.position()
        next_pos = next_cell.position()
        curr_cell.break_wall_from_cell(subtract_tuples(curr_pos, next_pos))
        next_cell.break_wall_from_cell(subtract_tuples(next_pos, curr_pos))

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
    maze = Maze(5, 5)
    maze.print_maze()
    print()
    curr = maze.get_cell(3, 4)
    next = maze.get_cell(3, 3)
    maze.break_wall(curr, next)
    print(curr.east)
    maze.print_maze()


if __name__ == "__main__":
    main()
