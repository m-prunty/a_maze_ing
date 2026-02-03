# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    a-maze-ing.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: sdeppe <sdeppe@student.42heilbronn.de>    +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:26:52 by sdeppe           #+#    #+#              #
#    Updated: 2026/01/31 04:21:50 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""TODO: Short module summary.

Optional longer description.
"""

# import random
import sys

from graphics import Render
# from options import Options
from src.a_maze import A_Maze
# from helper import Vec2

class Start():
    def __init__(self):
        # self.options = Options(1000, 1000)
        self.rend = Render()
        self.render_start()
  
    def render_start(self):
        rend.init_window(self.options.height, self.options.width, " -- A-maze-ing -- ")
        
        

rend = Render()


def main():
    """Drive the main loop."""
    av = sys.argv
    ac = len(av)
    # rend.init_grid(Vec2(3, 3))
    # print(rend.generate_grid_sprits())
    # print(rend.cell_siz)
    if 1 <= ac <= 2:
        a = A_Maze.cfg_from_file("config.txt")
        print(a.config)
        print("yay")


if __name__ == "__main__":
    main()
