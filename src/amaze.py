#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    amaze.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/24 07:55:50 by maprunty         #+#    #+#              #
#    Updated: 2026/02/03 16:58:15 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""First attempts at the A-Maze-ing project."""

from . import Generators, Grid, Render, Vec2


class AMaze:
    """Docstring for AMaze.

    generate maze - extend
    solve maze - mulitple methods
    output text

    """

    def __init__(self, cfg: dict, render: Render):
        """TODO: to be defined."""
        self.config = cfg
        if render is None:
            self.genrend()
        else:
            self.rend = render
        self.startup()
        self.rend.launch()

    def __repr__(self):
        cls = self.__class__.__name__()
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
        self.grid = Grid(self.config, self.width, self.height)
        g = Generators(self.grid, self.config)
        g.animate(self.rend, Vec2(0, 0))

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
        return cls(c_dct, None)


# if __name__ == "__main__":
#    main()
