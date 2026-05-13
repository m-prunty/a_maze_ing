"""Animator module to handle animation tasks using an event loop."""

from collections.abc import Callable
from typing import Any

from .event_loop import Event_loop


class Animator:
    """Animator class to manage animations using the Event_loop."""

    @staticmethod
    def animate(
        func: Callable[[Any], Any], params: tuple[Any], delay: int
    ) -> None:
        """Schedule a function to call repeatedly with a specified delay."""
        Event_loop.do_repeat(func, params, delay)
