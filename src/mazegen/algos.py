#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    algos.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/01 08:04:43 by maprunty         #+#    #+#              #
#    Updated: 2026/05/01 21:30:00 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import math
import random
from abc import ABC, abstractmethod

from common.config import Config
from common.grid_tools import Cell, Dir, Path, Vec2

from .graph import Graph
from .staging import (
    BaseStage,
    EType,
    MazeEvent,
)


class BaseStrat(ABC):
    """Base strategy for maze generation and pathfinding."""

    def __init__(self, graph: Graph, cfg: Config) -> None:
        """Initializes BaseStrat with a graph and config."""
        self.config = cfg
        self.rng = (
            random.Random() if cfg.seed == 0 else random.Random(cfg.seed)
        )
        self.stages: list[BaseStage] = []
        self.graph = graph
        self.grid = graph.grid
        self._n_imperfect = ((self.width * self.height) ** 0.7) * int(
            not self.config.perfect
        )
        print(f"n_imperfect: {self._n_imperfect}")

    def add_stage(self, stage: BaseStage) -> None:
        """Adds a stage to the strategy."""
        self.stages.append(stage)

    @abstractmethod
    def generate(self):
        """Generates a maze or path."""
        self.entry_cell = self.grid[self.config.entry]
        self.exit_cell = self.grid[self.config.exit]
        self._open_entry_exit(self.entry_cell)
        self._open_entry_exit(self.exit_cell)
        self._imperfect()

    def _imperfect(self) -> None:
        """Carve random walls to make maze imperfect."""
        while self._n_imperfect >= 0:
            cell = self.entry_cell
            while cell in (self.entry_cell, self.exit_cell) or cell.ispic:
                cell = self.grid[
                    (
                        self.rng.randint(0, self.width - 1),
                        self.rng.randint(0, self.height - 1),
                    )
                ]
            n_lst = [
                n[0]
                for n in self.graph.neighbours(cell)
                if n[1] and not n[1].ispic
            ]
            print(cell.ispic, n_lst, not n_lst)
            self.rng.shuffle(n_lst)
            if n_lst:
                n = self.rng.randint(1, len(n_lst))
                for _ in n_lst[:n]:
                    cell.rm_wall_nb(_)
            self._n_imperfect -= 1

    def _dispatch(self, event: MazeEvent) -> bool:
        """Dispatches a maze event to all stages.

        Return: True if all stages accept the event, False if stage rejects it.
        """
        for stage in self.stages:
            result = stage.process(event)
            if result is False:
                return False
        return True

    def _open_entry_exit(self, cell: Cell):
        """Open entry/exits gaps on border."""
        if cell:
            if cell.loc.x == 0:
                cell.rm_wall(Dir.W)
            elif cell.loc.x == self.grid.width - 1:
                cell.rm_wall(Dir.E)
            elif cell.loc.y == 0:
                cell.rm_wall(Dir.N)
            elif cell.loc.y == self.grid.height - 1:
                cell.rm_wall(Dir.S)
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


class Dfs(BaseStrat):
    """Depth-first search maze generation."""

    def generate(self):
        """Generates a maze using depth-first search."""
        super().generate()
        self._imperfect()
        start = self.config.entry
        yield from self._dfs(start)

    def _dfs(self, pos: Vec2 = Vec2):
        """TODO: Docstring for gen_rand.

        Args:
            arg1 (TODO): TODO

        Returns: TODO

        """
        cell = self.grid[pos]
        enter = MazeEvent(cell, etype=EType.ENTER)
        if not self._dispatch(enter):
            return enter.found
        directions = [*self.graph.neighbours(cell)]
        self.rng.shuffle(directions)

        for direction, neighbour in directions:
            if not neighbour:
                continue
            e = MazeEvent(cell, neighbour, direction, EType.EDGE)
            if not self._dispatch(e):
                continue
            yield neighbour.loc
            if (yield from self._dfs(neighbour.loc)):
                return True
        back = MazeEvent(cell, etype=EType.EXIT)
        self._dispatch(back)
        return False


class Dijkstra(BaseStrat):
    """PSuuedocode https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm.

        1  function Dijkstra(Graph, source):
         2
         3      for each vertex v in Graph.Vertices:
         4          dist[v] ← INFINITY
         5          prev[v] ← UNDEFINED
         6          add v to Q
         7      dist[source] ← 0
         8
         9      while Q is not empty:
        10          u ← vertex in Q with minimum dist[u]
        11          Q.remove(u)
        12
        13          for each edge (u, v) in Graph:
        14              alt ← dist[u] + Graph.Distance(u,v)
        15              if alt < dist[v]:
        16                  dist[v] ← alt
        17                  prev[v] ← u
        18
        19      return dist[], prev[]

    procedure uniform_cost_search(start) is
        node ← start
        frontier ← priority queue containing node only
        expanded ← empty set
        do
            if frontier is empty then
                return failure
            node ← frontier.pop()
            if node is a goal state then
                return solution(node)
            expanded.add(node)
            for each of node's neighbors n do
                if n is not in expanded and not in frontier then
                    frontier.add(n)
                else if n is in frontier with higher cost
                    replace existing node with n
    """

    def generate(self):
        super().generate()
        self._imperfect()
        start = self.config.entry
        yield from self._dijks(start)

    def _dijks(self, pos: Vec2 = Vec2):
        node: Cell = self.grid[pos]
        frontier: list[Cell] = [(0, node)]
        expanded: set[Cell] = set()

        parent: dict[Cell, Cell] = {node: None}
        while True:
            if not frontier:
                return False
            i = min(frontier, key=lambda f: f[0])
            frontier.remove(i)
            cost, node = i

            if node in expanded:
                continue
            enter = MazeEvent(cell=node, etype=EType.ENTER)
            if not self._dispatch(enter):
                break
            expanded.add(node)
            for direction, neighbour in self.graph.neighbours(node):
                if not neighbour:
                    continue
                e = MazeEvent(node, neighbour, direction, EType.EDGE)
                if not self._dispatch(e):
                    continue

                if neighbour not in expanded:
                    _neighbour = next(
                        (f for f in frontier if f[1] == neighbour), None
                    )
                    if not _neighbour:
                        frontier.append((cost + 1, neighbour))
                    elif _neighbour[0] > (cost + 1):
                        frontier.remove(_neighbour)
                        frontier.append((cost + 1, neighbour))
                    parent[neighbour] = node
            back = MazeEvent(node, etype=EType.EXIT)
            self._dispatch(back)
        cell = parent[self.exit_cell]
        while cell != self.entry_cell:
            yield cell
            cell = parent[cell]


class Pic(BaseStrat):
    def generate(self):
        super().generate()
        # start = self.config.entry
        yield from self._gen_pic(self.config.pic_scalar)

    @staticmethod
    def get_pic(select: int) -> list[int]:
        """Get the picture data for the maze based on the selected option."""
        if select == 1:
            pic = [
                0b1010111,
                0b1010001,
                0b1110111,
                0b0010100,
                0b0010111,
            ]
        elif select == 2:
            pic = [
                0b001111010001011101110111,
                0b001101011111010100010100,
                0b001111010101011100100111,
                0b001101010101010101000100,
                0b001101010101010101110111,
            ]
        elif select == 3:
            pic = [
                0b000000011110000011111111,
                0b000001111100001110000111,
                0b000111001100000000011100,
                0b011100111000000011100000,
                0b111111111100011100000000,
                0b000011100001110000000000,
                0b000111000111111110110000,
            ]
        else:
            pic = [0b1111111, 0b1000001, 0b1011101, 0b1010101, 0b1010111]
        print(f"== PIC SELECTED: {select} ==")
        print(pic)
        return pic

    def _gen_pic(self, pic_scalar: int):
        """Prep for 42pic Check pic dimension against h / w.

        Calculate topleft and botright and passes to pic_lst

        Raises:
            ExceptionType: When this is raised.
        """
        try:
            if not self.grid.pic:
                raise Exception("No picture data found in grid.")
        except Exception as e:
            print(f"Error in _gen_pic: {e}")
        pic = self.grid.pic
        wpic = int(math.log2(max(pic)) * (pic_scalar)) - 1
        hpic = int(len(pic) * pic_scalar)
        mx = max(wpic, hpic)
        mn = min(self.height, self.width)
        if mx < int(mn / 5) * 3:
            pic_scalar = int(((mn / 5) * 3) / mx)
            wpic = int((math.log2(max(pic))) * (pic_scalar))
            hpic = int(len(pic) * pic_scalar)
        self.config.pic_scalar = pic_scalar

        if self.width >= wpic + 2 and self.height >= hpic + 2:
            tleft = self.grid[
                int((self.width - wpic) / 2),
                int((self.height - hpic) / 2),
            ]
            bright = self.grid[tleft.loc + Vec2(wpic, hpic)]
            yield from self._pic_lst(tleft, bright, pic)

    def _pic_lst(self, tleft: Vec2, bright: Vec2, pic: list[bin]) -> any:
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
        r_lst: list[Cell] = []
        j = 0
        while j < delta.y:
            i = 0
            while i <= delta.x:
                curr = tleft.loc + (Dir.E.v() * i) + (Dir.S.v() * j)
                cell = self.grid[curr]
                r_lst.append(cell.loc)
                if pic[int(j / self.config.pic_scalar)] & (
                    1 << int((delta.x - i) / self.config.pic_scalar)
                ):
                    self._dispatch(MazeEvent(cell=cell, _dir=Dir.N))
                    self._dispatch(MazeEvent(cell=cell, _dir=Dir.S))
                i += 1
            j += 1
        yield from r_lst


class Prim(BaseStrat):
    """Prims Algo.

    https://en.wikipedia.org/wiki/Prim%27s_algorithm

    #Setup
    frontier ← empty list
    start ← grid.entry
    emit ENTER(start)
    for each neighbour of start:
        frontier.add((start, neighbour, direction))

    #Main Loop
    while frontier not empty:
        (parent, cell, dir) ← random choice from frontier
        remove from frontier
        emit EDGE(parent → cell, dir)
        if stages reject event:
            continue
        emit ENTER(cell)
        if stages reject event:
            continue
        yield cell.loc

    #Expand Frontier
    for each (dir, neighbour) of cell:
    if neighbour exists:
        emit EDGE(cell → neighbour, dir)
        if stages accept:
            frontier.add((cell, neighbour, dir))
    """

    def generate(self):
        super().generate()
        yield from self._prim()

    def _prim(self):
        head = self.entry_cell
        head.visited = True
        visited = {head}
        enter = MazeEvent(head, etype=EType.ENTER)
        if not self._dispatch(enter):
            return enter.found
        frontier = {v for k, v in [*self.graph.neighbours(head)]}
        while frontier:
            cell = frontier.pop()
            # print(cell.neighbours)
            v = [
                k
                for k, c in cell.neighbours.items()
                if c and c.visited and not c.ispic
            ]
            # print("neighbours>>>>", v)
            self.rng.shuffle(v)
            direction = v[0] if len(v) else None
            neighbour = cell.neighbours[direction] if direction else None

            self._dispatch(MazeEvent(cell, neighbour, direction))
            cell.visited = True

            visited |= {cell}
            frontier |= {
                *[n for n in cell.neighbours.values() if n and not n.visited]
            }
            # print(frontier)
            yield frontier


class Sidewinder(BaseStrat):
    def generate(self, grid):
        super().generate(grid)
        yield from self._sidewind()

    def _sidewind(self):
        """Function generate_sidewinder(grid):.

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

        def e_bound(v):
            return v.x == self.width - 1

        def n_bound(v):
            return v.y == 0

        for cell in self.grid:
            run.append(cell)
            close = (e_bound(cell.loc)) or (
                not n_bound(cell.loc) and bool(self.rng.getrandbits(1))
            )
            self.rng.shuffle(run)
            r = run.pop()
            if not r.ispic:
                if close:
                    if (
                        Dir.N in r.neighbours.keys()
                        and r.neighbours[Dir.N]
                        and not r.neighbours[Dir.N].ispic
                    ):
                        neighbour = r.neighbours[Dir.N]
                        r.rm_wall(Dir.N)
                        neighbour.rm_wall(Dir.N.opps())
                    run = []
                else:
                    neighbour = r.neighbours[Dir.E]
                    if neighbour and not neighbour.ispic:
                        r.rm_wall(Dir.E)
                        neighbour.rm_wall(Dir.E.opps())
            cell.visited = True
            yield cell


class Wilson(BaseStrat):
    def generate(self, grid):
        super().generate(grid)
        yield from self._wilson()

    def _wilson(self):
        current = self.grid[self.config.entry]
        ngrid = {*self.grid}
        path = {current: None, "walls": Path()}
        # print("\n\n>>>>", type(ngrid))
        while len(ngrid) and current:
            n = [*current.neighbours]
            self.rng.shuffle(n)
            next_cell = current.neighbours[n[0]]
            if next_cell and next_cell not in path:
                path[current] = next_cell
                path["walls"] += next_cell.wall
                current.visited = True
                ngrid.discard(current)
            else:
                path, r_set = self._rewind(path, next_cell)
                ngrid |= r_set
            current = next_cell
            yield current

    def _rewind(self, path, current):
        curr = current
        r_set: set = set()
        while curr in path:
            # tmp = curr
            # print(curr)
            curr = path[curr]
            # print("pop", path.pop(tmp))
            curr.visited = False
        return (path, r_set)
