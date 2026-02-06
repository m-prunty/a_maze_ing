from graphics import Render
from config import Config
from helper import Vec2

import time
import os


class Options:
    def __init__(self):
        self.cfg = Config.cfg_from_file("config.txt")
        print("+++++++++ FROM OPTIONS +++++++")
        print(self.cfg)
        self.rend = Render()
        self.rend.init_window(self.cfg.width * 50, self.cfg.height * 50, "A-Maze_Ing")
        self.opt_rend = Options_render(self.rend)
        self.opt_rend.add_cursor("Width", (0, self.cfg.width, 50))
        self.opt_rend.add_cursor("Width", (0, self.cfg.width, 50))
        self.opt_rend.render_options()
        # opt_rend.change_cursor("Width", 5)
        self.rend.add_hook(self.rend.close, 33, None)
        self.rend.add_mous_hook(self.mouse_event, None)
        self.rend.launch()
        # time.sleep(0.1)

        print("++++++++++++++++++++++++++++++")
    
    def mouse_event(self, button, x, y, baa):
        if (button == 4):
            self.opt_rend.scroll -= 10
            self.opt_rend.render_options()
        if (button == 5):
            self.opt_rend.scroll += 10
            self.opt_rend.render_options()
        if (button == 1):
            self.opt_rend.check_click(Vec2(x, y))
        

    # def reset_siz(self, width: int, height: int):




class Options_render:
    
    def __init__(self, rend: Render):
        self.rend = rend
        self.sids_padding = rend.width * 0.2
        self.top_padding = rend.height * 0.04
        self.bar_width = rend.width - self.sids_padding * 2
        self.bar_height = self.top_padding / 4 # padding times 4
        self.text_siz = self.bar_height 

        self.fields = {}
        
        path = os.path.dirname(os.path.abspath(__file__)) + "/"
        logo_siz = Vec2(rend.width * (1 - (10 * 0.02)),
                        rend.height * (1 - (10 * 0.02)))
        
        self.imgs = {}
        print(path + "options_logo.png")
        self.imgs["Logo"] = rend.generate_sprit(path, "options_logo.png", logo_siz, (0,))
        self.imgs["Bar"] = rend.generate_sprit(path,"bar(1).png",
                                                 Vec2(self.bar_width, 
                                                      self.bar_height),
                        						  (0,))
        self.imgs["Cursor"] = rend.generate_sprit(path, "cursor.png",
                                                 Vec2(self.bar_height,
                        						 self.bar_width / 100), (0,))
    
        self.scroll = 0

    def render_options(self):
        self.rend.clear_window()
        self.rend.render_text("OPTIONS", Vec2(self.sids_padding * 2,
                                    0 + self.scroll))
        for field in self.fields.keys():
            self.render_cursor(field)

    def add_cursor(self, name: str, vals: tuple):
        """ "vals 0 min, 1 default, 2 max"""
        self.fields[name] = {
            "NAME": name,
            "POS": len(self.fields),
            "MIN": vals[0],
            "MAX": vals[2],
            "VAL": (vals[1] - vals[0]) / (vals[2] - vals[0]),
            "INDEX": len(self.fields) - 1
        }

    def change_cursor(self, name: str, new_val: int):
        if name not in self.fields:
            print("Field not found !")
        
        self.fields[name]["VAL"] = (new_val - self.fields[name]["MIN"]) / (
            self.fields[name]["MAX"] - self.fields[name]["MIN"]
        )
        print(self.fields[name]["VAL"])
        self.render_cursor(name)
        
    def render_cursor(self, name: str):
        if name not in self.fields:
            print("Field not found !")
        self.rend.render_text(name, Vec2(self.sids_padding * 1.5,
                                    self.rend.height * 0.05 + self.scroll))
        self.rend.render_image(self.imgs["Bar"][0] - 1,
                               Vec2(self.sids_padding,
                                    self.rend.height * 0.05 + self.text_siz 
                                    	+ self.bar_height + self.scroll))
        time.sleep(0.001)
        self.rend.render_image(self.imgs["Cursor"][0] - 1,
                               Vec2(self.sids_padding + (self.bar_width * self.fields[name]["VAL"]),
                                    self.rend.height * 0.052 + self.text_siz 
                                    	+ self.bar_height + self.scroll))

    def check_click(self, pos: Vec2):
        for field_name, field_value in self.fields.items():
            fpos = Vec2(self.sids_padding,
                                    self.rend.height * 0.05 + self.text_siz 
                                    	+ self.bar_height + self.scroll)
            siz = Vec2(self.bar_width, self.bar_height)
            if (fpos.y < pos.y and fpos.y + siz.y > pos.y):
                if (fpos.x < pos.x and fpos.x + siz.x > pos.x):
                    print((field_value["MIN"]) * self.bar_width / 100)
                    self.change_cursor(field_name, (field_value["MAX"] - field_value["MIN"]) * (pos.x - fpos.x) / (siz.x - ((field_value["MIN"]) * self.bar_width / 100)))

if __name__ == "__main__":
    # rend = Render()
    # rend
    opt = Options()
