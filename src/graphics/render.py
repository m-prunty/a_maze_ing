"""TODO: Short module summary.

Optional longer description.
"""

import os

from mlx import Mlx
from PIL import Image

from helper import Cell, Grid, Vec2


class Render:
    def __init__(self):
        self.m = Mlx()
        self.mlx_ptr = self.m.mlx_init()
        self.images = [[]]

    def generate_window(self):
        self.win_ptr = self.m.mlx_new_window(
            self.mlx_ptr, self.width, self.height, self.name
        )
        self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)

    def init_window(self, height: int, width: int, name: str):
        self.width = width
        self.height = height
        self.name = name
        self.generate_window()

    def clear_window(self):
        self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)

    def add_image(self, path: str, image: str, siz: Vec2) -> int:
        ret = self.generate_sprit(path, image, siz)
        return ret

    def render_image(self, image: int, place: Vec2):
        # img_ptr = self.m.mlx_png_file_to_image(self.mlx_ptr, self.images[image][1])
        self.m.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.images[image + 1][1][0],
            place.x,
            place.y,
        )

    def generate_grid_sprits(self) -> tuple:
        path = (
            os.path.dirname(os.path.abspath(__file__))
            + "/includes/sprits/grid/"
        )
        sprits = list(filter(lambda f: f.endswith(".png"), os.listdir(path)))
        sprits.sort()
        ret = []
        for sprit in sprits:
            ret.append(
                (
                    self.generate_sprit(
                        path, sprit, self.tile_siz, (0, 90, 180, 270)
                    ),
                    sprit,
                )
            )
        return ret

    def generate_sprit(
        self, path: str, sprit: str, siz: Vec2, degs: tuple
    ) -> list:
        # print(degs)
        ret = []
        for deg in degs:
            try:
                # print(deg)
                im = Image.open(path + sprit).convert("RGBA")
                im_rot = im.rotate(deg)
                new_im = im_rot.resize(
                    (int(siz.x) + 1, int(siz.y) + 1), Image.Resampling.NEAREST
                )
                new_im.save(path + "resized/" + f"{deg}_" + sprit, "png")
            except OSError:
                print(f"cannot create {sprit}")
            self.images.append(
                [
                    (len(self.images), path + "resized/" + f"{deg}_" + sprit),
                    self.m.mlx_png_file_to_image(
                        self.mlx_ptr, path + "resized/" + f"{deg}_" + sprit
                    ),
                ]
            )
            ret.append(len(self.images) - 1)
        return ret

    def init_grid(self, siz: Vec2):
        self.gridx = siz.x
        self.gridy = siz.y
        # self.grid = [[0 for _ in range(siz.y)] for _ in range(siz.x)]
        self.tile_siz = Vec2(
            self.width / (siz.x * 2 + 1), self.height / (siz.y * 2 + 1)
        )
        # self.cell_siz = Vec2(self.width / (siz.x + 4), self.height / (self.gridy) + (self.height / (self.gridy) / 3) - 1)

    def render_cell(self, pos: Vec2, grid: Grid, color: int, special: int):
        """ " Sepcial: 0 none, 1 home, 2 arival"""
        # img_siz = Vec2(self.cell_siz.x / 3, self.cell_siz.y / 3)
        hex = grid[pos].wall
        if color > 2:
            color = 0
        if special > 2:
            special = 0
        n = grid.neighbour(pos)
        for i in range(3):
            for y in range(3):
                if y == 1 and i % 2 == 0:
                    if (hex >> 2 * (i == 0) + 1) & 1:
                        self.render_image(
                            1 * 4 + 1 + color * 28,
                            Vec2(
                                int(
                                    pos.x * self.tile_siz.x * 2
                                    + i * self.tile_siz.x
                                ),
                                int(
                                    pos.y * self.tile_siz.y * 2
                                    + y * self.tile_siz.y
                                ),
                            ),
						)
                    else:
                        self.render_image(
                            0 + color * 28,
                            Vec2(
                                int(
                                    pos.x * self.tile_siz.x * 2
                                    + i * self.tile_siz.x
                                ),
                                int(
                                    pos.y * self.tile_siz.y * 2
                                    + y * self.tile_siz.y
                                ),
                            ),
                        )
                elif i == 1 and y % 2 == 0:
                    if (hex >> y) & 1:
                        self.render_image(
                            1 * 4 + color * 28,
                            Vec2(
                                int(
                                    pos.x * self.tile_siz.x * 2
                                    + i * self.tile_siz.x
                                ),
                                int(
                                    pos.y * self.tile_siz.y * 2
                                    + y * self.tile_siz.y
                                ),
                            ),
                        )
                    else:
                        self.render_image(
                            0 + color * 28,
                            Vec2(
                                int(
                                    pos.x * self.tile_siz.x * 2
                                    + i * self.tile_siz.x
                                ),
                                int(
                                    pos.y * self.tile_siz.y * 2
                                    + y * self.tile_siz.y
                                ),
                            ),
                        )
                elif y % 2 == 1 and i % 2 == 1:
                    self.render_image(
                        0
                        + (special == 1) * 24
                        + (special == 2) * 20
                        + color * 28,
                        Vec2(
                            int(
                                pos.x * self.tile_siz.x * 2
                                + i * self.tile_siz.x
                            ),
                            int(
                                pos.y * self.tile_siz.y * 2
                                + y * self.tile_siz.y
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
                        if pos.y < self.gridy - 1
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
                        if pos.x < self.gridx - 1
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
                    # print(ori, tile)
                    self.render_image(
                        (tile * 4 + ori) + color * 28,
                        Vec2(
                            int(
                                pos.x * self.tile_siz.x * 2
                                + i * self.tile_siz.x
                            ),
                            int(
                                pos.y * self.tile_siz.y * 2
                                + y * self.tile_siz.y
                            ),
                        ),
                    )

    def add_hook(self, func: callable, event: int, param):
        self.m.mlx_hook(self.win_ptr, event, 0, func, None)

    def add_mous_hook(self, func: callable, param):
        self.m.mlx_mouse_hook(self.win_ptr, func, param)

    def add_key_hook(self, func: callable, param):
        self.m.mlx_key_hook(self.win_ptr, func, param)

    def close(self, dummy):
        self.m.mlx_loop_exit(self.mlx_ptr)

    def launch(self):
        self.m.mlx_loop(self.mlx_ptr)
