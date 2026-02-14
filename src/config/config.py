#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    config.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/02/03 21:19:22 by maprunty         #+#    #+#              #
#    Updated: 2026/02/04 20:33:39 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import random

from pydantic import ConfigDict, Field, field_validator, model_validator
from pydantic.dataclasses import dataclass

from helper import Vec2

maxw = 30


@dataclass
class Config:
    maxw = 30
    width: int
    height: int
    entry: Vec2
    exit: Vec2
    perfect: bool | None = None
    pic: list[int] | None = None
    pic_scalar: float | None = 1
    filename: str | None = Field(default="config.txt")
    output_file: str | None = Field(default="maze.txt")
    model_config = ConfigDict(revalidate_instances="always")
    color = 2

    def is_grid(self, vec: Vec2) -> Vec2:
        """Check if a vector lives in the grid.

        Args:
            vec (Vec2): the coordinates to check if exist in grid

        Returns:
            type: Vec2(vec) if valid othereise Vec2(width-1, height-1)
        """
        rx = random.randint(0, 1)
        ry = random.randint(0, 1)
        tst = (self.width, self.height)
#         print(
#             f"test{tst} {vec} {not 0 <= vec.x < tst[0]} or {not 0 <= vec.y < tst[1]}\
#  == {not 0 <= vec.x < tst[0] or not 0 <= vec.y < tst[1]}"
#         )
#         print("aa", vec, tst)
        if not (0 <= vec.x < tst[0]) or not (0 <= vec.y < tst[1]):
            print(f"Wont fit on the grid...{tst} {vec}")
            return Vec2(
                ((tst[0] * rx) - 1 + rx) % (self.width - 1),
                ((tst[1] * ry) - 1 + ry) % (self.height - 1),
            )
        return vec

    @field_validator("width", "height", mode="before")
    @classmethod
    def valid_sz(cls, value: int) -> int:
        """Check if value is within bounds (1, 30).

        Args:
            value (int): value to check against.

        Returns:
            type: Int the bvalue itself.

        Raises:
            ExceptionType: When out of bountds .
        """
        if 1 <= value <= maxw:
            cls.maxw = value
            return value
        raise ValueError(f"range (1, 30); value = {value}")

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
        # print(c_dct)
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
                        elif "," in v:
                            v = v.split(",")
                            v = Vec2(v[0], v[1])
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
