import math
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

    @property
    def width(self):
        """Get WIDTH from config file."""
        return self.config["WIDTH"]

    @property
    def height(self):
        """Get HEIGHT from config file."""
        return self.config["HEIGHT"]

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

    @staticmethod
    def gen_rand_iter(grid: Grid, cfg: dict, pos: tuple = (0, 0)):
        """TODO: Docstring for gen_rand.

        Args:
            arg1 (TODO): TODO

        Returns: TODO

        """
        for cell in grid:
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

    def gen_42(self):
        """Prep for 42pic Check pic dimension against h / w.

        Calculate tleft and bright and passes to pic_lst

        Raises:
            ExceptionType: When this is raised.
        """
        pic = [
            0b1010111,
            0b1010001,
            0b1110111,
            0b0010100,
            0b0010111,
        ]
        wpic = int(math.log2(pic[0])) + 1
        hpic = len(pic)
        if self.width >= wpic + 2 and self.height >= hpic + 2:
            i = 0
            tleft = self.grid[
                int((self.width - wpic) / 2), int((self.height - hpic) / 2)
            ]
            bright = self.grid[tleft.loc + Vec2(wpic, hpic)]
            self.pic_lst(tleft, bright, pic)

    def pic_lst(self, tleft: Vec2, bright: Vec2, pic: list[bin]) -> list[Cell]:
        """Check and set if elements of subgrid from tleft to bright are is42.

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
        """Open entry/exits gaps on border."""
        if cell.loc.x == 0:
            cell.rm_wall(Cell.W)
        elif cell.loc.x == grid.width - 1:
            cell.rm_wall(Cell.E)
        elif cell.loc.y == 0:
            cell.rm_wall(Cell.N)
        elif cell.loc.y == grid.height - 1:
            cell.rm_wall(Cell.S)

    def neighbour(self, pos: Vec2) -> dict[list[Cell]]:
        """TODO: Docstring."""
        neighbours: dict[list[Cell]] = {}
        for k, v in Cell.DIRS.items():
            try:
                neighbours.update({k: self[v + pos].wall})
            except AttributeError:
                print("is none")
        return neighbours

    def animate(self, rend, current=(0, 0), delay=0.0):
        """TODO: Docstring."""
        # ANSI clear screen + cursor home
        CLEAR = "\x1b[2J\x1b[H"
        Generators.open_entry_exit(self.grid[self.config["ENTRY"]], self.grid)
        Generators.open_entry_exit(self.grid[self.config["EXIT"]], self.grid)
        self.gen_42()
        pos = self.grid[current].loc
        rend.render_cell(pos, self.grid)
        # t wmp
        #        print(sys.getrecursionlimit())
        # for pos in self.gen_rand(self.grid, self.config, self.config["ENTRY"]):
        for pos in self.gen_rand_iter(
            self.grid, self.config, self.config["ENTRY"]
        ):
            #            print(CLEAR, end="")
            #            print(self.grid.__str__(pos))
            # hex_walls = cell.wall
            # print(pos)
            try:
                rend.render_cell(pos, self.grid)
                time.sleep(delay)
            except Exception:
                print(
                    ">>>>>>>>>>>>>>>>>>\n\n\n\n\n\nrend, pos\n\n\n<<<<<<<<<<<<<<<<<<<<<<<<<<"
                )
                self.animate(rend, pos)
        self.grid.reset
