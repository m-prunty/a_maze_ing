# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    a-maze-ing.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: sdeppe <sdeppe@student.42heilbronn.de>    +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:26:52 by sdeppe           #+#    #+#              #
#    Updated: 2026/02/17 21:02:11 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""TODO: Short module summary.

Optional longer description.
"""

import os
import sys

from src import (
    AMaze,
    Config,
    Event_loop,
    Options,
    Render_grid,
    Renderer,
    Textures,
    Vec2,
    Window,
)

sys.setrecursionlimit(2000)


class Start:
    def __init__(self):
        # self.options = Options(1000, 1000)
        self.on_start = True
        self.cfg = Config.cfg_from_file("config.txt")
        Window.create(self.cfg.window_siz, " -- A-maze-ing -- ")
        self.opt = Options(self.cfg)
        self.a = AMaze(self.cfg)
        self.render_start()

    def render_start(self):
        start_btn = Textures.load(
            os.path.dirname(os.path.abspath(__file__)) + "/includes/",
            "start_button.png",
            Vec2(300, 90),
            (0,),
        )[0]
        opt_logo = Textures.load(
            os.path.dirname(os.path.abspath(__file__)) + "/includes/",
            "options_button.png",
            Vec2(90, 90),
            (0,),
        )[0]
        print(Textures(opt_logo))
        Renderer.render_text("A-MAZE-ING", Vec2(400, 50))
        Renderer.render_image(opt_logo, Vec2(650, 650))
        Renderer.render_image(start_btn, Vec2(300, 150))
        self.add_hooks()
        Event_loop.launch()

    def add_hooks(self):
        print("== HOOKS PROPERLY ADDED ==")
        Event_loop.add_mous_hook(self.mouse_func, None)
        Event_loop.add_hook(Event_loop.close, 33, None)
        Event_loop.add_key_hook(self.restart, None)
        # Event_loop.add_key_hook(self.restart, None)
        # Event_loop.add_hook(self.opt.save(), 65307, None)

    def restart(self, input):
        print(input)
        if (input == 65307):
            if (self.on_start):
                Event_loop.close(None)
            else:
                self.opt.save()
        
    def mouse_func(self, button, x, y, _):
        # print(self.on_start)
        if self.on_start:
            if button == 1 and x > 650 and x < 760 and y > 650 and y < 760:
                self.on_start = False
                self.opt.render()
            if button == 1 and x > 300 and x < 600 and y > 150 and y < 240:
                self.on_start = False
                Window.clear_window()
                # Render_grid.render_grid()
                # Mlx_context._mlx.mlx_do_sync(Mlx_context.get())
                # Event_loop.add_key_hook(self.restart, None)
                self.a.startup()


def main4():
    start = Start()
    start.render_start()


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
