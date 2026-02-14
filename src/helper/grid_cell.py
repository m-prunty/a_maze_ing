#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    grid_cell.py                                      :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:38:19 by maprunty         #+#    #+#              #
#    Updated: 2026/02/04 22:06:41 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""TODO: Short module summary.

Optional longer description.
"""

import random

from .vector import Vec2


class Cell:
    """Docstring for Cell.

    wall is a 4-bit represantaion. i.e
    0000 has all walls
    0100 has one opening to south
    """

    N = 1 << 0
    E = 1 << 1
    S = 1 << 2
    W = 1 << 3

    DIRS = {
        N: Vec2(0, -1),
        E: Vec2(1, 0),
        S: Vec2(0, 1),
        W: Vec2(-1, 0),
    }

    OPPS = {
        N: S,
        E: W,
        S: N,
        W: E,
    }

    def __init__(self, loc: Vec2):
        """TODO: to be defined."""
        self.wall = 0b1111
        self.loc = loc
        self.ispic = False
        self.ispath = False
        self.visited = False

    # @property
    # def scale_factor(self, tile_siz):
    #     return tile_siz.x * 2 + i * tile_siz.x

    def __repr__(self):
        """Return a tuple represantation of a Vec2 instance."""
        cls = self.__class__.__name__
        return f"{cls}(loc={self.loc}, wall={self.wall},\
ispic={self.ispic}, visited={self.visited})"

    def __str__(self):
        """TODO: Docstring."""
        r_str = f"{self.loc} "
        r_str += f"{bin(self.wall)}"
        return r_str

    @property
    def loc(self) -> Vec2:
        """TODO: Docstring."""
        return self._loc

    @loc.setter
    def loc(self, value: Vec2):
        self._loc = value

    @property
    def visited(self) -> bool:
        """TODO: Docstring."""
        return self._visited

    @visited.setter
    def visited(self, value: bool):
        """TODO: Docstring."""
        self._visited = value

    def has_wall(self, direction):
        """TODO: Docstring."""
        return self.wall & direction

    def add_wall(self, direction):
        """TODO: Docstring."""
        self.wall |= direction

    def rm_wall(self, direction):
        """TODO: Docstring."""
        self.wall &= ~direction


class Grid:
    """Docstring for Grid."""

    def __init__(self, width, height):
        """TODO: to be defined."""
        #        if not cfg.items():
        #            self.set_def_cfg(width, height)
        self.width, self.height = width, height
        self.grid = [
            [Cell(Vec2(x, y)) for x in range(self.width)]
            for y in range(self.height)
        ]

    def __getitem__(self, key):
        """TODO: Docstring."""
        try:
            x, y = key
            if 0 <= x < self.width and 0 <= y < self.height:
                return self.grid[y][x]
            else:
                raise ValueError(
                    f"\
{x} or {y} is out of range {self.width},{self.height}"
                )
        except ValueError as ve:
            print(f"Grid key error:{key} not a valid tuple {ve}")
            return None

    #    def set_def_cfg(self, width, height):
    #        self.config = {
    #            "FILENAME": "config.txt",
    #            "WIDTH": 20 if not width else width,
    #            "HEIGHT": 10 if not height else height,
    #            "ENTRY": (0, 0),
    #            "EXIT": (19, 9),
    #            "OUTPUT_FILE": "maze.txt",
    #            "PERFECT": True,
    #        }

    def is_grid(self, vec: Vec2) -> Vec2:
        """Check if a vector lives in the grid.

        Args:
            vec (Vec2): the coordinates to check if exist in grid

        Returns:
            type: Vec2(vec) if valid othereise Vec2(width-1, height-1)
        """
        rx = random.randint(0, 1)
        ry = random.randint(0, 1)
        tst = (self.width, self.height)
        print(
            f"test{tst} {vec} {not 0 <= vec.x < tst[0]} or {not 0 <= vec.y < tst[1]}\
 == {not 0 <= vec.x < tst[0] or not 0 <= vec.y < tst[1]}"
        )
        print("aa", vec, tst)
        if not (0 <= vec.x < tst[0]) or not (0 <= vec.y < tst[1]):
            print(f"Wont fit on the grid...{tst} {vec}")
            return Vec2(
                ((tst[0] * rx) - 1 + rx) % (self.width - 1),
                ((tst[1] * ry) - 1 + ry) % (self.height - 1),
            )
        return vec

    def __str__(self, cursor=None):
        """TODO: Docstring."""
        r_str = ""
        for x in range(self.width):
            cell = self[x, 0]
            r_str += "+"
            r_str += "---" if cell.has_wall(Cell.N) else "   "
        r_str += "+\n"
        for y in range(self.height):
            for x in range(self.width):
                cell = self[x, y]
                if cell.has_wall(Cell.W):
                    r_str += "|"
                else:
                    r_str += " "
                if cursor and cursor == cell.loc:
                    r_str += " @ "
                else:
                    r_str += "   " if not cell.ispic else " X "
            r_str += "|\n" if cell.has_wall(Cell.E) else " \n"
            for x in range(self.width):
                cell = self[x, y]
                r_str += "+"
                if cell.has_wall(Cell.S):
                    r_str += "---"
                else:
                    r_str += "   "
            r_str += "+\n"
        return r_str

    @classmethod
    def fill_grid_from_map(cls, hexlist, cfg):
        c = cls(cfg.width, cfg.height)
        print(hexlist)
        for y, row in enumerate(hexlist[1:]):
            if y < c.height:
                for x, i in enumerate(row):
                    if x < c.width:
                        c[x, y].wall = i
        print(hexlist)
        return c

    def dump_grid(self) -> list[list[hex]]:
        """Produce a list(list(hex))to represent the currnet layof the grid."""
        hexlist = [[f"{hex(c.wall)[2:]}" for c in r] for r in self.grid]
        return hexlist

    #
    #    @property
    #    def width(self):
    #        """Get WIDTH from config file."""
    #        return self._width
    #
    #    @property
    #    def height(self):
    #        """Get HEIGHT from config file."""
    #        return self._height
    #

    def neighbour(self, pos: Vec2) -> dict[list[Cell]]:
        """Get four closest cells."""
        neighbours: dict[list[Cell]] = {}
        for k, v in Cell.DIRS.items():
            try:
                neighbours.update({k: self[v + pos].wall})
            except AttributeError:
                print("is none")
        # print(neighbours)
        return neighbours

    def reset(self):
        """Reset all vistied values to false."""
        for row in self.grid:
            for cell in row:
                cell.visited = False
                # print(cell)
