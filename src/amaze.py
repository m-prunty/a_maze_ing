# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    amaze.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/24 07:55:50 by maprunty         #+#    #+#              #
#    Updated: 2026/05/07 22:07:38 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""First attempts at the A-Maze-ing project."""

import os
import sys

from common import Config, ConfigIO, Grid, Vec2
from graphics import (
    Animations,
    Event_loop,
    Render_cell,
    Render_grid,
    Renderer,
    Textures,
    Window,
)
from mazegen import MazeGenerator

from .options import Options


class Start:
    """Class to handle the start screen and options menu."""

    def __init__(self) -> None:
        """Initialize the start screen."""
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
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(f"Error during initialization: {e}")
            raise Exception(e) from e

    def render_start(self) -> None:
        """Render the start screen."""
        start_btn = Textures.load(
            os.path.dirname(os.path.abspath(__file__)) + "/../includes/",
            "start_button.png",
            Vec2(300, 90),
            (0,),
        )[0]
        opt_logo = Textures.load(
            os.path.dirname(os.path.abspath(__file__)) + "/../includes/",
            "options_button.png",
            Vec2(90, 90),
            (0,),
        )[0]
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
                self.a = AMaze(self.cfg)
                self.on_start = False
                Window.clear_window()
                Render_grid.is_a_path = False
                self.a.startup()
                self.a.grid.path.insert(0, Render_grid._cfg.entry)
                Event_loop.add_key_hook(self.a.launch_animation, None)
                Animations.grid(0.02)

            if button == 1 and x > 300 and x < 600 and y > 300 and y < 640:
                self.on_start = False
                Window.clear_window()
                
                Render_grid.is_a_path = False
                self.a = AMaze.maze_fromfile("maze.txt")
                self.a.grid.path.insert(0, Render_grid._cfg.entry)
                Event_loop.add_key_hook(self.a.launch_animation, None)
                Animations.grid(0.02)


class AMaze:
    """Main class for the A-Maze-ing project."""

    def __init__(self, cfg: Config) -> None:
        """Initialize the AMaze class."""
        self.config = cfg
        self.grid = Grid(cfg.width, cfg.height)
        print("== GRID CREATED ==")
        Render_grid.load(self.grid, cfg)
        Render_cell.create()

    def __repr__(self) -> str:
        """Return a epresentation of the AMaze class for instantiation."""
        cls = self.__class__.__name__
        return f"{cls}({self.config})"

    def startup(self) -> None:
        """Start the maze generation and animation."""
        g = MazeGenerator(self.grid, self.config)
        g.driver()
        self.maze_tofile(self.config.output_file)

    def launch_animation(self, key: int) -> None:
        """Launch the path animation when the spacebar is pressed."""
        if key == 32 and not Render_grid.is_a_path:
            Animations.path()
            Render_grid.is_a_path = True
        elif key == 32 and Render_grid.is_a_path:
            Animations.path()
            Render_grid.is_a_path = False

    def maze_tofile(self, filename: str) -> None:
        """Write the maze to a file."""
        try:
            hexlist = self.grid.dump_grid()
            with open(filename, "w") as f:
                for y in hexlist:
                    f.write("\n")
                    for x in y:
                        f.write(x)
                f.write("\n")
                f.write(f"\n{self.config.entry}\n")
                f.write(f"{self.config.exit}\n")
                f.write(
                    "".join(
                        list(
                            map(
                                lambda p, q: f"{p - q}",
                                self.grid.path,
                                self.grid.path[1:],
                            )
                        )
                    )
                )
            print(f"{filename} created with maze data.")
        except Exception as e:
            print(f"Error writing maze to file: {e}")
            raise Exception(e) from e

    # needs work
    @classmethod
    def maze_fromfile(cls, filename: str) -> "AMaze":
        """Create a maze from a file."""
        cfg = ConfigIO.from_filemap(filename)
        c = cls(cfg)
        with open(filename) as f:
            hexlist = f.read().split("\n")
        c.grid.fill_grid_from_map(hexlist, cfg)
        return c
