# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    amaze.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/24 07:55:50 by maprunty         #+#    #+#              #
#    Updated: 2026/02/04 22:18:02 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""First attempts at the A-Maze-ing project."""

from config import Config
from graphics import Render
from helper import Grid, Vec2
from mazegen import Generators


class AMaze:
    """Docstring for AMaze.

    generate maze - extend
    solve maze - mulitple methods
    output text

    """

    def __init__(self, cfg: Config, render: Render = None):
        """TODO: to be defined."""
        self.config = cfg
        self.grid = Grid(self.width, self.height)
        self.rend = render

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}({self.config})"

    def genrend(self):
        self.rend = Render()
        self.rend.init_window(900, 900, "A_maze_ing")
        self.rend.init_grid(Vec2(self.width, self.height))
        self.rend.add_hook(self.rend.close, 33, None)
        self.rend.generate_grid_sprits()

    def startup(self):
        """TODO: Summary line.

        Args:
            param (type): Description.

        Returns:
            type: Description.

        Raises:
            ExceptionType: When this is raised.
        """
        if self.rend is None:
            self.genrend()
        g = Generators(self.grid, self.config)
        g.animate(self.rend, Vec2(0, 0))
        self.rend.launch()
        self.grid.dump_grid()
        self.maze_tofile(self.config.output_file)

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

    #   def grid_from_hexlist(self, hexlist) -> list[hex]:
    #       for i in

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


