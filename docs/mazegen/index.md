Module mazegen
==============
A-Maze-ing is a maze generation and pathfinding visualization project.

Sub-modules
-----------
* mazegen.algos
* mazegen.config
* mazegen.errors
* mazegen.graph
* mazegen.grid_tools
* mazegen.mazegenerator
* mazegen.staging

Classes
-------

`Cell(loc: mazegen.grid_tools.vector.Vec2)`
:   Cell class has a location and a wall attribute.
    
    The wall is a 4-bit represantaion. i.e
    0000 has all walls
    0100 has one opening to south
    Args:
        loc (Vec2): The location of the cell in the grid.
    
    Returns:
        int: Product of a and b.
    
    Init a cell with a Vec2 location and all walls.

    ### Class variables

    `E`
    :

    `N`
    :

    `S`
    :

    `W`
    :

    ### Instance variables

    `loc: mazegen.grid_tools.vector.Vec2`
    :   Return the location of a Cell instance as a Vec2.

    `visited: bool`
    :   Return the visited status of a Cell instance.

    ### Methods

    `add_wall(self, direction: mazegen.grid_tools.cell.Dir) ‑> None`
    :   Add a wall in the given direction.

    `debug(self) ‑> str`
    :   Debug string representation of a Cell instance.

    `has_wall(self, direction: mazegen.grid_tools.cell.Dir) ‑> mazegen.grid_tools.cell.Dir`
    :   Check if a wall exists in the given direction.

    `rm_wall(self, direction: mazegen.grid_tools.cell.Dir) ‑> None`
    :   Remove a wall in the given direction.

`Config(**data: Any)`
:   Configuration class for maze generation and rendering.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Class variables

    `color: Literal[0, 1, 2]`
    :

    `entry: mazegen.grid_tools.vector.Vec2`
    :

    `exit: mazegen.grid_tools.vector.Vec2`
    :

    `filename: str`
    :

    `gen_algo: Literal['dfs', 'prim', 'swinder', 'wilson', 'dijkstra']`
    :

    `height: int`
    :

    `model_config`
    :

    `output_file: str`
    :

    `path_algo: Literal['dfs', 'prim', 'swinder', 'wilson', 'dijkstra']`
    :

    `perfect: bool`
    :

    `pic: Literal[0, 1, 2]`
    :

    `pic_scalar: float`
    :

    `seed: int`
    :

    `width: int`
    :

    `window_siz: mazegen.grid_tools.vector.Vec2`
    :

    ### Static methods

    `parse_Literal(v: Any) ‑> Any`
    :   Parse a string repr of a Literal into the appropriate type.

    `parse_bool(v: Any) ‑> bool`
    :   Parse a string repr of a bool into a bool.

    `parse_int(v: Any) ‑> int`
    :   Parse a string repr of an int into an int.

    `parse_str(v: Any) ‑> str`
    :   Parse a string repr of a str into a str.

    `parse_vec2(v: Any) ‑> mazegen.grid_tools.vector.Vec2`
    :   Parse input into a Vec2.

    ### Methods

    `is_grid(self, vec: mazegen.grid_tools.vector.Vec2) ‑> mazegen.grid_tools.vector.Vec2`
    :   Check if a Vec2 instance is within the grid bounds.

    `validate_bounds(self) ‑> mazegen.config.config.Config`
    :   Validate that the entry and exit are within the grid bounds.

`ConfigError(message: str)`
:   Exception raised for errors in configuration loading.
    
    Initialize the ConfigError.

    ### Ancestors (in MRO)

    * mazegen.errors.MazeError
    * builtins.Exception
    * builtins.BaseException

`ConfigIO()`
:   Class for handling input and output of Config instances.

    ### Static methods

    `from_file(path: str) ‑> mazegen.config.config.Config`
    :   Create a Config instance from a configuration file.

    `from_filemap(path: str) ‑> mazegen.config.config.Config`
    :   Create a Config instance from a hexlist repr of the maze.

    `to_file(cfg: mazegen.config.config.Config, path: str | None = None) ‑> None`
    :   Write the Config instance to a configuration file.

`Dir(*args, **kwds)`
:   Direction class for maze generation and pathfinding.
    
    N, E, S, W are represented as 1, 2, 4, 8 respectively.
    A is the bitwise OR of all four directions.
    non is 0.

    ### Ancestors (in MRO)

    * enum.IntFlag
    * builtins.int
    * enum.ReprEnum
    * enum.Flag
    * enum.Enum

    ### Class variables

    `A`
    :

    `E`
    :

    `N`
    :

    `S`
    :

    `W`
    :

    `non`
    :

    ### Static methods

    `from_str(s: str) ‑> mazegen.grid_tools.cell.Dir`
    :   Return the Dir instance corresponding to a string.

    `from_vec(v: mazegen.grid_tools.vector.Vec2) ‑> mazegen.grid_tools.cell.Dir`
    :   Return the Dir instance corresponding to a Vec2 instance.

    ### Methods

    `opps(self) ‑> mazegen.grid_tools.cell.Dir`
    :   Return the opposite direction of a Dir instance.

    `v(self) ‑> mazegen.grid_tools.vector.Vec2`
    :   Return the vector representation of a Dir instance.

`Edge(a: mazegen.grid_tools.cell.Cell, b: mazegen.grid_tools.cell.Cell)`
:   Edge class for maze generation and pathfinding.

    ### Instance variables

    `a: mazegen.grid_tools.cell.Cell`
    :

    `b: mazegen.grid_tools.cell.Cell`
    :

    `dir: mazegen.grid_tools.cell.Dir`
    :

    ### Methods

    `rm_walls(self) ‑> None`
    :   Remove walls between the two cells defined by the edge.

`Graph(*args, **kwargs)`
:   Graph protocol for maze generation and pathfinding.

    ### Ancestors (in MRO)

    * typing.Protocol
    * typing.Generic

    ### Class variables

    `grid: mazegen.grid_tools.grid.Grid`
    :

    ### Methods

    `edges(self, cell: mazegen.grid_tools.cell.Cell) ‑> Iterable[mazegen.graph.Edge]`
    :   Returns list of edges of cell.

`Grid(width: int, height: int)`
:   Grid class has a width, height, and a 2D list of Cell instances.
    
    Init a grid with the given width and height of Cell instances.

    ### Methods

    `debug(self) ‑> str`
    :   Debug string representation of a Grid instance.

    `dump_grid(self) ‑> list[list[str]]`
    :   Produce a list(list(hex))to represent the currnet layof the grid.

    `fill_empty_grid(self) ‑> None`
    :   Fill a grid with empty Cell instances.

    `fill_grid_from_map(self, hexlist: list[str]) ‑> None`
    :   Fill a grid from a list of lists of hex values repr walls.

    `isvalid(self, v: mazegen.grid_tools.vector.Vec2 | tuple[int, int] | mazegen.grid_tools.cell.Cell) ‑> bool`
    :   Check if a Vec2 instance is within the bounds of the grid.

    `neighbour(self, pos: mazegen.grid_tools.vector.Vec2 | mazegen.grid_tools.cell.Cell) ‑> dict[mazegen.grid_tools.cell.Dir, mazegen.grid_tools.cell.Cell]`
    :   Get four closest cells.

    `neighbour_walls(self, pos: mazegen.grid_tools.vector.Vec2 | mazegen.grid_tools.cell.Cell) ‑> dict[mazegen.grid_tools.cell.Dir, int]`
    :   Get the wall values of the four closest cells.

    `path_from_str(self, s: str) ‑> None`
    :   Create a path from a string of directions.

    `reset(self) ‑> None`
    :   Reset all vistied values to false.

`GridGraph(grid: mazegen.grid_tools.grid.Grid)`
:   Graph for maze generation.
    
    Returns all neighbours of cell, even if wall between them.
    
    Initializes GenGraph with a grid.

    ### Methods

    `edges(self, cell: mazegen.grid_tools.cell.Cell) ‑> Iterable[mazegen.graph.Edge]`
    :   Returns list of edges of cell.

`MazeError(message: str)`
:   Custom exception for maze generation and pathfinding errors.
    
    Initialize the MazeError with a message incl file and line info.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

    ### Descendants

    * mazegen.errors.AlgoError
    * mazegen.errors.ConfigError
    * mazegen.errors.RenderError
    * mazegen.errors.StageError
    * mazegen.errors.StartError

`MazeGenerator(grid: mazegen.grid_tools.grid.Grid, cfg: mazegen.config.config.Config)`
:   Generate a maze grid and a path through it.
    
    Initializes MazeGenerator with a grid and a config.

    ### Class variables

    `ALGOS: dict[str, type[mazegen.algos.BaseStrat]]`
    :

    ### Static methods

    `retryIO(loc: mazegen.grid_tools.vector.Vec2, config: mazegen.config.config.Config, neg: int) ‑> mazegen.grid_tools.vector.Vec2`
    :   Retry opening entry or exit if they are  in the picture.

    ### Methods

    `driver(self) ‑> None`
    :   Driver function to generate the maze and path.

    `gen_grid(self, algo: str = 'dfs') ‑> None`
    :   Generate the maze grid using the specified algorithm.

    `gen_path(self, algo: str) ‑> None`
    :   Generate a path through the maze using the specified algorithm.

    `gen_pic(self, select: int) ‑> None`
    :   Generate the maze grid based on the picture data.

    `to_path(self, v_lst: list[mazegen.grid_tools.vector.Vec2]) ‑> list[mazegen.grid_tools.vector.Vec2]`
    :   Converts a list of Vec2 to a path.

`RenderError(message: str)`
:   Exception raised for errors during rendering.
    
    Initialize the RenderError.

    ### Ancestors (in MRO)

    * mazegen.errors.MazeError
    * builtins.Exception
    * builtins.BaseException

`StartError(message: str)`
:   Exception raised for errors during the start screen.
    
    Initialize the StartError.

    ### Ancestors (in MRO)

    * mazegen.errors.MazeError
    * builtins.Exception
    * builtins.BaseException

`Vec2(*args: Any, **kwargs: Any)`
:   Class for storing 2D Coords.

    ### Instance variables

    `x: int | float`
    :

    `y: int | float`
    :

    ### Methods

    `normalized(self) ‑> mazegen.grid_tools.vector.Vec2`
    :   Return a normalized version of the vector.