from mlx import Mlx
from ntpath import join
from PIL import Image
import os

class Vec2():
    """Class for storing 2D Coords."""

    def __init__(self, x: int = 0, y: int = 0):
        """TODO: to be defined."""
        self.x = 0
        self.y = 0
        try:
            self.x = x
            self.y = y
        except Exception as e:
            print(e)
            # raise ValueError(e)

    def __add__(self, other):
        """Add a vec2 instance with another."""
        return Vec2(self.x + other.x,
                    self.y + other.y,
                    )

    def __sub__(self, other):
        """Sub a vec2 instance with another."""
        return Vec2(self.x - other.x,
                    self.y - other.y,
                    )

    def __eq__(self, other):
        """Equate a vec2 instance with another."""
        return (self.x == other.x and 
                self.y == other.y)
    
    def __abs__(self):
        """Return magnitude of a vector."""
        return sqrt(self.x**2 + self.y**2)

    def __repr__(self):
        """Return a tuple represantation of a Vec2 instance."""
        return (self.x, self.y)

    def __str__(self):
        """Return a str tuple represantation of a Vec2 instance."""
        return f"{self.__repr__()}"

    def __iter__(self):
        """Return a tuple iterable  represantation of a Vec2 instance."""
        return iter(self.__repr__())

    @classmethod
    def from_str(cls, coord: str) -> "Vec2":
        """TODO: Docstring for from_str.

        Args:
            coord (str): coordinates in form "x,y,z"

        Returns: An instance of Vec2

        """
        try:
            lst = [0]
            lst += cls.ft_split(coord, ",")
            lst = cls.parse_args(len(lst), lst)
            return cls(lst[0], lst[1])
        except Exception as e:
            r_str = (f"Error details - Type: {e.__class__.__name__}")
            r_str += (f", Args: (\"{e.args[0]}\",)")
            raise ValueError(r_str)


class Render :
	def __init__(self):
		self.m = Mlx()
		self.mlx_ptr = self.m.mlx_init()
		self.images = []



	def generate_window(self):
		self.win_ptr = self.m.mlx_new_window(self.mlx_ptr, self.width, self.height, self.name)
		self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)
	
	def init_window(self, height: int, width: int, name: str) :
		self.width = width
		self.height = height
		self.name = name
		self.generate_window()
	
	def clear_window(self):
		self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)


	def add_image(self, path: str, image: str, siz: Vec2) -> int:
		ret = self.generate_sprit(path, image, siz)
		return ret

	def render_image(self, image: int, place: Vec2):
		img_ptr = self.m.mlx_png_file_to_image(self.mlx_ptr, self.images[image][1])
		self.m.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, img_ptr[0], place.x, place.y)




	def generate_grid_sprits(self) -> tuple:
		path = os.path.dirname(os.path.abspath(__file__)) + "/includes/sprits/grid/"
		sprits = list(filter(lambda f: f.endswith('.png'), os.listdir(path)))
		ret = []
		for sprit in sprits:
			ret.append((self.generate_sprit(path, sprit, self.tile_siz, (0, 90, 180, 270)), sprit))
		return ret

	def generate_sprit(self, path: str, sprit: str, siz: Vec2, degs: tuple) -> list:
		# print(degs)
		ret = []
		for deg in degs:
			try:
				# print(deg)
				im = Image.open(path + sprit).convert("RGBA")
				im_rot = im.rotate(deg)
				new_im = im_rot.resize((int(siz.x) + 1, int(siz.y) + 1), Image.Resampling.NEAREST)
				new_im.save(path + "resized/" + f"{deg}_" + sprit, "png")
			except IOError:
				print(f"cannot create {sprit}")
			self.images.append((len(self.images), path + "resized/" + f"{deg}_" + sprit))
			ret.append(len(self.images) - 1)
		return ret



	def init_grid(self, siz: Vec2):
		self.gridx = siz.x
		self.gridy = siz.y
		self.grid = [[0 for _ in range(siz.y)] for _ in range(siz.x)]
		self.tile_siz = Vec2(self.width / (siz.x * 2 + 1), self.height / (siz.y * 2 + 1))
		# self.cell_siz = Vec2(self.width / (siz.x + 4), self.height / (self.gridy) + (self.height / (self.gridy) / 3) - 1)

	def render_cell(self, hex: int, pos: Vec2):
		# img_siz = Vec2(self.cell_siz.x / 3, self.cell_siz.y / 3)
		self.grid[pos.x][pos.y] = hex
		for i in range(3):
			for y in range(3):
				if (y == 1 and i % 2 == 0):
					if ((hex >> 2 * (i == 0) + 1) & 1):
						self.render_image(1 * 4 + 1, Vec2(int(pos.x * self.tile_siz.x * 2 + i * self.tile_siz.x), int(pos.y * self.tile_siz.y * 2 + y * self.tile_siz.y)))
					else:
						self.render_image(0, Vec2(int(pos.x * self.tile_siz.x * 2 + i * self.tile_siz.x), int(pos.y * self.tile_siz.y * 2 + y * self.tile_siz.y)))
						
				elif (i == 1 and y % 2 == 0):
					if ((hex >> y) & 1):
						self.render_image(1 * 4, Vec2(int(pos.x * self.tile_siz.x * 2 + i * self.tile_siz.x), int(pos.y * self.tile_siz.y * 2 + y * self.tile_siz.y)))
					else:
						self.render_image(0, Vec2(int(pos.x * self.tile_siz.x * 2 + i * self.tile_siz.x), int(pos.y * self.tile_siz.y * 2 + y * self.tile_siz.y)))
				elif (y % 2 == 1 and i % 2 == 1):
					self.render_image(0, Vec2(int(pos.x * self.tile_siz.x * 2 + i * self.tile_siz.x), int(pos.y * self.tile_siz.y * 2 + y * self.tile_siz.y)))
				else:
					top = (hex >> (2 * (i == 0) + 1)) & 1 if y > 0 else (self.grid[pos.x][pos.y  - 1] >> (2 * (i == 0) + 1)) & 1 if pos.y > 0 else 0
					bot = (hex >> (2 * (i == 0) + 1)) & 1 if y == 0 else (self.grid[pos.x][pos.y + 1] >> (2 * (i == 0) + 1)) & 1 if pos.y < self.gridy - 1 else 0
					left = (hex >> y) & 1 if i > 0 else (self.grid[pos.x - 1][pos.y] >> y) & 1 if pos.x > 0 else 0
					right = (hex >> y) & 1 if i == 0 else (self.grid[pos.x + 1][pos.y] >> y) & 1 if pos.x < self.gridx - 1 else 0
					tile = top + bot + left + right
					# print(f"i {i}, y {y} => left:{left}, right:{right}, top:{top}, bottom:{bot} => {tile}")
					print(right, bot)
					if (tile == 2):
						if (top + bot == 2 or right + left == 2):
							tile -= 1
					ori = 0
					if (tile == 1):
						ori = bot or top
					elif (tile == 2):
						ori = (top or left) * 2 + right * -1 + bot
					elif (tile == 3):
						ori = 6 - (bot * 3 + left * 2 + top * 1)
					# print(ori, tile)
					self.render_image(tile * 4 + ori, Vec2(int(pos.x * self.tile_siz.x * 2 + i * self.tile_siz.x), int(pos.y * self.tile_siz.y * 2 + y * self.tile_siz.y)))
				
				
					# corner
				# self.render_image(hex, Vec2(int(pos.x * self.cell_siz.x + img_siz * i), int(pos.y * self.cell_siz.y + img_siz * y)))
				




	def add_hook(self, func: callable, event: int, param):
		self.m.mlx_hook(self.win_ptr, event, 0, func, None)
	
	def add_mous_hook(self, func: callable, param):
		self.m.mlx_mouse_hook(self.win_ptr, func, param)

	def add_key_hook(self, func: callable, param):
		self.m.mlx_key_hook(self.win_ptr, func, param)

	def close(self, dummy):
		self.m.mlx_loop_exit(self.mlx_ptr)



	def launch(self):
		self.m.mlx_loop(self.mlx_ptr)

	# def add_event(self, type, ):
		



	
		



	
# def mymouse(button, x, y, mystuff):
#     print(f"Got mouse event! button {button} at {x},{y}.")

# def mykey(keynum, mystuff):
#     print(f"Got key {keynum}, and got my stuff back:")
#     print(mystuff)
#     if keynum == 32:
#         m.mlx_mouse_hook(win_ptr, None, None)
        
# def gere_close(dummy):
#     m.mlx_loop_exit(mlx_ptr)
#     print("Window closed")




# include_dir = os.path.dirname(os.path.abspath(__file__)) + "/includes/"
# print(include_dir + "walls.png")
# img_ptr = m.mlx_new_image(mlx_ptr, 200, 2000)
# img_ptr = m.mlx_png_file_to_image(mlx_ptr, include_dir + "image.png")
# print(img_ptr)
# ret = m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr[0], 0, 0)
# if (ret == None):
# 	print("error")
# print(ret)
# (ret, w, h) = m.mlx_get_screen_size(mlx_ptr)
# print(f"Got screen size: {w} x {h} .")

# stuff = [1, 2]
# m.mlx_mouse_hook(win_ptr, mymouse, None)
# m.mlx_key_hook(win_ptr, mykey, stuff)
# m.mlx_hook(win_ptr, 33, 0, gere_close, None)

# print("hello ") 

# m.mlx_loop(mlx_ptr)