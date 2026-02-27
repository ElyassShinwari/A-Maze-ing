from collections import deque
from typing import Dict, List, Optional

from mazegen.config import Coord
from mazegen.maze import Maze


class Solver:
    def __init__(self, maze: Maze):
        self.maze = maze

    def solve(self) -> List[Coord]:
        queue = deque([self.maze.config.entry])
        visited = {self.maze.config.entry}
        parent: Dict[Coord, Optional[Coord]] = {self.maze.config.entry: None}

        while queue:
            current = queue.popleft()

            if current == self.maze.config.exit:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                path.reverse()
                return path

            x, y = current
            for d, nx, ny in self.maze.neighbors(x, y):
                neighbor = (nx, ny)
                cell = self.maze.cells[y][x]
                if neighbor not in visited and not cell.is_closed(d):
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        return []
