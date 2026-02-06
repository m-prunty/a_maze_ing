# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    a-maze-ing.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: sdeppe <sdeppe@student.42heilbronn.de>    +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:26:52 by sdeppe           #+#    #+#              #
#    Updated: 2026/02/04 21:26:44 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""TODO: Short module summary.

Optional longer description.
"""

import random
import sys
import os

from src import AMaze, Config, Grid, Render, Vec2, Options

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
        self.rend.init_window(
            900, 900, " -- A-maze-ing -- "
        )
        self.on_start = True
        self.opt = Options(self.rend)
        self.a = AMaze(self.opt.cfg, self.rend)
        self.render_start()

    def render_start(self):
        start_btn = self.rend.generate_sprit(os.path.dirname(os.path.abspath(__file__)) + "/includes/", "start_button.png", Vec2(300, 90), (0,))
        opt_logo = self.rend.generate_sprit(os.path.dirname(os.path.abspath(__file__)) + "/includes/", "options_logo.png", Vec2(90, 90), (0,))
        self.rend.render_text("A-MAZE-ING", Vec2(400, 50))
        self.rend.render_image(opt_logo[0], Vec2(650, 650))
        self.rend.render_image(start_btn[0], Vec2(300, 150))
        self.rend.m.mlx_do_sync(self.rend.mlx_ptr)
        self.add_hooks()
        self.rend.launch()
        
    def add_hooks(self):
        self.rend.add_mous_hook(self.mouse_func, None)
        self.rend.add_hook(self.rend.close, 33, None)
        
    
    def mouse_func(self, button, x, y, _):
        if (self.on_start):
            if (button == 1 and
                x > 650 and x < 760 and
                y > 650 and y < 760):
                self.opt.render()
                self.on_start = False
            if (button == 1 and
                x > 300 and x < 600 and
                y > 150 and y < 240):
                self.rend.clear_window()
                self.on_start = False
                self.a.startup()
        
        


def main4():
    start = Start()
    start.render_start()
    

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
    main4()
