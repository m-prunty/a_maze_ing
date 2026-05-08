# import threading
import time

from Xlib import XK   # type: ignore 

from ..mlx_context import Mlx_context
from .window import Window
from collections.abc import Callable
from typing import Any


class Event_loop:
    _events: list[tuple]= []
    _repeatables: list[list] = []
    _key_funcs: list[dict] = []
    _str: dict= {}

    @staticmethod
    def launch() -> None:
        Mlx_context._mlx.mlx_loop_hook(
            Mlx_context.get(), Event_loop.render_event, None
        )
        Mlx_context._mlx.mlx_key_hook(
            Window.get(), Event_loop.input_event, None
        )
        Mlx_context._mlx.mlx_loop(Mlx_context.get())

    @staticmethod
    def add_hook(func: Callable, event: int, param) -> None:
        Mlx_context._mlx.mlx_hook(Window.get(), event, 0, func, None)

    @staticmethod
    def add_mous_hook(func: Callable, param) -> None:
        Mlx_context._mlx.mlx_mouse_hook(Window.get(), func, param)

    @classmethod
    def add_key_hook(cls, func: Callable, param) -> None:
        cls._key_funcs.append({"FUNCTION": func, "PARAMS": param})
        # Mlx_context._mlx.mlx_key_hook(Window.get(), func, param)

    @staticmethod
    def add_loop_hook(func: Callable, param) -> None:
        Mlx_context._mlx.mlx_loop_hook(Window.get(), func, param)

    @staticmethod
    def close(dummy: Any):
        Mlx_context._mlx.mlx_destroy_window(Mlx_context.get(), Window.get())
        Mlx_context._mlx.mlx_loop_exit(Mlx_context.get())

    @classmethod
    def do_event(cls, event: Callable, params: tuple = tuple()) -> None:
        cls._events.append((event, params))

    @classmethod
    def do_repeat(
        cls, event: Callable, params: tuple = tuple(), delay=0.3
    ) -> None:
        """Will stop when function returns -1"""
        cls._repeatables.append([event, delay, time.time() + delay, params])

    @classmethod
    def render_event(cls, params) -> None:
        # Mlx_context._mlx.mlx_do_sync(Mlx_context.get())
        # print(cls._events)
        for event in cls._events:
            event[0](*event[1])
        # Mlx_context._mlx.mlx_do_sync(Mlx_context.get())

        cls._events.clear()
        now = time.time()
        for animation in cls._repeatables:
            # print("yo")
            if now >= animation[2]:
                if hasattr(animation[3], "__iter__"):
                    if animation[0](*animation[2]) == -1:
                        cls._repeatables.remove(animation)
                else:
                    if animation[0]() == -1:
                        cls._repeatables.remove(animation)
                animation[2] = now + animation[1]
        # cls._repeatables.clear()

    @classmethod
    def input_to_str(
        cls,
        field,
        key,
        func: Callable,
        params: tuple,
        end_func: Callable,
        end_params: tuple,
    ) -> None:
        if cls._str:
            val = cls._str["FIELD"][cls._str["KEY"]]
            if cls._str["END_PARA"] is not None:
                cls._str["FIELD"][cls._str["KEY"]] = (
                    f"{val[: cls._str['CURSOR']]}{val[cls._str['CURSOR'] + 1 :]}"
                )
                cls._str["END"](*cls._str["END_PARA"])
            else:
                cls._str["FIELD"][cls._str["KEY"]] = (
                    f"{val[: cls._str['CURSOR']]}{val[cls._str['CURSOR'] + 1 :]}"
                )
                cls._str["END"]()
            # cls._str = {}
        cls._str = {
            "FIELD": field,
            "KEY": key,
            "CURSOR": 0,
            "SPECIAL": None,
            "FUNCTION": func,
            "PARAMS": params,
            "END": end_func,
            "END_PARA": end_params,
        }
        # cls.input_event(0, None)

    @classmethod
    def input_event(cls, input, _) -> None:
        # print(input)
        for func in cls._key_funcs:
            if func["PARAMS"] is not None:
                func["FUNCTION"](input, *func["PARAMS"])
            else:
                func["FUNCTION"](input)

        key = XK.keysym_to_string(input)
        # print(key, input)
        if cls._str:
            val = cls._str["FIELD"][cls._str["KEY"]]
            if input == 65293:
                # print(string["END_PARA"])
                befor = val[: cls._str["CURSOR"]]
                if cls._str["END_PARA"] is not None:
                    cls._str["FIELD"][cls._str["KEY"]] = (
                        f"{befor}{val[cls._str['CURSOR'] + 1 :]}"
                    )
                    cls._str["END"](*cls._str["END_PARA"])
                else:
                    cls._str["FIELD"][cls._str["KEY"]] = (
                        f"{befor}{val[cls._str['CURSOR'] + 1 :]}"
                    )
                    cls._str["END"]()
                cls._str = {}
            else:
                befor = val[: cls._str["CURSOR"]]
                cls._str["FIELD"][cls._str["KEY"]] = (
                    f"{befor}{val[cls._str['CURSOR'] + 1 :]}"
                )
                if input == 65288:
                    befor = val[: cls._str["CURSOR"] - 1]
                    val = cls._str["FIELD"][cls._str["KEY"]]
                    cls._str["FIELD"][cls._str["KEY"]] = (
                        f"{befor}{val[cls._str['CURSOR'] :]}"
                    )
                    cls._str["CURSOR"] -= 1
                elif input == 65361 and cls._str["CURSOR"] > 0:
                    cls._str["CURSOR"] -= 1
                elif input == 65363 and cls._str["CURSOR"] < len(
                    cls._str["FIELD"][cls._str["KEY"]]
                ):
                    cls._str["CURSOR"] += 1
                elif key is None or not key.isprintable:
                    print(input, "is not supported")
                elif cls._str["SPECIAL"] is None and key.isprintable:
                    val = cls._str["FIELD"][cls._str["KEY"]]
                    befor = val[: cls._str["CURSOR"]]
                    cls._str["FIELD"][cls._str["KEY"]] = (
                        f"{befor}{f'{key}'}{val[cls._str['CURSOR'] :]}"
                    )
                    cls._str["CURSOR"] += 1
                val = cls._str["FIELD"][cls._str["KEY"]]
                cls._str["FIELD"][cls._str["KEY"]] = (
                    f"{val[: cls._str['CURSOR']]}|{val[cls._str['CURSOR'] :]}"
                )
                if cls._str["PARAMS"] is not None:
                    cls._str["FUNCTION"](*cls._str["PARAMS"])
                else:
                    cls._str["FUNCTION"]()
