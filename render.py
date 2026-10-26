def colorize_string(
        text: str,
        red: int,
        green: int,
        blue: int,
        is_background: bool = False
        ) -> str:
    red = red % 256
    green = green % 256
    blue = blue % 256
    return f"\033[{38 + is_background * 10};2;{red};{green};{blue}m{text}\033[0m"


def render_maze(
        maze_representation: str,
        rgb_wall: tuple[int, int, int],
        rgb_floor: tuple[int, int, int],
        show_maze: bool = False
        ) -> str:
    result = ""
    red_wall, green_wall, blue_wall = rgb_wall
    red_floor, green_floor, blue_floor = rgb_floor
    for char in maze_representation:
        if char == " " or (char == "-" and not show_maze):
            result += colorize_string(" ", red_floor, green_floor, blue_floor, True)
        elif char == "-":
            result += colorize_string("█", red_floor - 70, green_floor - 10, blue_floor - 50)
        elif char == "#":
            result += colorize_string("█", red_wall - 20, green_wall - 20, blue_wall - 20)
        elif char == "s":
            result += colorize_string(" ", red_floor - 30, green_floor + 30, blue_floor + 50, True)
        elif char == "e":
            result += colorize_string(" ", red_floor + 70, green_floor - 100, blue_floor - 30, True)
        else:
            result += colorize_string(char, red_wall, green_wall, blue_wall)
    return result
