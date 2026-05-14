# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    vector.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:37:00 by maprunty         #+#    #+#              #
#    Updated: 2026/05/14 12:57:00 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""TODO: Short module summary.

Optional longer description.
"""

from collections.abc import Iterator
from math import sqrt

from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class Vec2:
    """Class for storing 2D Coords."""

    x: int | float = Field(default=0)
    y: int | float = Field(default=0)

    def normalized(self) -> "Vec2":
        """Return a normalized version of the vector."""
        mag = abs(self)
        if mag == 0:
            raise ValueError("Cannot normalize zero vector")
        return self / mag

    def __add__(self, other: "Vec2") -> "Vec2":
        """Add a vec2 instance with another."""
        return Vec2(
            self.x + other.x,
            self.y + other.y,
        )

    def __sub__(self, other: "Vec2") -> "Vec2":
        """Sub a vec2 instance with another."""
        return Vec2(
            self.x - other.x,
            self.y - other.y,
        )

    def __mul__(self, scaler: int) -> "Vec2":
        """Multiply a vec2 instance by a scalar."""
        return Vec2(
            self.x * scaler,
            self.y * scaler,
        )

    def __truediv__(self, scalar: float) -> "Vec2":
        """Divide a vec2 instance by a scalar."""
        return Vec2(self.x / scalar, self.y / scalar)

    def __eq__(self, other: object) -> bool:
        """Equate a vec2 instance with another."""
        if not isinstance(other, Vec2):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __gt__(self, other: "Vec2") -> bool:
        """Equate a vec2 instance with another."""
        return abs(self) >= abs(other)

    def __ge__(self, other: "Vec2") -> bool:
        """Equate a vec2 instance with another."""
        return self > other or self == other

    def __lt__(self, other: "Vec2") -> bool:
        """Equate a vec2 instance with another."""
        return abs(self) <= abs(other)

    def __le__(self, other: "Vec2") -> bool:
        """Equate a vec2 instance with another."""
        return self < other or self == other

    def __abs__(self) -> float:
        """Return magnitude of a vector."""
        return sqrt(self.x**2 + self.y**2)

    def __repr__(self) -> str:
        """Return a tuple represantation of a Vec2 instance."""
        cls = self.__class__.__name__
        return f"{cls}(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        """Return a str tuple represantation of a Vec2 instance."""
        return f"{self.x},{self.y}"

    def __iter__(self) -> Iterator[float | int]:
        """Iterate over the fields of a Vec2 instance."""
        return iter((self.x, self.y))

    def __hash__(self) -> int:
        """Return a hash of a Vec2 instance."""
        return hash((self.x, self.y))
