"""Animator module to handle animation tasks using an event loop."""

from collections.abc import Callable
from typing import Any, Never

from .event_loop import Event_loop


class Animator:
    """Animator class to manage animations using the Event_loop."""

    @staticmethod
    def animate(
        func: Callable[..., Any],
        params: tuple[Never | Any, ...],
        delay: float = 0.01,
    ) -> None:
        """Schedule a function to call repeatedly with a specified delay."""
        Event_loop.do_repeat(func, params, delay)
