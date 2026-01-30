#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    a.py                                              :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/24 07:55:50 by maprunty         #+#    #+#              #
#    Updated: 2026/01/25 12:14:11 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""First attempts at the A-Maze-ing project."""
from math import sqrt
import random as random
from graphics.render import Render
import time
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

    def __eq__(self, other):
        """Equate a vec2 instance with another."""
        return (self.x == other.x and 
                self.y == other.y)
    
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



class Cell():
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
        N: (0, -1),
        E: (1, 0),
        S: (0, 1),
        W: (-1, 0),
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
        self.visited = False 

    def __str__(self):
        r_str = f"{self.loc} "
        r_str += f"{bin(self.wall)}"
        return r_str
   
    @property
    def loc(self) -> Vec2:
        """doc"""
        return self._loc
    
    @loc.setter
    def loc(self, value: Vec2):
        self._loc = value
    
    @property
    def visited(self) -> bool:
        """doc"""
        return self._visited
    
    @visited.setter
    def visited(self, value: bool):
        self._visited = value
    
    def has_wall(self, direction):
        return self.wall & direction

    def add_wall(self, direction):
        self.wall |= direction

    def rm_wall(self, direction):
        self.wall &= ~direction


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
            x, y = key
            if (0 <= x < self.width and  0 <= y < self.height):
                return self.grid[y][x]
            else:
                raise ValueError(f"\
{x} or {y} is out of range {self.width},{self.height}")
                return None
        except ValueError as ve:
            print(f"Grid key error:{key} not a valid tuple {ve}")
    
    def __str__(self, cursor=None):
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
                if cursor == cell.loc:
                    r_str += " @ "
                else:
                    r_str += "   "
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


class A_Maze:
    """Docstring for A_Maze."""

    def __init__(self, cfg: dict):
        """TODO: to be defined."""
        self.config = cfg
        self.startup()
        self.gen_rand()
        self.animate(self.grid, 0.02)
    
    @staticmethod
    def gen_rand(grid: Grid, cfg: dict, pos: tuple = (0,0)):
        """TODO: Docstring for gen_rand.

        Args:
            arg1 (TODO): TODO

        Returns: TODO

        """
        cell = grid[pos]
        cell.visited = True
        directions = list(Cell.DIRS.items())
        random.shuffle(directions)
        def open_entry_exit(cell):
            print("EXIT\n\n>>>>>", cell.loc, grid.width, grid.height, "\n",
                  cell.loc.x == grid.width - 1,  cell.loc.y == grid.height - 1)
            if cell.loc.x == 0:
                cell.rm_wall(Cell.W)
            elif cell.loc.x == grid.width - 1:
                cell.rm_wall(Cell.E)
            elif cell.loc.y == 0:
                cell.rm_wall(Cell.N)
            elif cell.loc.y == grid.height - 1:
                cell.rm_wall(Cell.S)

        if (cell.loc == grid[cfg["ENTRY"]].loc):
            print(">>>>>", cell)
            open_entry_exit(cell)
        if (cell.loc == grid[cfg["EXIT"]].loc): 
            print("EXIT\n\n>>>>>", cell)
            open_entry_exit(cell)

        for direction, (dx, dy) in directions:
            neighbour = grid[cell.loc + Vec2(dx, dy)]
            if not neighbour or neighbour.visited:
                continue
            cell.rm_wall(direction)
            neighbour.rm_wall(Cell.OPPS[direction])
            A_Maze.gen_rand(grid, cfg, neighbour.loc)

    @staticmethod
    def open_entry_exit(cell: Cell, directions: dict):
        for direction, (dx, dy) in directions:
            neighbour = Grid[cell.loc + Vec2(dx, dy)]
            if not neighbour:
                cell.rm_wall(direction)
                return

    def animate(self, grid, delay=0.01):
        # ANSI clear screen + cursor home
        CLEAR = "\x1b[2J\x1b[H"
        for pos in self.gen_rand(self.grid, self.config, self.config["ENTRY"]):
            print(CLEAR, end="")
            print(self.grid.__str__(pos))
            cell = self.grid[pos[0], pos[1]]
            hex_walls = cell.wall
            rend.render_cell(hex_walls, pos[0], pos[1])
            time.sleep(delay)

    def startup(self):
        self.grid = Grid(self.width, self.height)
        rend.init_grid(Vec2(self.width, self.height))
        

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

rend = Render()
def main():
    """Drive the main loop."""
    av = sys.argv
    ac = len(av)
    rend.init_window(900, 900, "hello")
    rend.init_grid(Vec2(3, 3))
    print(rend.generate_grid_sprits())
    print(rend.cell_siz)
    rend.add_hook(rend.close, 33, None)
    if 1 <= ac <= 2:
        a = A_Maze.cfg_from_file("config.txt")
        print(a.config)
        print("yay")
    rend.launch()

if __name__ == "__main__":
    main()
