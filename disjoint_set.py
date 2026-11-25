from typing import Any


class DisjointSet:
    def __init__(self, list: list) -> None:
        self.parents = {x: x for x in list}

    def find(self, x: Any) -> Any:
        if self.parents[x] == x:
            return x
        return self.find(self.parents[x])

    def union(self, x: Any, y: Any) -> None:
        x_rep = self.find(x)
        y_rep = self.find(y)
        self.parents[y_rep] = x_rep
