class Cell:
    """
    Defines a 2D cell which has properties like its position and which
    sides are open.

    Think about that as a square:
      ----
      |  |
      ----
    """
    def __init__(self, row: int, col: int) -> None:
        """
        Instantiate a new cell.

        Args:
            ----> column
            |
            v
            row

            self.row : row-position of the cell
            self.column : column-position of the cell

        """
        self.row = row
        self.col = col
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False
        self.is_42 = False

    def position(self) -> tuple[int, int]:
        return (self.row, self.col)

    def hex(self) -> str:
        return hex(self.north + 2*self.east + 4*self.south + 8*self.west)[2:]
