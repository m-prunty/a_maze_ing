# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    a-maze-ing.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: sdeppe <sdeppe@student.42heilbronn.de>    +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:26:52 by sdeppe           #+#    #+#              #
#    Updated: 2026/02/03 18:22:36 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""TODO: Short module summary.

Optional longer description.
"""

import random
import sys

from src.amaze import AMaze, Grid, Render, Vec2

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
        print(hex)
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


def cfg_from_file(filename: str):
    """TODO: Docstring for from_fil.

    Args:
        filename (str): TODO

    Returns: TODO

    """
    c_dct = {"FILENAME": filename}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                k, v = line.split("=")
                k = k.strip().upper()
                try:
                    if "," in v:
                        v = v.split(",")
                        v = tuple(int(i) for i in v)
                    elif v.lower() in ("true", "false"):
                        v = v.lower() == "true"
                    elif v.isnumeric():
                        v = int(v)
                except ValueError as ve:
                    print(
                        f"Error: {ve} something's not right with config\
                          {k}:{v} "
                    )
                c_dct.update({k: v})
    return c_dct


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
        a = AMaze.cfg_from_file("config.txt")
        print(a.config)
        print("yay")


if __name__ == "__main__":
    main()
