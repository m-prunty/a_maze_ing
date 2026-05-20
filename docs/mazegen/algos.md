Module mazegen.algos
====================
Maze generation and pathfinding algorithms.

Classes
-------

`BaseStrat(graph: mazegen.graph.Graph, cfg: mazegen.config.config.Config)`
:   Base strategy for maze generation and pathfinding.
    
    Initializes BaseStrat with a graph and config.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * mazegen.algos.Dfs
    * mazegen.algos.Dijkstra
    * mazegen.algos.Pic
    * mazegen.algos.Prim
    * mazegen.algos.Sidewinder
    * mazegen.algos.Wilson

    ### Instance variables

    `height: int`
    :   Get HEIGHT from config file.

    `width: int`
    :   Get WIDTH from config file.

    ### Methods

    `add_stage(self, stage: mazegen.staging.BaseStage) ‑> None`
    :   Adds a stage to the strategy.

    `generate(self) ‑> Iterable[mazegen.grid_tools.vector.Vec2]`
    :   Generates a maze or path.

`Dfs(graph: mazegen.graph.Graph, cfg: mazegen.config.config.Config)`
:   Depth-first search maze generation.
    
    Initializes BaseStrat with a graph and config.

    ### Ancestors (in MRO)

    * mazegen.algos.BaseStrat
    * abc.ABC

    ### Methods

    `generate(self) ‑> Iterable[mazegen.grid_tools.vector.Vec2]`
    :   Generates a maze using depth-first search.

`Dijkstra(graph: mazegen.graph.Graph, cfg: mazegen.config.config.Config)`
:   Dijkstra's algorithm for pathfinding.
    
    Initializes BaseStrat with a graph and config.

    ### Ancestors (in MRO)

    * mazegen.algos.BaseStrat
    * abc.ABC

    ### Methods

    `generate(self) ‑> Iterable[mazegen.grid_tools.vector.Vec2]`
    :   Generates using Dijkstra's algorithm.

`Pic(graph: mazegen.graph.Graph, cfg: mazegen.config.config.Config)`
:   Picture maze generation.
    
    Initializes BaseStrat with a graph and config.

    ### Ancestors (in MRO)

    * mazegen.algos.BaseStrat
    * abc.ABC

    ### Static methods

    `get_pic(select: int) ‑> list[int]`
    :   Get the picture data for the maze based on the selected option.

    ### Methods

    `generate(self) ‑> Iterable[mazegen.grid_tools.vector.Vec2]`
    :   Generates a picture to place in the maze.

`Prim(graph: mazegen.graph.Graph, cfg: mazegen.config.config.Config)`
:   Prims Algo.
    
    Initializes BaseStrat with a graph and config.

    ### Ancestors (in MRO)

    * mazegen.algos.BaseStrat
    * abc.ABC

    ### Methods

    `generate(self) ‑> Iterable[mazegen.grid_tools.vector.Vec2]`
    :   Generates using Prim's algorithm.

`Sidewinder(graph: mazegen.graph.Graph, cfg: mazegen.config.config.Config)`
:   Sidewinder maze generation.
    
    Initializes BaseStrat with a graph and config.

    ### Ancestors (in MRO)

    * mazegen.algos.BaseStrat
    * abc.ABC

    ### Methods

    `generate(self) ‑> Iterable[mazegen.grid_tools.vector.Vec2]`
    :   Generates using Sidewinder algorithm.

`Wilson(graph: mazegen.graph.Graph, cfg: mazegen.config.config.Config)`
:   Wilson's algorithm.
    
    Initializes BaseStrat with a graph and config.

    ### Ancestors (in MRO)

    * mazegen.algos.BaseStrat
    * abc.ABC

    ### Methods

    `generate(self) ‑> Iterable[mazegen.grid_tools.vector.Vec2]`
    :   Generates using Wilson's algorithm.