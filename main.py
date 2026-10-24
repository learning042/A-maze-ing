from maze_gen import MazeGenerator, DFSGenerator
from maze import Maze
from render import render_maze
from solve_maze import solve_maze
from parsing import build_config_dict
import os
import random
import subprocess
import sys


def make_maze(config: dict[str, str | bool | int | tuple[int, int]], gen: MazeGenerator) -> Maze | None:
    try:
        maze = gen.creator(config["WIDTH"], config["HEIGHT"], config["EXIT"], has_42=True)
        if not config["PERFECT"]:
            maze.pacman()
        return maze
    except Exception as error:
        print(error)
        sys.exit(1)
    if maze is None:
        return


def main() -> None:
    if len(sys.argv) > 2:
        sys.exit(1)
    try:
        config = build_config_dict(sys.argv[1])
    except Exception as e:
        print(e)
        sys.exit(1)
    if "SEED" in config:
        random.seed(config["SEED"])
    gen = DFSGenerator()
    maze = make_maze(config, gen)
    maze.show("hex", config["OUTPUT_FILE"])
    done = False
    while not done:
        subprocess.run(["cls" if os.name == "nt" else "clear"])
        view = maze.get_graphical_view()
        print(render_maze(view, 0, 50, 255, 200, 200, 50))
        #print(view)
        print("=== A-Maze-ing ===")
        choice = input(
            "1. Re-generate a new maze\n"
            "2. Show / Hide the shortest path\n"
            "3. Rotate the wall colours\n"
            "4. Quit\n"
            "Choice? (1-4): "
        )
        match choice:
            case "1":
                maze = make_maze(config, gen)
                maze.show("hex", config["OUTPUT_FILE"])
            case "4":
                print("Exiting...")
                done = True
            case _:
                print("Invalid choice. Try again...")



    #print(f"End: {maze.end}")
    #currently = solve_maze(maze)
    #print(f"currently: {currently.position()}")


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
    main()
