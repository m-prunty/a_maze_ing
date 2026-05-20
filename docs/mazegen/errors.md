Module mazegen.errors
=====================
Custom exceptions for A-Maze-ing.

Classes
-------

`AlgoError(message: str)`
:   Exception raised for errors in generation or pathfinding algorithms.
    
    Initialize the AlgoError.

    ### Ancestors (in MRO)

    * mazegen.errors.MazeError
    * builtins.Exception
    * builtins.BaseException

`ConfigError(message: str)`
:   Exception raised for errors in configuration loading.
    
    Initialize the ConfigError.

    ### Ancestors (in MRO)

    * mazegen.errors.MazeError
    * builtins.Exception
    * builtins.BaseException

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

`RenderError(message: str)`
:   Exception raised for errors during rendering.
    
    Initialize the RenderError.

    ### Ancestors (in MRO)

    * mazegen.errors.MazeError
    * builtins.Exception
    * builtins.BaseException

`StageError(message: str)`
:   Exception raised for errors in staging.
    
    Initialize the StageError.

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