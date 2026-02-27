from enum import Enum


class Direction(Enum):
    N = (0, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)

    @property
    def dx(self) -> int:
        return self.value[0]

    @property
    def dy(self) -> int:
        return self.value[1]

    @staticmethod
    def opposite(d: "Direction") -> "Direction":
        dirs = {
            Direction.N: Direction.S,
            Direction.S: Direction.N,
            Direction.E: Direction.W,
            Direction.W: Direction.E,
        }
        return dirs[d]
