# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    a-maze-ing.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: sdeppe <sdeppe@student.42heilbronn.de>    +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:26:52 by sdeppe           #+#    #+#              #
#    Updated: 2026/01/31 13:15:27 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""TODO: Short module summary.

Optional longer description.
"""

import random
import sys

from a_maze import A_Maze
from graphics import Render
from helper import Vec2

sys.setrecursionlimit(2000)


def print_image(button, x, y, mystuff):
    """TODO: Docstring."""
    print(
        f"Got mouse event! button {button} at x: \
{int((x / rend.width) * rend.gridx)}, y: {int(y / rend.width * rend.gridy)}"
    )
    if button == 1:
        hex = random.randrange(0, 15)
        print(hex)
        rend.render_cell(
            hex,
            Vec2(
                int((x / rend.height) * rend.gridx),
                int(y / rend.width * rend.gridy),
            ),
        )
    #     # rend.render_cell(0, Vec2(1, 9))


rend = Render()


def main():
    """TODO: Docstring."""
    rend.init_window(700, 700, "hello")
    rend.init_grid(Vec2(3, 3))
    print(rend.generate_grid_sprits())
    # print(rend.cell_siz)
    rend.add_hook(rend.close, 33, None)
    rend.add_mous_hook(print_image, [1, 2])

    rend.launch()
    print("Hello from amazing!")


def main2():
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
    main2()
