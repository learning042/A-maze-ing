from maze_gen import DFSGenerator


def main() -> None:
    gen = DFSGenerator()
    maze = gen.generator(15, 15)
    maze.show("hex", "output_maze.txt")
    maze.print_maze()


if __name__ == "__main__":
    main()
