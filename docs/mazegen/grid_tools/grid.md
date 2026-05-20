Module mazegen.grid_tools.grid
==============================
Grid class to represent a 2D grid of Cell instances.

Classes
-------

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

`HasSize(*args, **kwargs)`
:   Protocol for objects that have width and height attributes.

    ### Ancestors (in MRO)

    * typing.Protocol
    * typing.Generic

    ### Class variables

    `height: int`
    :

    `width: int`
    :