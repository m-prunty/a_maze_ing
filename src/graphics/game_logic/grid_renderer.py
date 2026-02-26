from graphics import Textures, Window, Canvas
from helper import Grid, Cell, Vec2
from config import Config
import os
import time

from config import Config
from graphics import Canvas, Textures, Window
from helper import Cell, Grid, Vec2


class Render_grid:
    _tiles = []
    _initialized = False
    # _canva = None

    @classmethod
    def load(cls, grid: Grid, cfg: Config):
        if cls._initialized:
            raise RuntimeError("MlxContext already initialized")
        cls._grid = grid
        cls._tile_siz = Vec2(
            Window.get_siz().x / (grid.width * 2 + 1),
            Window.get_siz().y / (grid.height * 2 + 1),
        )
        cls._initialized = True
        cls._cfg = cfg
        if not cls._tiles:
            cls.load_tiles()

    @classmethod
    def load_tiles(cls):
        if not cls._initialized:
            if cls._grid is None or cls._cfg is None:
                raise RuntimeError("Grid was not created, please run Render_grid.create_grid first")
            cls.load(cls._grid, cls._grid)
        path = (
            os.path.dirname(os.path.abspath(__file__))
            + "/includes/sprits/grid/"
        )
        sprits = list(filter(lambda f: f.endswith(".png"), os.listdir(path)))
        sprits.sort()
        ret = []
        cls._tiles = []
        for sprit in sprits:
            imgs = Textures.load(
                path,
                sprit,
                Vec2(cls._tile_siz.x + 1, cls._tile_siz.y + 1),
                (0, 90, 180, 270),
            )
            ret.append(
                (
                    imgs,
                    sprit,
                )
            )

            for img in imgs:
                # print(img)
                cls._tiles.append(img)
        return ret

    @classmethod
    def render_grid(cls, canva : Canvas):
        # canva = cls.grid_canva(Vec2(cls._grid.width, cls._grid.height), Vec2())
        for x in range(cls._grid.width):
            for y in range(cls._grid.height):
                print("grid pos is :", x, y)
                Render_cell.render(Vec2(x, y), canva)
        canva.put_canva()

    @classmethod
    def grid_canva(cls, cells: Vec2, grid_pos: Vec2):
        """"  The cells pos """
        canva = Canvas(Vec2(cls._tile_siz.x * 3 * cells.x, cls._tile_siz.y * 3 * cells.y),
                      Vec2(cls._tile_siz.x * 3 * grid_pos.x, cls._tile_siz.y * 3 * grid_pos.y))
        return canva

        
    
    
class Render_cell:
    _init = False
    _tile_siz = Vec2

    # _canva = Canvas(Vec2(_tile_siz.x * 3, _tile_siz.y * 3))
    @classmethod
    def create(cls):
        if cls._init:
            raise RuntimeError("Class already initilazed")
        cls._init = True
        cls._grid = Render_grid._grid
        cls._tile_siz = Render_grid._tile_siz
        # print(cls._exit, type(cls._exit), cls._entry, type(cls._entry))
        # cls._canva = Canvas(Vec2(cls._tile_siz.x * 3, cls._tile_siz.y * 3))

    @classmethod
    def render(cls, pos: Vec2, canva: Canvas):
        """ " Pos is dependent on the canva """
        # print(pos)
        if not cls._init:
            cls.create()
        hex = cls._grid[pos].wall
        n = cls._grid.neighbour(pos)
        if pos == Render_grid._cfg.entry:
            special = 1
        elif pos == Render_grid._cfg.exit:
            special = 2
        else:
            special = 0
        if (cls._grid[pos].ispic):
            color = 1
        else:
            color = 2 # TODO: make a function to use the right color in here
        
        for i in range(3):
            for y in range(3):
                if y == 1 and i % 2 == 0:
                    if (hex >> 2 * (i == 0) + 1) & 1:
                        canva.add_image(Render_grid._tiles[5 + color * 28],
                                    Vec2(
                                        int(
                                            pos.x * cls._tile_siz.x * 2
                                            + i * cls._tile_siz.x
                                        ),
                                        int(
                                            pos.y * cls._tile_siz.y * 2
                                            + y * cls._tile_siz.y
                                        )))
                    else:
                        canva.add_image(Render_grid._tiles[color * 28],
                                            Vec2(
                                                    int(
                                                        pos.x * cls._tile_siz.x * 2
                                                        + i * cls._tile_siz.x
                                                    ),
                                                    int(
                                                        pos.y * cls._tile_siz.y * 2
                                                        + y * cls._tile_siz.y
                                                    ),
                                                ),
                                            )
                elif i == 1 and y % 2 == 0:
                    if (hex >> y) & 1:
                        canva.add_image(Render_grid._tiles[4 + color * 28],
                                Vec2(
                                        int(
                                            pos.x * cls._tile_siz.x * 2
                                            + i * cls._tile_siz.x
                                        ),
                                        int(
                                            pos.y * cls._tile_siz.y * 2
                                            + y * cls._tile_siz.y
                                        ),
                                    ),
                                )
                    else:
                        canva.add_image(Render_grid._tiles[color * 28],
                                 Vec2(
                        		        int(
                        		            pos.x * cls._tile_siz.x * 2
                        		            + i * cls._tile_siz.x
                        		        ),
                        		        int(
                        		            pos.y * cls._tile_siz.y * 2
                        		            + y * cls._tile_siz.y
                        		        ),
                        		    ),
                        		)
                elif y % 2 == 1 and i % 2 == 1:
                    canva.add_image(Render_grid._tiles[(special == 1) * 24
                                                        + (special == 2) * 20
                                                        + color * 28],
                                Vec2(
                                        int(
                                            pos.x * cls._tile_siz.x * 2
                                            + i * cls._tile_siz.x
                                        ),
                                        int(
                                            pos.y * cls._tile_siz.y * 2
                                            + y * cls._tile_siz.y
                                        ),
                                    ),
                                )
                else:
                    top = (
                        (hex >> (2 * (i == 0) + 1)) & 1
                        if y > 0
                        else (n[Cell.N] >> (2 * (i == 0) + 1)) & 1
                        if pos.y > 0
                        else 0
                    )
                    bot = (
                        (hex >> (2 * (i == 0) + 1)) & 1
                        if y == 0
                        else (n[Cell.S] >> (2 * (i == 0) + 1)) & 1
                        if pos.y < Render_grid._grid.height - 1  # y
                        else 0
                    )
                    left = (
                        (hex >> y) & 1
                        if i > 0
                        else (n[Cell.W] >> y) & 1
                        if pos.x > 0
                        else 0
                    )
                    right = (
                        (hex >> y) & 1
                        if i == 0
                        else (n[Cell.E] >> y) & 1
                        if pos.x < Render_grid._grid.width - 1  # x
                        else 0
                    )
                    tile = top + bot + left + right
                    if tile == 2:
                        if top + bot == 2 or right + left == 2:
                            tile -= 1
                    ori = 0
                    if tile == 1:
                        ori = bot or top
                    elif tile == 2:
                        ori = (top or left) * 2 + right * -1 + bot
                    elif tile == 3:
                        ori = 6 - (bot * 3 + left * 2 + top * 1)
                    
                    canva.add_image(Render_grid._tiles[(tile * 4 + ori) + color * 28],
                                        Vec2(
					                            int(
					                                pos.x * cls._tile_siz.x * 2
					                                + i * cls._tile_siz.x
					                            ),
					                            int(
					                                pos.y * cls._tile_siz.y * 2
					                                + y * cls._tile_siz.y
					                            ),
					                        ),
					                    )
                    