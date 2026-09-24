def sum_tuples(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
    """Add the coordinates of one tuple to the other."""
    return (p1[0] + p2[0], p1[1] + p2[1])


def subtract_tuples(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
    """Subtract the coordinates of one tuple to the other."""
    return (p1[0] - p2[0], p1[1] - p2[1])

def calculate_distance(p1: tuple[int, int], p2: tuple[int, int] = (0, 0)) -> float:
    """
    Calculate the distance between two points. 
    If p2 is not specified It is considered
    the distance between p1 and the origin
    """
    return (
        sqrt(
            (p1[0] - p2[0]) ** 2 +
            (p1[1] - p2[1]) ** 2
            )
        )
