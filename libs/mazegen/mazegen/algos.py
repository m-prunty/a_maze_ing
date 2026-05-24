#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    algos.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/01 08:04:43 by maprunty         #+#    #+#              #
#    Updated: 2026/05/24 02:55:27 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Maze generation and pathfinding algorithms."""

import math
import random
import sys
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any

from .errors import AlgoError
from .graph import Edge, Graph
from .grid_tools import Cell, Dir, Vec2
from .staging import (
    BaseStage,
    EventType,
    MazeEvent,
)


class BaseStrat(ABC):
    """Base strategy for maze generation and pathfinding."""

    def __init__(self, graph: Graph, cfg: Any) -> None:
        """Initializes BaseStrat with a graph and config."""
        from .config import Config

        self.config: Config = cfg
        print(f"Using seed: {cfg.seed}")
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
        sys.setrecursionlimit(max(1000, self.width * self.height * 2))
        yield from self._dfs(self.config.entry)

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


class Prim(BaseStrat):
    """Prims Algo."""

    def generate(self) -> Iterable[Vec2]:
        """Generates using Prim's algorithm."""
        self._imperfect()
        yield from self._prim()

    def _prim(self) -> Iterable[Vec2]:
        """Prim's algorithm from entry cell."""
        try:
            start = self.entry_cell
            enter = MazeEvent(start, etype=EventType.ENTER)
            if not self._dispatch(enter):
                return
            frontier: list[Edge] = [*self.graph.edges(start)]
            self.rng.shuffle(frontier)
            while frontier:
                idx = self.rng.randint(0, len(frontier) - 1)
                edge = frontier.pop(idx)
                if not edge or not edge.b:
                    continue
                e = MazeEvent(edge, EventType.EDGE)
                if not self._dispatch(e):
                    continue
                cell = edge.b
                enter = MazeEvent(cell, etype=EventType.ENTER)
                if not self._dispatch(enter):
                    continue
                yield cell.loc
                new_edges = [e for e in self.graph.edges(cell) if e.b]
                self.rng.shuffle(new_edges)
                frontier.extend(new_edges)
                back = MazeEvent(cell, etype=EventType.EXIT)
                self._dispatch(back)
            back = MazeEvent(start, etype=EventType.EXIT)
            self._dispatch(back)
        except Exception as e:
            raise AlgoError(f"Error in {self.__class__.__name__}: {e}") from e


class Kruskal(BaseStrat):
    """Kruskal's algorithm."""

    def generate(self) -> Iterable[Vec2]:
        """Generates using Kruskal's algorithm."""
        self._imperfect()
        yield from self._kruskal()

    def _kruskal(self) -> Iterable[Vec2]:
        """Kruskal's algorithm for maze generation and pathfinding."""
        try:
            sets: dict[Cell, set[Cell]] = {c: {c} for c in self.grid}
            edges: list[Edge] = [
                e
                for c in self.grid
                if not c.ispic
                for e in self.graph.edges(c)
            ]
            self.rng.shuffle(edges)
            for edge in edges:
                set_a = sets[edge.a]
                set_b = sets[edge.b]
                if set_a is not set_b:
                    e = MazeEvent(edge, EventType.EDGE)
                    if not self._dispatch(e):
                        continue
                    new_set = set_a.union(set_b)
                    for cell in new_set:
                        sets[cell] = new_set
                    yield edge.a.loc
                    yield edge.b.loc
        except Exception as e:
            raise AlgoError(f"Error in {self.__class__.__name__}: {e}") from e


class Sidewinder(BaseStrat):
    """Sidewinder maze generation."""

    def generate(self) -> Iterable[Vec2]:
        """Generates using Sidewinder algorithm."""
        self._imperfect()
        yield from self._sidewind()

    def _sidewind(self) -> Iterable[Vec2]:
        def e_bound(cell: Cell) -> Edge | Cell | bool | None:
            east = next(
                (edg for edg in self.graph.edges(cell) if edg.dir == Dir.E),
                None,
            )
            return cell.loc.x == self.width - 1 or (
                east and east.b and east.b.ispic
            )

        def n_bound(cell: Cell) -> Edge | Cell | bool | None:
            north = next(
                (edg for edg in self.graph.edges(cell) if edg.dir == Dir.N),
                None,
            )
            return cell.loc.y == 0 or (north and north.b and north.b.ispic)

        def next_edge(cell: Cell, direction: Dir) -> Edge | None:
            return next(
                (
                    edg
                    for edg in self.graph.edges(cell)
                    if edg.dir == direction and edg.b and not edg.b.ispic
                ),
                None,
            )

        try:
            run: list[Cell] = []
            for cell in self.grid:
                enter = MazeEvent(cell, etype=EventType.ENTER)
                if not self._dispatch(enter):
                    continue
                run.append(cell)
                at_e_bound = e_bound(cell)
                at_n_bound = n_bound(cell)
                close_run = at_e_bound or (
                    not at_n_bound and bool(self.rng.getrandbits(1))
                )
                if close_run:
                    candidates = [
                        c
                        for c in run
                        if not c.ispic
                        and any(
                            edg.dir == Dir.N and edg.b and not edg.b.ispic
                            for edg in self.graph.edges(c)
                        )
                    ]
                    if candidates:
                        member = self.rng.choice(candidates)
                        north_edge = next_edge(member, Dir.N)
                        if north_edge:
                            e = MazeEvent(
                                north_edge, EventType.EDGE, carve_only=True
                            )
                            if self._dispatch(e):
                                north_edge.rm_walls()
                    run = []
                else:
                    east_edge = next_edge(cell, Dir.E)
                    if east_edge:
                        e = MazeEvent(east_edge, EventType.EDGE)
                        if self._dispatch(e):
                            east_edge.rm_walls()
                back = MazeEvent(cell, etype=EventType.EXIT)
                self._dispatch(back)
                yield cell.loc
        except Exception as e:
            raise AlgoError(f"Error in {self.__class__.__name__}: {e}") from e


class Wilson(BaseStrat):
    """Wilson's algorithm."""

    def generate(self) -> Iterable[Vec2]:
        """Generates using Wilson's algorithm."""
        self._imperfect()
        yield from self._wilson()

    def _wilson(self) -> Iterable[Vec2]:
        def _randow_walk(start: Cell) -> dict[Cell, Edge]:
            path: dict[Cell, Edge] = {}
            current = walk_start
            while not current.visited:
                edges = [
                    e
                    for e in self.graph.edges(current)
                    if e.b and not e.b.ispic
                ]
                if not edges:
                    break
                edge = self.rng.choice(edges)
                if current in path:
                    keys = list(path)
                    idx = keys.index(current)
                    for k in keys[idx:]:
                        del path[k]

                path[current] = edge
                current = edge.b
            return path

        try:
            start = self.entry_cell
            if not self._dispatch(MazeEvent(start, etype=EventType.ENTER)):
                return
            yield start.loc

            unvisited: list[Cell] = [c for c in self.grid if not c.ispic]
            while unvisited:
                walk_start = self.rng.choice(unvisited)
                if walk_start.visited:
                    unvisited.remove(walk_start)
                    continue
                path = _randow_walk(walk_start)
                current = walk_start
                while current in path:
                    edge = path[current]

                    if not self._dispatch(
                        MazeEvent(
                            edge, EventType.EDGE, carve_only=edge.b.visited
                        )
                    ):
                        break
                    next_cell = edge.b
                    if not next_cell.visited and not self._dispatch(
                        MazeEvent(next_cell, EventType.ENTER)
                    ):
                        break
                    yield current.loc
                    self._dispatch(MazeEvent(current, EventType.EXIT))

                    if current in unvisited:
                        unvisited.remove(current)

                    current = next_cell
                self._dispatch(MazeEvent(current, EventType.EXIT))
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
                self._dispatch(MazeEvent(cell, etype=EventType.PATH))
                yield cell.loc
                cell = parent[cell]
        except Exception as e:
            raise AlgoError(f"Error in {self.__class__.__name__}: {e}") from e


class Pic(BaseStrat):
    """Picture maze generation."""

    def generate(self) -> Iterable[Vec2]:
        """Generates a picture to place in the maze."""
        yield from self._gen_pic(self.config.pic_scalar)

    def _gen_pic(self, pic_scalar: int | float) -> Iterable[Vec2]:
        """Prep for 42pic Check pic dimension against h / w.

        Calculate topleft and botright and passes to pic_lst

        Raises:
            Excepetion
        """
        try:
            pic = self.grid.pic
            wpic = int(math.log2(max(pic)) * (pic_scalar))
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
