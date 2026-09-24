from maze_gen import DFSGenerator


def main() -> None:
    gen = DFSGenerator()
    maze = gen.generator(5, 5)
    maze.print_maze()


if __name__ == "__main__":
    main()
