#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    grid_cell.py                                      :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:38:19 by maprunty         #+#    #+#              #
#    Updated: 2026/05/03 11:59:41 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""TODO: Short module summary.

Optional longer description.
"""

from collections.abc import Generator
from enum import IntFlag
from typing import Protocol, Self

from .vector import Vec2


class HasSize(Protocol):
    """Protocol for objects that have width and height attributes."""

    width: int
    height: int


class Dir(IntFlag):
    """Direction class for maze generation and pathfinding.

    N, E, S, W are represented as 1, 2, 4, 8 respectively.
    A is the bitwise OR of all four directions.
    non is 0.
    """

    non = 0
    N = 1 << 0
    E = 1 << 1
    S = 1 << 2
    W = 1 << 3
    A = N | E | S | W

    def __repr__(self) -> str:
        """An evalutable string representation of a Dir instance."""
        cls = self.__class__.__name__
        return f"{cls}({self.name})"

    def __str__(self) -> str:
        """String representation of a Dir instance."""
        return f"{self.name}"

    def opps(self) -> "Dir":
        """Return the opposite direction of a Dir instance."""
        return _OPPOSITE[self]

    def v(self) -> Vec2:
        """Return the vector representation of a Dir instance."""
        return Vec2(*_DIR_TO_VEC[self])

    @classmethod
    def from_vec(cls, v: Vec2) -> "Dir":
        """Return the Dir instance corresponding to a Vec2 instance."""
        return _VEC_TO_DIR[v]


_VEC_TO_DIR: dict[Vec2, Dir] = {
    Vec2(0, -1): Dir.N,
    Vec2(1, 0): Dir.E,
    Vec2(0, 1): Dir.S,
    Vec2(-1, 0): Dir.W,
}

_DIR_TO_VEC: dict[Dir, Vec2] = {v: k for k, v in _VEC_TO_DIR.items()}

_OPPOSITE: dict[Dir, Dir] = {
    Dir.N: Dir.S,
    Dir.E: Dir.W,
    Dir.S: Dir.N,
    Dir.W: Dir.E,
    Dir.A: Dir.non,
    Dir.non: Dir.A,
}


class Cell:
    """Cell class has a location and a wall attribute.

    The wall is a 4-bit represantaion. i.e
    0000 has all walls
    0100 has one opening to south
    Args:
        a (int): First number.
        b (int): Second number.

    Returns:
        int: Product of a and b.
    """

    N = Dir.N
    E = Dir.E
    S = Dir.S
    W = Dir.W

    def __init__(self, loc: Vec2):
        """Init a cell with a Vec2 location and all walls."""
        self.wall = Dir.A
        self.loc = loc
        self.ispath = False
        self.ispic = False
        self.visited = False

    def debug(self) -> str:
        r_str = ""
        for k, v in vars(self).items():
            r_str += f"{k}:{v} "
        return r_str

    def __repr__(self) -> str:
        """An evalutable string representation of a Cell instance."""
        cls = self.__class__.__name__
        r_str = f"{cls}({self.loc})"
        return r_str

    def __str__(self):
        """TODO: Docstring."""
        r_str = f"{self.loc} "
        r_str += f"{self.wall}"
        return r_str

    def __sub__(self, other) -> Dir:
        """Subtract two cells to get the direction from self to other."""
        if abs(self.loc - other.loc) != 1:
            raise ValueError("Cells are not adjacent")
        return Dir.from_vec(other.loc - self.loc)

    @property
    def loc(self) -> Vec2:
        """TODO: Docstring."""
        return self._loc

    @loc.setter
    def loc(self, value: Vec2):
        self.x, self.y = value
        self._loc = value

    @property
    def neighbours(self):
        return self._neighbours

    def get_neighbours(self, grid) -> dict[Dir, "Cell"]:
        """Doc"""
        self._neighbours: dict[Dir, Cell] = {}
        for k in Dir:
            try:
                if grid.isvalid(k.v() + self.loc):
                    self._neighbours.update({k: grid[k.v() + self.loc]})
            except AttributeError as ae:
                print(f"Neighbours is none {ae}")
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

    def rm_wall_nb(self, direction):
        neighbour = self.neighbours[direction]
        self.rm_wall(direction)
        neighbour.rm_wall(direction.opps())


class Path:
    __slots__ = ["_bits"]
    CELL_BITS = 4
    CELL_MASK = (1 << CELL_BITS) - 1

    def __init__(self, bits: Dir = Dir.non, loc: Vec2 = Vec2(0, 0)):
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

    def __add__(self, dir_: Dir):
        # print(dir_, "3", self._bits << self.CELL_BITS | dir_)
        return (self._bits << self.CELL_BITS) | dir_

    def add(self, dir_: Dir):
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
            path += [Dir(p)]
        path.reverse()
        for p in path:
            yield p


class Grid:
    """Docstring for Grid."""

    def __init__(self, width: int, height: int):
        """TODO: to be defined."""
        self.width, self.height = width, height
        self.path = []
        self.grid = [
            [Cell(Vec2(x, y)) for x in range(self.width)]
            for y in range(self.height)
        ]
        self.get_cell_neighbours()
        self.pic = []

    def __getitem__(self, key: tuple[int, int] | Vec2) -> Cell | None:
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
        except ValueError:
            # print(
            #    f"Grid key error:{key} not a valid tuple {ve}", file=sys.stderr
            # )
            return None

    def isvalid(self, v: Vec2) -> int | Vec2:
        if (
            v.x is not None
            and v.y is not None
            and 0 <= v.x <= self.width
            and 0 <= v.y <= self.height
        ):
            return v
        return 0

    def __iter__(self) -> Generator[Cell, None, None]:
        for y in self.grid:
            for x in y:
                yield x

    # def path_mk(self, start):
    #     pos = self[start]
    #     # print(">>>>", self.path)
    #     for s in self.path.path_yd_rev():
    #         print(s, "asjkld", pos, type(pos))
    #         try:
    #             print(pos.neighbours, type(s), s)
    #             pos.ispath = True
    #             pos = pos.neighbours[s]
    #         except Exception:
    #             print("AAAAAA")

    @classmethod
    def fill_grid_from_map(cls, hexlist: list[Dir], cfg: HasSize) -> Self:
        c = cls(cfg.width, cfg.height)
        # print(hexlist)
        for y, row in enumerate(hexlist[1:]):
            if y < c.height:
                for x, i in enumerate(row):
                    if x < c.width:
                        c[x, y].wall = i
        # print(hexlist)
        return c

    def dump_grid(self) -> list[list[str]]:
        """Produce a list(list(hex))to represent the currnet layof the grid."""
        hexlist = [[f"{hex(c.wall)[2:]}" for c in r] for r in self.grid]
        return hexlist

    def get_cell_neighbours(self) -> None:
        for c in self:
            c.get_neighbours(self)

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

    def reset(self) -> None:
        """Reset all vistied values to false."""
        for row in self.grid:
            for cell in row:
                cell.visited = False
                # print(cell)

    def debug(self) -> str:
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

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}(width={self.width}, height={self.height})"

    def __str__(self, cursor: Vec2) -> str:
        """TODO: Docstring."""
        r_str = ""
        for x in range(self.width):
            cell = self[x, 0]
            if cell is None:
                continue
            r_str += "+"
            r_str += "---" if cell.has_wall(Dir.N) else "   "
        r_str += "+\n"
        for y in range(self.height):
            for x in range(self.width):
                cell = self[x, y]
                if cell is None:
                    continue
                if cell.has_wall(Dir.W):
                    r_str += "|"
                else:
                    r_str += " "
                if cursor and cursor == cell.loc:
                    r_str += " @ "
                else:
                    r_str += "   " if not cell.ispic else " X "
            if cell is None:
                continue
            r_str += "|\n" if cell.has_wall(Dir.E) else " \n"
            for x in range(self.width):
                cell = self[x, y]
                r_str += "+"
                if cell is None:
                    continue
                if cell.has_wall(Dir.S):
                    r_str += "---"
                else:
                    r_str += "   "
            r_str += "+\n"
        return r_str
