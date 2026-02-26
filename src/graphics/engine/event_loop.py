from graphics import Mlx_context, Window
import threading
import time

class Event_loop:
    _events = []
    _repeatables = []
    _repeatables = []
    
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
    def do_event(cls, event: callable, params: tuple=None):
        cls._events.append((event, params))

    @classmethod
    def do_repeat(cls, event: callable, params: tuple=None, delay=0.3):
        """ Will stop when function returns -1"""
        print("param is :", params)
        cls._repeatables.append([event, delay, time.time() + delay, params])

    @classmethod
    def render_event(cls, params):
        Mlx_context._mlx.mlx_do_sync(Mlx_context.get())
        # print(cls._events)
        for event in cls._events:
            event[0](*event[1])
        # Mlx_context._mlx.mlx_do_sync(Mlx_context.get())
            
        cls._events.clear()
        now = time.time()
        for animation in cls._repeatables:
            # print("yo")
            if (now >= animation[2]):
                if hasattr(animation[3], '__iter__'):
                    if (animation[0](*animation[2]) == -1):
                        cls._repeatables.remove(animation)
                else:
                    if (animation[0]() == -1):
                        cls._repeatables.remove(animation)
                animation[2] = now + animation[1]
        # cls._repeatables.clear()
        
            
			
    # @classmethod
    # def run_anim(cls, animation):
    #     # print(animation[2])
    #     # if (animation[0] and animation[2] is not None):
    #     if (hasattr(animation[2], '__iter__')):
    #         if (animation[0](*animation[2]) != -1):
    #             cls._repeatables.append(animation)
    #     else:
    #         if (animation[0]() != -1):
    #             cls._repeatables.append(animation)