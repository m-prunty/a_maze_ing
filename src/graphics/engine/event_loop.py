from graphics import mlx, Mlx_context, Window

class Event_loop:
    _events = []
    
    @classmethod
    def launch():
        mlx.mlx_loop_hook(Mlx_context.get(), Event_loop.render_event, None)
        mlx.mlx_loop(Mlx_context.get())
    
    @classmethod
    def add_hook(func: callable, event: int, param):
        mlx.mlx_hook(Window.get(), event, 0, func, None)

    @classmethod
    def add_mous_hook(func: callable, param):
        mlx.mlx_mouse_hook(Window.get(), func, param)

    @classmethod
    def add_key_hook(func: callable, param):
        mlx.mlx_key_hook(Window.get(), func, param)

    @classmethod
    def close(dummy):
        mlx.mlx_destroy_window(Mlx_context.get(), Window.get())
        mlx.mlx_loop_exit(Mlx_context.get())
    
    @classmethod
    def do_event(cls, event: callable, params: tuple):
        # if cls._initialized:
        #     raise RuntimeError("MlxContext already initialized")
        cls._events.append((event, params))
        cls._initialized = True
    
    @classmethod
    def render_event(cls, params):
        mlx.mlx_do_sync(Mlx_context.get())
        for event in cls._events:
            event[0](*event[1])
        cls._events.clear()