#! /usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    main.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: sdeppe <sdeppe@student.42heilbronn.de>    +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:26:52 by sdeppe           #+#    #+#              #
#    Updated: 2026/05/08 04:06:38 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Main file to run A-maze-ing."""

from src import Start


def main() -> None:
    try:
        start = Start()
        start.render_start()
    except Exception as e:
        print(f"Error during main loop: {e}")


if __name__ == "__main__":
    main()
