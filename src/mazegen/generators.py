import random
import time

from helper import *


class Generators:
    """TODO: Summary of the class.

    Optional longer description.

    Attributes:
        attr (type): Description.
    """

    def __init__(self, grid: Grid, cfg: dict[str, int]) -> None:
        """TODO: init summary for Generators.

        Args:
            grid (Grid): Description.
        """
        self.grid = grid
        self.config = cfg

    @staticmethod
    def gen_rand(grid: Grid, cfg: dict, pos: tuple = (0, 0)):
        """TODO: Docstring for gen_rand.

        Args:
            arg1 (TODO): TODO

        Returns: TODO

        """
        cell = grid[pos]
        cell.visited = True
        directions = list(Cell.DIRS.items())
        random.shuffle(directions)

        for direction, (dx, dy) in directions:
            neighbour = grid[cell.loc + Vec2(dx, dy)]
            if not neighbour or neighbour.visited:
                continue
            cell.rm_wall(direction)
            neighbour.rm_wall(Cell.OPPS[direction])
            yield neighbour.loc  # yield after carving a passage
            yield from Generators.gen_rand(grid, cfg, neighbour.loc)

    def open_entry_exit(cell: Cell, grid: Grid):
        if cell.loc.x == 0:
            cell.rm_wall(Cell.W)
        elif cell.loc.x == grid.width - 1:
            cell.rm_wall(Cell.E)
        elif cell.loc.y == 0:
            cell.rm_wall(Cell.N)
        elif cell.loc.y == grid.height - 1:
            cell.rm_wall(Cell.S)

    def animate(self, rend, delay=0.001):
        # ANSI clear screen + cursor home
        CLEAR = "\x1b[2J\x1b[H"
        Generators.open_entry_exit(self.grid[self.config["ENTRY"]], self.grid)
        Generators.open_entry_exit(self.grid[self.config["EXIT"]], self.grid)
        pos = self.grid[self.config["ENTRY"]].loc
        rend.render_cell(
        	pos,
			self.grid,
			2,
			1
        )
        
        for pos in self.gen_rand(self.grid, self.config, self.config["ENTRY"]):
            # print(CLEAR, end="")
            # print(self.grid.__str__(pos))
            rend.render_cell(
				pos,
				self.grid,
				2,
				0
			)
            time.sleep(delay)

        pos = self.grid[self.config["EXIT"]].loc
        rend.render_cell(
        	pos,
			self.grid,
			2,
			2
        )