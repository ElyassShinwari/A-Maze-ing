const CELL_SIZE = 40;
const WALL = 1;
const PATH = 0;

class Maze {
  constructor(cols, rows) {
    this.cols = cols;
    this.rows = rows;
    this.grid = [];
    this.generate();
  }

  generate() {
    // Initialize grid with all walls
    this.grid = Array.from({ length: this.rows * 2 + 1 }, () =>
      Array(this.cols * 2 + 1).fill(WALL)
    );

    const visited = Array.from({ length: this.rows }, () =>
      Array(this.cols).fill(false)
    );

    const stack = [];
    const startCol = 0;
    const startRow = 0;
    visited[startRow][startCol] = true;
    stack.push([startCol, startRow]);

    // Carve out starting cell
    this.grid[startRow * 2 + 1][startCol * 2 + 1] = PATH;

    while (stack.length > 0) {
      const [col, row] = stack[stack.length - 1];
      const neighbors = this.getUnvisitedNeighbors(col, row, visited);

      if (neighbors.length === 0) {
        stack.pop();
      } else {
        const [nc, nr] = neighbors[Math.floor(Math.random() * neighbors.length)];
        visited[nr][nc] = true;

        // Remove wall between current and neighbor
        const wallCol = col + nc + 1;
        const wallRow = row + nr + 1;
        this.grid[wallRow][wallCol] = PATH;
        // Carve neighbor cell
        this.grid[nr * 2 + 1][nc * 2 + 1] = PATH;

        stack.push([nc, nr]);
      }
    }

    // Carve entrance and exit
    this.grid[1][0] = PATH;
    this.grid[this.rows * 2 - 1][this.cols * 2] = PATH;
  }

  getUnvisitedNeighbors(col, row, visited) {
    const dirs = [
      [0, -1],
      [0, 1],
      [-1, 0],
      [1, 0],
    ];
    return dirs
      .map(([dc, dr]) => [col + dc, row + dr])
      .filter(
        ([nc, nr]) =>
          nc >= 0 &&
          nc < this.cols &&
          nr >= 0 &&
          nr < this.rows &&
          !visited[nr][nc]
      );
  }

  isWall(gridCol, gridRow) {
    if (
      gridRow < 0 ||
      gridRow >= this.grid.length ||
      gridCol < 0 ||
      gridCol >= this.grid[0].length
    ) {
      return true;
    }
    return this.grid[gridRow][gridCol] === WALL;
  }
}

class Game {
  constructor(canvasId, cols, rows) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.cols = cols;
    this.rows = rows;
    this.cellSize = CELL_SIZE;

    this.reset();

    document.addEventListener('keydown', (e) => this.handleKey(e));
    document.getElementById('btn-new').addEventListener('click', () => this.reset());
    document.getElementById('btn-solve').addEventListener('click', () => this.solve());
  }

  reset() {
    this.maze = new Maze(this.cols, this.rows);
    // Player position in grid coordinates (odd indices = cell centers)
    this.playerGridCol = 1;
    this.playerGridRow = 1;
    this.won = false;
    this.solutionPath = null;

    this.canvas.width = (this.cols * 2 + 1) * this.cellSize;
    this.canvas.height = (this.rows * 2 + 1) * this.cellSize;

    document.getElementById('message').textContent = '';
    this.draw();
  }

  handleKey(e) {
    if (this.won) return;

    const moves = {
      ArrowUp: [0, -2],
      ArrowDown: [0, 2],
      ArrowLeft: [-2, 0],
      ArrowRight: [2, 0],
      w: [0, -2],
      s: [0, 2],
      a: [-2, 0],
      d: [2, 0],
    };

    const move = moves[e.key];
    if (!move) return;
    e.preventDefault();

    const [dc, dr] = move;
    const newCol = this.playerGridCol + dc;
    const newRow = this.playerGridRow + dr;

    // Check wall between current and new position
    const wallCol = this.playerGridCol + dc / 2;
    const wallRow = this.playerGridRow + dr / 2;

    if (!this.maze.isWall(wallCol, wallRow) && !this.maze.isWall(newCol, newRow)) {
      this.playerGridCol = newCol;
      this.playerGridRow = newRow;
      this.solutionPath = null;
      this.checkWin();
      this.draw();
    }
  }

  checkWin() {
    if (
      this.playerGridCol === this.cols * 2 - 1 &&
      this.playerGridRow === this.rows * 2 - 1
    ) {
      this.won = true;
      document.getElementById('message').textContent = '🎉 You solved the maze!';
    }
  }

  solve() {
    if (this.won) return;
    const startCol = 1;
    const startRow = 1;
    const endCol = this.cols * 2 - 1;
    const endRow = this.rows * 2 - 1;

    // BFS on the grid
    const key = (c, r) => `${c},${r}`;
    const queue = [[startCol, startRow]];
    const visited = new Set([key(startCol, startRow)]);
    const parent = new Map();

    const dirs = [
      [0, -2],
      [0, 2],
      [-2, 0],
      [2, 0],
    ];

    let found = false;
    while (queue.length > 0) {
      const [col, row] = queue.shift();
      if (col === endCol && row === endRow) {
        found = true;
        break;
      }
      for (const [dc, dr] of dirs) {
        const nc = col + dc;
        const nr = row + dr;
        const wallCol = col + dc / 2;
        const wallRow = row + dr / 2;
        if (
          !this.maze.isWall(wallCol, wallRow) &&
          !this.maze.isWall(nc, nr) &&
          !visited.has(key(nc, nr))
        ) {
          visited.add(key(nc, nr));
          parent.set(key(nc, nr), [col, row]);
          queue.push([nc, nr]);
        }
      }
    }

    if (found) {
      const path = [];
      let cur = [endCol, endRow];
      while (cur) {
        path.unshift(cur);
        cur = parent.get(key(cur[0], cur[1]));
      }
      this.solutionPath = path;
      this.draw();
    }
  }

  draw() {
    const ctx = this.ctx;
    const cs = this.cellSize;
    const grid = this.maze.grid;

    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw maze
    for (let r = 0; r < grid.length; r++) {
      for (let c = 0; c < grid[r].length; c++) {
        if (grid[r][c] === WALL) {
          ctx.fillStyle = '#2c3e50';
        } else {
          ctx.fillStyle = '#ecf0f1';
        }
        ctx.fillRect(c * cs, r * cs, cs, cs);
      }
    }

    // Draw entrance and exit markers
    ctx.fillStyle = '#27ae60';
    ctx.fillRect(0, cs, cs, cs);
    ctx.fillStyle = '#e74c3c';
    ctx.fillRect(this.cols * 2 * cs, (this.rows * 2 - 1) * cs, cs, cs);

    // Draw solution path
    if (this.solutionPath) {
      ctx.fillStyle = 'rgba(241, 196, 15, 0.5)';
      for (const [col, row] of this.solutionPath) {
        ctx.fillRect(col * cs, row * cs, cs, cs);
      }
      // Fill connecting walls between path steps
      for (let i = 1; i < this.solutionPath.length; i++) {
        const [pc, pr] = this.solutionPath[i - 1];
        const [nc, nr] = this.solutionPath[i];
        const wc = (pc + nc) / 2;
        const wr = (pr + nr) / 2;
        ctx.fillRect(wc * cs, wr * cs, cs, cs);
      }
    }

    // Draw player
    const px = this.playerGridCol * cs + cs / 2;
    const py = this.playerGridRow * cs + cs / 2;
    const radius = cs * 0.35;

    ctx.beginPath();
    ctx.arc(px, py, radius, 0, Math.PI * 2);
    ctx.fillStyle = '#3498db';
    ctx.fill();
    ctx.strokeStyle = '#2980b9';
    ctx.lineWidth = 2;
    ctx.stroke();
  }
}

window.addEventListener('DOMContentLoaded', () => {
  new Game('maze-canvas', 15, 10);
});
