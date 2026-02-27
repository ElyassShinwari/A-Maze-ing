import random
from typing import Set, Tuple

from mazegen.direction import Direction
from mazegen.maze import Maze


class Genarator:
    def __init__(self, maze: Maze):
        self.maze = maze

    def _random_unlocked_cell(self) -> Tuple[int, int]:
        x = random.randint(0, self.maze.config.width - 1)
        y = random.randint(0, self.maze.config.height - 1)
        while self.maze.cells[y][x].locked:
            x = random.randint(0, self.maze.config.width - 1)
            y = random.randint(0, self.maze.config.height - 1)
        return (x, y)

    def _would_create_wide_corridor(
        self, x: int, y: int, d: Direction
    ) -> bool:
        nx, ny = x + d.dx, y + d.dy

        # Normalize the carved wall to an E or S wall for consistent checking
        if d == Direction.E:
            carved = (x, y, Direction.E)
        elif d == Direction.W:
            carved = (nx, ny, Direction.E)
        elif d == Direction.S:
            carved = (x, y, Direction.S)
        else:
            carved = (nx, ny, Direction.S)

        # Check all 3x3 regions that contain both (x,y) and (nx,ny)
        tx_min = max(x, nx) - 2
        tx_max = min(x, nx)
        ty_min = max(y, ny) - 2
        ty_max = min(y, ny)

        for tx in range(tx_min, tx_max + 1):
            for ty in range(ty_min, ty_max + 1):
                if self._is_3x3_open(tx, ty, carved):
                    return True
        return False

    def _is_3x3_open(
        self,
        tx: int,
        ty: int,
        carved: Tuple[int, int, Direction],
    ) -> bool:
        """Check if 3x3 region at top-left (tx,ty) would be fully open,
        treating the carved wall as already open."""
        # Bounds check for all 9 cells
        for row in range(3):
            for col in range(3):
                if not self.maze.in_bounds(tx + col, ty + row):
                    return False

        # Check 6 east (horizontal) internal walls: cols 0-1, rows 0-2
        for row in range(3):
            for col in range(2):
                px, py = tx + col, ty + row
                if (px, py, Direction.E) == carved:
                    continue
                if self.maze.cells[py][px].is_closed(Direction.E):
                    return False

        # Check 6 south (vertical) internal walls: cols 0-2, rows 0-1
        for row in range(2):
            for col in range(3):
                px, py = tx + col, ty + row
                if (px, py, Direction.S) == carved:
                    continue
                if self.maze.cells[py][px].is_closed(Direction.S):
                    return False

        return True

    def _add_loops(self, visited: Set[Tuple[int, int]]):
        num_loops = int(len(visited) * 0.1)
        attempts = 0
        max_attempts = num_loops * 10

        while num_loops > 0 and attempts < max_attempts:
            attempts += 1
            x = random.randint(0, self.maze.config.width - 1)
            y = random.randint(0, self.maze.config.height - 1)

            if (x, y) not in visited or self.maze.cells[y][x].locked:
                continue

            neighbors = self.maze.neighbors(x, y)
            if not neighbors:
                continue

            d, nx, ny = random.choice(neighbors)
            if (nx, ny) in visited and not self.maze.cells[ny][nx].locked:
                if self.maze.cells[y][x].is_closed(d):
                    if not self._would_create_wide_corridor(x, y, d):
                        self.maze.carve(x, y, d)
                        num_loops -= 1

    def generate(self, seed: int):
        self.maze.reset()

        random.seed(seed)
        visited: Set[Tuple[int, int]] = set()

        start_x, start_y = self._random_unlocked_cell()
        stack = [(start_x, start_y)]
        visited.add((start_x, start_y))

        while stack:
            x, y = stack[-1]

            candidates = []
            for d, nx, ny in self.maze.neighbors(x, y):
                isLocked = self.maze.cells[ny][nx].locked
                if (nx, ny) not in visited and not isLocked:
                    if not self._would_create_wide_corridor(x, y, d):
                        candidates.append((d, nx, ny))

            if candidates:
                d, nx, ny = random.choice(candidates)
                self.maze.carve(x, y, d)
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        if not self.maze.config.perfect:
            self._add_loops(visited)
