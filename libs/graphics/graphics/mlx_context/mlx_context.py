"""MlxContext is a singleton class that manages the mlx context."""

from typing import Any

from mlx import Mlx


class Mlx_context:
    """MlxContext is a singleton class that manages the mlx context.

    It ensures that only one instance of the mlx context is created
    and provides a global access point to it.
    """

    _mlx_ptr = None
    _mlx = Mlx()
    _initialized = False

    @classmethod
    def create(cls) -> None:
        """Create the mlx context if it hasn't been initialized yet."""
        if cls._initialized:
            raise RuntimeError("MlxContext already initialized")
        cls._mlx_ptr = cls._mlx.mlx_init()
        cls._initialized = True

    @classmethod
    def get(cls) -> Any:
        """Get the mlx context pointer, creating it if necessary."""
        if not cls._initialized:
            cls.create()
        return cls._mlx_ptr
