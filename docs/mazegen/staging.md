Module mazegen.staging
======================
Staging classes for maze generation and pathfinding.

Classes
-------

`BaseStage(*args, **kwargs)`
:   Base stage protocol for maze generation and pathfinding.

    ### Ancestors (in MRO)

    * typing.Protocol
    * typing.Generic

    ### Methods

    `process(self, e: mazegen.staging.MazeEvent) ‑> bool`
    :   Processes a maze.

`EventType(*args, **kwds)`
:   Event type for maze generation and pathfinding.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `EDGE`
    :

    `ENTER`
    :

    `EXIT`
    :

`GoalStage(goal: mazegen.grid_tools.cell.Cell)`
:   Stage for checking if goal is reached.
    
    Initializes GoalStage with a goal.

    ### Methods

    `process(self, e: mazegen.staging.MazeEvent) ‑> bool`
    :   Checks if goal is reached.

`MazeEvent(edge: mazegen.graph.Edge | mazegen.grid_tools.cell.Cell, etype: mazegen.staging.EventType = EventType.ENTER, carve_only: bool = False)`
:   Event class for maze generation and pathfinding.

    ### Instance variables

    `carve_only: bool`
    :

    `cell: mazegen.grid_tools.cell.Cell`
    :   Returns the cell associated with the event.

    `edge: mazegen.graph.Edge | mazegen.grid_tools.cell.Cell`
    :

    `etype: mazegen.staging.EventType`
    :

`PathStage()`
:   Stage for marking path cells.

    ### Methods

    `process(self, e: mazegen.staging.MazeEvent) ‑> bool`
    :   Marks path cells.

`PicStage()`
:   Stage for marking picture cells.

    ### Methods

    `process(self, e: mazegen.staging.MazeEvent) ‑> bool`
    :   Marks picture cells.

`RmStage()`
:   Stage for removing walls between cells.

    ### Methods

    `process(self, e: mazegen.staging.MazeEvent) ‑> bool`
    :   Removes walls between cells.

`VisitStage()`
:   Stage for marking visited cells.

    ### Methods

    `process(self, e: mazegen.staging.MazeEvent) ‑> bool`
    :   Marks visited cells.