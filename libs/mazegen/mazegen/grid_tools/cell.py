#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    cell.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/11 09:07:39 by maprunty         #+#    #+#              #
#    Updated: 2026/05/16 12:37:24 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Cell and Dir classes for maze generation and pathfinding."""

from collections.abc import Iterator
from enum import IntFlag

from .vector import Vec2


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

    @classmethod
    def from_str(cls, s: str) -> "Dir":
        """Return the Dir instance corresponding to a string."""
        return _DIR_FROM_STR[s]


_DIR_FROM_STR: dict[str, Dir] = {
    "N": Dir.N,
    "E": Dir.E,
    "S": Dir.S,
    "W": Dir.W,
    "A": Dir.A,
    "non": Dir.non,
}

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
        r_str += f"{vars(self)}"
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
