# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    amaze.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/24 07:55:50 by maprunty         #+#    #+#              #
#    Updated: 2026/03/08 15:31:46 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""First attempts at the A-Maze-ing project."""

from config import Config
from graphics import Animations, Event_loop, Render_cell, Render_grid
from helper import Grid
from mazegen import Generators


class AMaze:
    """Docstring for AMaze.

    generate maze - extend
    solve maze - mulitple methods
    output text

    """

    def __init__(self, cfg: Config):
        """TODO: to be defined."""
        self.config = cfg
        self.grid = Grid(self.width, self.height)
        Render_grid.load(self.grid, cfg)
        Render_cell.create()

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}({self.config})"

    def startup(self):
        """TODO: Summary line.

        Args:
            param (type): Description.

        Returns:
            type: Description.

        Raises:
            ExceptionType: When this is raised.
        """
        g = Generators(self.grid, self.config)
        g.gen_grid()
        Animations.grid(0.02)
        self.is_a_path = False
        Event_loop.add_key_hook(self.launch_animation, None)
        self.maze_tofile(self.config.output_file)

    def launch_animation(self, key: int, dummy):
        if key == 32 and not self.is_a_path:
            Animations.path(self.grid.path, 0.2)
            self.is_a_path = True
        elif key == 32 and not self.is_a_path:
            print(key)

    def maze_tofile(self, filename: str):
        hexlist = self.grid.dump_grid()
        with open(filename, "w") as f:
            for y in hexlist:
                f.write("\n")
                for x in y:
                    f.write(x)
            f.write("\n")
            f.write(f"\n{self.config.entry}\n")
            f.write(f"{self.config.exit}\n")

    @classmethod
    def maze_fromfile(cls, filename: str):
        hexlist = []
        with open(filename) as f:
            hexlist = f.read().split("\n")
        cfg = Config.cfg_from_filemap(hexlist)
        c = cls(cfg, None)
        c.grid.fill_grid_from_map(hexlist, c)
        return c

    @property
    def width(self):
        """Get WIDTH from config file."""
        return self.config.width

    @property
    def height(self):
        """Get HEIGHT from config file."""
        return self.config.height
