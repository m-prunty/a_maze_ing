# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    amaze.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/24 07:55:50 by maprunty         #+#    #+#              #
#    Updated: 2026/05/01 13:19:33 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""First attempts at the A-Maze-ing project."""

from common import Config, Grid
from mazegen import Generators

from .graphics import Animations, Event_loop, Render_cell, Render_grid


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
