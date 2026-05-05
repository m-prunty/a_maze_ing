#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    staging.py                                        :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/01 08:05:00 by maprunty         #+#    #+#              #
#    Updated: 2026/05/04 11:41:34 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol

from common.grid_tools import Cell, Dir


class EType(Enum):
    """Event type for maze generation and pathfinding."""

    ENTER = auto()
    EDGE = auto()
    EXIT = auto()


@dataclass
class MazeEvent:
    """Event class for maze generation and pathfinding."""

    cell: Cell
    neighbour: Cell | None = None
    _dir: Dir | None = None
    etype: EType = EType.ENTER
    found: bool = False


class BaseStage(Protocol):
    """Base stage protocol for maze generation and pathfinding."""

    def process(self, e: MazeEvent) -> bool:
        """Processes a maze."""
        ...


# class IOStage:
#    """Stage for opening entry and exit of maze."""
#
#    def process(self, e: MazeEvent) -> bool:
#        """Opens entry and exit of maze."""
#        self._open_entry_exit(e.cell)
#        return e


class MkStage:
    """Stage for marking picture cells."""

    MKDCT = {
        Dir.N: "visited",
        Dir.S: "ispic",
        Dir.E: "visited",
        Dir.W: "visited",
    }

    def process(self, e: MazeEvent) -> bool:
        """Marks picture cells."""
        attr = self.MKDCT[e._dir] if e._dir else ""
        setattr(e.cell, attr, True)
        return e.cell


class VisitStage:
    """Stage for marking visited cells."""

    def process(self, e: MazeEvent) -> bool:
        """Marks visited cells."""
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
    """Stage for marking path cells."""

    def process(self, e: MazeEvent) -> bool:
        """Marks path cells."""
        if e.etype == EType.ENTER or e.etype == EType.EXIT:
            e.cell.ispath = False
        elif e.etype == EType.EDGE:
            if e.neighbour and e.neighbour.ispath:
                return False
            e.cell.ispath = True
        return True


class RmStage:
    """Stage for removing walls between cells."""

    def process(self, e: MazeEvent) -> bool:
        """Removes walls between cells."""
        if e.etype != EType.EDGE:
            return True
        assert e.neighbour and e._dir
        e.cell.rm_wall_nb(e.neighbour, e._dir)
        return True


class GoalStage:
    """Stage for checking if goal is reached."""

    def __init__(self, goal: Cell) -> None:
        """Initializes GoalStage with a goal."""
        self.goal = goal

    def process(self, e: MazeEvent) -> bool:
        """Checks if goal is reached."""
        if e.etype == EType.ENTER and e.cell.loc == self.goal:
            e.found = True
        return not e.found
