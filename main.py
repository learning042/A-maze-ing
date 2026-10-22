from maze_gen import DFSGenerator
from maze import Maze
from render import render_maze
from solve_maze import solve_maze
from parsing import build_config_dict
import sys


def main() -> None:
    if len(sys.argv) > 2:
        sys.exit(1)
    config = build_config_dict()
    gen = DFSGenerator()
    try:
        maze = gen.creator(config["WIDTH"], config["HEIGHT"], config["EXIT"], has_42 = False)
    except Exception as error:
        print(error)
        sys.exit(1)
    if maze is None:
        return
    view = maze.get_graphical_view()
    print(render_maze(view, 0, 50, 255, 200, 200, 50))
    print(f"End: {maze.end}")
    currently = solve_maze(maze)
    print(f"currently: {currently.position()}")


def main2() -> None:
    gen = DFSGenerator()
    maze = gen.creator(10, 10, (9, 9))
    maze.show("hex", "output.txt")
    view = maze.get_graphical_view()
    print(render_maze(view, 0, 50, 255, 200, 200, 50))
    #print(view)
    #print(f"End: {maze.end}")
    #currently = solve_maze(maze)
    #print(f"currently: {currently.position()}")
    #while currently is not None:
    #    print(currently.position())
    #    currently = currently.parent
    #maze = Maze(20, 20, (0, 0))
    #print(maze.get_graphical_view())
    maze.pacman()
    maze.pacman2()
    maze.pacman3()
    view = maze.get_graphical_view()

    print(render_maze(view, 0, 50, 255, 200, 200, 50))

    maze.show("hex", "pacman.txt")


if __name__ == "__main__":
    main2()
