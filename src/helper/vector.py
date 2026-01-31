# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    vector.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:37:00 by maprunty         #+#    #+#              #
#    Updated: 2026/01/31 02:58:38 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""TODO: Short module summary.

Optional longer description.
"""


class Vec2:
    """Class for storing 2D Coords."""

    def __init__(self, x: int = 0, y: int = 0):
        """TODO: to be defined."""
        self.x = 0
        self.y = 0
        try:
            self.x = x
            self.y = y
        except Exception as e:
            print(e)
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

    def __eq__(self, other):
        """Equate a vec2 instance with another."""
        return self.x == other.x and self.y == other.y

    def __abs__(self):
        """Return magnitude of a vector."""
        return sqrt(self.x**2 + self.y**2)

    def __repr__(self):
        """Return a tuple represantation of a Vec2 instance."""
        return (self.x, self.y)

    def __str__(self):
        """Return a str tuple represantation of a Vec2 instance."""
        return f"{self.__repr__()}"

    def __iter__(self):
        """Return a tuple iterable  represantation of a Vec2 instance."""
        return iter(self.__repr__())

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
