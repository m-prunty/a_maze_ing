#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    graph.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/01 08:04:28 by maprunty         #+#    #+#              #
#    Updated: 2026/05/11 09:03:42 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Graph classes for maze generation and pathfinding."""

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Protocol

from mazegen.grid_tools import Cell, Dir, Grid


@dataclass(frozen=True)
class Edge:
    """Edge class for maze generation and pathfinding."""

    a: Cell
    b: Cell
    dir: Dir = field(init=False)

    def __post_init__(self) -> None:
        """Initializes Edge with direction from a to b."""
        try:
            object.__setattr__(self, "dir", self.a - self.b)
        except ValueError as e:
            raise ValueError(
                f"Cells {self.a} and {self.b} are not neighbours."
            ) from e

    def rm_walls(self) -> None:
        """Remove walls between the two cells defined by the edge."""
        if self.b is None:
            raise ValueError("Edge requires two cells.")
        self.a.rm_wall(self.dir)
        self.b.rm_wall(self.dir.opps())


class Graph(Protocol):
    """Graph protocol for maze generation and pathfinding."""

    grid: Grid

    def edges(self, cell: Cell) -> Iterable[Edge]:
        """Returns list of edges of cell."""
        ...


class GridGraph:
    """Graph for maze generation.

    Returns all neighbours of cell, even if wall between them.
    """

    def __init__(self, grid: Grid) -> None:
        """Initializes GenGraph with a grid."""
        self.grid = grid

    def edges(self, cell: Cell) -> Iterable[Edge]:
        """Returns list of edges of cell."""
        cell_nb = self.grid.neighbour(cell)
        for _, nb in cell_nb.items():
            yield Edge(cell, nb)


class MazeGraph:
    """Graph for pathfinding.

    Returns only neighbours of cell if no wall between them.
    """

    def __init__(self, grid: Grid) -> None:
        """Initializes PathGraph with a grid."""
        self.grid = grid

    def edges(self, cell: Cell) -> Iterable[Edge]:
        """Returns list of edges of cell if no wall between cell and dir."""
        cell_nb = self.grid.neighbour(cell)
        for dir, nb in cell_nb.items():
            if not cell.has_wall(dir):
                yield Edge(cell, nb)
