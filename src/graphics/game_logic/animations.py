import os

from graphics import Animator, Render_cell, Render_grid, Textures
from helper import Vec2


class Animations:
    @classmethod
    def grid(cls, delay=0.01):
        cls._grid_steps = 0
        cls._grid = Render_grid._grid
        cls._canvas = Render_grid.grid_canva(
            Vec2(cls._grid.width, cls._grid.height), Vec2(0, 0)
        )
        Animator.animate(cls.grid_step, None, delay)

    @classmethod
    def grid_step(cls):
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
    def path(cls, path: list[Vec2], delay=0.01):
        print(path)
        if not cls._grid:
            cls._grid = Render_grid._grid
        cls._path_canvas = Render_grid.grid_canva(
            Vec2(cls._grid.width, cls._grid.height), Vec2(0, 0)
        )
        cls._path_steps = len(path)
        cls._path_step = 0
        Animator.animate(cls.path_step, None, delay)
        texture = Textures.load(
            os.path.dirname(os.path.abspath(__file__)) + "/includes/sprits/",
            "path.png",
            Vec2(Render_grid._tile_siz.x + 2, Render_grid._tile_siz.y + 2),
            (0,),
        )[0]
        Render_grid.load_path(path, texture)

    @classmethod
    def path_step(cls):
        if cls._path_step >= cls._path_steps:
            return -1
        Render_cell.render_path(cls._path_step, cls._path_canvas)
        cls._path_step += 1
        cls._path_canvas.put_canva()
        return 1
