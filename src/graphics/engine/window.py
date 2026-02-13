from graphics import Mlx_context, Mlx
from helper import Vec2

class Window:
    _win_ptr = None
    _siz : Vec2 = None
    _initialized = False

    @classmethod
    def create(cls, siz: Vec2, name: str):
        if cls._initialized:
            raise RuntimeError("MlxContext already initialized")
        cls._siz = siz
        cls._win_ptr = Mlx_context._mlx.mlx_new_window(Mlx_context.get(), siz.x, siz.y, name) 
        cls._initialized = True

    @classmethod
    def get_siz(cls) -> Vec2:
        if cls._siz is not None:
            print("siz not initilized run Window.create")
        return cls._siz

    @classmethod
    def get(cls):
        if not cls._initialized:
            raise RuntimeError("First need to call Window.create for initialization")
        return cls._win_ptr
    
    @classmethod
    def clear_window(self):
        Mlx_context._mlx.mlx_clear_window(Mlx_context.get(), self._win_ptr)