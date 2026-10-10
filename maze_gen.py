from maze import Maze
from abc import ABC, abstractmethod
from collections.abc import Generator
import random
import time
import os
import sys

class MazeGenerator(ABC):
    @abstractmethod
    def generator(self, maze: Maze, stack: list[Cell]) -> Generator[Maze, None, Maze]:
        ...

    @abstractmethod
    def creator(self, width: int, height: int, start: tuple[int, int] = (0, 0)) -> Maze:
        ...


class DFSGenerator(MazeGenerator):
    def generator(self, maze: Maze, stack: list[Cell]) -> Generator[Maze, None, Maze]: 
        while stack:
            current = stack[-1]
            neighbors = maze.return_available_neighbors(current)
            if not neighbors:
                stack.pop()
            else:
                next = random.choice(neighbors)
                next.mark_visited()
                maze.break_wall(current, next)
                stack.append(next)
            yield maze
        return maze
        
        
    def creator(self, width: int, height: int, end: tuple[int, int], start: tuple[int, int] = (0, 0), has_42: bool = True) -> Maze:
        maze = Maze(width, height, end, start)
        if has_42:
            if width < 9 or height < 6:
            	del maze
            	raise ValueError("Invalid maze size.")
            maze.add_42icon()
        stack = [maze.get_cell(*start)]
        sys.stdout.write("\033[2J\033[?25l")  # limpa uma vez e esconde o cursor
        for snapshot in self.generator(maze, stack):
            frame = snapshot.get_graphical_view().replace("\n", "\n\r")
            print("\033[H" + frame)
            time.sleep(0.001)
        print("\033[?25h\n")
        os.system("cls" if os.name == "nt" else "clear")
        print(width)
        print(height)
        maze.turn_all_cells_unvisited()
        return maze
