#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    grid_cell.py                                      :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:38:19 by maprunty         #+#    #+#              #
#    Updated: 2026/05/08 07:08:48 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Module for grid and cell classes."""

from collections.abc import Generator, Iterator
from enum import IntFlag
from typing import Protocol

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
        if self == Dir.non:
            return Vec2()
        return _DIR_TO_VEC[self]

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
        loc (Vec2): The location of the cell in the grid.

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
        """Debug string representation of a Cell instance."""
        r_str = ""
        for k, v in vars(self).items():
            r_str += f"{k}:{v} "
        return r_str

    def __repr__(self) -> str:
        """An evalutable string representation of a Cell instance."""
        cls = self.__class__.__name__
        r_str = f"{cls}({self.loc})"
        return r_str

    def __str__(self) -> str:
        """String representation of a Cell instance."""
        r_str = f"{self.loc} "
        r_str += f"{self.wall}"
        return r_str

    def __sub__(self, other: "Cell") -> Dir:
        """Subtract two cells to get the direction from self to other."""
        if abs(self.loc - other.loc) != 1:
            raise ValueError("Cells are not adjacent")
        return Dir.from_vec(other.loc - self.loc)

    def __iter__(self) -> Iterator[float | int]:
        """Iterate over the fields of a Vec2 instance."""
        return iter((self.x, self.y))

    @property
    def loc(self) -> Vec2:
        """Return the location of a Cell instance as a Vec2."""
        return self._loc

    @loc.setter
    def loc(self, value: Vec2) -> None:
        """Set the location of a Cell instance and update x and y."""
        self.x, self.y = value
        self._loc = value

    @property
    def visited(self) -> bool:
        """Return the visited status of a Cell instance."""
        return self._visited

    @visited.setter
    def visited(self, value: bool) -> None:
        """Set the visited status of a Cell instance."""
        self._visited = value

    def has_wall(self, direction: Dir) -> Dir:
        """Check if a wall exists in the given direction."""
        return self.wall & direction

    def add_wall(self, direction: Dir) -> None:
        """Add a wall in the given direction."""
        self.wall |= direction

    def rm_wall(self, direction: Dir) -> None:
        """Remove a wall in the given direction."""
        self.wall &= ~direction

    def rm_wall_nb(self, neighbour: "Cell", direction: Dir) -> None:
        """Remove a wall in the given direction and the neighbour wall."""
        self.rm_wall(direction)
        neighbour.rm_wall(direction.opps())


class Grid:
    """Grid class has a width, height, and a 2D list of Cell instances."""

    def __init__(self, width: int, height: int):
        """Init a grid with the given width and height of Cell instances."""
        self.width, self.height = width, height
        self.path: list[Vec2] = []
        print(f"Creating grid of size {self.width}x{self.height}")
        self.grid = [
            [Cell(Vec2(x, y)) for x in range(self.width)]
            for y in range(self.height)
        ]
        self.pic: list[int] = []

    def __getitem__(self, key: tuple[int, int] | Vec2 | Cell) -> Cell:
        """Get a cell from the grid using a tuple of (x, y) or a Vec2 instance.

        Where th key is out of bounds, return a Cell with location (-1, -1)
        and all walls.
        """
        try:
            if self.isvalid(key):
                x, y = key
                return self.grid[int(y)][int(x)]
            else:
                raise IndexError(f"Key {key} is out of bounds")
        except Exception:
            return Cell(Vec2(-1, -1))

    def isvalid(self, v: Vec2 | tuple[int, int] | Cell) -> bool:
        """Check if a Vec2 instance is within the bounds of the grid."""
        if isinstance(v, tuple):
            v = Vec2(*v)
        return (
            v.x is not None
            and v.y is not None
            and 0 <= v.x <= self.width
            and 0 <= v.y <= self.height
        )

    def __iter__(self) -> Generator[Cell, None, None]:
        """Iterate over all cells in the grid."""
        for y in self.grid:
            yield from y

    @classmethod
    def fill_grid_from_map(cls, hexlist: list[str], cfg: HasSize) -> "Grid":
        """Fill a grid from a list of lists of hex values repr walls."""
        c = cls(cfg.width, cfg.height)
        for y, row in enumerate(hexlist[1:]):
            if y < c.height:
                for x, i in enumerate(row):
                    if x < c.width:
                        c[x, y].wall = Dir(int(i))
        return c

    def dump_grid(self) -> list[list[str]]:
        """Produce a list(list(hex))to represent the currnet layof the grid."""
        hexlist = [[f"{hex(c.wall)[2:]}" for c in r] for r in self.grid]
        return hexlist

    def neighbour(self, pos: Vec2 | Cell) -> dict[Dir, Cell]:
        """Get four closest cells."""
        n: dict[Dir, Cell] = {}
        cell = self[pos]
        for d in (Dir.N, Dir.W, Dir.S, Dir.E):
            new_pos = cell.loc + d.v()

            if not self.isvalid(new_pos):
                continue

            candidate = self[new_pos]
            if candidate.loc != Vec2(-1, -1):
                n[d] = candidate
        return n

    def neighbour_walls(self, pos: Vec2 | Cell) -> dict[Dir, int]:
        """Get the wall values of the four closest cells."""
        n: dict[Dir, int] = {}
        for k, v in self.neighbour(pos).items():
            n[k] = v.wall
        return n

    def reset(self) -> None:
        """Reset all vistied values to false."""
        for row in self.grid:
            for cell in row:
                cell.visited = False

    def debug(self) -> str:
        """Debug string representation of a Grid instance."""
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
        """An evalutable string representation of a Grid instance."""
        cls = self.__class__.__name__
        return f"{cls}(width={self.width}, height={self.height})"

    def __str__(self) -> str:
        """String representation of a Grid instance."""
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
