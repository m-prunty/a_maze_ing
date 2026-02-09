

from graphics import mlx

class Mlx_context:
    _mlx_ptr = None
    _initialized = False

    @classmethod
    def create(cls):
        if cls._initialized:
            raise RuntimeError("MlxContext already initialized")
        cls._mlx_ptr = mlx.mlx_init()
        cls._initialized = True

    @classmethod
    def get(cls):
        if not cls._initialized:
            cls.create()
        return cls._mlx_ptr