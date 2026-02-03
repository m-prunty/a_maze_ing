#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    amaze.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/24 07:55:50 by maprunty         #+#    #+#              #
#    Updated: 2026/02/03 14:37:08 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""First attempts at the A-Maze-ing project."""

from .graphics.render import Render
from .helper.grid_cell import Grid
from .helper.vector import Vec2
from .mazegen.generators import Generators


class AMaze:
    """Docstring for AMaze.

    generate maze - extend
    solve maze - mulitple methods
    output text
        

    """

    def __init__(self, cfg: dict, render: Render):
        """TODO: to be defined."""
        self.rend = render
        self.config = cfg
        self.startup()
        g = Generators(self.grid, self.config, "rng")
        g.animate(self.rend, Vec2(0, 0))
#         self.rend.launch()
    
    def __repr__(self):
        cls = self.__class__.__name__()
        return (f"{cls}({self.config})")

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
        return cls(c_dct, None)


# if __name__ == "__main__":
#    main()
