from maze import Maze, NORTH, EAST, SOUTH, WEST
from abc import ABC, abstractmethod
from collections.abc import Generator
from cell import Cell
from disjoint_set import DisjointSet
from tuple_op import sum_tuples

import random
import time
import os
import subprocess
import sys


class MazeGenerator(ABC):
    @abstractmethod
    def generator(self,
                  maze: Maze,
                  ) -> Generator[Maze, None, Maze]:
        ...

    def creator(self,
                width: int,
                height: int,
                end: tuple[int, int],
                start: tuple[int, int] = (0, 0),
                has_42: bool = True,
                frame_duration: float = 0.001
                ) -> Maze | None:
        if width == 0 and height == 0:
            return None
        maze = Maze(width, height, end, start)
        if has_42:
            if width < 9 or height < 6:
                del maze
                raise ValueError("Invalid maze size.")
            maze.add_42icon()
        # limpa uma vez e esconde o cursor
        sys.stdout.write("\033[2J\033[?25l")
        for snapshot in self.generator(maze):
            frame = snapshot.get_graphical_view().replace("\n", "\n\r")
            print("\033[H" + frame)
            time.sleep(frame_duration)
        print("\033[?25h\n")
        subprocess.run(["cls" if os.name == "nt" else "clear"])
        print(width)
        print(height)
        maze.turn_all_cells_unvisited()
        return maze


class DFSGenerator(MazeGenerator):
    def generator(self,
                  maze: Maze,
                  ) -> Generator[Maze, None, Maze]:
        stack = [maze.get_cell(*maze.start)]
        while stack:
            current = stack[-1]
            neighbors = maze.return_available_neighbors(current)
            if not neighbors:
                stack.pop()
            else:
                next = random.choice(neighbors)
                next.mark_visited()
                maze.edit_wall(current, next, False)
                stack.append(next)
            yield maze
        return maze


class KruskalGenerator(MazeGenerator):
    def generator(self,
                  maze: Maze
                  ) -> Generator[Maze, None, Maze]:
        cell_set = DisjointSet([cell for row in maze.grid for cell in row])
        walls = [[cell, neighbour] for row in maze.grid for cell in row for neighbour in maze.return_available_neighbors(cell) if
                 (cell.row < neighbour.row) or (cell.row == neighbour.row and cell.col < neighbour.col)]
        while walls:
            random_wall = walls.pop(random.randrange(len(walls)))
            cell1, cell2 = random_wall
            if not cell1.is_42 and not cell2.is_42 and cell_set.find(cell1) != cell_set.find(cell2):
                maze.edit_wall(cell1, cell2, False)
                cell_set.union(cell1, cell2)
                yield maze
        return maze


class AldousBroderGenerator(MazeGenerator):
    def generator(self,
                  maze: Maze) -> Generator[Maze, None, Maze]:
        maze.turn_all_cells_unvisited()
        curr = maze.get_cell(*maze.start)
        curr.mark_visited()
        while any([not cell.visited and not cell.is_42 for row in maze.grid for cell in row]):
            position = curr.position()
            neighbors: list[Cell] = []
            for direction in (NORTH, EAST, SOUTH, WEST):
                cell_position = sum_tuples(position, direction)
                if cell_position[0] < 0 or cell_position[1] < 0:
                    continue
                try:
                    cell = maze.grid[cell_position[0]][cell_position[1]]
                except IndexError:
                    continue
                if not cell.is_42:
                    neighbors.append(cell)
            next = random.choice(neighbors)
            if not next.visited:
                maze.edit_wall(curr, next, False)
                next.mark_visited()
            curr = next
            yield maze
        return maze
