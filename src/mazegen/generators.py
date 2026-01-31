import math
import random
import sys

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

    def gen_42(self, h, w):
        pic = [
            0b1010111,
            0b1010001,
            0b1110111,
            0b0010100,
            0b0010111,
        ]
        wpic = int(math.log2(pic[0])) + 1
        hpic = len(pic)
        if w >= wpic + 2 and h >= hpic + 2:
            i = 0
            tleft = self.grid[int((w - wpic) / 2), int((h - hpic) / 2)]
            bright = self.grid[tleft.loc + Vec2(wpic, hpic)]
            self.pic_lst(tleft, bright, pic)
            #    n = len(row)
            # print(">>>>>", pic << n, cell)
            # for cell in row[0]:
            #     n -= 1

    def pic_lst(self, tleft: Vec2, bright: Vec2, pic: list[bin]) -> list[Cell]:
        delta = bright.loc - tleft.loc
        r_lst: list[list[Cell]] = [[] for x in range(delta.y)]
        j = 0
        while j < delta.y:
            r_lst[j]: list[Cell] = []
            i = 0
            while i <= delta.x:
                curr = (
                    tleft.loc
                    + (Cell.DIRS[Cell.E] * i)
                    + (Cell.DIRS[Cell.S] * j)
                )
                cell = self.grid[curr]
                cell.is42 = pic[j] & (1 << (delta.x - i))
                cell.visited = cell.is42
                i += 1
            j += 1
        return r_lst

    def open_entry_exit(cell: Cell, grid: Grid):
        if cell.loc.x == 0:
            cell.rm_wall(Cell.W)
        elif cell.loc.x == grid.width - 1:
            cell.rm_wall(Cell.E)
        elif cell.loc.y == 0:
            cell.rm_wall(Cell.N)
        elif cell.loc.y == grid.height - 1:
            cell.rm_wall(Cell.S)

    def animate(self, rend, delay=0.0):
        # ANSI clear screen + cursor home
        CLEAR = "\x1b[2J\x1b[H"
        Generators.open_entry_exit(self.grid[self.config["ENTRY"]], self.grid)
        Generators.open_entry_exit(self.grid[self.config["EXIT"]], self.grid)
        w = self.config["WIDTH"]
        h = self.config["HEIGHT"]
        self.gen_42(w, h)
        pos = self.grid[self.config["ENTRY"]].loc
        rend.render_cell(pos, self.grid)
        # tmp
        print(sys.getrecursionlimit())
        for pos in self.gen_rand(self.grid, self.config, self.config["ENTRY"]):
            # print(CLEAR, end="")
            # print(self.grid.__str__(pos))
            # hex_walls = cell.wall
            # print(pos)
            rend.render_cell(pos, self.grid)
            # for dir in (Cell.DIRS.items()):
            #     neighbour = pos + dir[1]
            #     print(neighbour)
            #     try:
            #         rend.render_cell(
            # 			self.grid[neighbour].wall,
            # 			self.grid[neighbour].loc,
            # 		)
            #     except AttributeError :
            #         print("out of grid")
            # time.sleep(delay)
        for cell in self.grid
