"""Managing animation sequences for rendering the grid and pathfinding."""

from common.grid_tools import Vec2

from ..assets import Textures
from ..engine import Animator
from .grid_renderer import Render_cell, Render_grid


class Animations:
    """Manage animation seq for rendering the grid and pathfinding."""

    _grid_steps: int
    _grid: Render_grid

    @classmethod
    def grid(cls, delay: float = 0.01) -> None:
        """Animate the rendering of the grid."""
        cls._grid_steps = 0
        cls._grid = Render_grid._grid
        cls._canvas = Render_grid.grid_canva(
            Vec2(cls._grid.width, cls._grid.height), Vec2(0, 0)
        )
        Animator.animate(cls.grid_step, None, delay)

    @classmethod
    def grid_step(cls) -> int:
        """Render the next step in the grid animation."""
        x = cls._grid.height - 1
        y = cls._grid.width - 1
        ma = max(x, y)
        mi = min(x, y)
        if cls._grid_steps == mi + ma + 1:
            return -1
        for i in range(
            min(mi, cls._grid_steps) + min(0, ma - cls._grid_steps) + 1
        ):
            Render_cell.render(
                Vec2(
                    max(cls._grid_steps - x, 0) + i,
                    min(cls._grid_steps, x) - i,
                ),
                cls._canvas,
            )
        cls._canvas.put_canva()
        cls._grid_steps += 1
        return 1

    @classmethod
    def path(cls, delay: float = 0.0):
        """Animate the rendering of the pathfinding solution."""
        if not cls._grid:
            cls._grid = Render_grid._grid
        path = cls._grid.path
        cls._path_steps = len(path)
        cls._path_step = 0
        Animator.animate(cls.path_step, None, delay)
        texture = Textures.load(
            "path.png",
            Vec2(Render_grid._tile_siz.x + 1, Render_grid._tile_siz.y + 1),
            (0, 180),
        )[0]
        Render_grid.load_path(path, texture)

    @classmethod
    def path_step(cls):
        """Render the next step in the pathfinding animation."""
        if cls._path_step >= cls._path_steps:
            return -1
        Render_cell.render_path(cls._path_step, cls._canvas)
        cls._path_step += 1
        cls._canvas.put_canva()
        return 1
