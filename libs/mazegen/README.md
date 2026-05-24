# mazegen

**A robust, extensible Python library for maze generation and pathfinding, supporting multiple algorithms and event-dispatch-based extensibility.**

---

## Overview

`mazegen` is a standalone, type-safe, and extensible maze generation toolkit written in Python. It is designed for reusability and integration—serving as the generation engine for projects like *A-Maze-ing*, and for any future project requiring advanced maze logic, animation hooks, or graph algorithms.

---

## Features

- Five fully supported maze generation algorithms
- Deterministic output with random seeding
- Type-safe, Pydantic-based configuration and validation
- Pluggable architecture: easily add new algorithms/events
- Complete API for grid and cell access
- Full pytest test suite (`make test`)
- Clean Makefile for build, test, lint, clean

---

## Supported Algorithms

**Maze Generation Algorithms** (selectable via config):
- **dfs**: Depth-First Search (classic recursive backtracker)
- **prim**: Prim's Algorithm (randomized MST)
- **kruskal**: Kruskal's Algorithm (union-find)
- **swinder**: Sidewinder (row-wise sweep, horizontal corridors bias)
- **wilson**: Wilson's Algorithm (loop-erased random walk)

**Pathfinding Algorithm**:
- **dijkstra**: Dijkstra's algorithm for shortest path (entry ↔ exit)

All algorithms share a common event/stage/dispatch model enabling animation, visualization, and clean extensibility.

---

## Installation

**In the `libs/mazegen/` directory:**
```bash
# Install development dependencies and tools
make dev

# Build a distributable wheel (creates dist/mazegen-*.whl)
make build

# Install the built package locally (for development or usage)
pip install dist/mazegen-*.whl
# or, for immediate usage/edit/dev:
pip install -e .
```

---

## Running Tests

```bash
make test
```

---

## Clean-up

```bash
make clean
# To remove all build and venv artifacts:
make fclean
```

---

## Quick Usage Example

```python
from mazegen import MazeGenerator, Config, Grid

cfg = Config(width=12, height=12, entry=(0,0), exit=(11,11), gen_algo="kruskal")

grid = Grid(cfg.width, cfg.height)
mg = MazeGenerator(grid, cfg)

mg.gen_grid(cfg.gen_algo)   # Generate a maze with selected algorithm
mg.gen_path(cfg.path_algo)  # (Optional) Find shortest path (Dijkstra)

print(grid)         # Grid/wall output
```

All config parameters are type-checked, with detailed errors if misconfigured.

---

## Configuration

| Name        | Type         | Description                       | Example      |
|-------------|--------------|-----------------------------------|--------------|
| `width`     | int          | Maze width (cells)                | 10           |
| `height`    | int          | Maze height (cells)               | 10           |
| `entry`     | tuple[int]   | Entry coordinates                  | (0, 0)       |
| `exit`      | tuple[int]   | Exit coordinates                   | (9, 9)       |
| `output_file` | str        | Write output file for grid         | "maze.txt"   |
| `perfect`   | bool         | If true, guarantees single path    | True         |
| `seed`      | int          | Random seed (for reproducibility)  | 42           |
| `gen_algo`  | str          | Algorithm: dfs, prim, kruskal, swinder, wilson | "dfs" |
| `path_algo` | str          | Pathfinding: dijkstra             | "dijkstra"   |
| ...         | ...          | See in-code docstrings for more    |              |

All values are validated with descriptive errors.

---

## Event-Dispatch Algorithm Model

All algorithms in mazegen are implemented as event-driven strategies. This model means:

- **Algorithms yield events (cell visit, wall removal, etc.)** instead of just mutating state.
- **Stage handlers** are registered (such as VisitStage, PathStage, RmStage) and process these events, allowing for extensible logic, visualization, and animation.
- **Custom stages** (implemented as Protocol) can be inserted for logging, metric collection, or stepwise GUI animation, without modifying the core algorithm code.

*This design makes adding features, debugging, and interactive visualization simple and robust.*

---

## Error Handling

- Rich, custom error types for configuration, grid, or algorithm issues
- Example:
    ```python
    from mazegen.errors import ConfigError, MazeError

    try:
        ...
    except ConfigError as e:
        print("Config issue:", e)
    except MazeError as e:
        print("Maze runtime error:", e)
    ```

---

## Development

- Extend by subclassing `BaseStrat` or registering new stage/event handlers.
- Add new algorithms by adding to `registry.py` and using dispatch for ENTRY, EDGE, EXIT events.
- See the `algos.py` and docstrings for examples of how to implement new strategies.

---

