from typing import Tuple

Coord = Tuple[int, int]


class Config:
    def __init__(self):
        self.width: int = 20
        self.height: int = 15
        self.entry: Coord = (0, 0)
        self.exit: Coord = (19, 14)
        self.output_file: str = "maze.txt"
        self.perfect: bool = True

    def load(self, address: str) -> None:
        with open(address, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                if key == "WIDTH":
                    self.width = int(value)
                elif key == "HEIGHT":
                    self.height = int(value)
                elif key == "ENTRY":
                    x, y = value.split(",")
                    self.entry = (int(x), int(y))
                elif key == "EXIT":
                    x, y = value.split(",")
                    self.exit = (int(x), int(y))
                elif key == "OUTPUT_FILE":
                    self.output_file = value
                elif key == "PERFECT":
                    self.perfect = value.lower() == "true"
