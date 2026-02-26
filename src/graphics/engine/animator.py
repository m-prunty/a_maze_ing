from graphics import Renderer
from graphics import Event_loop

class Animator:
    @staticmethod
    def animate(func, params, delay):
        Event_loop.do_repeat(func, params, delay)
	

    