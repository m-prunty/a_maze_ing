# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: sdeppe <sdeppe@student.42heilbronn.de>    +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:26:52 by sdeppe           #+#    #+#              #
#    Updated: 2026/05/04 08:34:52 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Main file to run A-maze-ing."""

from src.a_maze_ing import Start


def main() -> None:
    """Drive the main loop."""
    try:
        start = Start()
        start.render_start()
    except Exception as e:
        print(f"Error during main loop: {e}")


if __name__ == "__main__":
    main()
