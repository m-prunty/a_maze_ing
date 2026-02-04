# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    vector.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:37:00 by maprunty         #+#    #+#              #
#    Updated: 2026/02/04 13:31:05 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""TODO: Short module summary.

Optional longer description.
"""

from math import sqrt

from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class Vec2:
    """Class for storing 2D Coords."""

    x: int | float | None = Field(default=0)
    y: int | float | None = Field(default=0)
    # except Exception as e:
    #    print(e)
    # raise ValueError(e)

    def __add__(self, other):
        """Add a vec2 instance with another."""
        return Vec2(
            self.x + other.x,
            self.y + other.y,
        )

    def __sub__(self, other):
        """Sub a vec2 instance with another."""
        return Vec2(
            self.x - other.x,
            self.y - other.y,
        )

    def __mul__(self, scaler: int):
        """Multiply a vec2 instance by a scalar."""
        return Vec2(
            self.x * scaler,
            self.y * scaler,
        )

    def __eq__(self, other):
        """Equate a vec2 instance with another."""
        return self.x == other.x and self.y == other.y

    def __gt__(self, other):
        """Equate a vec2 instance with another."""
        return self.x >= other.x and self.y >= other.y

    def __lt__(self, other):
        """Equate a vec2 instance with another."""
        return self.x <= other.x and self.y <= other.y

    def __abs__(self):
        """Return magnitude of a vector."""
        return sqrt(self.x**2 + self.y**2)

    def __repr__(self):
        """Return a tuple represantation of a Vec2 instance."""
        cls = self.__class__.__name__
        return f"{cls}(x={self.x}, y={self.y})"

    def __str__(self):
        """Return a str tuple represantation of a Vec2 instance."""
        return f"{self.x},{self.y}"


    def __iter__(self):
        """Return a tuple iterable  represantation of a Vec2 instance."""
        return iter((self.x, self.y))

    @classmethod
    def from_str(cls, coord: str) -> "Vec2":
        """TODO: Docstring for from_str.

        Args:
            coord (str): coordinates in form "x,y,z"

        Returns: An instance of Vec2

        """
        try:
            lst = [0]
            lst += cls.ft_split(coord, ",")
            lst = cls.parse_args(len(lst), lst)
            return cls(lst[0], lst[1])
        except Exception as e:
            r_str = f"Error details - Type: {e.__class__.__name__}"
            r_str += f', Args: ("{e.args[0]}",)'
            raise ValueError(r_str)
