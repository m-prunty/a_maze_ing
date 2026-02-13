from graphics import Textures, Window, Renderer
from helper import Grid, Cell, Vec2
from config import Config
import os

class Render_grid:
    _tiles = []
    _initialized = False

    @classmethod
    def create_grid(cls, grid: Grid):
        if cls._initialized:
            raise RuntimeError("MlxContext already initialized")
        cls._grid = grid
        cls._tile_siz = Vec2(Window.get_siz().x / (grid.width * 2 + 1),
                       Window.get_siz().y / (grid.height * 2 + 1))
        cls._initialized = True
        if not cls._tiles:
            cls.load_tiles()
        
        
    @classmethod
    def load_tiles(cls):
        if not cls._initialized:
            if cls._grid is None:
                raise RuntimeError("Grid was not created, please run Render_grid.create_grid first")
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
                        path, sprit, cls._tile_siz, (0, 90, 180, 270))
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

        
    
    
class Render_cell:
    _init = False
    
    @classmethod
    def create(cls):
        if cls._init:
            raise RuntimeError("Class already initilazed")
        cls._grid = Render_grid._grid
        cls._cfg = Config.cfg_from_file("config.txt")
        cls._color = cls._cfg.color
        cls._entry = cls._cfg.entry
        cls._exit = cls._cfg.exit
        cls._tile_siz = Render_grid._tile_siz

    @classmethod
    def render(cls, pos: Vec2):
        """ " Sepcial: 0 none, 1 home, 2 arival"""
        if not cls._init:
            cls.create()
        hex = cls._grid[pos].wall
        n = cls._grid.neighbour(pos)
        if (pos == cls._entry):
            special = 1
        elif pos == cls._exit:
            special = 2
        else:
            special = 0
        print(Render_grid._tiles)
        for i in range(3):
            for y in range(3):
                if y == 1 and i % 2 == 0:
                    if (hex >> 2 * (i == 0) + 1) & 1:
                        Renderer.render_image(
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
                        Renderer.render_image(
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
                        Renderer.render_image(
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
                        Renderer.render_image(
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
                    Renderer.render_image(
                        Render_grid._tiles[(special == 1) * 24
                        + (special == 2) * 20
                        + cls._color * 28],
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
                        if pos.y < Render_grid._grid.height - 1 #y
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
                        if pos.x < Render_grid._grid.width  - 1 #x
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
                    Renderer.render_image(
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