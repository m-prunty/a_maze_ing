import math
import random
import time

from config import Config
from helper import Cell, Grid, Vec2


class Generators:
    """TODO: Summary of the class.

    Optional longer description.

    Attributes:
        attr (type): Description.
    """

    def __init__(self, grid: Grid, cfg: Config) -> None:
        """TODO: init summary for Generators.

        Args:
            grid (Grid): Description.
        """
        self.grid = grid
        self.config = cfg

    @property
    def width(self):
        """Get WIDTH from config file."""
        return self.config.width

    @property
    def height(self):
        """Get HEIGHT from config file."""
        return self.config.height

    @staticmethod
    def gen_rand(grid: Grid, cfg: Config, pos: tuple = (0, 0)):
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

    def gen_42(self, pic: list[bin], pic_scalar: int):
        """Prep for 42pic Check pic dimension against h / w.

        Calculate topleft and botright and passes to pic_lst

        Raises:
            ExceptionType: When this is raised.
        """
        self.config.get_pic(1)
        pic = self.config.pic
        # print(pic)
        wpic = int((math.log2(pic[0])) * (pic_scalar))
        hpic = int(len(pic) * pic_scalar)
        if self.width >= wpic + 2 and self.height >= hpic + 2:
            tleft = self.grid[
                int((self.width - wpic) / 2),
                int((self.height - hpic) / 2),
            ]
            bright = self.grid[tleft.loc + Vec2(wpic, hpic)]
            self.pic_lst(tleft, bright, pic)

    def pic_lst(self, tleft: Vec2, bright: Vec2, pic: list[bin]) -> list[Cell]:
        """Check and set if elements of subgrid from tleft to bright are ispic.

        gets a list of cells that will be ispic and steps through marking ispic
        as 1 for every 1 in the bitmask (self.pic)

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
        # print(tleft, bright, delta, self.config.width, self.config.height)
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
                cell.ispic = pic[int(j / self.config.pic_scalar)] & (
                    1 << int((delta.x - i) / self.config.pic_scalar)
                )
                cell.visited = cell.ispic
                i += 1
            j += 1
        return r_lst

    def open_entry_exit(cell: Cell, grid: Grid):
        """Open entry/exits gaps on border."""
        if cell:
            if cell.loc.x == 0:
                cell.rm_wall(Cell.W)
            elif cell.loc.x == grid.width - 1:
                cell.rm_wall(Cell.E)
            if cell.loc.y == 0:
                cell.rm_wall(Cell.N)
            elif cell.loc.y == grid.height - 1:
                cell.rm_wall(Cell.S)
        else:
            print(Exception(f"cell={cell}; dosent exist"))

    def neighbour(self, pos: Vec2) -> dict[list[Cell]]:
        """TODO: Docstring."""
        neighbours: dict[list[Cell]] = {}
        for k, v in Cell.DIRS.items():
            try:
                neighbours.update({k: self[v + pos].wall})
            except AttributeError:
                print("is none")
        return neighbours

    def animate(self, rend, current, delay=0.0):
        """TODO: Docstring."""
        # ANSI clear screen + cursor home
        CLEAR = "\x1b[2J\x1b[H"
        print(self.grid)
        print(self.config.exit)
        Generators.open_entry_exit(self.grid[self.config.entry], self.grid)
        Generators.open_entry_exit(self.grid[self.config.exit], self.grid)
        self.gen_42(self.config.pic, self.config.pic_scalar)
        pos = self.grid[current].loc
        rend.render_cell(pos, self.grid, 2, 1)
        random.seed(42)
        ##>>>>>>>>>^^^^<<set seed here BEFORE calls to random will determinethe starting seed

        for pos in self.gen_rand(self.grid, self.config, pos):
            rend.render_cell(pos, self.grid, 2, 0)
            time.sleep(delay)

        print(self.config.exit)
        pos = self.grid[self.config.exit].loc
        rend.render_cell(pos, self.grid, 2, 2)

        #       # t wmp
        #       #        print(sys.getrecursionlimit())
        #       # for pos in self.gen_rand(self.grid, self.config, self.config["ENTRY"]):
        #       for pos in self.gen_rand(self.grid, self.config, self.config["ENTRY"]):
        #           #            print(CLEAR, end="")
        #           #            print(self.grid.__str__(pos))
        #           # hex_walls = cell.wall
        #           # print(pos)
        #           try:
        #               rend.render_cell(pos, self.grid)
        #               print(self.grid.__str__(pos))
        #               time.sleep(delay)
        #           except Exception:
        #               print(
        #                   ">>>>>>>>>>>>>>>>>>\n\n\n\n\n\nrend, pos\n\n\n<<<<<<<<<<<<<<<<<<<<<<<<<<"
        #               )
        #               self.animate(rend, pos)
        self.grid.reset()
