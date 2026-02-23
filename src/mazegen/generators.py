#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    generators.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/02/07 03:02:45 by maprunty         #+#    #+#              #
#    Updated: 2026/02/22 17:17:05 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import math
import random

from config import Config
from graphics import Render_cell, Render_grid
from helper import Cell, Dir, Grid, Path, Vec2


class Generators:
    """TODO: Summary of the class.

    Optional longer descrgiption.

    Attributes:
        attr (type): Description.
    """

    def __init__(self, grid: Grid, cfg: Config) -> None:
        """TODO: init summary for Generators.

        Args:
            grid (Grid): Description.
        """
        self.grid = grid
        self.config = cfg

    @property
    def width(self):
        """Get WIDTH from config file."""
        return self.config.width

    @property
    def height(self):
        """Get HEIGHT from config file."""
        return self.config.height

    @staticmethod
    def gen_rand(grid: Grid, cfg: Config, path: Path, pos: Vec2 = Vec2(0, 0)):
        """TODO: Docstring for gen_rand.

        Args:
            arg1 (TODO): TODO

        Returns: TODO

        """
        cell = grid[pos]
        cell.visited = True
        directions = list(cell.neighbours.items())
        random.shuffle(directions)

        for direction, neighbour in directions:
            if not neighbour or neighbour.visited:
                continue
            cell.rm_wall(direction)
            neighbour.rm_wall(direction.opps())

            if neighbour.loc == cfg.exit:
                print("p>>>>> = ", grid.path, direction, path)
                grid.path = path
            else:
                path = path.add_rec(direction)
            yield neighbour.loc
            yield from Generators.gen_rand(grid, cfg, path, neighbour.loc)

    def animate_path(self, canva, delay):
        pos = self.config.entry
        #        print("lkjahskjdhjaslkjdlkj", len(self.grid.path))
        # self.grid.path_mk(pos)
        print("hjasgjdgj", self.grid.path)
        for dir_ in self.grid.path.path_yd_rev():
            print(">>>", pos)
            pos += dir_.v()
            Render_cell.render(pos, canva, delay)
            # rend.render_cell(pos, self.grid, 3, 1)

    def gen_42(self, pic: list[bin], pic_scalar: int):
        """Prep for 42pic Check pic dimension against h / w.

        Calculate topleft and botright and passes to pic_lst

        Raises:
            ExceptionType: When this is raised.
        """
        Render_grid.render_grid()

        self.config.get_pic(1)
        pic = self.config.pic
        wpic = int((math.log2(pic[0])) * (pic_scalar))
        hpic = int(len(pic) * pic_scalar)
        if self.width >= wpic + 2 and self.height >= hpic + 2:
            tleft = self.grid[
                int((self.width - wpic) / 2),
                int((self.height - hpic) / 2),
            ]
            bright = self.grid[tleft.loc + Vec2(wpic, hpic)]
            self.pic_lst(tleft, bright, pic)

    def pic_lst(self, tleft: Vec2, bright: Vec2, pic: list[bin]) -> list[Cell]:
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
        r_lst: list[list[Cell]] = [[] for x in range(delta.y)]
        j = 0
        while j < delta.y:
            r_lst[j]: list[Cell] = []
            i = 0
            while i <= delta.x:
                curr = tleft.loc + (Dir.E.v() * i) + (Dir.S.v() * j)
                cell = self.grid[curr]
                cell.ispic = pic[int(j / self.config.pic_scalar)] & (
                    1 << int((delta.x - i) / self.config.pic_scalar)
                )
                cell.visited = cell.ispic
                i += 1
            j += 1
        return r_lst

    def open_entry_exit(cell: Cell, grid: Grid):
        """Open entry/exits gaps on border."""
        if cell:
            if cell.loc.x == 0:
                cell.rm_wall(Dir.W)
            elif cell.loc.x == grid.width - 1:
                cell.rm_wall(Dir.E)
            if cell.loc.y == 0:
                cell.rm_wall(Dir.N)
            elif cell.loc.y == grid.height - 1:
                cell.rm_wall(Dir.S)
        else:
            print(Exception(f"cell={cell}; dosent exist"))

    def neighbour(self, pos: Vec2) -> dict[list[Cell]]:
        """TODO: Docstring."""
        neighbours: dict[list[Cell]] = {}
        for k, v in Cell.DIRS.items():
            try:
                neighbours.update({k: self[v + pos].wall})
            except AttributeError:
                print("Not a neighbour:{k}, {v}: {ae}")
        return neighbours

    def animate(self, current, delay=0.001):
        """TODO: Docstring."""
        # ANSI clear screen + cursor home
        CLEAR = "\x1b[2J\x1b[H"
        # print(self.grid)
        # print(self.config.exit)
        Generators.open_entry_exit(self.grid[self.config.entry], self.grid)
        Generators.open_entry_exit(self.grid[self.config.exit], self.grid)
        canva = Render_grid.cells_canva(
            Vec2(self.grid.width, self.grid.height), Vec2()
        )
        self.gen_42(self.config.pic, self.config.pic_scalar)
        random.seed(self.config.seed)
        pos = self.grid[current].loc
        # print("pos is")
        # print(pos)
        Render_cell.render(pos, canva, delay)

        random.seed(42)

        for pos in self.gen_rand(self.grid, self.config, self.grid.path, pos):
            Render_cell.render(pos, canva, delay)
        # time.sleep(delay)
        self.animate_path(canva, delay)
        print(self.grid.path)
        canva.put_canva()
        # print(self.config.exit)
