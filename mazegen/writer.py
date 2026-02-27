from typing import List

from mazegen.config import Coord
from mazegen.maze import Maze


class Writer:
    def __init__(self, maze: Maze):
        self.maze = maze

    def save(self, solution: List[Coord]) -> None:
        with open(self.maze.config.output_file, "w") as f:
            for y in range(self.maze.config.height):
                row_bits = []
                for x in range(self.maze.config.width):
                    row_bits.append(self.maze.cells[y][x].to_bits())
                f.write("".join(row_bits) + "\n")

            f.write("\n")

            ex, ey = self.maze.config.entry
            f.write(f"{ex} {ey}\n")

            tx, ty = self.maze.config.exit
            f.write(f"{tx} {ty}\n")

            directions = []
            for i in range(len(solution) - 1):
                cx, cy = solution[i]
                nx, ny = solution[i + 1]
                dx, dy = nx - cx, ny - cy
                if dx == 1:
                    directions.append("E")
                elif dx == -1:
                    directions.append("W")
                elif dy == 1:
                    directions.append("S")
                else:
                    directions.append("N")
            f.write("".join(directions) + "\n")
