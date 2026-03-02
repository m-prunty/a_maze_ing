#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    generators.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/02/07 03:02:45 by maprunty         #+#    #+#              #
#    Updated: 2026/03/01 05:01:02 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import math
import random
from typing import Protocol, Any

from config import Config
from graphics import Render_cell, Render_grid
from helper import Cell, Dir, Grid, Path, Vec2
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class MazeEvent:
    cell: Cell
    parent: Cell| None = None
    _dir: Dir| None = None
    config: Config| None = None

class BaseStage(Protocol):
    def generate(self, e: MazeEvent) -> Any:
        pass

class IOStage:

    def generate(self, e: MazeEvent) -> Any:
        self._open_entry_exit(e.cell)
        return e 


class MkStage:
    MKDCT = {
            Dir.N:  "visited",
            Dir.S:  "ispic",
            Dir.E:  "visited",
            Dir.W:  "visited",
             }

    def generate(self, e: MazeEvent) -> Any:
        attr = self.MKDCT[e._dir] if e._dir else ""
        setattr(e.cell, attr, True)
        return e.cell




class GenStage:
    def generate(self, e: MazeEvent) -> Any:
        e.cell.rm_wall_nb(e._dir)
        return e.cell


class BaseGen(ABC):
    def __init__(self, cfg: Config) -> None:
        """TODO: init summary for Generators.

        Args:
            grid (Grid): Description.
        """
        self.config = cfg
        self.rng = random.Random(0)#cfg.seed)
        self.stages: list[BaseStage] = []

    def add_stage(self, stage: BaseStage) -> None:
        self.stages.append(stage)


    @abstractmethod
    def generate(self, grid: Grid ):
        self.grid = grid
        self.entry_cell = self.grid[self.config.entry]
        self.exit_cell = self.grid[self.config.exit]
        self._open_entry_exit(self.entry_cell)
        self._open_entry_exit(self.exit_cell)
        #print(">>", [s for s in self.stages])
        #print(self.stages[0])
    
    def _dispatch(self, event: MazeEvent):
        for stage in self.stages:
            stage.generate(event)

    def _open_entry_exit(self,cell: Cell):
        """Open entry/exits gaps on border."""
        if cell and not cell.visited:
            if cell.loc.x == 0:
                cell.rm_wall(Dir.W)
            elif cell.loc.x == self.grid.width - 1:
                cell.rm_wall(Dir.E)
            elif cell.loc.y == 0:
                cell.rm_wall(Dir.N)
            elif cell.loc.y == self.grid.height - 1:
                cell.rm_wall(Dir.S)
            #cell.visited = True
        else:
            print(Exception(f"cell={cell}; dosent exist"))

    @property
    def width(self):
        """Get WIDTH from config file."""
        return self.config.width

    @property
    def height(self):
        """Get HEIGHT from config file."""
        return self.config.height



class DfsGen(BaseGen):
    def generate(self, grid: Grid):
        super().generate(grid)
        start = self.config.entry
        path = Path()
        yield from self._dfs(grid, start)

    def _dfs(self, grid: Grid, pos: Vec2 = Vec2(0, 0)):
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

            self._dispatch(MazeEvent(cell, neighbour, direction))
            yield neighbour.loc
            yield from self._dfs(grid, neighbour.loc)

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
        wpic = int(math.log2(max(pic)) * (pic_scalar)) - 1 
        hpic = int(len(pic) * pic_scalar)
        #print("pic>>>>", wpic, self.width, pic_scalar)
        mx = max(wpic, hpic)
        mn = min(self.height, self.width)
        #print(mx, int(mn / 5) * 3)
        if ( mx < int(mn / 5) * 3):
            pic_scalar = int(((mn / 5) * 3 )/ mx) 
            wpic = int((math.log2(max(pic))) * (pic_scalar)) - 1 
            hpic = int(len(pic) * pic_scalar)
        self.config.pic_scalar = pic_scalar

        #print("pic>>>>", wpic, self.width, pic_scalar)
        #print("pic>>>>", hpic, self.height)
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
                #cell.ispic = pic[int(j / self.config.pic_scalar)] & (
                #    1 << int((delta.x - i) / self.config.pic_scalar)
                #)
                if pic[int(j / self.config.pic_scalar)] & (
                    1 << int((delta.x - i) / self.config.pic_scalar)
                    ):
                    self._dispatch(MazeEvent(cell=cell,_dir=Dir.N))
                    self._dispatch(MazeEvent(cell=cell,_dir=Dir.S))
                #cell.visited = cell.ispic
                i += 1
            j += 1
        yield from r_lst

# class PathGen(BaseGen):
#    def generate(self, grid):
#        super().generate(grid)
#        yield from self._path()
# 
#    def _path(self):
#        from time import time 
#        pos = self.config.entry
#        self.grid[pos].ispath = True 
#        for dir_ in self.grid.path.path_yd_rev():
#            print(">>>", pos)
#            self.grid[pos].ispath = True 
#            yield self.grid[pos]
#            pos += dir_.v()
# 

class PrimGen(BaseGen):
    """Prims Algo.

https://en.wikipedia.org/wiki/Prim%27s_algorithm
chatgpt.com
Core Idea

Maintain frontier cells:
- Pick random frontier
- Connect to random visited neighbor

Properties
- Many short branches
- Very “organic” look
- More uniform density than DFS
- Still perfect maze

Complexity
- Time: O(N)
- Space: O(N)

Good For
- Balanced maze feel
- Less corridor bias than DFS
    """
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
            #print(cell)
            v = [k for k,c in cell.neighbours.items() if c and c.visited and not c.ispic]
            #print(v)
            self.rng.shuffle(v)
            direction = v[0] if len(v) else None 
            neighbour = cell.neighbours[direction] if direction else None

            self._dispatch(MazeEvent(cell,neighbour, direction))
            cell.visited = True

            visited |= {cell}
            frontier |= {*[n for n in cell.neighbours.values() if n and not n.visited ]}
            #print(frontier)
            yield frontier

class Sidewinder(BaseGen):
    def generate(self, grid):
        super().generate(grid)
        yield from self._sidewind()

    def _sidewind(self):
        """
        function generate_sidewinder(grid):

    for each row y in grid:

        run = empty list

        for each cell x in row:

            current = grid[x, y]
            add current to run

            at_eastern_boundary = (x == grid.width - 1)
            at_northern_boundary = (y == 0)

            should_close_run =
                at_eastern_boundary OR
                (NOT at_northern_boundary AND random_boolean())

            if should_close_run:

                choose random cell from run → member

                if NOT at_northern_boundary:
                    carve passage from member to NORTH

                clear run

            else:
                carve passage EAST from current
        """
        start = self.config.entry
        run = [self.grid[start]]
        e_bound = (lambda v: v.x == self.width - 1 )
        n_bound = (lambda v: 0 == v.y )
        for cell in self.grid:
            run.append(cell)
            close = ((e_bound(cell.loc)) or 
            (not n_bound(cell.loc) and bool(self.rng.getrandbits(1))))
            self.rng.shuffle(run)
            r = run.pop()
            if not r.ispic:
                if (close):
                    if (Dir.N in r.neighbours.keys() and r.neighbours[Dir.N] and not r.neighbours[Dir.N].ispic):
                        neighbour = r.neighbours[Dir.N]
                        r.rm_wall(Dir.N)
                        neighbour.rm_wall(Dir.N.opps())
                    run= []
                else:
                    neighbour = r.neighbours[Dir.E]
                    if neighbour and not neighbour.ispic:
                        r.rm_wall(Dir.E)
                        neighbour.rm_wall(Dir.E.opps())
            cell.visited = True
            yield cell

class WilsonGen(BaseGen):
    def generate(self, grid):
        super().generate(grid)
        yield from self._wilson()

    def _wilson(self):
        current = self.grid[self.config.entry]
        ngrid = {*self.grid}
        path= {current: None, "walls": Path()}
        print("\n\n>>>>", type(ngrid))
        while (len(ngrid) and current):
            n = [*current.neighbours]
            self.rng.shuffle(n)
            next_cell = current.neighbours[n[0]]
            if (next_cell and next_cell not in path):
                path[current] = next_cell
                path["walls"] += next_cell.wall
                current.visited = True
                ngrid.discard(current)
            else:
                path, r_set = self._rewind(path, next_cell)
                ngrid |= r_set
            current = next_cell
            #print("\n\n>>>>", ngrid)
            yield current 

    def _rewind(self, path, current):
        curr = current
        r_set: set = set()
        while (curr in path):
            tmp = curr
            print(curr)
            curr = path[curr]
            print("pop",path.pop(tmp))
            curr.visited = False
        return (path, r_set)




        

class Generators:
    """TODO: Summary of the class.

    Optional longer descrgiption.

    Attributes:
        attr (type): Description.
    """
    ADAPT = {"dfs": DfsGen,
             "prim": PrimGen,
             "swinder":Sidewinder,
             "wilson":WilsonGen,
             }

    def __init__(self, grid:Grid, cfg: Config):
        self.grid = grid
        self.config = cfg
        #self.adapters = 

    def gen_grid(self):
        """TODO: thes becomes open walls and give the hande to the animator"""
        pic = PicGen(self.config)
        pic.add_stage(MkStage())
        [*pic.generate(self.grid)]

        #dfs = DfsGen(self.config)
        #dfs.add_stage(GenStage())
        #[*dfs.generate(self.grid)]

        prim = PrimGen(self.config)
        #prim.add_stage(MkStage())
        prim.add_stage(GenStage())
        [*prim.generate(self.grid)]
        
        #swinder = Sidewinder(self.config)
        #[*swinder.generate(self.grid)]
 #       wilson = WilsonGen(self.config)
 #       [*wilson.generate(self.grid)]

        #path = PathGen(self.config)
        #[*path.generate(self.grid)]
        # print()
        # print("Grid properly GENEATED")
        # self.animate_path(canva, 0.0)
        # print(self.config.exit)
