#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    grid_cell.py                                      :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:38:19 by maprunty         #+#    #+#              #
#    Updated: 2026/02/09 23:51:36 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""TODO: Short module summary.

Optional longer description.
"""

from enum import IntFlag

from .vector import Vec2


class Dir(IntFlag):
    non = 0
    N = 1 << 0
    E = 1 << 1
    S = 1 << 2
    W = 1 << 3
    A = N | E | S | W

    def __repr__(self):
        """Return a tuple represantation of a Vec2 instance."""
        cls = self.__class__.__name__
        return f"{cls}.{self.name}"

    def __str__(self):
        return f"{self.name}"

    def opps(self) -> "Dir":
        return {
            Dir.N: Dir.S,
            Dir.E: Dir.W,
            Dir.S: Dir.N,
            Dir.W: Dir.E,
            Dir.A: Dir.non,
            Dir.non: Dir.A,
        }[self]

    def v(self):
        return {
            Dir.N: Vec2(0, -1),
            Dir.E: Vec2(1, 0),
            Dir.S: Vec2(0, 1),
            Dir.W: Vec2(-1, 0),
        }[self]


class Cell:
    """Docstring for Cell.

    wall is a 4-bit represantaion. i.e
    0000 has all walls
    0100 has one opening to south
    """

    N = Dir.N
    E = Dir.E
    S = Dir.S
    W = Dir.W

    def __init__(self, loc: Vec2):
        """TODO: to be defined."""
        self.wall = Dir.A
        self.loc = loc
        self.ispath = False
        self.ispic = False
        self.visited = False

    # @property
    # def scale_factor(self, tile_siz):
    #     return tile_siz.x * 2 + i * tile_siz.x
    def debug(self):
        r_str = ""
        for k, v in vars(self).items():
            r_str += f"{k}:{v} "
        return r_str

    def __repr__(self):
        """Return a tuple represantation of a Vec2 instance."""
        cls = self.__class__.__name__
        r_str = f"{cls}(loc={self.loc})"
        return r_str

    def __str__(self):
        """TODO: Docstring."""
        r_str = f"{self.loc} "
        r_str += f"{self.wall}"
        return r_str

    @property
    def loc(self) -> Vec2:
        """TODO: Docstring."""
        return self._loc

    @loc.setter
    def loc(self, value: Vec2):
        self._loc = value

    @property
    def neighbours(self) -> dict[Dir, "Cell"]:
        return self._neighbours

    def get_neighbours(self, grid) -> dict[Dir, "Cell"]:
        """Doc"""
        self._neighbours: dict[Dir, Cell] = {}
        for k in Dir:
            try:
                self._neighbours.update({k: grid[k.v() + self.loc]})
            except AttributeError:
                print("is none")
        # print("   ?????", self._neighbours)
        return self._neighbours

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


class Path:
    __slots__ = ["_bits"]
    CELL_BITS = 4
    CELL_MASK = (1 << CELL_BITS) - 1

    def __init__(self, bits: Dir = Dir.non):
        self._bits = bits

    def __str__(self):
        r_str = ""
        print(f"{self._bits:b}")
        for d in self.path_yd_rev():
            r_str += str(f"{d.name}, ")
        return r_str

    @property
    def bits(self) -> int:
        """Doc"""
        # print(f"{self.bits:b}")
        return self._bits

    def add(self, dir_: Dir):
        # print(dir_, "3", self._bits << self.CELL_BITS | dir_)
        self._bits = (self._bits << self.CELL_BITS) | dir_

    def add_rec(self, dir_: Dir):
        return Path((self._bits << self.CELL_BITS) | dir_)

    #  def path_add(self, dir_: int):
    # print(f"{self.bits:b}")

    def path_yd(self):
        path = self.bits
        while path:
            p = Dir(path & self.CELL_MASK)
            path >>= self.CELL_BITS
            # print("11", p)
            yield p

    def path_yd_rev(self):
        path = []
        for p in self.path_yd():
            path += [p]
        path.reverse()
        for p in path:
            yield p


class Grid:
    """Docstring for Grid."""

    def __init__(self, width, height):
        """TODO: to be defined."""
        self.width, self.height = width, height
        self.path = Path()
        self.grid = [
            [Cell(Vec2(x, y)) for x in range(self.width)]
            for y in range(self.height)
        ]
        self.get_cell_neighbours(self)

    def __getitem__(self, key):
        """TODO: Docstring."""
        try:
            x, y = key
            # print(x,y)
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

    def __iter__(self):
        for y in self.grid:
            for x in y:
                yield x

    def path_mk(self, start):
        pos = self[start]
        # print(">>>>", self.path)
        for s in self.path.path_yd_rev():
            print(s, "asjkld", pos, type(pos))
            try:
                print(pos.neighbours, type(s), s)
                pos.ispath = True
                pos = pos.neighbours[s]
            except:
                print("AAAAAA")

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

    @staticmethod
    def get_cell_neighbours(grid):
        for c in grid:
            c.get_neighbours(grid)

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

    def neighbour(self, pos: Vec2) -> dict[str, int]:
        """Get four closest cells."""
        n = dict()
        for k, v in self[pos].neighbours.items():
            try:
                if v:
                    n[k] = v.wall
            except AttributeError as ae:
                print(f"is none {k}: {v} - {ae}")
        # print(n)
        return n

    def reset(self):
        """Reset all vistied values to false."""
        for row in self.grid:
            for cell in row:
                cell.visited = False
                # print(cell)

    def debug(self):
        r_str = ""
        tmp = ""
        for k, v in vars(self).items():
            if k == "grid":
                for row in v:
                    row = list(map(lambda c: f"{c.debug()}\n", row))
                    tmp += "".join(row)
                v = tmp
            r_str += f"{k}, {v}\n"
        return r_str

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}(width={self.width}, height={self.height})"

    def __str__(self, cursor=None):
        """TODO: Docstring."""
        r_str = ""
        for x in range(self.width):
            cell = self[x, 0]
            r_str += "+"
            r_str += "---" if cell.has_wall(Dir.N) else "   "
        r_str += "+\n"
        for y in range(self.height):
            for x in range(self.width):
                cell = self[x, y]
                if cell.has_wall(Dir.W):
                    r_str += "|"
                else:
                    r_str += " "
                if cursor and cursor == cell.loc:
                    r_str += " @ "
                else:
                    r_str += "   " if not cell.ispic else " X "
            r_str += "|\n" if cell.has_wall(Dir.E) else " \n"
            for x in range(self.width):
                cell = self[x, y]
                r_str += "+"
                if cell.has_wall(Dir.S):
                    r_str += "---"
                else:
                    r_str += "   "
            r_str += "+\n"
        return r_str
