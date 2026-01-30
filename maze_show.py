from ntpath import join
from .src.graphics.render import Render
from PIL import Image
import os

class Grid:
	def __init__(self, width: int, heigth: int, cell_siz: int):
		render = Render()
		self.width = width
		self.heigth = heigth
		self.cell_siz = cell_siz
		self.generate_sprits()
		render.init_window(heigth, width, "test")

	def generate_sprits(self):
		path = os.path.dirname(os.path.abspath(__file__)) + "/includes/"
		sprits = list(filter(lambda f: f.endswith('.png'), os.listdir(path)))
		print(sprits)
		size = 100
		for sprit in sprits:
			try:
				im = Image.open(path + sprit)
				im.thumbnail((size, size), Image.Resampling.LANCZOS)
				im.save(path + "resized/" + sprit , "png")
			except IOError:
				print(f"cannot create {sprit}")
	

		