"""Texture management module for loading and handling textures."""

import os

from common.grid_tools import Vec2
from PIL import Image

from ..mlx_context import Mlx_context


class Textures:
    """Class for loading and handling textures."""

    _include_path: str
    _textures: list = [tuple]
    _sizes: list = []

    @classmethod
    def get_element(cls, id: int) -> int:
        """Return the texture ID for the given ID."""
        return cls._textures[id]

    @classmethod
    def get_siz(cls, id: int) -> Vec2:
        """Return the size of the texture for the given ID."""
        return cls._sizes[id]

    @classmethod
    def set_path(cls, path: str) -> None:
        if not os.path.exists(path):
            raise RuntimeError(f"{path} not found")
        cls._include_path = path

    @classmethod
    def load(cls, image: str, siz: Vec2, degs: tuple, path: str = ""):
        # def generate_texture(path, image, siz, degs) -> tuple:

        if not os.path.exists(cls._include_path + path + image):
            print(f"file: {cls._include_path + path + image} not found")
        images = []
        for deg in degs:
            try:
                if not os.path.exists(cls._include_path + path + "resized/"):
                    os.mkdir(cls._include_path + path + "resized/")
                im = Image.open(cls._include_path + path + image).convert(
                    "RGBA"
                )
                im_rot = im.rotate(deg)
                new_im = im_rot.resize(
                    (int(siz.x) + 1, int(siz.y) + 1), Image.Resampling.NEAREST
                )
                new_im.save(
                    cls._include_path + path + "/resized/" + f"{deg}_" + image,
                    "png",
                )
                images.append(
                    cls._include_path + path + "/resized/" + f"{deg}_" + image
                )
            except OSError:
                print(f"cannot create {image}")
        ret = []
        for img in images:
            id = len(cls._textures)
            # MLX dependency here is a boundary violation current import
            # is ahotfix
            # we need to consider moving this oput of here and into mlx_context
            # Mlx_context.load_texture() or something like that
            # then call from renderer
            ptr = Mlx_context._mlx.mlx_png_file_to_image(
                Mlx_context.get(), img
            )
            cls._textures.append(ptr[0])
            cls._sizes.append(siz)
            ret.append(id)
        return ret
