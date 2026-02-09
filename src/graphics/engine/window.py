from graphics import mlx_context, mlx
from helper import Vec2

class Window:
    _win_ptr = None
    _siz = None
    _initialized = False

    @classmethod
    def create(cls, siz: Vec2, name: str):
        if cls._initialized:
            raise RuntimeError("MlxContext already initialized")
        
        cls._win_ptr = mlx.mlx_new_window(mlx_context.get(), siz.x, siz.y, name) 
        cls._initialized = True

    @classmethod
    def get_siz(cls):
        if cls._siz is not None:
            print("siz not initilized run Window.create")
        return cls._siz

    @classmethod
    def get(cls):
        if not cls._initialized:
            raise RuntimeError("First need to call Window.create for initialization")
        return cls._win_ptr