#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    registry.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/22 15:21:04 by maprunty         #+#    #+#              #
#    Updated: 2026/05/22 17:40:15 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Registry module for maze generation and pathfinding algorithms."""

from .algos import (
    BaseStrat,
    Dfs,
    Dijkstra,
    Kruskal,
    Prim,
    Sidewinder,
    Wilson,
)

ALGOS: dict[str, type[BaseStrat]] = {
    "dfs": Dfs,
    "prim": Prim,
    "swinder": Sidewinder,
    "wilson": Wilson,
    "kruskal": Kruskal,
    "dijkstra": Dijkstra,
}
PICS: dict[int, list[int]] = {
    0: [
        0b1010111,
        0b1010001,
        0b1110111,
        0b0010100,
        0b0010111,
    ],
    1: [
        0b111010001011101110111,
        0b101011111010100010100,
        0b111010101011100100111,
        0b101010101010101000100,
        0b101010101010101110111,
    ],
    2: [
        0b000000011110000011111111,
        0b000001111100001110000111,
        0b000111001100000000011100,
        0b011100111000000011100000,
        0b111111111100011100000000,
        0b000011100001110000000000,
        0b000111000111111110110000,
    ],
}
