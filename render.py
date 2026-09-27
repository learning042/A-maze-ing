def colorize_string(
        text: str,
        red: int,
        green: int,
        blue: int,
        is_background: bool = False
	) -> None:
    red = red % 256
    green = green % 256
    blue = blue % 256
    return f"\033[{38 + is_background * 10};2;{red};{green};{blue}m{text}\033[0m"

def render_maze(
        maze_representation: str,
        red_wall: int,
        green_wall: int,
        blue_wall: int,
        red_floor: int,
        green_floor: int,
        blue_floor: int
	) -> str:
    result = ""
    for char in maze_representation:
        if char == " ":
            result += colorize_string(char, red_floor, green_floor, blue_floor, True)
        else:
            result += colorize_string(char, red_wall, green_wall, blue_wall)
    return result
