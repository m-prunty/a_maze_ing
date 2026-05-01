#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    config.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                               +#+#+#+#+#+   +#+            #
#    Created: 2026/02/03 21:19:22 by maprunty         #+#    #+#              #
#    Updated: 2026/05/01 05:03:31 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Configuration module for maze generation and rendering."""

import random
from collections.abc import Generator
from typing import Any, Literal

from pydantic import ConfigDict, Field, model_validator
from pydantic.dataclasses import dataclass

from ..grid_tools import Vec2


@dataclass
class Config:
    """Configuration class for maze generation and rendering."""

    window_siz: Vec2 = Field(default=Vec2(900, 900))
    width: int = Field(ge=5, le=30, default=10)
    height: int = Field(ge=5, le=30, default=10)
    entry: Vec2 = Field(default=Vec2(0, 0))
    exit: Vec2 = Field(default=Vec2(5, 0))
    seed: int = Field(default=0)
    perfect: bool = Field(default=True)
    pic: Literal[1, 2, 3] = Field(default=1)
    pic_scalar: float = Field(default=1.0)
    filename: str = Field(default="config.txt")
    output_file: str = Field(default="maze.txt")
    model_config = ConfigDict(revalidate_instances="always")
    color: Literal[0, 1, 2] = 0
    gen_algo: Literal["Dfs", "prim", "swinder", "wilson"] = "Dfs"

    def is_grid(self, vec: Vec2) -> Vec2:
        """Check if a Vec2 instance is within the grid bounds."""
        rx = random.randint(0, 1)
        ry = random.randint(0, 1)
        tst = (self.width, self.height)
        if not (0 <= vec.x < tst[0]) or not (0 <= vec.y < tst[1]):
            print(f"Wont fit on the grid...{tst} {vec}")
            return Vec2(
                ((tst[0] - 1 * rx) - 1 + rx),
                ((tst[1] - 1 * ry) - 1 + ry),
            )
        return vec

    @model_validator(mode="after")
    def is_valid(self):
        """Validate the entry and exit points are within the grid bounds."""
        try:
            self.exit = self.is_grid(self.exit)
            return self
        except Exception as e:
            print(e)

    @classmethod
    def cfg_from_filemap(cls, hexlist):
        """Create a Config instance from a hexlist repr of the maze."""
        vlst = []
        c_dct = {"width": len(hexlist[1])}
        for i, j in enumerate(hexlist[1:]):
            if "," in j:
                vlst += j.split(",")
                i -= 1
        c_dct["height"] = i - 3
        c_dct["entry"] = Vec2(vlst[0], vlst[1])
        c_dct["exit"] = Vec2(vlst[2], vlst[3])
        return cls(**c_dct)

    def get_pic(self, select: int):
        """Get the picture data for the maze based on the selected option."""
        if select == 1:
            self.pic = [
                0b1010111,
                0b1010001,
                0b1110111,
                0b0010100,
                0b0010111,
            ]
        elif select == 2:
            self.pic = [
                0b111010001011101110111,
                0b101011111010100010100,
                0b111010101011100100111,
                0b101010101010101000100,
                0b101010101010101110111,
            ]
        elif select == 3:
            self.pic = [
                0b000000011110000011111111,
                0b000001110100001110000111,
                0b000111011100000000011100,
                0b011100111000000011100000,
                0b111111111100011100000000,
                0b000011100001110000000000,
                0b000111000111111110110000,
            ]

    @classmethod
    def cfg_from_file(cls, filename: str) -> "Config":
        """Create a Config instance from a configuration file."""
        c_dct = {"filename": filename}
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    try:
                        k, v = line.split("=")
                        k = k.strip().lower()
                        if "[" in v:
                            v = Vec2(*[e.strip(",[]") for e in (v.split(","))])
                        elif "(" in v:
                            v = Vec2(
                                *[int(e.strip(",()")) for e in (v.split(","))]
                            )
                        elif v == "None":
                            v = None
                        elif "," in v:
                            v = v.split(",")
                            v = (v[0], v[1])
                        elif v.lower() in ("true", "false"):
                            v = v.lower() == "true"
                        elif v.isnumeric():
                            v = int(v)
                    except ValueError as ve:
                        print(
                            f"Error: {ve} something's not right with config\
                                        {k}:{v} "
                        )
                    c_dct.update({k: v})
                    # print(c_dct)
        return cls(**c_dct)

    def cfg_to_file(self) -> None:
        """Write the Config instance to a configuration file."""
        with open(self.filename, "w") as f:
            for k, v in vars(self).items():
                f.write(f"{k.upper()}={v.__str__()}\n")

    def __iter__(self) -> Generator[tuple[str, Any], None, None]:
        """Iterate over the fields of the Config instance."""
        for v in fields(self):
            yield v.name, getattr(self, v.name)


#
#    @property
#    def entry(self) -> Vec2:
#        """Get the entry point as a Vec2 instance."""
#        return Vec2(self.entry[0], self.entry[1])
#
#    @entry.setter
#    def entry(self, val: Vec2) -> None:
#        """Set the entry point, ensuring it is within the grid bounds."""
#        print("entred setter")
#        if val.x < 0 or val.y < 0 or val.x > self.width or val.y > self.height:
#            raise ValueError
#        self.entry = Vec2(val.x, val.y)
#
#    @property
#    def exit(self) -> Vec2:
#        """Get the exit point as a Vec2 instance."""
#        return Vec2(self.exit[0], self.exit[1])
#
#    @exit.setter
#    def exit(self, val: Vec2) -> None:
#        """Set the exit point, ensuring it is within the grid bounds."""
#        print("entred setter")
#        if val.x < 0 or val.y < 0 or val.x > self.width or val.y > self.height:
#            raise ValueError
#        self.exit = Vec2(val.x, val.y)
#
#    @property
#    def window_siz(self) -> Vec2:
#        """Get the window size as a Vec2 instance."""
#        return Vec2(self.window_siz[0], self.window_siz[1])
#
#    @window_siz.setter
#    def window_siz(self, val: Vec2) -> None:
#        """Set the window size, ensuring it is positive."""
#        self.window_siz = Vec2(val.x, val.y)
