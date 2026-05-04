# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    amaze.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/24 07:55:50 by maprunty         #+#    #+#              #
#    Updated: 2026/05/03 11:26:34 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""First attempts at the A-Maze-ing project."""

import os
import sys

from common import Config, ConfigIO, Grid, Vec2
from mazegen import Generators

from .graphics import (
    Animations,
    Event_loop,
    Render_cell,
    Render_grid,
    Renderer,
    Textures,
    Window,
)
from .options import Options


class Start:
    """Class to handle the start screen and options menu."""

    def __init__(self) -> None:
        """Initialize the start screen."""
        # self.options = Options(1000, 1000)
        try:
            self.on_start = True
            if len(sys.argv) == 2:
                self.cfg = ConfigIO.from_file(sys.argv[1])
            else:
                select = input("Do you want to use default (y/n): ")
                if select.lower() == "y":
                    self.cfg = Config()
                else:
                    print("Aborted")
                    sys.exit(0)
            Window.create(self.cfg.window_siz, " -- A-maze-ing -- ")
            self.opt = Options(self.cfg)
            self.a = AMaze(self.cfg)
        except Exception as e:
            print(f"Error during initialization: {e}")

    def render_start(self) -> None:
        """Render the start screen."""
        start_btn = Textures.load(
            os.path.dirname(os.path.abspath(__file__)) + "/../../includes/",
            "start_button.png",
            Vec2(300, 90),
            (0,),
        )[0]
        opt_logo = Textures.load(
            os.path.dirname(os.path.abspath(__file__)) + "/../../includes/",
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


class AMaze:
    """Main class for the A-Maze-ing project."""

    def __init__(self, cfg: Config) -> None:
        """Initialize the AMaze class."""
        self.config = cfg
        self.grid = Grid(cfg.width, cfg.height)
        Render_grid.load(self.grid, cfg)
        Render_cell.create()

    def __repr__(self) -> str:
        """Return a epresentation of the AMaze class for instantiation."""
        cls = self.__class__.__name__
        return f"{cls}({self.config})"

    def startup(self) -> None:
        """Start the maze generation and animation."""
        # try:
        g = Generators(self.grid, self.config)
        g.driver()
        Animations.grid(0.02)
        self.is_a_path = False
        Event_loop.add_key_hook(self.launch_animation, None)
        self.maze_tofile(self.config.output_file)
        # except Exception as e:
        #    print(f"Error during startup: {e}")

    def launch_animation(self, key: int) -> None:
        """Launch the path animation when the spacebar is pressed."""
        if key == 32 and not self.is_a_path:
            Animations.path()
            self.is_a_path = True
        # elif key == 32 and not self.is_a_path:
        # print(key)

    def maze_tofile(self, filename: str) -> None:
        """Write the maze to a file."""
        hexlist = self.grid.dump_grid()
        print(f"{filename} created with maze data.")
        try:
            f = open(filename, "w")
        except FileNotFoundError as e:
            f = open(filename, "x")
            raise FileNotFoundError(e) from e
        for y in hexlist:
            f.write("\n")
            for x in y:
                f.write(x)
        f.write("\n")
        f.write(f"\n{self.config.entry}\n")
        f.write(f"{self.config.exit}\n")
        f.write(
            f"{''.join(list(map(lambda p, q: f'{p - q}', self.grid.path, self.grid.path[1:])))}\n"
        )
        f.close()

    @classmethod
    def maze_fromfile(cls, filename: str) -> Grid:
        """Create a maze from a file."""
        hexlist = []
        with open(filename) as f:
            hexlist = f.read().split("\n")
        cfg = Config.cfg_from_filemap(hexlist)
        c = cls(cfg)
        c.grid.fill_grid_from_map(hexlist, c)
        return c
