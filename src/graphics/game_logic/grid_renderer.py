import os
import time

from config import Config
from graphics import Canvas, Textures, Window
from helper import Cell, Grid, Vec2


class Render_grid:
    _tiles = []
    _initialized = False

    @classmethod
    def create_grid(cls, grid: Grid):
        if cls._initialized:
            raise RuntimeError("MlxContext already initialized")
        cls._grid = grid
        cls._tile_siz = Vec2(
            Window.get_siz().x / (grid.width * 2 + 1),
            Window.get_siz().y / (grid.height * 2 + 1),
        )
        cls._initialized = True
        if not cls._tiles:
            cls.load_tiles()

    @classmethod
    def load_tiles(cls):
        if not cls._initialized:
            if cls._grid is None:
                raise RuntimeError(
                    "Grid was not created, please run Render_grid.create_grid first"
                )
            cls.create_grid(cls._grid)
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
    def render_grid(cls):
        canva = cls.cells_canva(
            Vec2(cls._grid.width, cls._grid.height), Vec2()
        )
        for x in range(cls._grid.width):
            for y in range(cls._grid.height):
                Render_cell.render(Vec2(x, y), canva, 0)
        canva.put_canva()

    @classmethod
    def cells_canva(cls, cells: Vec2, grid_pos: Vec2):
        """ "  The cells pos"""
        return Canvas(
            Vec2(cls._tile_siz.x * 3 * cells.x, cls._tile_siz.y * 3 * cells.y),
            Vec2(
                cls._tile_siz.x * 3 * grid_pos.x,
                cls._tile_siz.y * 3 * grid_pos.y,
            ),
        )


class Render_cell:
    _init = False
    _tile_siz = Vec2

    # _canva = Canvas(Vec2(_tile_siz.x * 3, _tile_siz.y * 3))
    @classmethod
    def create(cls):
        if cls._init:
            raise RuntimeError("Class already initilazed")
        cls._grid = Render_grid._grid
        cls._cfg = Config.cfg_from_file("config.txt")
        print(type(cls._cfg), cls._cfg)
        print(
            cls._cfg.exit,
            type(cls._cfg.exit),
            cls._cfg.entry,
            type(cls._cfg.entry),
        )
        cls._color = cls._cfg.color
        cls._entry = cls._cfg.entry
        cls._exit = cls._cfg.exit
        cls._tile_siz = Render_grid._tile_siz
        print(cls._exit, type(cls._exit), cls._entry, type(cls._entry))
        # cls._canva = Canvas(Vec2(cls._tile_siz.x * 3, cls._tile_siz.y * 3))

    @classmethod
    def render(cls, pos: Vec2, canva: Canvas, delay: int):
        """ " Pos is dependent on the canva"""
        if not cls._init:
            cls.create()
        hex = cls._grid[pos].wall
        n = cls._grid.neighbour(pos)
        if pos == cls._entry:
            special = 1
        elif pos == cls._exit:
            special = 2
        else:
            special = 0
        # print(Render_grid._tiles)

        for i in range(3):
            for y in range(3):
                if y == 1 and i % 2 == 0:
                    if (hex >> 2 * (i == 0) + 1) & 1:
                        # Renderer.render_image(
                        #     Render_grid._tiles[5 + cls._color * 28],
                        #     Vec2(
                        #         int(
                        #             pos.x * cls._tile_siz.x * 2
                        #             + i * cls._tile_siz.x
                        #         ),
                        #         int(
                        #             pos.y * cls._tile_siz.y * 2
                        #             + y * cls._tile_siz.y
                        #         ),
                        #     ),
                        # )
                        canva.add_image(
                            Render_grid._tiles[5 + cls._color * 28],
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
                        # Renderer.render_image(
                        #     Render_grid._tiles[cls._color * 28],
                        #     Vec2(
                        #         int(
                        #             pos.x * cls._tile_siz.x * 2
                        #             + i * cls._tile_siz.x
                        #         ),
                        #         int(
                        #             pos.y * cls._tile_siz.y * 2
                        #             + y * cls._tile_siz.y
                        #         ),
                        #     ),
                        # )

                        canva.add_image(
                            Render_grid._tiles[cls._color * 28],
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
                        # Renderer.render_image(
                        #     Render_grid._tiles[4 + cls._color * 28],
                        #     Vec2(
                        #         int(
                        #             pos.x * cls._tile_siz.x * 2
                        #             + i * cls._tile_siz.x
                        #         ),
                        #         int(
                        #             pos.y * cls._tile_siz.y * 2
                        #             + y * cls._tile_siz.y
                        #         ),
                        #     ),
                        # )

                        canva.add_image(
                            Render_grid._tiles[4 + cls._color * 28],
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
                        # Renderer.render_image(
                        # 	Render_grid._tiles[cls._color * 28],
                        #     Vec2(
                        #         int(
                        #             pos.x * cls._tile_siz.x * 2
                        #             + i * cls._tile_siz.x
                        #         ),
                        #         int(
                        #             pos.y * cls._tile_siz.y * 2
                        #             + y * cls._tile_siz.y
                        #         ),
                        #     ),
                        # )

                        canva.add_image(
                            Render_grid._tiles[cls._color * 28],
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
                    # Renderer.render_image(
                    #     Render_grid._tiles[(special == 1) * 24
                    #     + (special == 2) * 20
                    #     + cls._color * 28],
                    #     Vec2(
                    #         int(
                    #             pos.x * cls._tile_siz.x * 2
                    #             + i * cls._tile_siz.x
                    #         ),
                    #         int(
                    #             pos.y * cls._tile_siz.y * 2
                    #             + y * cls._tile_siz.y
                    #         ),
                    #     ),
                    # )

                    canva.add_image(
                        Render_grid._tiles[
                            (special == 1) * 24
                            + (special == 2) * 20
                            + cls._color * 28
                        ],
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
                    # Renderer.render_image(
                    #     Render_grid._tiles[(tile * 4 + ori) + cls._color * 28],
                    #     Vec2(
                    #         int(
                    #             pos.x * cls._tile_siz.x * 2
                    #             + i * cls._tile_siz.x
                    #         ),
                    #         int(
                    #             pos.y * cls._tile_siz.y * 2
                    #             + y * cls._tile_siz.y
                    #         ),
                    #     ),
                    # )

                    canva.add_image(
                        Render_grid._tiles[(tile * 4 + ori) + cls._color * 28],
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
                    time.sleep(delay)
                    # canva.put_canva(Vec2(pos.x * cls._tile_siz.x * 2, pos.y * cls._tile_siz.y * 2))
