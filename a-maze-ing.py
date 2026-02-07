# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    a-maze-ing.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: sdeppe <sdeppe@student.42heilbronn.de>    +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:26:52 by sdeppe           #+#    #+#              #
#    Updated: 2026/02/06 21:34:38 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""TODO: Short module summary.

Optional longer description.
"""

import random
import sys

from src.amaze import AMaze, Config, Grid, Render, Vec2

# from src.graphics import Render
# from src.helper import *

sys.setrecursionlimit(2000)


def print_image(button, x, y):
    """TODO: Docstring."""
    print(
        f"Got mouse event! button {button} at x: \
{int((x / rend.width) * rend.gridx)}, y: {int(y / rend.width * rend.gridy)}"
    )
    if button == 1:
        hex = random.randrange(0, 15)
        grid = Grid({}, rend.gridx, rend.gridy)
        vec = Vec2(
            int((x / rend.height) * rend.gridx),
            int(y / rend.width * rend.gridy),
        )
        grid[vec].wall = hex
        print(grid)
        # print(hex)
        rend.render_cell(vec, grid)
    #     # rend.render_cell(0, Vec2(1, 9))


class Start:
    def __init__(self):
        # self.options = Options(1000, 1000)
        self.rend = Render()
        self.render_start()

    def render_start(self):
        rend.init_window(
            self.options.height, self.options.width, " -- A-maze-ing -- "
        )


rend = Render()


def main():
    """TODO: Docstring."""
    rend.init_window(700, 700, "hello")
    rend.init_grid(Vec2(3, 3))
    print(rend.generate_grid_sprits())
    # print(rend.cell_siz)
    rend.add_hook(rend.close, 33, None)
    rend.add_mous_hook(print_image, (1, 2))

    rend.launch()
    print("Hello from amazing!")


def main2():
    """Drive the main loop."""
    av = sys.argv
    ac = len(av)
    # rend.init_grid(Vec2(3, 3))
    # print(rend.generate_grid_sprits())
    # print(rend.cell_siz)
    if 1 <= ac <= 2:
        cfg = Config.cfg_from_file("config.txt")
        # print("____________", cfg.entry, cfg.exit)
        a = AMaze(cfg)
        a.startup()


def main3():
    a = AMaze.maze_fromfile("maze.txt")
    a.startup()
    print(a)


if __name__ == "__main__":
    main2()
