"""Texture management module for loading and handling textures."""

import os

from common.grid_tools import Vec2
from PIL import Image

from ..mlx_context import Mlx_context


class Textures:
    """Class for loading and handling textures."""

    _textures: list[int] = []
    _sizes: list[Vec2] = []

    @classmethod
    def get_element(cls, id: int) -> int:
        """Return the texture ID for the given ID."""
        return cls._textures[id]

    @classmethod
    def get_siz(cls, id: int) -> Vec2:
        """Return the size of the texture for the given ID."""
        return cls._sizes[id]

    @classmethod
    def load(
        cls, path: str, image: str, siz: Vec2, degs: tuple[int, int, int, int]
    ) -> list[int]:
        """Load a texture from a file and return its ID."""
        if not os.path.exists(path + image):
            print(f"file: {path + image} not found")
        images = []
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
                images.append(path + "/resized/" + f"{deg}_" + image)
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
