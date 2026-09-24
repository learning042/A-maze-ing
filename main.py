from maze_gen import DFSGenerator


def main() -> None:
    gen = DFSGenerator()
    maze = gen.generator(5, 5)
    maze.show("hex", "output_maze.txt")


if __name__ == "__main__":
    main()
