from graphics import Textures
import os

class RenderGrid:
    _tiles = []


    @classmethod
    def set_tile_siz(window_siz, grid_siz):
        
    @classmethod
    def load_tiles(cls):
        path = (
            os.path.dirname(os.path.abspath(__file__))
            + "/includes/sprits/grid/"
        )
        sprits = list(filter(lambda f: f.endswith(".png"), os.listdir(path)))
        sprits.sort()
        ret = []
        cls.grid_tiles = []
        for sprit in sprits:
            imgs = Textures.load(
                        path, sprit, cls._tile_siz, (0, 90, 180, 270))
            ret.append(
                (
                    imgs,
                    sprit,
                )
            )
            for img in imgs:
                cls._tiles.append(img)
        return ret

        
    
    
class RenderCell:
    