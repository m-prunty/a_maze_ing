#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    algos.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/01 08:04:43 by maprunty         #+#    #+#              #
#    Updated: 2026/05/13 22:42:50 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Maze generation and pathfinding algorithms."""

import math
import random
from abc import ABC, abstractmethod
from collections.abc import Iterable

from common.config import Config
from common.errors import AlgoError
from common.grid_tools import Cell, Dir, Vec2

from .graph import Graph
from .staging import (
    BaseStage,
    EventType,
    MazeEvent,
)


class BaseStrat(ABC):
    """Base strategy for maze generation and pathfinding."""

    def __init__(self, graph: Graph, cfg: Config) -> None:
        """Initializes BaseStrat with a graph and config."""
        self.config: Config = cfg
        self.rng = (
            random.Random() if cfg.seed == 0 else random.Random(cfg.seed)
        )
        self.stages: list[BaseStage] = []
        self.graph = graph
        self.grid = graph.grid
        self._n_imperfect = ((self.width * self.height) ** 0.7) * int(
            not self.config.perfect
        )
        self.entry_cell = self.grid[self.config.entry]
        self.exit_cell = self.grid[self.config.exit]
        self._open_entry_exit(self.entry_cell)
        self._open_entry_exit(self.exit_cell)

    def add_stage(self, stage: BaseStage) -> None:
        """Adds a stage to the strategy."""
        self.stages.append(stage)

    @abstractmethod
    def generate(self) -> Iterable[Vec2]:
        """Generates a maze or path."""
        ...

    def _imperfect(self) -> None:
        """Carve random walls to make maze imperfect."""
        while self._n_imperfect > 0:
            cell = self.entry_cell
            while cell in (self.entry_cell, self.exit_cell) or cell.ispic:
                cell = self.grid[
                    (
                        self.rng.randint(0, self.width - 1),
                        self.rng.randint(0, self.height - 1),
                    )
                ]
            e_list = [
                e
                for e in self.graph.edges(cell)
                if e.b and not e.b.ispic and cell.has_wall(e.dir)
            ]
            self.rng.shuffle(e_list)
            if len(e_list):
                e_list[0].rm_walls()
            self._n_imperfect -= 1

    def _dispatch(self, event: MazeEvent) -> bool:
        """Dispatches a maze event to all stages.

        Return: True if all stages accept the event, False if stage rejects it.
        """
        try:
            for stage in self.stages:
                result = stage.process(event)
                if result is False:
                    return False
            return True
        except Exception as e:
            raise AlgoError(f"Error in {self.__class__.__name__}: {e}") from e

    def _open_entry_exit(self, cell: Cell) -> None:
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
    def width(self) -> int:
        """Get WIDTH from config file."""
        return self.config.width

    @property
    def height(self) -> int:
        """Get HEIGHT from config file."""
        return self.config.height


class Dfs(BaseStrat):
    """Depth-first search maze generation."""

    def generate(self) -> Iterable[Vec2]:
        """Generates a maze using depth-first search."""
        self._imperfect()
        start = self.config.entry
        yield from self._dfs(start)

    def _dfs(self, pos: Vec2) -> Iterable[Vec2]:
        """Recursive depth-first search from a position."""
        try:
            cell = self.grid[pos]

            enter = MazeEvent(cell, etype=EventType.ENTER)
            if not self._dispatch(enter):
                return
            directions = [*self.graph.edges(cell)]
            self.rng.shuffle(directions)

            for edge in directions:
                if not edge:
                    continue
                e = MazeEvent(edge, EventType.EDGE)
                if not self._dispatch(e):
                    continue
                assert edge.b is not None, "Edge must have a destination cell."
                yield edge.b.loc
                yield from self._dfs(edge.b.loc)
            back = MazeEvent(cell, etype=EventType.EXIT)
            self._dispatch(back)
            return
        except Exception as e:
            raise AlgoError(f"Error in {self.__class__.__name__}: {e}") from e


class Dijkstra(BaseStrat):
    """Dijkstra's algorithm for pathfinding."""

    def generate(self) -> Iterable[Vec2]:
        """Generates using Dijkstra's algorithm."""
        self._imperfect()
        yield from self._dijks(self.entry_cell)

    def _dijks(self, start: Cell) -> Iterable[Vec2]:
        try:
            frontier: list[tuple[int, Cell]] = [(0, start)]

            cell: Cell | None = None
            dist: dict[Cell, int] = {start: 0}
            parent: dict[Cell, Cell | None] = {start: None}
            visited: set[Cell] = set()
            while frontier:
                i = min(frontier, key=lambda f: f[0])
                frontier.remove(i)
                cost, cell = i
                if cell in visited:
                    continue
                enter = MazeEvent(cell, etype=EventType.ENTER)
                if not self._dispatch(enter):
                    break
                visited.add(cell)

                for edge in self.graph.edges(cell):
                    if not edge.b:
                        continue
                    e = MazeEvent(edge, EventType.EDGE)
                    if not self._dispatch(e):
                        continue
                    nb = edge.b
                    new_cost = cost + 1
                    if nb not in dist or new_cost < dist[nb]:
                        dist[nb] = new_cost
                        parent[nb] = cell
                        existing = next(
                            (f for f in frontier if f[1] == nb), None
                        )
                        if not existing:
                            frontier.append((new_cost, nb))
                        elif existing[0] > (new_cost):
                            frontier.remove(existing)
                            frontier.append((new_cost, nb))

                back = MazeEvent(cell, etype=EventType.EXIT)
                self._dispatch(back)
            cell = parent.get(self.exit_cell, None)
            while cell and cell != self.entry_cell:
                assert cell is not None, "No path found from entry to exit."
                yield cell.loc
                cell = parent[cell]
        except Exception as e:
            raise AlgoError(f"Error in {self.__class__.__name__}: {e}") from e


class Pic(BaseStrat):
    """Picture maze generation."""

    def generate(self) -> Iterable[Vec2]:
        """Generates a picture to place in the maze."""
        yield from self._gen_pic(self.config.pic_scalar)

    @staticmethod
    def get_pic(select: int) -> list[int]:
        """Get the picture data for the maze based on the selected option."""
        if select == 0:
            pic = [
                0b1010111,
                0b1010001,
                0b1110111,
                0b0010100,
                0b0010111,
            ]
        elif select == 1:
            pic = [
                0b001111010001011101110111,
                0b001101011111010100010100,
                0b001111010101011100100111,
                0b001101010101010101000100,
                0b001101010101010101110111,
            ]
        elif select == 2:
            pic = [
                0b000000011110000011111111,
                0b000001111100001110000111,
                0b000111001100000000011100,
                0b011100111000000011100000,
                0b111111111100011100000000,
                0b000011100001110000000000,
                0b000111000111111110110000,
            ]
        return pic

    def _gen_pic(self, pic_scalar: int | float) -> Iterable[Vec2]:
        """Prep for 42pic Check pic dimension against h / w.

        Calculate topleft and botright and passes to pic_lst

        Raises:
            Excepetion
        """
        try:
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
        except Exception as e:
            raise AlgoError(f"Error in {self.__class__.__name__}: {e}") from e

    def _pic_lst(
        self, tleft: Cell, bright: Cell, pic: list[int]
    ) -> Iterable[Vec2]:
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
        try:
            delta = bright.loc - tleft.loc
            r_lst: list[Vec2] = []
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
                        self._dispatch(MazeEvent(cell))
                    i += 1
                j += 1
            yield from r_lst
        except Exception as e:
            raise AlgoError(f"Error in {self.__class__.__name__}: {e}") from e


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

    def generate(self) -> Iterable[Vec2]:
        """Generates using Prim's algorithm."""
        yield from self._prim()

    def _prim(self) -> Iterable[Vec2]:
        return [Vec2(0, 0)]
        """
        start = self.entry_cell
        start.visited = True
        if not self._dispatch(MazeEvent(start, etype=EventType.ENTER)):
            return
        frontier




        head = self.entry_cell
        head.visited = True
        visited = {head}
        enter = MazeEvent(head, etype=EventType.ENTER)
        print("enter>>>>", enter)
        if not self._dispatch(enter):
            return
        frontier = {v for k, v in [*self.graph.neighbours(head)]}
        print("frontier>>>>", frontier)
        while frontier:
            cell = frontier.pop()
            print(self.grid.neighbour(cell))
            v = [
                k
                for k, c in self.graph.neighbours(cell)
                if c and not c.visited and not c.ispic
            ]
            print("neighbours>>>>", v)
            self.rng.shuffle(v)
            direction = v[0] if len(v) else None
            neighbour = (
                self.graph.neighbours(cell)[direction] if direction else None
            )

            self._dispatch(MazeEvent(cell, neighbour, direction))
            cell.visited = True

            visited |= {cell}
            frontier |= {
                *[n for n in cell.neighbours.values() if n and not n.visited]
            }
            # print(frontier)
            yield frontier
"""


class Sidewinder(BaseStrat):
    """Sidewinder maze generation."""

    def generate(self) -> Iterable[Vec2]:
        """Generates using Sidewinder algorithm."""
        yield from self._sidewind()

    def _sidewind(self) -> Iterable[Vec2]:
        return [Vec2(0, 0)]
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
        start = self.config.entry
        run = [self.grid[start]]

        def e_bound(v):
            Check if cell is at eastern boundary.
            return v.x == self.width - 1

         def n_bound(v):
             Check if cell is at northern boundary.
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
        """


class Wilson(BaseStrat):
    """Wilson's algorithm."""

    def generate(self) -> Iterable[Vec2]:
        """Generates using Wilson's algorithm."""
        yield from self._wilson()

    def _wilson(self) -> Iterable[Vec2]:
        return [Vec2(0, 0)]


#        current = self.grid[self.config.entry]
#        ngrid = {*self.grid}
# path = {current: None, "walls": Path()}
# print("\n\n>>>>", type(ngrid))
#        while len(ngrid) and current:
#            n = [*current.neighbours]
#            self.rng.shuffle(n)
#            next_cell = current.neighbours[n[0]]
#            if next_cell and next_cell not in path:
#                path[current] = next_cell
#                path["walls"] += next_cell.wall
#                current.visited = True
#                ngrid.discard(current)
#            else:
#                path, r_set = self._rewind(path, next_cell)
#                ngrid |= r_set
#            current = next_cell
#            yield current
#
#    def _rewind(self, path, current) -> tuple[dict, set]:
#        curr = current
#        r_set: set = set()
#        while curr in path:
#            curr = path[curr]
# print("pop", path.pop(tmp))
#            curr.visited = False
#        return (path, r_set)
#
