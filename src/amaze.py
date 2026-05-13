# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    amaze.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/24 07:55:50 by maprunty         #+#    #+#              #
#    Updated: 2026/05/12 20:54:15 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""First attempts at the A-Maze-ing project."""

import os
import sys

from common import Config, ConfigError, ConfigIO, Dir, Grid, StartError, Vec2
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
        # try:
        print(os.path.dirname(os.path.abspath(__file__))
        + "/../includes/sprits/")
        Textures.set_path(os.path.dirname(os.path.abspath(__file__))
        + "/../includes/sprits/")
        self.on_start = True
        self._load_cfg()
        Window.create(self.cfg.window_siz, " -- A-maze-ing -- ")
        self.opt = Options(self.cfg)
        # except Exception as e:
            # raise StartError(f"{e}") from e

    def _load_cfg(self) -> None:
        if len(sys.argv) == 2:
            try:
                self.cfg = ConfigIO.from_file(sys.argv[1])
                return
            except (ConfigError, FileNotFoundError):
                pass
        self.no_cfg()

    def no_cfg(self) -> None:
        """Handle the case where no valid configuration file is provided."""
        print("No valid configuration file provided.\n")
        select = input("Do you want to use default (y/n): ")
        if select.lower() == "y":
            self.cfg = Config()
        else:
            print("Aborted")
            sys.exit(0)

    def render_start(self) -> None:
        """Render the start screen."""
        start_btn = Textures.load(
            "start_button.png",
            Vec2(300, 90),
            (0,),
        )[0]
        opt_logo = Textures.load(
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
        print(f"Mouse click at ({x}, {y}) with button {button}")
        if self.on_start:
            if button == 1 and x > 650 and x < 760 and y > 650 and y < 760:
                self.on_start = False
                self.opt.render()
            if button == 1 and x > 300 and x < 600 and y > 150 and y < 240:
                self.a = AMaze.maze_fromconfig(self.cfg)
                self.launch_maze()

            if button == 1 and x > 300 and x < 600 and y > 300 and y < 640:
                self.a = AMaze.maze_fromfile("maze.txt")
                self.launch_maze()

    def launch_maze(self) -> None:
        """Launch the maze rendering and animation."""
        self.a.launch_renders()
        self.on_start = False
        Window.clear_window()
        Render_grid.is_a_path = False
        Event_loop.add_key_hook(self.a.launch_animation, None)


class AMaze:
    """Main class for the A-Maze-ing project."""

    def __init__(self, cfg: Config) -> None:
        """Initialize the AMaze class."""
        self.config = cfg
        self.grid = Grid(cfg.width, cfg.height)
        print("== GRID CREATED ==")

    def __repr__(self) -> str:
        """Return a epresentation of the AMaze class for instantiation."""
        cls = self.__class__.__name__
        return f"{cls}({self.config})"

    def launch_renders(self) -> None:
        """Launch the renders for the maze."""
        Render_grid.load(self.grid, self.config)
        Render_cell.create()
        Animations.grid(0.02)

    def launch_animation(self, key: int) -> None:
        """Launch the path animation when the spacebar is pressed."""
        if key == 32 and not Render_grid.is_a_path:
            Animations.path()
            Render_grid.is_a_path = True
        elif key == 32 and Render_grid.is_a_path:
            Animations.path()
            Render_grid.is_a_path = False

    @classmethod
    def maze_fromconfig(cls, cfg: Config) -> "AMaze":
        """Start the maze generation and animation."""
        try:
            c = cls(cfg)
            c.grid.fill_empty_grid()
            g = MazeGenerator(c.grid, c.config)
            g.driver()
            c.maze_tofile(c.config.output_file)
            return c
        except Exception as e:
            raise StartError(f"Error during setup: {e}") from e

    @classmethod
    def maze_fromfile(cls, filename: str) -> "AMaze":
        """Create a maze from a file."""
        try:
            cfg = ConfigIO.from_filemap(filename)
            c = cls(cfg)
            c.grid.fill_empty_grid()
            with open(filename) as f:
                hexlist = f.read().split("\n")
            c.grid.path = [c.grid[c.config.entry].loc]
            c.grid.fill_grid_from_map(hexlist)
            return c
        except Exception as e:
            raise StartError(f"Error during setup: {e}") from e

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
                                lambda p, q: f"{Dir.from_vec(q - p)}",
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
