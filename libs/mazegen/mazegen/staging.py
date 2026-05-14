#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    staging.py                                        :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/01 08:05:00 by maprunty         #+#    #+#              #
#    Updated: 2026/05/12 22:10:19 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Staging classes for maze generation and pathfinding."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol

from mazegen.errors import StageError
from mazegen.grid_tools import Cell

from .graph import Edge


class EventType(Enum):
    """Event type for maze generation and pathfinding."""

    ENTER = auto()
    EDGE = auto()
    EXIT = auto()


@dataclass
class MazeEvent:
    """Event class for maze generation and pathfinding."""

    edge: Edge | Cell
    etype: EventType = EventType.ENTER

    @property
    def cell(self) -> Cell:
        """Returns the cell associated with the event."""
        return self.edge if isinstance(self.edge, Cell) else self.edge.a


class BaseStage(Protocol):
    """Base stage protocol for maze generation and pathfinding."""

    def process(self, e: MazeEvent) -> bool:
        """Processes a maze."""
        ...


class PicStage:
    """Stage for marking picture cells."""

    def process(self, e: MazeEvent) -> bool:
        """Marks picture cells."""
        try:
            attr = "ispic"
            setattr(e.edge, attr, True)
            return True
        except Exception as e:
            raise StageError(f"Error in {self.__class__.__name__}: {e}") from e


class VisitStage:
    """Stage for marking visited cells."""

    def process(self, e: MazeEvent) -> bool:
        """Marks visited cells."""
        try:
            if e.etype == EventType.ENTER:
                if e.cell.visited or e.cell.ispic:
                    return False
                e.cell.visited = True
                return True
            elif e.etype == EventType.EDGE:
                assert isinstance(e.edge, Edge)
                if e.edge.b and (e.edge.b.visited or e.edge.b.ispic):
                    return False
            return True
        except Exception as e:
            raise StageError(f"Error in {self.__class__.__name__}: {e}") from e


class PathStage:
    """Stage for marking path cells."""

    def process(self, e: MazeEvent) -> bool:
        """Marks path cells."""
        try:
            if e.etype == EventType.ENTER or e.etype == EventType.EXIT:
                e.cell.ispath = False
            elif e.etype == EventType.EDGE:
                assert isinstance(e.edge, Edge)
                if e.edge.b and e.edge.b.ispath:
                    return False
                e.edge.a.ispath = True
            return True
        except Exception as e:
            raise StageError(f"Error in {self.__class__.__name__}: {e}") from e


class RmStage:
    """Stage for removing walls between cells."""

    def process(self, e: MazeEvent) -> bool:
        """Removes walls between cells."""
        try:
            if e.etype != EventType.EDGE:
                return True

            assert isinstance(e.edge, Edge) and e.edge.b and e.edge.dir
            e.edge.rm_walls()
            return True
        except Exception as e:
            raise StageError(f"Error in {self.__class__.__name__}: {e}") from e


class GoalStage:
    """Stage for checking if goal is reached."""

    def __init__(self, goal: Cell) -> None:
        """Initializes GoalStage with a goal."""
        self.goal = goal
        self.found = False

    def process(self, e: MazeEvent) -> bool:
        """Checks if goal is reached."""
        try:
            if e.etype == EventType.ENTER and e.cell.loc == self.goal:
                self.found = True
            return not self.found
        except Exception as e:
            raise StageError(f"Error in {self.__class__.__name__}: {e}") from e
