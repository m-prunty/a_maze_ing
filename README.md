*This project has been created as part of the 42 curriculum by sdeppe, maprunty

# A-Maze-ing

## Description

A-Maze-ing is a maze generation and visualization project that creates perfect and imperfect mazes using various graph-based algorithms. The project generates mazes of configurable dimensions, embeds ASCII art within the maze structure, and provides an interactive GUI to visualize maze generation and pathfinding algorithms in real-time.

### Goal

The primary goal of A-Maze-ing is to implement multiple maze generation and pathfinding algorithms, provide a configurable framework for comparing their performance and visual output, and deliver an engaging interactive visualization system using modern graphics libraries.

### Key Features

- **Multiple Maze Generation Algorithms**: DFS, Prim's Algorithm, Sidewinder, Wilson's Algorithm
- **Pathfinding**: Dijkstra's algorithm for finding optimal paths through generated mazes
- **Perfect & Imperfect Mazes**: Toggle between mazes with exactly one solution and mazes with multiple solutions
- **ASCII Art Embedding**: Embed 42 school logo or custom ASCII art within maze structure
- **Configurable Parameters**: Customize maze dimensions, entry/exit points, color schemes, output formats
- **Interactive GUI**: Real-time visualization of maze generation and pathfinding processes
- **File I/O**: Save and load mazes to/from files with complete reconstruction capability

## Instructions

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd amazing
   ```

2. **Install dependencies** (using uv package manager):
   ```bash
   make install
   ```
   
   This will install all project dependencies including:
   - `common`: Common utilities and grid tools
   - `graphics`: Graphics rendering engine using MLX
   - `mazegen`: Maze generation algorithms
   - `mlx`: Graphics library bindings (includes prebuilt wheel)

3. **Enter virtual environment** (if needed):
   ```bash
   source .venv/bin/activate
   ```

### Compilation & Execution

**Run the application**:
```bash
make run
```

Or directly:
```bash
python3 a_maze_ing.py [config.txt]
```

The application will:
1. Display a start screen with options
2. Allow configuration of maze parameters through the options menu
3. Generate maze on demand using the "Start" button
4. Display the generated maze with generation visualization
5. Show pathfinding animation when spacebar is pressed

**Debug mode**:
```bash
make debug
```

Launches the Python debugger (pdb) for debugging.

### Configuration File Format

Configuration is managed through `config.txt` with the following parameters:

```
WIDTH=17                # Maze width in cells (5-30)
HEIGHT=18               # Maze height in cells (5-30)
ENTRY=0,0               # Entry point coordinates (x,y)
EXIT=16,17              # Exit point coordinates (x,y)
OUTPUT_FILE=maze.txt    # Output file for maze data
PERFECT=False           # Perfect maze (True) or imperfect (False)
SEED=0                  # Random seed (0 for random)
WINDOW_SIZE=900,900     # Window dimensions in pixels
PIC=1                   # Picture selection: 0=custom, 1=medium, 2=large
PIC_SCALAR=3.0          # Scaling factor for embedded pictures
FILENAME=config.txt     # Configuration filename
COLOR=0                 # Color scheme (0=default)
GEN_ALGO=prim           # Generation algorithm: dfs|prim|swinder|wilson
PATH_ALGO=dijkstra      # Pathfinding algorithm: dfs|dijkstra
```

### Maintenance Commands

```bash
make clean              # Remove __pycache__, .mypy_cache, temporary files
make fclean             # Clean + remove virtual environment and dependencies
make lint               # Run flake8 and mypy type checking
make lint-strict        # Run linters with strict mypy settings
make build-mazegen      # Build mazegen library wheel
make dev                # Install with development dependencies
```

## Maze Generation Algorithms

### Selected Algorithm: Depth-First Search (DFS)

**Why DFS was chosen:**
- TODO: Document why DFS was selected as the primary generation algorithm
- Efficient implementation with linear time complexity
- Naturally creates long corridors which are aesthetically pleasing
- Simple recursive implementation suitable for animation/visualization

**Algorithm Overview:**
DFS-based maze generation creates a spanning tree of the grid by randomly carving passages. The algorithm starts from the entry point and recursively visits neighboring cells, carving passages between them. This naturally creates mazes with a single path from any cell to any other cell (perfect mazes).

**Implementation Details:**
- Located in: [libs/mazegen/mazegen/algos.py](libs/mazegen/mazegen/algos.py#L99-L140)
- Uses randomized edges for non-deterministic maze variations
- Supports event dispatching for animation stages (ENTER, EDGE, EXIT events)
- Can be made imperfect by carving additional random walls

### Other Implemented Algorithms

**Dijkstra's Algorithm** (Pathfinding):
- Single-source shortest path algorithm
- Finds optimal route from entry to exit
- Implemented at: [libs/mazegen/mazegen/algos.py](libs/mazegen/mazegen/algos.py#L155-L213)

**Prim's Algorithm** (In Development):
- Alternative maze generation using frontier expansion
- TODO: Complete implementation details when Prim is fully implemented
- Planned reference: https://en.wikipedia.org/wiki/Prim%27s_algorithm

**Sidewinder Algorithm** (Stubbed):
- TODO: Complete Sidewinder implementation and documentation

**Wilson's Algorithm** (Stubbed):
- TODO: Complete Wilson's implementation and documentation

## Reusable Components

The project is structured as a modular collection of libraries that can be reused independently:

### 1. **common Library**
**Location**: [libs/common/](libs/common/)

**Reusable Components**:
- `Grid`: Core grid data structure supporting arbitrary dimensions and cell operations
- `Cell`: Individual cell with wall/visited state tracking
- `Vec2`: 2D vector mathematics for coordinate operations
- `Direction`: Enumeration for cardinal directions with vector operations
- `Config`: Configuration management with validation and file I/O
- `ConfigIO`: File serialization/deserialization for configuration

**How to Use**:
```python
from common import Grid, Config, Vec2

# Create a 10x10 grid
grid = Grid(10, 10)
grid.fill_empty_grid()

# Access cells
cell = grid[Vec2(5, 5)]
cell.rm_wall(Dir.N)  # Remove north wall
```

### 2. **mazegen Library**
**Location**: [libs/mazegen/mazegen/](libs/mazegen/mazegen/)

**Reusable Components**:
- `MazeGenerator`: Unified interface for all maze generation algorithms
- `BaseStrat`: Abstract strategy class for implementing new algorithms
- `Graph` / `GridGraph` / `MazeGraph`: Graph representations of grid structures
- Individual algorithm classes: `Dfs`, `Prim`, `Sidewinder`, `Wilson`, `Dijkstra`

**How to Use**:
```python
from mazegen import MazeGenerator
from common import Grid, Config

grid = Grid(20, 20)
grid.fill_empty_grid()
config = Config()

generator = MazeGenerator(grid, config)
generator.gen_grid("dfs")  # Generate using DFS
generator.gen_path("dijkstra")  # Find path with Dijkstra
```

### 3. **graphics Library**
**Location**: [libs/graphics/graphics/](libs/graphics/graphics/)

**Reusable Components**:
- `Window`: Main window management with MLX backend
- `Renderer`: Low-level image and text rendering
- `Canvas`: Bitmap canvas with pixel drawing capabilities
- `Animator`: Animation frame sequencing and timing
- `Event_loop`: Event handling system with hooks
- `Textures`: Asset loading and caching system
- `Render_grid` / `Render_cell`: High-level maze rendering

**How to Use**:
```python
from graphics import Window, Renderer, Event_loop
from common import Vec2

# Create window
Window.create(Vec2(900, 900), "My App")

# Render text/images
Renderer.render_text("Hello", Vec2(400, 50))

# Add event hooks
Event_loop.add_key_hook(callback_function, None)
Event_loop.launch()
```

### 4. **mlx Library**
**Location**: [libs/mlx/python/](libs/mlx/python/)

A prebuilt Python binding for the MLX graphics library (C-based). Provides:
- Window creation and management
- Low-level pixel drawing
- Image loading (PNG, XPM formats)
- Event handling (keyboard, mouse, timing)

## Team & Project Management

### Team Members and Roles

TODO: Document each team member's login and role:
- TODO: login1 - Role/responsibilities
- TODO: login2 - Role/responsibilities
- TODO: login3 - Role/responsibilities (if applicable)

### Planning & Evolution

**Initial Planning**:
TODO: Describe the initial project plan and goals

**Evolution During Development**:
TODO: Document how the plan evolved as the project developed:
- Changes in algorithm selection
- Feature additions or removals
- Technical challenges encountered
- Pivots in approach

**Timeline**:
- Project Start: 2026/01/24
- Last Update: 2026/05/14

### What Worked Well

TODO: Document successful aspects:
- Architecture decisions that proved effective
- Algorithms that performed as expected
- Development practices that improved productivity
- Tools that enhanced workflow

### What Could Be Improved

TODO: Document limitations and improvement opportunities:
- Performance bottlenecks
- Code organization improvements
- Testing coverage gaps
- Algorithm implementation completions (Prim, Sidewinder, Wilson)
- UI/UX enhancements
- Documentation areas needing expansion

### Tools & Technologies Used

**Development Tools**:
- **uv**: Fast Python package manager (replacing pip)
- **flake8**: Linter with docstring checking (pydantic plugins)
- **mypy**: Static type checker with strict settings
- **pdb**: Python debugger for runtime debugging
- **make**: Task automation (install, run, lint, clean)

**Core Dependencies**:
- **pydantic**: Data validation and configuration management
- **mlx**: C-based graphics library with Python bindings
- **Python 3.11+**: Primary language runtime

**Project Structure Tools**:
- **uv workspaces**: Monorepo management with local library dependencies
- **setuptools**: Package building and distribution
- **pyproject.toml**: Modern Python project configuration

## Advanced Features

### Perfect vs. Imperfect Mazes

The `PERFECT` configuration parameter controls maze complexity:

- **Perfect Maze** (`PERFECT=True`): Exactly one path between any two cells. Algorithm generates a spanning tree.
- **Imperfect Maze** (`PERFECT=False`): Multiple paths exist. The algorithm carves additional random walls after creating the spanning tree, calculated as: `(width * height)^0.7`

### Color Schemes

Multiple visual themes available via `COLOR` parameter (values 0-2):
- TODO: Document each color scheme's visual characteristics
- TODO: Explain how color schemes are implemented in the graphics library

### Picture Embedding (ASCII Art)

Three predefined pictures can be embedded:
- **PIC=0**: Custom small pattern (5x7 bits)
- **PIC=1**: Medium 42 logo variant (5x24 bits)
- **PIC=2**: Large 42 logo variant (7x24 bits)

The `PIC_SCALAR` parameter scales the picture size. The algorithm:
1. Calculates optimal scaling to fit within 60% of maze dimensions
2. Centers the picture in the maze
3. Marks embedded cells as "ispic" (picture cells)
4. Adjusts entry/exit if they conflict with picture placement

### Visualization Stages

Maze generation is animated using an event-dispatching system with four stages:

1. **VisitStage**: Highlights cells as they are visited during generation
2. **RmStage**: Visually shows wall removal during generation
3. **PathStage**: Highlights cells discovered during pathfinding
4. **GoalStage**: Marks the exit cell

Each algorithm generates events: `ENTER` (cell visited), `EDGE` (passage carved), `EXIT` (backtrack)

### File Format

Mazes are persisted in a custom format with hexadecimal wall encoding:

```
<hex_row_1>
<hex_row_2>
...
<entry_x>,<entry_y>
<exit_x>,<exit_y>
<direction_sequence>
```

Each cell is encoded as a nibble (4 bits) with wall states:
- Bit 0: North wall
- Bit 1: East wall
- Bit 2: South wall
- Bit 3: West wall

The direction sequence encodes the path from entry to exit as: N/S/E/W characters

## Resources & References

### Maze Generation Theory
- [Maze Generation Algorithms - Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Depth-First Search - Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- [Prim's Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Prim%27s_algorithm)
- [Sidewinder Algorithm Guide](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Sidewinder)
- [Wilson's Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Wilson's_algorithm)

### Pathfinding Theory
- [Dijkstra's Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)

### Graphics & Visualization
- [MLX Graphics Library](https://github.com/codam-coding-school/MLX42) - Modern C graphics library

### Related Concepts
- [Graph Theory Fundamentals](https://en.wikipedia.org/wiki/Graph_theory)
- [Spanning Trees](https://en.wikipedia.org/wiki/Spanning_tree)
- [Event-Driven Architecture](https://en.wikipedia.org/wiki/Event-driven_architecture)

### Python & Development Tools
- [Pydantic Documentation](https://docs.pydantic.dev/) - Data validation
- [mypy Type Checking](https://www.mypy-lang.org/)
- [flake8 Linter](https://flake8.pycqa.org/)
- [uv Package Manager](https://docs.astral.sh/uv/)

## AI Usage

TODO: Specify which parts of the project utilized AI assistance:

- Generation algorithms implementation
- Graphics rendering pipeline
- TODO: Document any other AI-assisted components
- TODO: Describe specific tasks where AI was used and its effectiveness
- TODO: Note limitations encountered with AI assistance
- TODO: Specify which code sections were AI-generated vs. manually written

---

**Last Updated**: May 14, 2026  
**Repository**: [GitHub Link - TODO: Add repository URL]  
**Contact**: TODO: Add team contact information
