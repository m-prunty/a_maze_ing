Module mazegen.mazegenerator
============================
MazeGenerator class to generate a maze grid and a path through it.

Classes
-------

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