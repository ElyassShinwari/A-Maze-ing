*This project has been created as part of the 42 curriculum by ayafshar and eshinwar.*

# A-Maze-ing

A terminal-based maze generator and solver that creates perfect mazes with a distinctive "42" pattern in the middle. The project generates random mazes, finds the shortest path from entry to exit, and provides an interactive visualization with colorful rendering.

## Description

This maze generator creates procedurally generated mazes using the **Recursive Backtracker algorithm** (also known as Depth-First Search maze generation). The algorithm ensures that each maze is a perfect maze - meaning there is exactly one unique path between any two points in the maze, with no loops or inaccessible areas (unless configured otherwise).

The program draws a colored "42" logo in the center of the maze by locking specific cells, which the generator must work around. The maze can be visualized in the terminal with ASCII characters, and users can interact with it to regenerate mazes, toggle solution paths, and change wall colors.

## Instructions

### Installation

This project uses `uv` for dependency management. To install dependencies:

```bash
make install
```

Or manually:
```bash
uv sync --dev
```

### Running the Program

To run the interactive maze application:

```bash
make run
```

Or directly:
```bash
python3 a_maze_ing.py
```

### Configuration File Format

The maze behavior is controlled by a `config.txt` file in the root directory:

```
# Maze configuration
WIDTH=15           # Width of the maze (number of cells)
HEIGHT=10          # Height of the maze (number of cells)
ENTRY=0,0          # Entry coordinates (x,y)
EXIT=7,7           # Exit coordinates (x,y)
OUTPUT_FILE=maze.txt   # Output file name for the maze data
PERFECT=True       # True for perfect maze, False to add loops
```

- **WIDTH** and **HEIGHT**: Define the maze dimensions in cells
- **ENTRY** and **EXIT**: Coordinates (x,y) for start and end points
- **OUTPUT_FILE**: Name of the file where maze data is saved
- **PERFECT**: If `True`, generates a perfect maze; if `False`, adds some loops (~10% extra passages)

### Interactive Commands

Once the program is running, you can:

1. **Re-generate a new maze** - Creates a new random maze with a different seed
2. **Show/Hide path from entry to exit** - Toggle visualization of the shortest solution path (blue)
3. **Rotate maze colors** - Cycle through different wall color schemes (default, yellow, red, white)
4. **Quit** - Exit the program

### Building the Package

To build the reusable `mazegen` package:

```bash
uv build
```

This creates a `.whl` file in the `dist/` directory that can be installed with pip.

### Linting

To check code quality:

```bash
make lint        # Standard linting
make lint-strict # Strict mode with all checks
```

## Maze Generation Algorithm

### Algorithm: Recursive Backtracker (Depth-First Search)

The Recursive Backtracker is one of the most popular maze generation algorithms. It works by:

1. Starting at a random unlocked cell
2. Marking the current cell as visited
3. Randomly choosing an unvisited neighbor and carving a path to it
4. Moving to that neighbor and repeating
5. Backtracking when there are no unvisited neighbors
6. Continuing until all cells are visited

### Why This Algorithm?

I chose the Recursive Backtracker algorithm for several reasons:

- **Simplicity**: Easy to understand and implement, making the code maintainable
- **Perfect Mazes**: Naturally creates perfect mazes (one path between any two points)
- **Long Passages**: Creates mazes with long, winding corridors that are visually interesting
- **Efficient**: Fast generation even for large mazes
- **Stack-based**: No recursion limits since it uses an explicit stack

The algorithm also includes a custom enhancement to prevent wide corridors (3x3 open areas), making the mazes more challenging and visually appealing.

### Optional Loop Generation

When `PERFECT=False`, the generator adds approximately 10% additional passages after the initial generation, creating alternative paths and making the maze easier to solve.

## Code Reusability

### Reusable Module: `mazegen`

The entire maze generation, solving, and rendering logic is contained in the `mazegen` module, which includes:

- **`Maze`**: Core maze data structure with cells and walls
- **`Genarator`**: Maze generation using recursive backtracker
- **`Solver`**: Finds the shortest path using breadth-first search
- **`Renderer`**: Terminal-based visualization with colors
- **`Writer`**: Exports maze data to file format
- **`Config`**: Configuration management from file
- **`Cell`**: Individual cell with wall states and locking
- **`Direction`**: Enum for cardinal directions

### Using the Module

```python
from mazegen.config import Config
from mazegen.maze import Maze
from mazegen.generator import Genarator
from mazegen.solver import Solver
from mazegen.renderer import Renderer

# Load configuration
config = Config()
config.load("config.txt")

# Create and generate maze
maze = Maze(config)
generator = Genarator(maze)
generator.generate(seed=42)

# Solve and render
solver = Solver(maze)
solution = solver.solve()

renderer = Renderer(maze)
renderer.render(solution)
```

### Custom Parameters

You can also create mazes programmatically:

```python
config = Config()
config.width = 30
config.height = 20
config.entry = (0, 0)
config.exit = (29, 19)
config.perfect = True

maze = Maze(config)
generator = Genarator(maze)
generator.generate(seed=12345)

solver = Solver(maze)
solution = solver.solve()
```

### Accessing Generated Data

- **Maze structure**: Access cells via `maze.cells[y][x]`
- **Cell walls**: Check walls with `cell.north`, `cell.east`, `cell.south`, `cell.west` (boolean values)
- **Locked cells**: Check if a cell is part of the "42" pattern with `cell.locked`
- **Solution path**: The `solver.solve()` returns a list of `(x, y)` coordinates representing the shortest path
- **Export to file**: Use `Writer(maze).save(solution)` to save in the hexadecimal format specified in the subject

### Output File Format

The generated maze is saved in a compact hexadecimal format:

- First line: `WIDTH HEIGHT`
- Following lines: Each cell's walls encoded as a hex digit (N=1, E=2, S=4, W=8)
- After an empty line: entry coordinates, exit coordinates, and solution path (using N/E/S/W letters)

## Visual Features

### Color Scheme

- **Green (█)**: Entry point
- **Red (█)**: Exit point
- **Blue (█)**: Solution path when toggled
- **Cyan (▒)**: The digit "4" in the center
- **Magenta (▒)**: The digit "2" in the center
- **Wall colors**: Rotatable between default, yellow, red, and white

### The "42" Pattern

The program draws a "42" pattern in the middle of the maze using locked cells. The pattern requires at least an 8x6 maze to display properly. The "4" is rendered in cyan and the "2" in magenta, making them visually distinct and more aesthetically pleasing.

## Team and Project Management

### Team Members

- **ayafshar**: Co-developer - responsible for implementation, testing, and documentation
- **eshinwar**: Co-developer - responsible for implementation, testing, and documentation

### Planning and Evolution

**Initial Plan:**
- Day 1-2: Understand requirements and design data structures
- Day 3-4: Implement maze generation algorithm
- Day 5: Implement solver and file writer
- Day 6-7: Create interactive UI and renderer
- Day 8: Testing, refinement, and documentation

**Evolution:**
The project followed the plan closely, with additional time spent on:
- Preventing wide corridors (3x3 open areas) for better maze quality
- Fine-tuning the "42" pattern to look aesthetically pleasing
- Adding color differentiation between the digits "4" and "2"
- Ensuring proper handling of locked cells in the generator

### What Worked Well

- Clear separation of concerns (generator, solver, renderer, writer)
- Using dataclasses for clean, simple data structures
- The recursive backtracker algorithm was straightforward to implement
- The BFS solver reliably finds shortest paths
- Terminal rendering with ANSI colors provides good visual feedback
- Type hints throughout the codebase improved maintainability

### What Could Be Improved

- Could add animation during maze generation to show the algorithm in action
- Could support multiple generation algorithms (Prim's, Kruskal's, etc.)
- Could add more interactive features (manual solving, hints, step-by-step visualization)
- Could implement graphical rendering with MiniLibX as a bonus
- Could add unit tests for better code coverage

### Tools Used

- **uv**: Fast Python package manager for dependency management
- **flake8**: Code linting to maintain style consistency (PEP 8)
- **mypy**: Static type checking for better code quality and type safety
- **git**: Version control for tracking changes
- **Python 3+**: Programming language with modern type hints support

## Resources

### Classic References

- **Maze Generation Algorithms**: 
  - [Think Labyrinth - Maze Algorithms](http://www.astrolog.org/labyrnth/algrithm.htm)
  - [Jamis Buck's Maze Generation Series](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)
  - [Wikipedia: Maze Generation Algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
  
- **Graph Theory**:
  - Introduction to Algorithms (CLRS) - Chapter on Graph Algorithms and DFS
  - [Spanning Trees and Perfect Mazes](https://en.wikipedia.org/wiki/Spanning_tree)

- **Python Documentation**:
  - [Python Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
  - [Type Hints](https://docs.python.org/3/library/typing.html)
  - [Dataclasses](https://docs.python.org/3/library/dataclasses.html)

### AI Usage

AI tools were used for the following tasks:

- **Documentation**: AI assisted in structuring the README and explaining technical concepts clearly in an accessible way
- **Testing scenarios**: AI helped generate test cases for various maze configurations and edge cases (small mazes, entry/exit on borders, etc.)
- **Readme refactoring**: AI provided suggestions for improving readme structure and type annotations


## License

This project is part of the 42 curriculum and follows 42 school guidelines.
