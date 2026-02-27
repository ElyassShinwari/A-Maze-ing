import os
import random

from mazegen.config import Config
from mazegen.maze import Maze
from mazegen.writer import Writer


def main():
    from mazegen.generator import Genarator
    from mazegen.renderer import Renderer
    from mazegen.solver import Solver

    try:
        config = Config()
        config.load("config.txt")

        maze = Maze(config)
        g = Genarator(maze)
        s = Solver(maze)
        w = Writer(maze)
        r = Renderer(maze)

        seed = 42
        show_solution = False

        g.generate(seed)
        solution = s.solve()
        w.save(solution)
        os.system("clear")
        r.render([])

        while True:

            print("\n=== A-Maze-ing ===")
            print("1) Re-generate a new maze")
            print("2) Show/Hide path from entry to exit")
            print("3) Rotate maze colors")
            print("4) Quit")
            if not maze.did_draw_42:
                print(
                    "\n\033[93mMaze size is too small"
                    " to draw the '42' in the middle\033[0m"
                )
            choice = input("Choice (1 - 4) ")

            if choice == "4":
                break

            if choice == "1":
                seed = random.randint(0, 999999)
                g.generate(seed)
                solution = s.solve()
                w.save(solution)
            elif choice == "2":
                show_solution = not show_solution
            elif choice == "3":
                r.rotate_colors()

            os.system("clear")
            r.render(solution if show_solution else [])

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
