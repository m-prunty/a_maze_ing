from graphics.render import Render, Vec2
from mazegen.a import A_Maze
import random

def print_image(button, x, y, mystuff):
    print(f"Got mouse event! button {button} at x: {int((x / rend.width) * rend.gridx)}, y: {int(y / rend.width * rend.gridy)}")
    if (button == 1):
        hex = random.randrange(0,15)
        print(hex)
        rend.render_cell(hex, Vec2(int((x / rend.height) * rend.gridx), int(y / rend.width * rend.gridy)))
    #     # rend.render_cell(0, Vec2(1, 9))
		

rend = Render()
def main():
	rend.init_window(700, 700, "hello")
	rend.init_grid(Vec2(3, 3))
	print(rend.generate_grid_sprits())
	# print(rend.cell_siz)
	rend.add_hook(rend.close, 33, None)
	rend.add_mous_hook(print_image, [1, 2])
    
	rend.launch()
	print("Hello from amazing!")


if __name__ == "__main__":
    main()
