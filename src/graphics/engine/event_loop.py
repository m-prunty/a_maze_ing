from graphics import Mlx, Mlx_context, Window

class Event_loop:
    _events = []
    
    @staticmethod
    def launch():
        Mlx_context._mlx.mlx_loop_hook(Mlx_context.get(), Event_loop.render_event, None)
        Mlx_context._mlx.mlx_loop(Mlx_context.get())
    
    @staticmethod
    def add_hook(func: callable, event: int, param):
        Mlx_context._mlx.mlx_hook(Window.get(), event, 0, func, None)

    @staticmethod
    def add_mous_hook(func: callable, param):
        Mlx_context._mlx.mlx_mouse_hook(Window.get(), func, param)

    @staticmethod
    def add_key_hook(func: callable, param):
        Mlx_context._mlx.mlx_key_hook(Window.get(), func, param)

    @staticmethod
    def close(dummy):
        Mlx_context._mlx.mlx_destroy_window(Mlx_context.get(), Window.get())
        Mlx_context._mlx.mlx_loop_exit(Mlx_context.get())
    
    @classmethod
    def do_event(cls, event: callable, params: tuple):
        # if cls._initialized:
        #     raise RuntimeError("MlxContext already initialized")
        cls._events.append((event, params))
        cls._initialized = True
    
    @classmethod
    def render_event(cls, params):
        Mlx_context._mlx.mlx_do_sync(Mlx_context.get()) 
        for event in cls._events:
            event[0](*event[1])
        cls._events.clear()