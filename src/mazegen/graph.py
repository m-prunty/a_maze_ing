#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    graph.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/01 08:04:28 by maprunty         #+#    #+#              #
#    Updated: 2026/05/01 08:12:32 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from collections.abc import Iterable
from typing import Protocol

from common.grid_tools import Cell, Grid


class Graph(Protocol):
    """Graph protocol for maze generation and pathfinding."""

    def neighbours(self, cell: Cell) -> Iterable[Cell]:
        """Returns list of neighbours of cell."""
        ...


class GenGraph:
    """Graph for maze generation.

    Returns all neighbours of cell, even if wall between them.
    """

    def __init__(self, grid: Grid) -> None:
        """Initializes GenGraph with a grid."""
        self.grid = grid

    def neighbours(self, cell: Cell) -> Iterable[Cell]:
        """Returns list of neighbours of cell."""
        yield from list(cell.neighbours.items())


class PathGraph:
    """Graph for pathfinding.

    Returns only neighbours of cell if no wall between them.
    """

    def __init__(self, grid: Grid) -> None:
        """Initializes PathGraph with a grid."""
        self.grid = grid

    def neighbours(self, cell: Cell) -> Iterable[Cell]:
        """Returns list of neighbours if no wall between cell and dir."""
        c_list = [
            c for c in list(cell.neighbours.items()) if not cell.has_wall(c[0])
        ]
        c_list.sort(key=lambda x: (x[0], x[1].loc.x, x[1].loc.y))
        yield from c_list
