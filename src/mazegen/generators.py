#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    generators.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/02/07 03:02:45 by maprunty         #+#    #+#              #
#    Updated: 2026/03/26 10:44:13 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import math
import random
from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Protocol

from config import Config
from helper import Cell, Dir, Grid, Path, Vec2


class EType(Enum):
    ENTER = auto()
    EDGE = auto()
    EXIT = auto()


@dataclass
class MazeEvent:
    cell: Cell
    neighbour: Cell | None = None
    _dir: Dir | None = None
    etype: EType = EType.ENTER
    found: bool = None


class Graph(Protocol):
    def neighbours(self, cell: Cell) -> Iterable[Cell]: ...


class GenGraph:
    def __init__(self, grid: Grid) -> None:
        self.grid = grid

    def neighbours(self, cell: Cell) -> Iterable[Cell]:
        yield from list(cell.neighbours.items())


class PathGraph:
    def __init__(self, grid: Grid) -> None:
        self.grid = grid

    def neighbours(self, cell: Cell) -> Iterable[Cell]:
        """Returns list of neighbours if no wall between cell and dir."""
        c_list = [
            c for c in list(cell.neighbours.items()) if not cell.has_wall(c[0])
        ]
        c_list.sort(key=lambda x: (x[0], x[1].loc.x, x[1].loc.y))
        yield from c_list


class BaseStage(Protocol):
    def process(self, e: MazeEvent) -> Any: ...


class IOStage:
    def process(self, e: MazeEvent) -> Any:
        self._open_entry_exit(e.cell)
        return e


class MkStage:
    MKDCT = {
        Dir.N: "visited",
        Dir.S: "ispic",
        Dir.E: "visited",
        Dir.W: "visited",
    }

    def process(self, e: MazeEvent) -> Any:
        attr = self.MKDCT[e._dir] if e._dir else ""
        setattr(e.cell, attr, True)
        return e.cell


class VisitStage:
    def process(self, e: MazeEvent) -> bool:
        if e.etype == EType.ENTER:
            if e.cell.visited:
                return False
            e.cell.visited = True
            return True
        elif e.etype == EType.EDGE:
            if e.neighbour and e.neighbour.visited:
                return False
        return True


class PathStage:
    def process(self, e: MazeEvent) -> bool:
        if e.etype == EType.ENTER:
            e.cell.ispath = True
        elif e.etype == EType.EXIT:
            e.cell.ispath = False
        return True


class RmStage:
    def process(self, e: MazeEvent) -> Any:
        if e.etype != EType.EDGE:
            return True
        e.cell.rm_wall_nb(e._dir)
        return True


class GoalStage:
    def __init__(self, goal):
        self.goal = goal

    def process(self, e) -> bool:
        if e.etype == EType.ENTER and e.cell.loc == self.goal:
            e.found = True
        return not e.found


class BaseStrat(ABC):
    def __init__(self, graph: Graph, cfg: Config) -> None:
        """TODO: init summary for Generators.

        Args:
            grid (Grid): Description.
        """
        self.config = cfg
        self.rng = random.Random(cfg.seed)
        self.stages: list[BaseStage] = []
        self.graph = graph
        self.grid = graph.grid
        self._n_imperfect = ((self.width * self.height) ** 0.5) * int(
            not self.config.perfect
        )

    def add_stage(self, stage: BaseStage) -> None:
        self.stages.append(stage)

    @abstractmethod
    def generate(self):
        self.entry_cell = self.grid[self.config.entry]
        self.exit_cell = self.grid[self.config.exit]
        self._open_entry_exit(self.entry_cell)
        self._open_entry_exit(self.exit_cell)

    def _imperfect(self) -> None:
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
    def generate(self):
        super().generate()
        self._imperfect()
        start = self.config.entry
        yield from self._dfs(start)

    def _dfs(self, pos: Vec2 = Vec2(0, 0)):
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

    def _dijks(self, pos: Vec2 = Vec2(0, 0)):
        node: Cell = self.grid[pos]
        frontier: list[Cell] = [(0, node)]
        expanded: set[Cell] = set()

        print("nnn", node)
        # cost: dict[Cell, int] = {node: 0}
        parent: Dict[Cell, Cell] = {node: None}
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
            # return enter.found

            # print(node.loc)
            # yield node.loc
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
        print("nnn", node)
        cell = parent[self.exit_cell]
        print("aaa", cell)
        while cell != self.entry_cell:
            print(cell)
            cell = parent[cell]
            yield cell


class Pic(BaseStrat):
    def generate(self):
        super().generate()
        start = self.config.entry
        yield from self._gen_pic(1)

    def _gen_pic(self, pic_scalar: int):
        """Prep for 42pic Check pic dimension against h / w.

        Calculate topleft and botright and passes to pic_lst

        Raises:
            ExceptionType: When this is raised.
        """
        self.config.get_pic(self.config.pic)
        pic = self.config.pic
        wpic = int(math.log2(max(pic)) * (pic_scalar)) - 1
        hpic = int(len(pic) * pic_scalar)
        mx = max(wpic, hpic)
        mn = min(self.height, self.width)
        if mx < int(mn / 5) * 3:
            pic_scalar = int(((mn / 5) * 3) / mx)
            wpic = int((math.log2(max(pic))) * (pic_scalar)) - 1
            hpic = int(len(pic) * pic_scalar)
        self.config.pic_scalar = pic_scalar

        if self.width >= wpic + 2 and self.height >= hpic + 2:
            tleft = self.grid[
                int((self.width - wpic) / 2),
                int((self.height - hpic) / 2),
            ]
            bright = self.grid[tleft.loc + Vec2(wpic, hpic)]
            yield from self._pic_lst(tleft, bright, pic)

    def _pic_lst(
        self, tleft: Vec2, bright: Vec2, pic: list[bin]
    ) -> list[Cell]:
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
        e_bound = lambda v: v.x == self.width - 1
        n_bound = lambda v: v.y == 0
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
            tmp = curr
            # print(curr)
            curr = path[curr]
            # print("pop", path.pop(tmp))
            curr.visited = False
        return (path, r_set)


class Generators:
    """TODO: Summary of the class.

    Optional longer descrgiption.

    Attributes:
        attr (type): Description.
    """

    ADAPT = {
        "dfs": Dfs,
        "prim": Prim,
        "swinder": Sidewinder,
        "wilson": Wilson,
    }

    def __init__(self, grid: Grid, cfg: Config):
        self.grid = grid
        self.config = cfg
        self.path = []

    def to_path(self, v_lst: list[Vec2]):
        return reversed(v_lst)
        # [print(v) for v in v_lst if self.grid[v].ispath]
        # yield from [v for v in v_lst if self.grid[v].ispath]

    def gen_grid(self):
        """Thes becomes open walls and give the hande to the animator."""
        pic = Pic(GenGraph(self.grid), self.config)
        pic.add_stage(MkStage())
        [*pic.generate()]

        dfs = Dfs(GenGraph(self.grid), self.config)
        dfs.add_stage(VisitStage())
        dfs.add_stage(RmStage())
        dfs_lst = [*dfs.generate()]

        #        prim = Prim(GenGraph(self.grid), self.config)
        #        prim.add_stage(VisitStage())
        #        prim.add_stage(RmStage())
        #        prim_lst = [*prim.generate()]

        self.grid.reset()

        path = Dijkstra(PathGraph(self.grid), self.config)
        path.add_stage(VisitStage())
        path.add_stage(PathStage())
        path.add_stage(GoalStage(self.config.exit))

        self.grid.path = [*self.to_path([*path.generate()])]
