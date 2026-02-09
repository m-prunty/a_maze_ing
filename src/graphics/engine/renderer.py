from graphics import Window, Mlx_context, mlx, Textures
from helper import Vec2

class Renderer:
    @classmethod
    def render_image(image: int, place: Vec2):
        mlx.mlx_put_image_to_window(
            Mlx_context.get(),
            Window.get(),
            Textures(image),
            int(place.x),
            int(place.y),
        )
        
    @classmethod
    def render_text(text: str, place: Vec2, color: int=0):
        mlx.mlx_string_put(
            Mlx_context.get(),
            Window.get(),
            int(place.x),
            int(place.y),
            color,
            text
        )