#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    config.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                               +#+#+#+#+#+   +#+             #
#    Created: 2026/02/03 21:19:22 by maprunty         #+#    #+#              #
#    Updated: 2026/05/07 21:37:34 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Configuration module for maze generation and rendering."""

import ast
import random
from collections.abc import Generator
from typing import Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from ..grid_tools import Vec2


class Config(BaseModel):
    """Configuration class for maze generation and rendering."""

    width: int = Field(ge=5, le=30, default=10)
    height: int = Field(ge=5, le=30, default=10)
    entry: Vec2 = Field(default_factory=lambda: Vec2(0, 0))
    exit: Vec2 = Field(default_factory=lambda: Vec2(5, 0))
    output_file: str = Field(default="maze.txt")
    perfect: bool = Field(default=True)
    seed: int = Field(default=0)
    window_siz: Vec2 = Field(default_factory=lambda: Vec2(900, 900))
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
        """Parse input into a Vec2."""
        if isinstance(v, Vec2):
            return v

        if isinstance(v, str):
            try:
                v = ast.literal_eval(v)
            except Exception as e:
                raise ValueError(f"Invalid Vec2 string: {v}") from e

        if isinstance(v, tuple) and len(v) == 2:
            x, y = v
            return Vec2(int(x), int(y))

        raise ValueError(
            f"Expected Vec2-compatible value, got {type(v).__name__}: {v}"
        )

    @field_validator("filename", "output_file", mode="before")
    @classmethod
    def parse_str(cls, v: Any) -> str:
        """Parse a string repr of a str into a str."""
        if isinstance(v, str):
            return v.strip("\"' ").lower()
        raise ValueError(f"Expected a string, got {type(v).__name__}")

    @field_validator("perfect", mode="before")
    @classmethod
    def parse_bool(cls, v: Any) -> bool:
        """Parse a string repr of a bool into a bool."""
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.strip().lower() in ("true", "1", "yes")
        raise ValueError(f"Expected a boolean, got {type(v).__name__}")

    @field_validator("gen_algo", "path_algo", "color", "pic", mode="before")
    @classmethod
    def parse_Literal(cls, v: Any) -> Any:
        """Parse a string repr of a Literal into the appropriate type."""
        if isinstance(v, int):
            return v if v in (0, 1, 2) else 0
        if isinstance(v, str):
            v = v.strip().lower()
            if v in ("dfs", "prim", "swinder", "wilson", "dijkstra"):
                return v
            if v in ("0", "1", "2"):
                return int(v)
        raise ValueError(
            "Expected a valid gen_algo/path_algo/color value,"
            + " got {type(v).__name__}: {v}"
        )

    @field_validator("width", "height", "seed", mode="before")
    @classmethod
    def parse_int(cls, v: Any) -> int:
        """Parse a string repr of an int into an int."""
        if isinstance(v, float):
            return int(v)
        if isinstance(v, str):
            return int(ast.literal_eval(v))
        if isinstance(v, int):
            return v
        raise ValueError(f"Expected an int, got {type(v).__name__}")

    def __iter__(self) -> Generator[tuple[str, Any], None, None]:
        """Iterate over the model fields and their values."""
        for field in self.model_fields.items():
            name = field[0]
            yield (
                name,
                {
                    "value": getattr(self, name),
                    "type": type(getattr(self, name)),
                },
            )


class ConfigIO:
    """Class for handling input and output of Config instances."""

    @staticmethod
    def from_file(path: str) -> Config:
        """Create a Config instance from a configuration file."""
        try:
            with open(path) as f:
                data: dict[str, Any] = {}
                for line in f:
                    key, value = line.strip().split("=", 1)
                    data[key.lower()] = value
                return Config(**data)
        except Exception as e:
            raise ConfigError(f"Error reading config from file: {e}") from e

    # needs work
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
        """Initialize the ConfigError with a message."""
        super().__init__(message)
