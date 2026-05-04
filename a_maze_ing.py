# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: sdeppe <sdeppe@student.42heilbronn.de>    +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:26:52 by sdeppe           #+#    #+#              #
#    Updated: 2026/05/03 09:44:48 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Main file to run A-maze-ing."""

import sys

from src.a_maze_ing import Start

sys.setrecursionlimit(2000)


def main() -> None:
    """Drive the main loop."""
    try:
        start = Start()
        start.render_start()
    except Exception as e:
        print(f"Error during main loop: {e}")


if __name__ == "__main__":
    main()
