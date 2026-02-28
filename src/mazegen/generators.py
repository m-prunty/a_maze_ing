#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    generators.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/02/07 03:02:45 by maprunty         #+#    #+#              #
#    Updated: 2026/02/28 05:50:06 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import math
import random

from config import Config
from graphics import Render_cell, Render_grid
from helper import Cell, Dir, Grid, Path, Vec2
from abc import ABC, abstractmethod

class BaseGen(ABC):
    def __init__(self, cfg: Config) -> None:
        """TODO: init summary for Generators.

        Args:
            grid (Grid): Description.
        """
        self.config = cfg
        self.rng = random.Random(cfg.seed)

    @abstractmethod
    def generate(self, grid: Grid ):
        self.grid = grid
        self.entry_cell = self.grid[self.config.entry]
        self.exit_cell = self.grid[self.config.exit]

        self.open_entry_exit(self.entry_cell, self.grid)
        self.open_entry_exit(self.exit_cell, self.grid)

    @property
    def width(self):
        """Get WIDTH from config file."""
        return self.config.width

    @property
    def height(self):
        """Get HEIGHT from config file."""
        return self.config.height

    def open_entry_exit(self,cell: Cell, grid: Grid):
        """Open entry/exits gaps on border."""
        if cell:
            if cell.loc.x == 0:
                cell.rm_wall(Dir.W)
            elif cell.loc.x == grid.width - 1:
                cell.rm_wall(Dir.E)
            elif cell.loc.y == 0:
                cell.rm_wall(Dir.N)
            elif cell.loc.y == grid.height - 1:
                cell.rm_wall(Dir.S)
        else:
            print(Exception(f"cell={cell}; dosent exist"))



class DfsGen(BaseGen):
    def generate(self, grid: Grid):
        super().generate(grid)
        start = self.config.entry
        path = Path()
        yield from self._dfs(grid, path, start)

    def _dfs(self, grid: Grid, path: Path, pos: Vec2 = Vec2(0, 0)):
        """TODO: Docstring for gen_rand.

        Args:
            arg1 (TODO): TODO

        Returns: TODO

        """
        cell = grid[pos]
        cell.visited = True
        directions = list(cell.neighbours.items())
        self.rng.shuffle(directions)

        for direction, neighbour in directions:
            if not neighbour or neighbour.visited:
                continue
            cell.rm_wall(direction)
            neighbour.rm_wall(direction.opps())
            if not self.exit_cell.visited:
                if neighbour.loc == self.config.exit:
                    print("p>>>>> = ", grid.path, direction, path)
                    grid.path = path
                else:
                    path = path.add_rec(direction)
            yield neighbour.loc
            yield from self._dfs(grid, path, neighbour.loc)

class PicGen(BaseGen):

    def generate(self, grid: Grid):
        super().generate(grid)
        start = self.config.entry
        path = Path()
        yield from self._gen_pic(1)

    def _gen_pic(self, pic_scalar: int):
        """Prep for 42pic Check pic dimension against h / w.

        Calculate topleft and botright and passes to pic_lst

        Raises:
            ExceptionType: When this is raised.
        """
        # Render_grid.render_grid()

        self.config.get_pic(3)
        pic = self.config.pic
        wpic = int((math.log2(pic[0])) * (pic_scalar)) - 1
        hpic = int(len(pic) * pic_scalar)
        if self.width >= wpic + 2 and self.height >= hpic + 2:
            tleft = self.grid[
                int((self.width - wpic) / 2),
                int((self.height - hpic) / 2),
            ]
            bright = self.grid[tleft.loc + Vec2(wpic, hpic)]
            yield from self._pic_lst(tleft, bright, pic)

    def _pic_lst(self, tleft: Vec2, bright: Vec2, pic: list[bin]) -> list[Cell]:
        """Check and set if elements of subgrid from tleft to bright are ispic.

        gets a list of cells that will be ispic and steps through marking ispic
        as 1 for every 1 in the bitmask (self.pic)

        Args:
            tleft (Vec2): topleft coordinates of subgroup
            bright (Vec2): bottom right coordinates of subgroup
            pic (list[bin]): binary representation of a pic

        Returns:
            list[Cell]: subgroup of Cells within range(topleft, botright)

        Raises:
            ExceptionType: When this is raised.
        """
        delta = bright.loc - tleft.loc
        # print(tleft, bright, delta, self.config.width, self.config.height)
        r_lst: list[Cell] = []
        j = 0
        while j < delta.y:
            i = 0
            while i <= delta.x:
                curr = tleft.loc + (Dir.E.v() * i) + (Dir.S.v() * j)
                cell = self.grid[curr]
                r_lst.append(cell.loc)
                cell.ispic = pic[int(j / self.config.pic_scalar)] & (
                    1 << int((delta.x - i) / self.config.pic_scalar)
                )
                cell.visited = cell.ispic
                i += 1
            j += 1
        yield from r_lst

class PathGen(BaseGen):
    def generate(self, grid):
        super().generate(grid)
        yield from self._path()

    def _path(self):
        pos = self.config.entry
        #        print("lkjahskjdhjaslkjdlkj", len(self.grid.path))
        # self.grid.path_mk(pos)
        print("hjasgjdgj", self.grid.path)
        for dir_ in self.grid.path.path_yd_rev():
            print(">>>", pos)
            pos += dir_.v()
            yield pos
            # Render_cell.render(pos, canva)
            # rend.render_cell(pos, self.grid, 3, 1)


class PrimGen(BaseGen):
    def generate(self, grid):
        super().generate(grid)
        yield from self._prim()

    def _prim(self):
        head = self.entry_cell
        head.visited = True
        visited = {head}
        frontier = {v for k,v in head.neighbours.items() }
        while(frontier):
            cell = frontier.pop()
            print(cell)
            v = [k for k,c in cell.neighbours.items() if c and c.visited and not c.ispic]
            self.rng.shuffle(v)
            direction = v[0]
            neighbour = cell.neighbours[direction]

            cell.rm_wall(direction)
            neighbour.rm_wall(direction.opps())
            cell.visited = True

            visited |= {cell}
            frontier |= {*[n for n in cell.neighbours.values() if n and not n.visited ]}
            #print(frontier)
            yield frontier

class Generators:
    """TODO: Summary of the class.

    Optional longer descrgiption.

    Attributes:
        attr (type): Description.
    """

    def __init__(self, grid:Grid, cfg: Config):
        self.grid = grid
        self.config = cfg


    def gen_grid(self):
        """TODO: thes becomes open walls and give the hande to the animator"""
        pic = PicGen(self.config)
        [*pic.generate(self.grid)]

        #dfs = DfsGen(self.config)
        #[*dfs.generate(self.grid)]

        prim = PrimGen(self.config)
        [*prim.generate(self.grid)]
        
        path = PathGen(self.config)
        [*path.generate(self.grid)]
        # print()
        # print("Grid properly GENEATED")
        # self.animate_path(canva, 0.0)
        # print(self.config.exit)
