"""Responsible for rendering imgs and txt onto window using the Mlx library."""

from mazegen.grid_tools import Vec2

from ..assets.textures import Textures
from ..mlx_context.mlx_context import Mlx_context
from .event_loop import Event_loop
from .window import Window


class Renderer:
    """Manage rendering of imgs and txt onto window using the Mlx library."""

    @classmethod
    def render_image(cls, image: int, place: Vec2) -> None:
        """Render an image onto the window at a specified position."""
        Event_loop.do_event(cls.render_image_event, (image, place))

    @staticmethod
    def render_image_event(image: int, place: Vec2) -> None:
        """Render an image onto the window at a specified position."""
        Mlx_context._mlx.mlx_put_image_to_window(
            Mlx_context.get(),
            Window.get(),
            Textures.get_element(image),
            int(place.x),
            int(place.y),
        )

    @classmethod
    def render_image_ptr(cls, image_ptr: int, place: Vec2) -> None:
        """Render an image onto the window using a direct image pointer."""
        Event_loop.do_event(cls.render_image_ptr_event, (image_ptr, place))
        # print("hello")

    @staticmethod
    def render_image_ptr_event(image_ptr: int, place: Vec2) -> None:
        """Render an image onto the window using a direct image pointer."""
        Mlx_context._mlx.mlx_put_image_to_window(
            Mlx_context.get(),
            Window.get(),
            image_ptr,
            int(place.x),
            int(place.y),
        )

    @classmethod
    def render_text(
        cls, text: str, place: Vec2, color: int = 0xFFFFFF
    ) -> None:
        """Render text onto the window at a specified position and color."""
        Event_loop.do_event(cls.render_text_event, (text, place, color))

    @staticmethod
    def render_text_event(
        text: str, place: Vec2, color: int = 0xFFFFFF
    ) -> None:
        """Render text onto the window at a specified position and color."""
        Mlx_context._mlx.mlx_string_put(
            Mlx_context.get(),
            Window.get(),
            int(place.x),
            int(place.y),
            color,
            text,
        )
