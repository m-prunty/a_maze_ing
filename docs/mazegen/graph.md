Module mazegen.graph
====================
Graph classes for maze generation and pathfinding.

Classes
-------

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

`GridGraph(grid: mazegen.grid_tools.grid.Grid)`
:   Graph for maze generation.
    
    Returns all neighbours of cell, even if wall between them.
    
    Initializes GenGraph with a grid.

    ### Methods

    `edges(self, cell: mazegen.grid_tools.cell.Cell) ‑> Iterable[mazegen.graph.Edge]`
    :   Returns list of edges of cell.

`MazeGraph(grid: mazegen.grid_tools.grid.Grid)`
:   Graph for pathfinding.
    
    Returns only neighbours of cell if no wall between them.
    
    Initializes PathGraph with a grid.

    ### Methods

    `edges(self, cell: mazegen.grid_tools.cell.Cell) ‑> Iterable[mazegen.graph.Edge]`
    :   Returns list of edges of cell if no wall between cell and dir.