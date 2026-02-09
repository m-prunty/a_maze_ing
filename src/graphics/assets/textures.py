from graphics import mlx
from helper import Vec2

import os
from PIL import Image

class Textures:
    _textures = []

    def __new__(cls, id: int):
        return cls._textures[id]

    @classmethod
    def load(cls, path: str, image: str, siz: Vec2, degs: tuple):
        def generate_texture(path, image, siz, degs) -> tuple:
            ret = []
            for deg in degs:
                try:
                    if not os.path.exists(path + "resized/"):
                        os.mkdir(path + "resized/")
                    im = Image.open(path + image).convert("RGBA")
                    im_rot = im.rotate(deg)
                    new_im = im_rot.resize(
                        (int(siz.x) + 1, int(siz.y) + 1), Image.Resampling.NEAREST
                    )
                    new_im.save(path + "/resized/" + f"{deg}_" + image, "png")
                    ret.append(path + "/resized/" + f"{deg}_" + image, "png")
                except OSError:
                    print(f"cannot create {image}")
	
        if not os.path.exists(path + image):
            print(f"file: {path + image} not found")
        images = generate_texture(path, image, siz, degs)
        cls._textures.extend()
        ret = ()
        for image in images:
            id = len(cls._textures)
            ptr = mlx.mlx_ (image)
            cls._textures.extend(ptr)
            ret += (image, id)
        return ret
