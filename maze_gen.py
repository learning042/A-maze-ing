from cell import Cell
from maze import Maze
from abc import ABC, abstractmethod


class MazeGenerator(ABC):
    @abstractmethod
    def generator() -> Maze:
        ...


class DfsGenerator(MazeGenerator):
    def generator() -> Maze:
        ...
        # 1 Set Start
        # 2 WALK opening not-visited cells
        # 3 IF NOT AVAILABLE cells around
        # 4    GO back to step 2 in previous visited point
        # 5 ELIF not-visited cells AVAILABLE
        # 6    STOP
        
