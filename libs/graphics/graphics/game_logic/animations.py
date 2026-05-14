"""Managing animation sequences for rendering the grid and pathfinding."""

from mazegen.grid_tools import Grid, Vec2

from graphics import Canvas

from ..assets import Textures
from ..engine import Animator
from .grid_renderer import Render_cell, Render_grid


class Animations:
    """Manage animation seq for rendering the grid and pathfinding."""

    _grid_steps: int
    _grid: Grid
    _canvas: Canvas
    _path_steps: int
    _path_step: int

    @classmethod
    def grid(cls, delay: float = 0.1) -> None:
        """Animate the rendering of the grid."""
        cls._grid_steps = 0
        cls._grid = Render_grid._grid
        cls._canvas = Render_grid.grid_canva(
            Vec2(cls._grid.width, cls._grid.height), Vec2(0, 0)
        )
        # show an empty grid at start
        Render_cell.render(
                Render_grid._cfg.entry,
                cls._canvas,
        )
        Animator.animate(cls.grid_step, tuple(), delay)

    @classmethod
    def grid_step(cls) -> int:
        """Render the next step in the grid animation."""
        if cls._grid_steps >= len(cls._grid.seq):
            Render_cell._is_genreated = True
            return -1
        current: Vec2 = cls._grid.seq[cls._grid_steps]
        Render_cell.render(
                current,
                cls._canvas,
        )
        cls._grid_steps += 1
        cls._canvas.put_canva()
        return 1
        

    @classmethod
    def path(cls, delay: float = 0.0) -> None:
        """Animate the rendering of the pathfinding solution."""
        if not cls._grid:
            cls._grid = Render_grid._grid
        path = cls._grid.path
        cls._path_steps = len(path)
        cls._path_step = 0
        Animator.animate(cls.path_step, tuple(), delay)
        texture = Textures.load(
            "path.png",
            Vec2(Render_grid._tile_siz.x + 1, Render_grid._tile_siz.y + 1),
            (0, 180),
        )[0]
        Render_grid.load_path(path, texture)

    @classmethod
    def path_step(cls) -> int:
        """Render the next step in the pathfinding animation."""
        if cls._path_step >= cls._path_steps:
            return -1
        Render_cell.render_path(cls._path_step, cls._canvas)
        cls._path_step += 1
        cls._canvas.put_canva()
        return 1
