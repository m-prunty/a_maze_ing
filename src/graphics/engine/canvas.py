from helper import Vec2
from graphics import Mlx_context, Textures, Renderer

class Canvas:
    def __init__(self, siz: Vec2, pos: Vec2):
        self.siz = siz
        self.pos = pos
        self.img = Mlx_context._mlx.mlx_new_image(
            Mlx_context.get(), int(siz.x), int(siz.y)
        )

        self.img_mem, self.bpp, self.siz_line, _ = Mlx_context._mlx.mlx_get_data_addr(self.img)

    
    
    def add_image(self, img_ptr, place: Vec2):
        src_data, src_bpp, src_size_line, _ = Mlx_context._mlx.mlx_get_data_addr(Textures(img_ptr))
        src_data = src_data.cast('B')
        # print("added one image")
        bytes_pp = src_bpp // 8
        siz = Vec2()
        siz.x = int(Textures.get_siz(img_ptr).x)
        siz.y = int(Textures.get_siz(img_ptr).y)
    
        for y in range(siz.y):
            src_start = y * src_size_line
            src_end = src_start + siz.x * bytes_pp
            dst_start = (y + place.y) * self.siz_line + place.x * bytes_pp
            dst_end = dst_start + siz.x * bytes_pp
            self.img_mem[dst_start:dst_end] = src_data[src_start:src_end].tobytes()
            
    def put_canva(self):
        Renderer.render_image_ptr(self.img, self.pos)