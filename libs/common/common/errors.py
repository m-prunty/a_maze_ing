#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    errors.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/10 07:46:29 by maprunty         #+#    #+#              #
#    Updated: 2026/05/12 10:01:25 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Custom exceptions for A-Maze-ing."""

import os
import sys


class MazeError(Exception):
    """Custom exception for maze generation and pathfinding errors."""

    def __init__(self, message: str) -> None:
        """Initialize the MazeError with a message incl file and line info."""
        exc_type, exc_obj, exc_tb = sys.exc_info()

        if exc_tb:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            line_no = exc_tb.tb_lineno
            full_message = f"{message} | " + f" in {fname} at line {line_no}"
        else:
            full_message = message
        super().__init__(full_message)


class StartError(MazeError):
    """Exception raised for errors during the start screen."""

    def __init__(self, message: str) -> None:
        """Initialize the StartError."""
        super().__init__(f"StartError: {message}")


class ConfigError(MazeError):
    """Exception raised for errors in configuration loading."""

    def __init__(self, message: str) -> None:
        """Initialize the ConfigError."""
        super().__init__(f"ConfigError: {message}")


class RenderError(MazeError):
    """Exception raised for errors during rendering."""

    def __init__(self, message: str) -> None:
        """Initialize the RenderError."""
        super().__init__(f"RenderError: {message}")


class AlgoError(MazeError):
    """Exception raised for errors in generation or pathfinding algorithms."""

    def __init__(self, message: str) -> None:
        """Initialize the AlgoError."""
        super().__init__(f"AlgoError: {message}")


class StageError(MazeError):
    """Exception raised for errors in staging."""

    def __init__(self, message: str) -> None:
        """Initialize the StageError."""
        super().__init__(f"StageError: {message}")
