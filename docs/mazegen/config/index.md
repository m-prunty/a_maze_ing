Module mazegen.config
=====================
Init file for the Config module.

Sub-modules
-----------
* mazegen.config.config

Classes
-------

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

`ConfigIO()`
:   Class for handling input and output of Config instances.

    ### Static methods

    `from_file(path: str) ‑> mazegen.config.config.Config`
    :   Create a Config instance from a configuration file.

    `from_filemap(path: str) ‑> mazegen.config.config.Config`
    :   Create a Config instance from a hexlist repr of the maze.

    `to_file(cfg: mazegen.config.config.Config, path: str | None = None) ‑> None`
    :   Write the Config instance to a configuration file.