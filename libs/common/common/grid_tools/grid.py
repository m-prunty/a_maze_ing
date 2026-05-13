#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    grid.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:38:19 by maprunty         #+#    #+#              #
#    Updated: 2026/05/12 09:40:17 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Grid class to represent a 2D grid of Cell instances."""

from collections.abc import Generator
from typing import Protocol

from .cell import Cell, Dir
from .vector import Vec2


class HasSize(Protocol):
    """Protocol for objects that have width and height attributes."""

    width: int
    height: int


class Grid:
    """Grid class has a width, height, and a 2D list of Cell instances."""

    def __init__(self, width: int, height: int):
        """Init a grid with the given width and height of Cell instances."""
        self.width, self.height = width, height
        self.path: list[Vec2] = []

    def fill_empty_grid(self) -> None:
        """Fill a grid with empty Cell instances."""
        print(f"Creating grid of size {self.width}x{self.height}")
        self.grid = [
            [Cell(Vec2(x, y)) for x in range(self.width)]
            for y in range(self.height)
        ]

    def fill_grid_from_map(self, hexlist: list[str]) -> None:
        """Fill a grid from a list of lists of hex values repr walls."""
        print(f"Populating grid of size {self.width}x{self.height}")
        for y, row in enumerate(hexlist[1 : self.height + 1]):
            if y < self.height:
                for x, i in enumerate(row):
                    if x < self.width:
                        self[x, y].wall = Dir(int(i, 16))
                        if self[x, y].wall == Dir.A:
                            self[x, y].ispic = True
        self.path_from_str(hexlist[-1])

    def path_from_str(self, s: str) -> None:
        """Create a path from a string of directions."""
        print(f"Creating path from string: {s}")
        pos = self.path[0]
        for c in s:
            delta = Dir.from_str(c).v()
            pos = Vec2(pos.x + delta.x, pos.y + delta.y)
            self.path.append(pos)
        print(f"Path from string: {self.path}")

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

    def __iter__(self) -> Generator[Cell, None, None]:
        """Iterate over all cells in the grid."""
        for y in self.grid:
            yield from y

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
