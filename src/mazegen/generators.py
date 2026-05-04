#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    generators.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/02/07 03:02:45 by maprunty         #+#    #+#              #
#    Updated: 2026/05/03 10:02:04 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #


from common.config import Config
from common.grid_tools import Cell, Grid, Vec2

from .algos import Dfs, Dijkstra, Pic, Prim, Sidewinder, Wilson
from .graph import GenGraph, PathGraph
from .staging import (
    GoalStage,
    MkStage,
    PathStage,
    RmStage,
    VisitStage,
)


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
        "dijkstra": Dijkstra,
    }

    def __init__(self, grid: Grid, cfg: Config) -> None:
        self.grid = grid
        self.config = cfg
        self.path = []

    def to_path(self, v_lst: list[Vec2]) -> list[Vec2]:
        """Converts a list of Vec2 to a path."""
        return reversed(v_lst)

    def gen_path(self, algo: str) -> None:
        """Generate a path through the maze using the specified algorithm."""
        path_algo = self.ADAPT.get(algo.lower())
        if not path_algo:
            raise ValueError(f"Algorithm '{algo}' not recognized.")
        path = path_algo(PathGraph(self.grid), self.config)
        path.add_stage(VisitStage())
        path.add_stage(PathStage())
        path.add_stage(GoalStage(self.config.exit))
        self.grid.path = [*self.to_path([*path.generate()])] + [
            Cell(self.config.exit)
        ]
        print(self.grid.path)

    def gen_grid(self, algo: str = "dfs") -> None:
        """Generate the maze grid using the specified algorithm."""
        gen_algo = self.ADAPT.get(algo.lower())
        if not gen_algo:
            raise ValueError(f"Algorithm '{algo}' not recognized.")
        generator = gen_algo(GenGraph(self.grid), self.config)
        generator.add_stage(VisitStage())
        generator.add_stage(RmStage())
        [*generator.generate()]

    @staticmethod
    def retryIO(loc: Vec2, config: Config, neg: int) -> Vec2:
        """Retry opening entry or exit if they are  in the picture."""
        print(f"Location {loc} is in the picture, adjusting...")
        return Vec2(
            (loc.x + (1 * neg)) % config.width,
            (loc.y + (1 * neg)) % config.height,
        )

    def gen_pic(self, select: int) -> None:
        """Generate the maze grid based on the picture data."""
        self.grid.pic = Pic.get_pic(select)
        if not self.grid.pic:
            raise ValueError(f"Picture selection '{select}' not recognized.")
        pic = Pic(GenGraph(self.grid), self.config)
        pic.add_stage(MkStage())
        [*pic.generate()]
        while (
            self.grid[self.config.entry] and self.grid[self.config.entry].ispic
        ):
            self.config.entry = self.retryIO(
                self.config.entry, self.config, -1
            )
        while (
            self.grid[self.config.exit] and self.grid[self.config.exit].ispic
        ):
            self.config.exit = self.retryIO(self.config.exit, self.config, 1)

    def driver(self) -> None:
        """Thes becomes open walls and give the hande to the animator."""
        try:
            self.gen_pic(self.config.pic)
            self.gen_grid(self.config.gen_algo)
            self.grid.reset()
            self.gen_path(self.config.path_algo)
        except Exception as e:
            print(f"Error during maze generation: {e}")
