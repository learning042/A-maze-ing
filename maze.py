from cell import Cell
from tuple_op import sum_tuples, subtract_tuples
from typing import IO
from render import colorize_string
import random
import sys
from contextlib import nullcontext

RESET = "\033[0m"
WALL_COLOR = "\033[38;2;200;200;220m"   # cinza claro / lavanda
START_COLOR = "\033[48;2;170;80;220m"   # roxo (fundo)
END_COLOR = "\033[48;2;220;60;90m"      # vermelho/rosa (fundo)


NORTH = (-1, 0)
EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)

DIRECTIONS = {
        "north": NORTH,
        "east": EAST,
        "south": SOUTH,
        "west": WEST
}


class Maze:
    """Defines the maze"""
    def __init__(self,
                 width: int,
                 height: int,
                 end: tuple[int, int],
                 start: tuple[int, int] = (0, 0)
                 ) -> None:
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
        self.grid = [
                     [Cell(row, col) for col in range(width)]
                     for row in range(height)
                     ]
        self.start = start
        self.end = end
        self.mark_visited(*self.start)

    def show(
        self,
        attribute: str,
        filename: str = "sys.stdout",
        clear: bool = False,
        append: bool = False
     ) -> None:
        
        from solve_maze import solve_maze
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
                    print(value, file=f, end="")
                print(file=f)
            print(f"\n{self.start[0]},{self.start[1]}", file=f)
            print(f"{self.end[0]},{self.end[1]}", file=f)
            print(solve_maze(self), file=f)

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
        return not_visited

    def return_available_moves(self, cell: Cell) -> list[Cell]:
        position = cell.position()
        not_visited: list[Cell] = []
        for direction in (NORTH, EAST, SOUTH, WEST):
            cell_position = sum_tuples(position, direction)
            if cell_position[0] < 0 or cell_position[1] < 0:
                continue
            try:
                neighbor = self.grid[cell_position[0]][cell_position[1]]
            except IndexError:
                continue
            key = next(k for k in DIRECTIONS.keys() if DIRECTIONS[k] == direction)
            if (not neighbor.visited and
                    not neighbor.is_42 and
                    not getattr(cell, key)):
                not_visited.append(neighbor)
        return not_visited

    def get_cell(self, row: int, column: int) -> Cell:
        return self.grid[row][column]

    def edit_wall(self, curr_cell: Cell, next_cell: Cell, state: bool) -> None:
        curr_pos = curr_cell.position()
        next_pos = next_cell.position()
        curr_cell.edit_wall_from_cell(subtract_tuples(next_pos, curr_pos), state)
        next_cell.edit_wall_from_cell(subtract_tuples(curr_pos, next_pos), state)

    def get_graphical_view(self) -> str:
        maze_representation = "██" + "█████" * self.width + "\n"
        for row in self.grid:
            row_raw = "██"
            for cell in row:
                position = cell.position()
                if cell.is_42:
                    row_raw += "###██"
                else:
                    if cell.east:
                        row_raw += "   ██"
                    elif self.get_cell(position[0], position[1] + 1).is_42:
                        row_raw += "   ##"
                    else:
                        row_raw += "     "
            maze_representation += row_raw + "\n"

            row_bottom = "██"
            for cell in row:
                if cell.south:
                    row_bottom += "█████"
                else:
                    position = cell.position()
                    try:
                        if (cell.east or
                                cell.south or
                                self.get_cell(position[0] + 1, position[1]).east or
                                self.get_cell(position[0], position[1] + 1).south):
                            row_bottom += "   ██"
                        else:
                            row_bottom += "     "
                    except IndexError:
                        row_bottom += "   ██"
            maze_representation += row_bottom + "\n"
        return maze_representation

    def add_42icon(self) -> None:
        icon = [
                "#   ###",
                "#     #",
                "### ###",
                "  # #  ",
                "  # ###",
                ]
        for row in range(5):
            for column in range(7):
                if icon[row][column] == "#":
                    self.get_cell(row + self.height // 2 - 2,
                                  column + self.width // 2 - 3).is_42 = True

    def turn_all_cells_unvisited(self) -> None:
        for row in self.grid:
            for cell in row:
                cell.visited = False

    def pacman(self) -> None:
        grid = self.grid
        for row in grid:
            for curr_cell in row:
                if curr_cell.is_deadend() and not curr_cell.is_42:
                    try:
                        neighbors = self.get_deadend_pos(curr_cell)
                        next_cell = random.choice(neighbors)
                        self.edit_wall(curr_cell, next_cell, False)
                    except IndexError:
                        continue
                    except StopIteration:
                        continue

    def pacman2(self) -> None:
        for i in range(self.height):
            for j in range(self.width):
                horizontal = 0
                try:
                    while (not self.get_cell(i, j + horizontal).east and
                           not self.get_cell(i, j + horizontal).south and
                           not self.get_cell(i + 1, j + horizontal).east and
                           not self.get_cell(i, j + horizontal + 1).south):
                        horizontal += 1
                except IndexError:
                    break
                if horizontal > 1:
                    for k in range(1, horizontal):
                        self.edit_wall(self.get_cell(i, j + k),
                                       self.get_cell(i + 1, j + k),
                                       True)

    def pacman3(self) -> None:
        for j in range(self.width):
            for i in range(self.height):
                vertical = 0
                try:
                    while (not self.get_cell(i + vertical, j).east and
                           not self.get_cell(i + vertical, j).south and
                           not self.get_cell(i + vertical, j + 1).south and
                           not self.get_cell(i + vertical + 1, j).east):
                        vertical += 1
                except IndexError:
                    break
                if vertical > 1:
                    for k in range(1, vertical):
                        self.edit_wall(self.get_cell(i + k, j),
                                       self.get_cell(i + k, j + 1),
                                       True)


    def get_deadend_pos(self, cell: Cell) -> list[Cell]:
        position = cell.position()
        deadends: list[Cell] = []
        for direction in DIRECTIONS.keys():
            cell_position = sum_tuples(position, DIRECTIONS[direction])
            if cell_position[0] < 0 or cell_position[1] < 0:
                continue
            try:
                adj_cell = self.get_cell(*cell_position)
            except IndexError:
                continue
            if getattr(cell, direction) and not adj_cell.is_42:
                deadends.append(adj_cell)
        return deadends






def main2() -> None:
    maze = Maze(5, 5, (4, 4))
    #maze.print_maze()
    print()
    #curr = maze.get_cell(3, 4)
    #next = maze.get_cell(3, 3)
    #maze.edit_wall(curr, next, False)

    maze.edit_wall(maze.get_cell(0, 0), maze.get_cell(0, 1), False)
    maze.edit_wall(maze.get_cell(0, 0), maze.get_cell(1, 0), False)
    maze.edit_wall(maze.get_cell(0, 1), maze.get_cell(1, 1), False)
    maze.edit_wall(maze.get_cell(1, 0), maze.get_cell(1, 1), False)
    #maze.edit_wall(maze.get_cell(0, 1), maze.get_cell(0, 2), False)
    #maze.edit_wall(maze.get_cell(1, 1), maze.get_cell(1, 2), False)
    #maze.edit_wall(maze.get_cell(0, 2), maze.get_cell(1, 2), False)

    maze.edit_wall(maze.get_cell(1, 0), maze.get_cell(2, 0), False)
    maze.edit_wall(maze.get_cell(1, 1), maze.get_cell(2, 1), False)
    maze.edit_wall(maze.get_cell(2, 0), maze.get_cell(2, 1), False)

    view = maze.get_graphical_view()
    print(view)
    maze.pacman3()
    view = maze.get_graphical_view()
    print(view)

    #maze.edit_wall(curr, next, True)
    #view = maze.get_graphical_view()
    #print(view)

def main() -> None:
    from maze_gen import DFSGenerator
    gen = DFSGenerator()#####
    maze = gen.generator(10, 10)
    maze.print_maze()


if __name__ == "__main__":
    main2()
