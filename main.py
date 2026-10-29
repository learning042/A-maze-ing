from maze_gen import MazeGenerator, DFSGenerator, KruskalGenerator, AldousBroderGenerator
from maze import Maze
from render import render_maze
from parsing import build_config_dict
import os
import random
import subprocess
import sys

MAZE_ALGORITHMS = {
                    "DFS": DFSGenerator,
                    "KRUSKAL": KruskalGenerator,
                    "ALDOUS_BRODER": AldousBroderGenerator
                   }


def make_maze(config: dict[str, str | bool | int | tuple[int, int]],
              gen: MazeGenerator) -> Maze | None:
    try:
        maze = gen.creator(config["WIDTH"], config["HEIGHT"], config["EXIT"], has_42=True)
        if maze is None:
            return
        elif not config["PERFECT"]:
            maze.pacman()
        return maze
    except Exception as error:
        print(error)
        sys.exit(1)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python a_maze_ing.py config.txt")
        sys.exit(1)
    try:
        config = build_config_dict(sys.argv[1])
    except ValueError as e:
        print(e)
        sys.exit(1)
    except (OSError, UnicodeDecodeError):
        print(f"Error opening {sys.argv[1]}, exiting...")
        sys.exit(1)
    if "SEED" in config:
        random.seed(config["SEED"])
    if "ALGORITHM" in config:
        gen = MAZE_ALGORITHMS[config["ALGORITHM"]]()
    else:
        gen = MAZE_ALGORITHMS["DFS"]() 
    maze = make_maze(config, gen)
    if maze is None:
        print("Maze generation failed!")
        sys.exit(1)
    maze.show("hex", config["OUTPUT_FILE"])
    done = False
    show_path = False
    rgb_wall = (0, 130, 170)
    rgb_floor = (200, 200, 50)
    while not done:
        subprocess.run(["cls" if os.name == "nt" else "clear"])
        view = maze.get_graphical_view()
        print(render_maze(view, rgb_wall, rgb_floor, show_path))
        print("=== A-Maze-ing ===")
        choice = 0
        while (choice not in range(1, 5)):
            try:
                choice = int(input(
                            "1. Re-generate a new maze\n"
                            "2. Show / Hide the shortest path\n"
                            "3. Change the wall colours\n"
                            "4. Quit\n"
                            "Choice? (1-4): "))
            except ValueError:
                print("Please insert a valid number")
                continue
            except (KeyboardInterrupt, EOFError):
                choice = 4
            finally:
                print("\033[7F\033[0J")
        match choice:
            case 1:
                maze = make_maze(config, gen)
                if maze is None:
                    print("Maze generation failed, exiting...")
                    sys.exit(1)
                maze.show("hex", config["OUTPUT_FILE"])
            case 2:
                show_path = not show_path
            case 3:
                color = input("Select wall color\n"
                              "1. White\n"
                              "2. Blue\n"
                              "3. Green\n"
                              "4. Red\n")
            case 4:
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
