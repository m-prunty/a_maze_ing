import os

from common.config import Config
from common.grid_tools import Cell, Dir, Grid, Vec2

from ..assets import Textures
from ..engine import Canvas, Window


class Render_grid:
    _tiles: list[int] = []
    _initialized = False
    _grid: Grid
    _tile_siz: Vec2
    _cfg: Config
    _path: list[Vec2]
    _path_texture: int
    is_a_path: bool
    # _canva = None

    @classmethod
    def load(cls, grid: Grid, cfg: Config) -> None:
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
                cls.load(cls._grid, cls._grid)
        path = Textures._include_path + "/grid/"
        sprits = list(filter(lambda f: f.endswith(".png"), os.listdir(path)))
        sprits.sort()
        ret = []
        cls._tiles = []
        for sprit in sprits:
            imgs = Textures.load(
                sprit,
                Vec2(cls._tile_siz.x + 1, cls._tile_siz.y + 1),
                (0, 90, 180, 270),
                path="/grid/"
            )
            ret.append(
                (
                    imgs,
                    sprit,
                )
            )

            for img in imgs:
                cls._tiles.append(img)
        return ret

    @classmethod
    def load_path(cls, path: list[Vec2], texture: int):
        cls._path = path
        cls._path_texture = texture

    @classmethod
    def render_grid(cls, canva: Canvas):
        for x in range(cls._grid.width):
            for y in range(cls._grid.height):
                Render_cell.render(Vec2(x, y), canva)
        canva.put_canva()

    @classmethod
    def grid_canva(cls, cells: Vec2, grid_pos: Vec2):
        """ "  The cells pos"""
        canva = Canvas(
            Vec2(cls._tile_siz.x * 3 * cells.x, cls._tile_siz.y * 3 * cells.y),
            Vec2(
                cls._tile_siz.x * 3 * grid_pos.x,
                cls._tile_siz.y * 3 * grid_pos.y,
            ),
        )
        return canva


class Render_cell:
    _init = False
    _tile_siz = Vec2

    @classmethod
    def create(cls):
        if cls._init:
            raise RuntimeError("Class already initilazed")
        cls._init = True
        cls._grid = Render_grid._grid
        cls._tile_siz = Render_grid._tile_siz

    @classmethod
    def render_path(cls, iteration: int, canva: Canvas):
        path: list[Dir] = Render_grid._grid.path
        curent: Dir = path[iteration]
        color = Render_grid._cfg.color
        # print(Render_grid.is_a_path)
        if iteration != 0 and curent != Render_grid._cfg.entry:
            prev: Vec2 = path[iteration - 1]
            canva.add_image(
                Render_grid._path_texture
                if Render_grid.is_a_path
                else Render_grid._tiles[color * 28],
                Vec2(
                    int(
                        curent.x * cls._tile_siz.x * 2
                        + (1 - (curent.x - prev.x)) * cls._tile_siz.x
                    ),
                    int(
                        curent.y * cls._tile_siz.y * 2
                        + (1 - (curent.y - prev.y)) * cls._tile_siz.y
                    ),
                ),
            )
        if (
            iteration != len(path)
            and iteration != 0
            and curent != Render_grid._cfg.exit
        ):
            canva.add_image(
                Render_grid._path_texture
                if Render_grid.is_a_path
                else Render_grid._tiles[color * 28],
                Vec2(
                    int(curent.x * cls._tile_siz.x * 2 + 1 * cls._tile_siz.x),
                    int(curent.y * cls._tile_siz.y * 2 + 1 * cls._tile_siz.y),
                ),
            )

    def set_pic_color(color: int):
        match color:
            case 0:
                return 1
            case 1:
                return 0
            case 2:
                return 0

    @classmethod
    def render(cls, pos: Vec2, canva: Canvas):
        """Pos is dependent on the canva."""
        if not cls._init:
            cls.create()
        hex = cls._grid[pos].wall
        n = cls._grid.neighbour_walls(pos)

        if pos == Render_grid._cfg.entry:
            special = 1
        elif pos == Render_grid._cfg.exit:
            special = 2
        else:
            special = 0
        if cls._grid[pos].ispic:
            color = cls.set_pic_color(Render_grid._cfg.color)
        else:
            color = Render_grid._cfg.color

        for i in range(3):
            for y in range(3):
                if y == 1 and i % 2 == 0:
                    if (hex >> 2 * (i == 0) + 1) & 1:
                        canva.add_image(
                            Render_grid._tiles[5 + color * 28],
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
                        canva.add_image(
                            Render_grid._tiles[color * 28],
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
                        canva.add_image(
                            Render_grid._tiles[4 + color * 28],
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
                        canva.add_image(
                            Render_grid._tiles[color * 28],
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
                    canva.add_image(
                        Render_grid._tiles[
                            (
                                (special == 1) * 24
                                + (special == 2) * 20
                                + color * 28
                            )
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
                        if pos.y < Render_grid._grid.height - 1
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
                        if pos.x < Render_grid._grid.width - 1
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

                    canva.add_image(
                        Render_grid._tiles[(tile * 4 + ori) + color * 28],
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
