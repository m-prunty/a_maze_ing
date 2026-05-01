# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    a-maze-ing.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: sdeppe <sdeppe@student.42heilbronn.de>    +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:26:52 by sdeppe           #+#    #+#              #
#    Updated: 2026/05/01 04:56:44 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Main file to run A-maze-ing."""

import os
import sys

from src.a_maze_ing import AMaze
from src.a_maze_ing.graphics import Event_loop, Renderer, Textures, Window
from src.a_maze_ing.options import Options
from src.common.config import Config
from src.common.grid_tools import Vec2

sys.setrecursionlimit(2000)


class Start:
    """Class to handle the start screen and options menu."""

    def __init__(self) -> None:
        """Initialize the start screen."""
        # self.options = Options(1000, 1000)
        self.on_start = True
        self.cfg = Config.cfg_from_file("config.txt")
        print(self.cfg)
        print(type(self.cfg.window_siz), self.cfg.window_siz)
        Window.create(self.cfg.window_siz, " -- A-maze-ing -- ")
        self.opt = Options(self.cfg)
        self.a = AMaze(self.cfg)
        self.render_start()

    def render_start(self) -> None:
        """Render the start screen."""
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

    def add_hooks(self) -> None:
        """Add hooks for the start screen."""
        print("== HOOKS PROPERLY ADDED ==")
        Event_loop.add_mous_hook(self.mouse_func, None)
        Event_loop.add_hook(Event_loop.close, 33, None)
        Event_loop.add_key_hook(self.restart, None)
        # Event_loop.add_key_hook(self.restart, None)
        # Event_loop.add_hook(self.opt.save(), 65307, None)

    def restart(self, input: int) -> None:
        """Restart the start screen or save options."""
        print(input)
        if input == 65307:
            if self.on_start:
                Event_loop.close(None)
            else:
                self.opt.save()

    def mouse_func(self, button: int, x: int, y: int, _: None) -> None:
        """Handle mouse clicks on the start screen."""
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


def main4() -> None:
    """Drive the main loop."""
    start = Start()
    start.render_start()


def main2() -> None:
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


if __name__ == "__main__":
    main4()
