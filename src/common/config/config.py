#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    config.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                               +#+#+#+#+#+   +#+             #
#    Created: 2026/02/03 21:19:22 by maprunty         #+#    #+#              #
#    Updated: 2026/05/04 09:24:57 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Configuration module for maze generation and rendering."""

import ast
import random
from typing import Any, Literal, cast

from pydantic import ConfigDict, Field, field_validator, model_validator
from pydantic.dataclasses import dataclass

from ..grid_tools import Vec2


@dataclass
class Config:
    """Configuration class for maze generation and rendering."""

    width: int = Field(ge=5, le=30, default=10)
    height: int = Field(ge=5, le=30, default=10)
    entry: Vec2 = Field(default=Vec2(0, 0))
    exit: Vec2 = Field(default=Vec2(5, 0))
    output_file: str = Field(default="maze.txt")
    perfect: bool = Field(default=True)
    seed: int = Field(default=0)
    window_siz: Vec2 = Field(default=Vec2(900, 900))
    pic: Literal[1, 2, 3] = Field(default=1)
    pic_scalar: float = Field(default=1.0)
    filename: str = Field(default="config.txt")
    model_config = ConfigDict(revalidate_instances="always")
    color: Literal[0, 1, 2] = 0
    gen_algo: Literal["dfs", "prim", "swinder", "wilson", "dijkstra"] = "dfs"
    path_algo: Literal["dfs", "prim", "swinder", "wilson", "dijkstra"] = (
        "dijkstra"
    )

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
    def validate_bounds(self) -> "Config":
        """Validate that the entry and exit are within the grid bounds."""
        if not (0 <= self.exit.x < self.width) or not (
            0 <= self.exit.y < self.height
        ):
            raise ValueError("exit out of bounds")
        if not (0 <= self.entry.x < self.width) or not (
            0 <= self.entry.y < self.height
        ):
            raise ValueError("entry out of bounds")
        return self

    @field_validator("entry", "exit", "window_siz", mode="before")
    @classmethod
    def parse_vec2(cls, v: Any) -> Vec2:
        """Parse a string repr of a Vec2 instance into a Vec2 instance."""
        if isinstance(v, str):
            x, y = ast.literal_eval(v)
        if isinstance(v, tuple) and len(v) == 2:
            x, y = v
        if isinstance(v, Vec2):
            return Vec2(x, y)
        else:
            try:
                x, y = int(x), int(y)
                return Vec2(x, y)
            except Exception as e:
                raise ValueError(
                    f"Expected a Vec2, got {type(v).__name__} with value {v}"
                ) from e

    @field_validator("filename", "output_file", "gen_algo", mode="before")
    @classmethod
    def parse_str(cls, v: Any) -> str:
        """Parse a string repr of a str into a str."""
        if isinstance(v, str):
            return v.strip("\"' ").lower()
        raise ValueError(f"Expected a string, got {type(v).__name__}")

    @field_validator("pic", "color", mode="before")
    @classmethod
    def parse_int(cls, v: Any) -> int:
        """Parse a string repr of an int into an int."""
        if isinstance(v, str):
            return cast(int, ast.literal_eval(v))
        if isinstance(v, int):
            return v
        raise ValueError(f"Expected an int, got {type(v).__name__}")


#    def __iter__(self) -> Generator[tuple[str, Any], None, None]:
#        """Iterate over the fields of the Config instance."""
#        for v in fields(self):
#            yield v.name, getattr(self, v.name)


class ConfigIO:
    """Class for handling input and output of Config instances."""

    @staticmethod
    def from_file(path: str) -> Config:
        """Create a Config instance from a configuration file."""
        try:
            with open(path) as f:
                data = {}
                for line in f:
                    key, value = line.strip().split("=", 1)
                    data[key.lower()] = value
                return Config(**data)
        except Exception as e:
            raise ConfigError(f"Error reading config from file: {e}") from e

    @staticmethod
    def from_filemap(path: str) -> Config:
        """Create a Config instance from a hexlist repr of the maze."""
        with open(path) as f:
            hexlist = f.read().split("\n")
        vlst = []
        c_dct: dict[str, Any] = {"width": len(hexlist[1])}
        for i, j in enumerate(hexlist[1:]):
            if "," in j:
                vlst += j.split(",")
                i -= 1
        c_dct["height"] = i - 3
        c_dct["entry"] = Vec2(int(vlst[0]), int(vlst[1]))
        c_dct["exit"] = Vec2(int(vlst[2]), int(vlst[3]))
        return Config(**c_dct)

    @staticmethod
    def to_file(cfg: Config, path: str | None = None) -> None:
        """Write the Config instance to a configuration file."""
        if path is None:
            path = cfg.filename
        try:
            with open(path, "w") as f:
                for k, v in vars(cfg).items():
                    f.write(f"{k.upper()}={v.__str__()}\n")
        except Exception as e:
            raise ConfigError(f"Error writing config to file: {e}") from e


class ConfigError(Exception):
    """Custom exception for configuration errors."""

    def __init__(self, message: str):
        super().__init__(message)


#    def cfg_from_file(cls, filename: str) -> "Config":
#        """Create a Config instance from a configuration file."""
#        c_dct = {"filename": filename}
#        with open(filename) as f:
#            for line in f:
#                line = line.strip()
#                if line and not line.startswith("#"):
#                    try:
#                        k, v = line.split("=")
#                        k = k.strip().lower()
#                        if "[" in v:
#                            v = Vec2(*[e.strip(",[]") for e in (v.split(","))])
#                        elif "(" in v:
#                            v = Vec2(
#                                *[int(e.strip(",()")) for e in (v.split(","))]
#                            )
#                        elif v == "None":
#                            v = None
#                        elif "," in v:
#                            v = v.split(",")
#                            v = (v[0], v[1])
#                        elif v.lower() in ("true", "false"):
#                            v = v.lower() == "true"
#                        elif v.isnumeric():
#                            v = int(v)
#                    except ValueError as ve:
#                        print(
#                            f"Error: {ve} something's not right with config\
#                                        {k}:{v} "
#                        )
#                    c_dct.update({k: v})
# print(c_dct)
#        return cls(**c_dct)
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
