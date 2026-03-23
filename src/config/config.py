#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    config.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/02/03 21:19:22 by maprunty         #+#    #+#              #
#    Updated: 2026/03/08 15:21:56 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import random

from typing import Literal
from pydantic import ConfigDict, Field, model_validator
from pydantic.dataclasses import dataclass
from dataclasses import fields

from helper import Vec2

# maxw = 30

@dataclass
class Config:
    _window_siz: tuple = (900, 900)
    width: int = Field(ge=5, le=30)
    height: int = Field(ge=5, le=30)
    _entry: tuple = (0, 0)
    _exit: tuple = (5, 0)
    seed: int = 0
    perfect: bool = True
    pic: Literal[1, 2, 3] = 1
    pic_scalar: float = 1.0
    filename: str = Field(default="config.txt")
    output_file: str = Field(default="maze.txt")
    model_config = ConfigDict(revalidate_instances="always")
    color: Literal[0, 1, 2] = 0
    gen_algo: Literal["Dfs", "prim", "swinder", "wilson"] = "Dfs"


    def is_grid(self, vec: Vec2) -> bool:
        """Check if a vector lives in the grid and return a border value if not.

        Args:
            vec (Vec2): the coordinates to check if exist in grid

        Returns:
            type: Vec2(vec) if valid othereise Vec2(width-1, height-1)
        """
        rx = random.randint(0, 1)
        ry = random.randint(0, 1)
        tst = (self.width, self.height)
        if not (0 <= vec.x < tst[0]) or not (0 <= vec.y < tst[1]):
            print(f"Wont fit on the grid...{tst} {vec}")
            return Vec2(
                ((tst[0] - 1 * rx) - 1 + rx),
                ((tst[1] - 1 * ry) - 1 + ry),
            )
        # print(vec)
        return vec

    # @field_validator("width", "height", mode="before")
    # @classmethod
    # def valid_sz(cls, value: int) -> int:
    #     """Check if value is within bounds (1, 30).

    #     Args:
    #         value (int): value to check against.

    #     Returns:
    #         type: Int the bvalue itself.

    #     Raises:
    #         ExceptionType: When out of bountds .
    #     """
    #     if 1 <= value <= maxw:
    #         cls.maxw = value
    #         return value
    #     raise ValueError(f"range (1, 30); value = {value}")

    @model_validator(mode="after")
    def is_valid(self):
        try:
            # print(self.is_grid(self.entry))
            self.exit = self.is_grid(self.exit)
            # print("height", self.entry)
            # print("width", self.exit)

        except Exception as e:
            # print(ingrid.index(v), "Out of grid bounds", v, e)
            # v = Vec2(ingrid.index(v), 0)
            print(e)

    @classmethod
    def cfg_from_filemap(cls, hexlist):
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
    def cfg_from_file(cls, filename: str):
        """TODO: Docstring for from_fil.

        Args:
            filename (str): TODO

        Returns: TODO

        """
        c_dct = {"filename": filename}
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    try:
                        k, v = line.split("=")
                        k = k.strip().lower()
                        if "[" in v:
                            v = [e.strip(",[]") for e in (v.split(","))]
                        elif "(" in v:
                            v = [int(e.strip(",()")) for e in (v.split(","))]
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

    def cfg_to_file(self):
        with open(self.filename, "w") as f:
            for k, v in vars(self).items():
                f.write(f"{k.upper()}={v.__str__()}\n")
                # print(f"{k.upper()}={v.__str__()}\n")
        # with open(filename) as f:
        #    for line in f:

    def __iter__(self):
        for v in fields(self):
            yield v.name, getattr(self, v.name)
            
    @property
    def entry(self):
        # print(self)
        return Vec2(self._entry[0], self._entry[1])
    
    @entry.setter
    def entry(self, val: Vec2):
        print("entred setter")
        if (val.x < 0 or val.y < 0
            or val.x > self.width or val.y > self.height):
            raise ValueError
        self._entry = (val.x, val.y)
        
    @property
    def exit(self):
        # print(Vec2(self._exit[0], self._exit[1]))
        return Vec2(self._exit[0], self._exit[1])
    
    @exit.setter
    def exit(self, val: Vec2):
        print("entred setter")
        if (val.x < 0 or val.y < 0
            or val.x > self.width or val.y > self.height):
            raise ValueError
        self._exit = (val.x, val.y)
        
    @property
    def window_siz(self):
        return Vec2(self._window_siz[0], self._window_siz[1])
    
    @window_siz.setter
    def window_siz(self, val: Vec2):
        self._window_siz = (val.x, val.y)