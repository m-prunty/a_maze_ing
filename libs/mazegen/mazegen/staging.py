#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    staging.py                                        :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/01 08:05:00 by maprunty         #+#    #+#              #
#    Updated: 2026/05/09 00:00:10 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Staging classes for maze generation and pathfinding."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol

from common.grid_tools import Cell

from .graph import Edge


class EventType(Enum):
    """Event type for maze generation and pathfinding."""

    ENTER = auto()
    EDGE = auto()
    EXIT = auto()


@dataclass
class MazeEvent:
    """Event class for maze generation and pathfinding."""

    edge: Edge
    etype: EventType = EventType.ENTER
    found: bool = False


class BaseStage(Protocol):
    """Base stage protocol for maze generation and pathfinding."""

    def process(self, e: MazeEvent) -> bool:
        """Processes a maze."""
        ...


class PicStage:
    """Stage for marking picture cells."""

    def process(self, e: MazeEvent) -> bool:
        """Marks picture cells."""
        attr = "ispic"
        setattr(e.edge.a, attr, True)
        return True


class VisitStage:
    """Stage for marking visited cells."""

    def process(self, e: MazeEvent) -> bool:
        """Marks visited cells."""
        if e.etype == EventType.ENTER:
            if e.edge.a.visited or e.edge.a.ispic:
                return False
            e.edge.a.visited = True
            return True
        elif e.etype == EventType.EDGE:
            if e.edge.b and (e.edge.b.visited or e.edge.b.ispic):
                return False
        return True


class PathStage:
    """Stage for marking path cells."""

    def process(self, e: MazeEvent) -> bool:
        """Marks path cells."""
        if e.etype == EventType.ENTER or e.etype == EventType.EXIT:
            e.edge.a.ispath = False
        elif e.etype == EventType.EDGE:
            if e.edge.b and e.edge.b.ispath:
                return False
            e.edge.a.ispath = True
        return True


class RmStage:
    """Stage for removing walls between cells."""

    def process(self, e: MazeEvent) -> bool:
        """Removes walls between cells."""
        if e.etype != EventType.EDGE:
            return True
        assert e.edge.b and e.edge.dir
        e.edge.a.rm_wall_nb(e.edge.b, e.edge.dir)
        return True


class GoalStage:
    """Stage for checking if goal is reached."""

    def __init__(self, goal: Cell) -> None:
        """Initializes GoalStage with a goal."""
        self.goal = goal

    def process(self, e: MazeEvent) -> bool:
        """Checks if goal is reached."""
        if e.etype == EventType.ENTER and e.edge.a.loc == self.goal:
            e.found = True
        return not e.found
