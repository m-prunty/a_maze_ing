from graphics import Animator, Canvas, Render_cell, Render_grid, Renderer
from helper import Vec2

class Animations:
    
    @classmethod
    def grid(cls, delay=3.0):
        cls._grid_steps = 0
        cls._grid = Render_grid._grid
        print(Vec2(cls._grid.width, cls._grid.height))
        cls._canvas = Render_grid.grid_canva(Vec2(cls._grid.width, cls._grid.height), Vec2(0, 0))
        Animator.animate(cls.grid_step, None, delay)

    @classmethod
    def grid_step(cls):
        print(cls._grid_steps)
        x = cls._grid.height - 1
        y = cls._grid.width - 1
        ma = max(x, y)
        mi = min(x, y)
        if cls._grid_steps == mi + ma + 1:
            return -1
        for i in range(min(mi, cls._grid_steps) + min(0, ma - cls._grid_steps) + 1):
            # print(min(cls._grid_steps, x) - i, max(cls._grid_steps + 1 - x, 0) + i)
            # Render_cell.render(Vec2(3, 3), cls._canvas)
            # print(cls._grid[min(cls._grid_steps, x) - i, max(cls._grid_steps + 1 - x, 0) + i].wall)
            Render_cell.render(Vec2(max(cls._grid_steps - x, 0) + i, min(cls._grid_steps, x) - i), cls._canvas)
        cls._canvas.put_canva()
        # print(cls._canvas)
        # Render_grid.render_grid(cls._canvas)
        # Renderer.render_image(1, Vec2())
        cls._grid_steps += 1
        return 1