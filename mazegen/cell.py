from dataclasses import dataclass

from mazegen.direction import Direction


@dataclass
class Cell:
    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True
    locked: bool = False
    color: int = 0

    def set_wall(self, d: Direction, closed: bool) -> None:
        if d == Direction.N:
            self.north = closed
        elif d == Direction.E:
            self.east = closed
        elif d == Direction.S:
            self.south = closed
        else:
            self.west = closed

    def is_closed(self, d: Direction) -> bool:
        if d == Direction.N:
            return self.north
        if d == Direction.E:
            return self.east
        if d == Direction.S:
            return self.south
        return self.west

    def to_bits(self) -> str:
        bits = 0
        if self.north:
            bits |= 1  # 0001
        if self.east:
            bits |= 2  # 0010
        if self.south:
            bits |= 4  # 0100
        if self.west:
            bits |= 8  # 1000
        return format(bits, "x")

    def lock(self) -> None:
        self.locked = True

    def reset(self) -> None:
        if self.locked:
            return
        self.north = self.east = self.west = self.south = True
