from annotated_types import Ge, Le
from graphics import Event_loop, Window, Textures, Renderer
# from matha

from config import Config
from helper import Vec2

import os
import sys

class Options:
    def __init__(self):
        self.cfg = Config.cfg_from_file("config.txt")
        self.opt_rend = Options_render()
        for key, val  in self.cfg:
            print(f"{key} has value:", val)
            min = None
            max = None
            for meta in Config.__pydantic_fields__[key].metadata:
                if isinstance(meta, Ge):
                    # print("ge =", meta.ge)
                    min = meta.ge
                if isinstance(meta, Le):
                    # print("le =", meta.le)
                    max = meta.le
            if min is not None and max is not None:
                print("cursor added")
                self.opt_rend.add_cursor(key, "", (min, val, max + 1))
            elif (type(val) is int):
                self.opt_rend.add_input(key, val, int)
            	# print()
                
        self.is_active = False
    
    def put_to_config(self, fields: list):
        """ vars: 0 width, 1 height"""
        for key, value  in self.cfg:
            try:
                val = type(value)(fields[key]["VAL"])
                # value = val
                setattr(self.cfg, key, val)
                print(key, " successfully changed to", fields[key]["VAL"])
            except KeyError:
                print(key, "is not handeld yet")
            # val = fval
        # self.cfg.exit = Vec2(self.cfg.width - 1, self.cfg.height - 1)
        # self.cfg.entry = Vec2(0, 0)
        self.cfg.cfg_to_file()
            

    def render(self):
        self.opt_rend.render_options()
        Event_loop.add_hook(Event_loop.close, 33, None)
        Event_loop.add_mous_hook(self.mouse_event, None)
        self.is_active = True

    def save(self):
        Event_loop.close(None)
        os.execv(sys.executable, [sys.executable] + sys.argv)
        self.is_active = False
        self.render()
    
    def mouse_event(self, button, x, y, baa):
        if (self.is_active):
            if (button == 4):
                self.opt_rend.scroll -= 10
                self.opt_rend.render_options()
            if (button == 5):
                self.opt_rend.scroll += 10
                self.opt_rend.render_options()
            if (button == 1):
                self.opt_rend.check_click(Vec2(x, y), self)
        

    # def reset_siz(self, width: int, height: int):




class Options_render:
    
    def __init__(self):
        self.width = Window.get_siz().x
        self.height = Window.get_siz().y
        self.sids_padding = self.width * 0.1
        self.top_padding = self.height * 0.03
        self.bar_width = self.width - self.sids_padding * 2
        self.bar_height = self.top_padding / 2
        self.text_siz = self.top_padding

        self.fields = {}
        
        path = os.path.dirname(os.path.abspath(__file__)) + "/includes/"
        
        self.imgs = {}
        self.imgs["Bar"] = Textures.load(path,"bar.png",
                                                 Vec2(self.bar_width * 1.05, 
                                                      self.bar_height),
                        						  (0,))[0]
        self.imgs["Box"] = Textures.load(path,"box_input.png",
                                                 Vec2(self.bar_width * 1.05,
                                                      self.bar_height + self.top_padding),
                        						  (0,))[0]
        self.imgs["Cursor"] = Textures.load(path, "cursor.png",
                                                 Vec2(self.bar_width / 100,
                        						 self.bar_height), (0,))[0]
        self.imgs["Save"] = Textures.load(path, "save_button.png",
                                                 Vec2(self.width * 0.4,
                        						 self.height * 0.1), (0,))[0]
        self.scroll = 0

    def render_options(self):
        Window.clear_window()
        Renderer.render_text("OPTIONS", Vec2(self.sids_padding * 2,
                                    self.scroll))
        Renderer.render_image(self.imgs["Save"], 
                               Vec2(self.width * 0.3,
                                    (self.height * 0.02) + ((self.text_siz
                                    + self.bar_height + self.top_padding) * len(self.fields)) + self.text_siz + self.scroll))
        for field in self.fields:
            # print(field)
            if (self.fields[field]["TYPE"] == "cursor"):
                self.render_cursor(field)
            if (self.fields[field]["TYPE"] == "input"):
                self.render_input(field)
        

    def add_cursor(self, name: str, unit: str, vals: tuple):
        """ "vals 0 min, 1 default, 2 max"""
        self.fields[name] = {
            "NAME": name,
            "UNIT": unit,
            # "POS": len(self.fields),
            "MIN": vals[0],
            "MAX": vals[2],
            "VAL": vals[1],
            "PERCENT": (vals[1] - vals[0]) / (vals[2] - vals[0]),
            "INDEX": len(self.fields),
            "TYPE": "cursor"
        }
        
    def add_input(self, name: str, val, type):
        """ "vals 0 min, 1 default, 2 max"""
        self.fields[name] = {
            "NAME": name,
            # "POS": len(self.fields),
            "VAL": val,
            "INPUT": None,
            "INDEX": len(self.fields),
            "DATA_TYPE": type,
            "TYPE": "input"
        }
    
    def render_input(self, name: str):
        # print("yo")
        if name not in self.fields:
            print("Field not found !")
        Renderer.render_text(f'{name}: {self.fields[name]["VAL"]}', Vec2(self.sids_padding * 1.5,
                                self.height * 0.02 + ((self.text_siz+ self.bar_height + self.top_padding)
                                                      * self.fields[name]["INDEX"]) + self.scroll))
        Renderer.render_image(self.imgs["Box"],
                               Vec2(int(self.sids_padding * 0.95),
                                    int(self.height * 0.02 + ((self.text_siz
                                    	+ self.bar_height + self.top_padding) * self.fields[name]["INDEX"]) + self.text_siz + self.scroll)))
        if self.fields[name]["INPUT"] is None:
            Renderer.render_text('Click to change', Vec2(int(self.sids_padding),
                                                    int(self.height * 0.025 + ((self.text_siz
                                    	            + self.bar_height + self.top_padding) * self.fields[name]["INDEX"]) + self.text_siz + self.scroll)))
        else:
            Renderer.render_text(str(self.fields[name]["INPUT"]), Vec2(int(self.sids_padding),
                                                    int(self.height * 0.025 + ((self.text_siz
                                    	            + self.bar_height + self.top_padding) * self.fields[name]["INDEX"]) + self.text_siz + self.scroll)))
        
    def change_cursor(self, name: str, new_val: tuple):
        """" new value: 0 value, 1 percent (from 0 to 1) (if one is not given the other is gesed)"""
        if name not in self.fields:
            print("Field not found !")
        if (new_val[0]):
            self.fields[name]["VAL"] = new_val[0]
        else:
            self.fields[name]["VAL"] = (self.fields[name]["MAX"] - self.fields[name]["MIN"]) * new_val[1] + self.fields[name]["MIN"]
        if (new_val[1]):
            self.fields[name]["PERCENT"] = new_val[1]
        else:
            self.fields[name]["PERCENT"] = (new_val[0] - self.fields[name]["MIN"]) / (
				self.fields[name]["MAX"] - self.fields[name]["MIN"]
			)
        self.render_options()
        
    def render_cursor(self, name: str):
        if name not in self.fields:
            print("Field not found !")
        Renderer.render_text(f'{name}: {int(self.fields[name]["VAL"])} {self.fields[name]["UNIT"]}', Vec2(self.sids_padding * 1.5,
                                    self.height * 0.02 + ((self.text_siz
                                    	+ self.bar_height + self.top_padding) * self.fields[name]["INDEX"]) + self.scroll))
        Renderer.render_image(self.imgs["Bar"],
                               Vec2(int(self.sids_padding * 0.95),
                                    int(self.height * 0.02 + ((self.text_siz
                                    	+ self.bar_height + self.top_padding) * self.fields[name]["INDEX"]) + self.text_siz + self.scroll)))
        Renderer.render_image(self.imgs["Cursor"],
                               Vec2(self.sids_padding + (self.bar_width * self.fields[name]["PERCENT"]),
                                    (self.height * 0.02) + ((self.text_siz
                                    	+ self.bar_height + self.top_padding) * self.fields[name]["INDEX"]) + self.text_siz + self.scroll))
    
    def set_field(self, field):
        print("field is :" , field)
        try:
            field["VAL"] = field["DATA_TYPE"](field["INPUT"])
            print("changed ", field["NAME"], "to: ", field["VAL"])
        except:
            field["INPUT"] = "This Value is impossible"
            print("This Value is impossible")
            # self.render_options()
        else:
            field["INPUT"] = None
        self.render_options()

    def check_click(self, pos: Vec2, opt: Options):
        # print("pos")
        for field_name, field_value in self.fields.items():
            # corsor
            if (field_value["TYPE"] == "cursor"):
                fpos = Vec2(self.sids_padding,
                                    (self.height * 0.02) + ((self.text_siz
                                    	+ self.bar_height + self.top_padding) * self.fields[field_name]["INDEX"]) + self.text_siz + self.scroll)
                siz = Vec2(self.bar_width, self.bar_height)
                if (fpos.y < pos.y and fpos.y + siz.y > pos.y):
                    if (fpos.x < pos.x and fpos.x + siz.x > pos.x):
                        self.change_cursor(field_name, (None , (pos.x - fpos.x) / siz.x))
            # inputs
            if (field_value["TYPE"] == "input" and (field_value["INPUT"] is None or field_value["INPUT"] == "This Value is impossible")):
                fpos = Vec2(self.sids_padding,
                                    (self.height * 0.02) + ((self.text_siz
                                    	+ self.bar_height + self.top_padding) * self.fields[field_name]["INDEX"]) + self.text_siz + self.scroll)
                siz = Vec2(self.bar_width, self.bar_height + self.top_padding)
                if (fpos.y < pos.y and fpos.y + siz.y > pos.y):
                    if (fpos.x < pos.x and fpos.x + siz.x > pos.x):
                        # print("inside")
                        field_value["INPUT"] = ""
                        self.render_options()
                        Event_loop.input_to_str(field_value, "INPUT", self.render_options, None, self.set_field, (field_value, ))
        
        save_pos = Vec2(self.width * 0.3,
            (self.height * 0.02) + ((self.text_siz
            + self.bar_height + self.top_padding) * len(self.fields)) + self.text_siz + self.scroll)
        save_siz = Vec2(self.width * 0.4,
                        self.height * 0.1)
        if (save_pos.y < pos.y and save_pos.y + save_siz.y > pos.y):
            if (save_pos.x < pos.x and save_pos.x + save_siz.x > pos.x):
                print("FROM SAVE:")
                vars = []
                for field_name, field_value in self.fields.items():
                    if field_value["TYPE"] == "input" and field_value["INPUT"] is not None:
                        print(field_name)
                        field_value["INPUT"] = field_value["INPUT"][:-1]
                        self.set_field(field_value)
                    vars.append(field_value["VAL"])
                opt.put_to_config(self.fields)
                opt.save()

if __name__ == "__main__":
    # rend = Render()
    # rend
    opt = Options()
