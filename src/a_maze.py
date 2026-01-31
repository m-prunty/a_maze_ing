#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    a_maze.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/24 07:55:50 by maprunty         #+#    #+#              #
#    Updated: 2026/01/31 14:11:59 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""First attempts at the A-Maze-ing project."""

import random as random

from graphics.render import Render
from helper.grid_cell import Grid
from helper.vector import Vec2
from mazegen.generators import Generators


class A_Maze:
    """Docstring for A_Maze."""

    def __init__(self, cfg: dict):
        """TODO: to be defined."""
        self.rend = Render()
        self.config = cfg
        self.rend.init_window(900, 900, "hello")
        self.rend.add_hook(self.rend.close, 33, None)
        self.startup()
        self.rend.generate_grid_sprits()
        # self.gen_rand()
        g = Generators(self.grid, self.config)
        # self.animate(self.grid, 0.0001)
        g.animate(self.rend)
        print("aaaaa")
        self.rend.launch()

    def startup(self):
        """TODO: Summary line.

        Args:
            param (type): Description.

        Returns:
            type: Description.

        Raises:
            ExceptionType: When this is raised.
        """
        self.grid = Grid(self.config, self.width, self.height)
        self.rend.init_grid(Vec2(self.width, self.height))

    @property
    def width(self):
        """Get WIDTH from config file."""
        return self.config["WIDTH"]

    @property
    def height(self):
        """Get HEIGHT from config file."""
        return self.config["HEIGHT"]

    @classmethod
    def cfg_from_file(cls, filename: str):
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
        return cls(c_dct)


# if __name__ == "__main__":
#    main()
