#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    test_mazegen.py                                   :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/23 20:30:49 by maprunty         #+#    #+#              #
#    Updated: 2026/05/23 22:35:29 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import pytest

from mazegen import Config, ConfigError, Grid, MazeGenerator


def test_basic_generation():
    """MazeGenerator generates a maze of correct dimensions with default config."""
    cfg = Config(
        width=10, height=10, entry=(0, 0), exit=(9, 9), gen_algo="dfs"
    )
    grid = Grid(cfg.width, cfg.height)
    mg = MazeGenerator(grid, cfg)
    mg.gen_grid(cfg.gen_algo)
    assert grid.width == 10
    assert grid.height == 10
    for row in grid:
        assert len(row) == 10


def test_perfect_maze():
    """Maze is perfect if PERFECT=True."""
    cfg = Config(width=8, height=8, perfect=True, entry=(0, 0), exit=(7, 7))
    grid = Grid(cfg.width, cfg.height)
    mg = MazeGenerator(grid, cfg)
    mg.gen_grid(cfg.gen_algo)
    mg.gen_path(cfg.path_algo)
    assert grid.path[0] == grid[0, 0].loc
    assert grid.path[-1] == grid[7, 7].loc


def test_invalid_entry_exit():
    """Raises ConfigError if entry/exit is out of bounds."""
    with pytest.raises(ConfigError):
        Config(width=5, height=5, entry=(6, 0), exit=(4, 4))
    with pytest.raises(ConfigError):
        Config(width=5, height=5, exit=(2, 8))


def test_all_algorithms_supported():
    """Each algorithm generates a valid maze without error."""
    algos = ["dfs", "prim", "swinder", "wilson"]
    for algo in algos:
        cfg = Config(
            width=8, height=8, gen_algo=algo, entry=(0, 0), exit=(7, 7)
        )
        grid = Grid(cfg.width, cfg.height)
        mg = MazeGenerator(grid, cfg)
        mg.gen_grid(cfg.gen_algo)


def test_pathfinding_algorithms():
    """Each supported pathfinding algorithm finds a path."""
    algos = ["dijkstra"]
    for algo in algos:
        cfg = Config(
            width=7, height=7, path_algo=algo, entry=(0, 0), exit=(6, 6)
        )
        grid = Grid(cfg.width, cfg.height)
        mg = MazeGenerator(grid, cfg)
        mg.gen_grid(cfg.gen_algo)
        mg.gen_path(cfg.path_algo)
        # There should always be a path from entry to exit
        assert grid.path[0] == grid[cfg.entry].loc
        assert grid.path[-1] == grid[cfg.exit].loc


def test_seed_reproducibility():
    """Given the same seed, two mazes are identical."""
    cfg1 = Config(width=6, height=6, seed=1234, entry=(0, 0), exit=(5, 5))
    cfg2 = Config(width=6, height=6, seed=1234, entry=(0, 0), exit=(5, 5))
    grid1 = Grid(cfg1.width, cfg1.height)
    grid2 = Grid(cfg2.width, cfg2.height)
    mg1 = MazeGenerator(grid1, cfg1)
    mg2 = MazeGenerator(grid2, cfg2)
    mg1.gen_grid(cfg1.gen_algo)
    mg2.gen_grid(cfg2.gen_algo)
    assert [[cell for cell in row] for row in grid1] == [
        [cell for cell in row] for row in grid2
    ]
