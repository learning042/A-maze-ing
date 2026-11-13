from maze_gen import (MazeGenerator,
                      DFSGenerator,
                      KruskalGenerator,
                      AldousBroderGenerator
                      )
from maze import Maze, COLORS
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


def make_maze(
            config: dict[str, str | bool | int | tuple[int, int]],
            gen: MazeGenerator,
            wcolor: tuple[int, int, int] = COLORS["yellow"],
            fcolor: tuple[int, int, int] = COLORS["blue"]
            ) -> Maze | None:
    try:
        maze = gen.creator(
                            config["WIDTH"],
                            config["HEIGHT"],
                            config["EXIT"],
                            wcolor=wcolor,
                            fcolor=fcolor,
                            has_42=True
                            )
        if maze is None:
            return
        elif not config["PERFECT"]:
            maze.pacman()
        return maze
    except Exception as error:
        print(error, file=sys.stderr)
        sys.exit(1)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)
    try:
        config = build_config_dict(sys.argv[1])
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except (OSError, UnicodeDecodeError):
        print(f"Error opening {sys.argv[1]}, exiting...", file=sys.stderr)
        sys.exit(1)
    if "SEED" in config:
        random.seed(config["SEED"])
    if "ALGORITHM" in config:
        gen = MAZE_ALGORITHMS[config["ALGORITHM"]]()
    else:
        gen = MAZE_ALGORITHMS["DFS"]()
    maze = make_maze(config, gen)
    if maze is None:
        print("Maze generation failed!", file=sys.stderr)
        sys.exit(1)
    maze.show("hex", config["OUTPUT_FILE"])
    done = False
    show_path = True
    while not done:
        subprocess.run(["cls" if os.name == "nt" else "clear"])
        view = maze.get_graphical_view()
        print(render_maze(view, maze.wcolor, maze.fcolor, show_path))
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
                print("Please insert a valid number", file=sys.stderr)
                continue
            except (KeyboardInterrupt, EOFError):
                choice = 4
            finally:
                print("\033[7F\033[0J")
        match choice:
            case 1:
                maze = make_maze(config, gen, maze.wcolor, maze.fcolor)
                if maze is None:
                    print("Maze generation failed, exiting...",
                          file=sys.stderr)
                    sys.exit(1)
                maze.show("hex", config["OUTPUT_FILE"])
            case 2:
                show_path = not show_path
            case 3:
                try:
                    color_wall = input(
                                  "Select wall color\n"
                                  "- Yellow\n"
                                  "- Orange\n"
                                  "- Purple\n"
                                  "- Cyan\n"
                                  "- Pink\n"
                                  "- Gray\n"
                                  "- Dark_gray\n"
                                  "- Black\n"
                                  "Choice: "
                                  ).lower()
                    color_floor = input(
                                  "Select floor color\n"
                                  "- Yellow\n"
                                  "- Orange\n"
                                  "- Purple\n"
                                  "- Cyan\n"
                                  "- Pink\n"
                                  "- Gray\n"
                                  "- Dark_gray\n"
                                  "- Black\n"
                                  "Choice: "
                                  ).lower()
                    maze.wcolor = COLORS[color_wall]
                    maze.fcolor = COLORS[color_floor]
                except (KeyboardInterrupt, EOFError):
                    pass
                except KeyError as error:
                    print(f"Invalid key: {error}")
            case 4:
                print("Exiting...")
                done = True
            case _:
                print("Invalid choice. Try again...", file=sys.stderr)


if __name__ == "__main__":
    main()
