"""Window class for managing the window in the application."""

from typing import Any

from mazegen.grid_tools import Vec2

from ..mlx_context import Mlx_context


class Window:
    """Window class to manage the window in the application."""

    _win_ptr = None
    _siz: Vec2
    _initialized = False

    @classmethod
    def create(cls, siz: Vec2, name: str) -> None:
        """Create the window with the specified size and name."""
        if cls._initialized:
            raise RuntimeError("MlxContext already initialized")
        cls._siz = siz
        cls._win_ptr = Mlx_context._mlx.mlx_new_window(
            Mlx_context.get(), siz.x, siz.y, name
        )
        cls._initialized = True

    @classmethod
    def get_siz(cls) -> Vec2:
        """Get the size of the window."""
        if cls._siz is None:
            print("siz not initilized run Window.create")
        return cls._siz

    @classmethod
    def get(cls) -> Any:
        """Get the window pointer."""
        if not cls._initialized:
            raise RuntimeError("First need to call")
        return cls._win_ptr

    @classmethod
    def clear_window(self) -> None:
        """Clear the window by filling it with a default color."""
        Mlx_context._mlx.mlx_clear_window(Mlx_context.get(), self._win_ptr)
