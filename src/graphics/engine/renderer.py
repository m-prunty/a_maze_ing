from graphics import Window, Mlx_context, Textures
from .event_loop import Event_loop
from helper import Vec2

class Renderer:
    @classmethod
    def render_image(cls, image: int, place: Vec2):
        Event_loop.do_event(cls.render_image_event, (image, place))
    
    @staticmethod
    def render_image_event(image: int, place: Vec2):
        Mlx_context._mlx.mlx_put_image_to_window(
            Mlx_context.get(),
            Window.get(),
            Textures(image),
            int(place.x),
            int(place.y),
        )



    @classmethod
    def render_image_ptr(cls, image_ptr: int, place: Vec2):
        Event_loop.do_event(cls.render_image_ptr_event, (image_ptr, place))
        print("hello")
         
    @staticmethod
    def render_image_ptr_event(image_ptr: int, place: Vec2):
        Mlx_context._mlx.mlx_put_image_to_window(
            Mlx_context.get(),
            Window.get(),
            image_ptr,
            int(place.x),
            int(place.y),
        )
        
    @classmethod
    def render_text(cls, text: str, place: Vec2, color: int=0xFFFFFF):
        Event_loop.do_event(cls.render_text_event, (text, place, color))
    
    @staticmethod
    def render_text_event(text: str, place: Vec2, color: int=0xFFFFFF):
    	Mlx_context._mlx.mlx_string_put(
            Mlx_context.get(),
            Window.get(),
            int(place.x),
            int(place.y),
            color,
            text
        )