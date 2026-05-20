Module mazegen.grid_tools
=========================
A-maze-ing grid tools package.

Sub-modules
-----------
* mazegen.grid_tools.cell
* mazegen.grid_tools.grid
* mazegen.grid_tools.vector

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