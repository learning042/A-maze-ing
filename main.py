from maze_gen import DFSGenerator
from render import colorize_string, render_maze
from solve_maze import solve_maze


def main() -> None:
    gen = DFSGenerator()
    maze = gen.generator(39, 39, (30, 19))
    maze.show("hex", "output_maze.txt")
    view = maze.get_graphical_view()
    print(render_maze(view, 0, 50, 255, 200, 200, 50))
    print(f"End: {maze.end}")
    currently = solve_maze(maze)
    print(f"currently: {currently.position()}")



if __name__ == "__main__":
    main()
