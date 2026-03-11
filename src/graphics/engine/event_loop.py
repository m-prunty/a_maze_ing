from graphics import Mlx_context, Window
from Xlib import XK
# import threading
import time

class Event_loop:
    _events = []
    _repeatables = []
    _strs = []
    
    def launch():
        Mlx_context._mlx.mlx_loop_hook(Mlx_context.get(), Event_loop.render_event, None)
        Event_loop.add_key_hook(Event_loop.input_event, None)
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
        # Mlx_context._mlx.mlx_do_sync(Mlx_context.get())
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
    
    @classmethod
    def input_to_str(cls, field, key, func: callable, params: tuple, end_func: callable, end_params: tuple):
        cls._strs.append({"FIELD": field, "KEY": key, "CURSOR": 0, "SPECIAL": None, "FUNCTION": func, "PARAMS": params, "END": end_func, "END_PARA": end_params})
        
    @classmethod
    def input_event(cls, input, _):
        # print(input)
        key = XK.keysym_to_string(input)
        # print(key, input)
        for dict in cls._strs:
            val = dict["FIELD"][dict["KEY"]]
            if (input == 65293):
                # print(string["END_PARA"])
                if (dict["END_PARA"] is not None):
                    dict["FIELD"][dict["KEY"]] = f"{val[: dict['CURSOR']]}{val[dict['CURSOR'] + 1:]}"
                    dict["END"](*dict["END_PARA"])
                else:
                    dict["FIELD"][dict["KEY"]] = f"{val[: dict['CURSOR']]}{val[dict['CURSOR'] + 1:]}"
                    dict["END"]()
                cls._strs.remove(dict)
            else:
                dict["FIELD"][dict["KEY"]] = f"{val[: dict['CURSOR']]}{val[dict['CURSOR'] + 1:]}"
                if (input == 65288):
                    val = dict["FIELD"][dict["KEY"]]
                    dict["FIELD"][dict["KEY"]] = f"{val[:dict['CURSOR'] - 1]}{val[dict['CURSOR']:]}"
                    dict['CURSOR'] -= 1
                elif (input == 65361 and dict['CURSOR'] > 0):
                    dict['CURSOR'] -= 1
                elif (input == 65363 and dict['CURSOR'] < len(dict["FIELD"][dict["KEY"]])):
                    dict['CURSOR'] += 1
                elif (key is None or not key.isprintable):
                    print(input, "is not supported")
                elif dict["SPECIAL"] is None and key.isprintable:
                    val = dict["FIELD"][dict["KEY"]]
                    dict["FIELD"][dict["KEY"]] = f"{val[: dict['CURSOR']]}{f'{key}'}{val[dict['CURSOR']:]}"
                    dict['CURSOR'] += 1
                val = dict["FIELD"][dict["KEY"]]
                dict["FIELD"][dict["KEY"]] = f"{val[:dict['CURSOR']]}|{val[dict['CURSOR']:]}"
                if (dict["PARAMS"] is not None):
                    dict["FUNCTION"](*dict["PARAMS"])
                else:
                    dict["FUNCTION"]()
            
            
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