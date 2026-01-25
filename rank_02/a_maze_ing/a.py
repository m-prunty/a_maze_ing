#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    a.py                                              :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/24 07:55:50 by maprunty         #+#    #+#              #
#    Updated: 2026/01/25 07:10:24 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""First attempts at the A-Maze-ing project."""
from math import sqrt
import sys


class Vec2():
    """Class for storing 2D Coords."""

    def __init__(self, x: int = 0, y: int = 0):
        """TODO: to be defined."""
        self.x = 0
        self.y = 0
        try:
            self.x = x
            self.y = y
        except Exception as e:
            print(e)
            # raise ValueError(e)

    def __add__(self, other):
        """Add a vec2 instance with another."""
        return Vec2(self.x + other.x,
                    self.y + other.y,
                    )

    def __sub__(self, other):
        """Sub a vec2 instance with another."""
        return Vec2(self.x - other.x,
                    self.y - other.y,
                    )

    def __abs__(self):
        """Return magnitude of a vector."""
        return sqrt(self.x**2 + self.y**2)

    def __repr__(self):
        """Return a tuple represantation of a Vec2 instance."""
        return (self.x, self.y)

    def __str__(self):
        """Return a str tuple represantation of a Vec2 instance."""
        return f"{self.__repr__()}"

    def __iter__(self):
        """Return a tuple iterable  represantation of a Vec2 instance."""
        return iter(self.__repr__())

    @property
    def x(self) -> int:
        """doc."""
        return self._x

    @x.setter
    def x(self, value: int):
        try:
            self._x = int(value)
        except ValueError as ve:
            r_str = (f"Error parsing coordinates: {ve}")
            self._x = 0
            raise ValueError(r_str)

    @classmethod
    def from_str(cls, coord: str) -> "Vec2":
        """TODO: Docstring for from_str.

        Args:
            coord (str): coordinates in form "x,y,z"

        Returns: An instance of Vec2

        """
        try:
            lst = [0]
            lst += cls.ft_split(coord, ",")
            lst = cls.parse_args(len(lst), lst)
            return cls(lst[0], lst[1])
        except Exception as e:
            r_str = (f"Error details - Type: {e.__class__.__name__}")
            r_str += (f", Args: (\"{e.args[0]}\",)")
            raise ValueError(r_str)

    @classmethod
    def assign_coord(cls, lst: list[int]):
        """Docstring for assign_coord.

        Args:
            lst (list [int]): TODO

        Returns: TODO

        """
        print(len(lst), lst)
        try:
            if len(lst) > 3:
                raise ValueError
            cls.x: int = lst[0]
            cls.y: int = lst[1]
            cls.z: int = lst[2]
        except ValueError as ve:
            print(f"ierr>>>{ve}")
        except IndexError as ie:
            print(f"ierr>>>{ie}")

    @staticmethod
    def parse_args(ac: int, av: list) -> list[int]:
        """TODO: Docstring for get_args.

        Args:
            ac (int): TODO
            av (list):
        Returns: TODO

        """
        i = 1
        r_lst = []
        while i < ac:
            try:
                r_lst += [int(av[i])]
            except ValueError as ve:
                r_str = (f"Error parsing coordinates: {ve}")
                raise ValueError(r_str)
            i += 1
        return r_lst


class Cell():
    """Docstring for Cell.

    wall is a 4-bit represantaion. i.e
    0000 has all walls
    0100 has one opening to south
    """

    N = 1 << 0
    E = 1 << 1
    S = 1 << 2
    W = 1 << 4
    
    def __init__(self, loc: Vec2):
        """TODO: to be defined."""
        self.wall = int(b'1111')
        self.loc = loc
        print(self.loc)

    def __str__(self):
        r_str = f"{self.loc}"
        r_str += f"{self.wall}"
        return r_str
   
    @property
    def loc(self) -> Vec2:
        """doc"""
        return self._loc
    
    @loc.setter
    def loc(self, value: Vec2):
        self._loc = value

    def has_wall(self, direction):
        return self.wall & direction

    def add_wall(self, direction):
        self.wall |= direction

    def rm_wall(self, direction):
        self.wall &= direction


class Grid(object):
    """Docstring for Grid."""
    
    def __init__(self, width, height):
        """TODO: to be defined."""
        self.grid = [[Cell(Vec2(x, y)) for x in range(width)]
                     for y in range(height)]
        self.width = width
        self.height = height

    def __getitem__(self, key):
        try:
            x, y = tuple(key)
            if 0 <= x < self.width and  0 <= y < self.height:
                return self.grid[y][x]
            else:
                raise ValueError(f"\
{x} or {y} is out of range {self.height},{self.width}")
        except ValueError as ve:
            print(f"Grid key error:{key} not a valid tuple {ve}")

    def __str__(self):
        r_str = "+"
        r_str += '+'.join("---" for x in range(self.width))
        r_str += "+\n"
        for y in range(self.height):
            for x in range(self.width):
                cell = self[x, y]
                if cell.has_wall(Cell.W):
                    r_str += "|"
                else:
                    r_str += " "
                r_str += "   "
            r_str += "|\n"
            for x in range(self.width):
                cell = self[x, y]
                r_str += "+"
                if cell.has_wall(Cell.S):
                    r_str += "---"
                else:
                    r_str += "   "
            r_str += "+\n"
        return r_str

    @staticmethod
    def gen_rand(grid, cfg: dict):
        """TODO: Docstring for gen_rand.

        Args:
            arg1 (TODO): TODO

        Returns: TODO

        """
        pass

class A_Maze:
    """Docstring for A_Maze."""

    def __init__(self, cfg: dict):
        """TODO: to be defined."""
        self.config = cfg
        self.startup()
        print(self.grid)

    def startup(self):
        self.grid = Grid(self.width, self.height)

    @property
    def width(self):
        return self.config["WIDTH"]

    @property
    def height(self):
        return self.config["HEIGHT"]

    @classmethod
    def cfg_from_file(cls, filename: str):
        """TODO: Docstring for from_fil.

        Args:
            s (str): TODO

        Returns: TODO

        """
        c_dct = {"FILENAME": filename}
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    k, v = line.split('=')
                    k = k.strip().upper()
                    try:
                        if ',' in v:
                            v = v.split(',')
                            v = tuple(int(i) for i in v)
                        elif v.lower() in ("true", "false"):
                            v = v.lower() == "true"
                        elif v.isnumeric():
                            v = int(v)
                    except ValueError as ve:
                        print(f"Error: {ve} something's not right with config\
                              {k}:{v} ")
                    c_dct.update({k: v})
        return cls(c_dct)


def main():
    """Drive the main loop."""
    av = sys.argv
    ac = len(av)
    if 1 <= ac <= 2:
        a = A_Maze.cfg_from_file("config.txt")
        print(a.config)
        print("yay")


if __name__ == "__main__":
    main()
