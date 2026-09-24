from maze import Maze
from abc import ABC, abstractmethod
import random


class MazeGenerator(ABC):
    @abstractmethod
    def generator(self, width: int, height: int, start: tuple[int, int] = (0, 0)) -> Maze:
        ...


class DFSGenerator(MazeGenerator):
    def generator(self, width: int, height: int, start: tuple[int, int] = (0, 0)) -> Maze:
        maze = Maze(width, height, start)
        stack = [maze.get_cell(*start)]  # 1 Set Start
        while stack:
            current = stack[-1]
            print(current.position())
            neighbors = maze.return_available_neighbors(current)
            if not neighbors:
                stack.pop()
            else:
                next = random.choice(neighbors)
                next.mark_visited()
                maze.break_wall(current, next)
                stack.append(next)
        return maze
        # 2 WALK opening not-visited cells
        # 3 IF NOT AVAILABLE cells around
        # 4    GO back to step 2 in previous visited point
        # 5 ELIF not-visited cells AVAILABLE
        # 6    STOP
