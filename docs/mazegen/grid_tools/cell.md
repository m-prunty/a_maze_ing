Module mazegen.grid_tools.cell
==============================
Cell and Dir classes for maze generation and pathfinding.

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