import os
import sys
from typing import Literal, get_args, get_origin

from annotated_types import Ge, Le

from common.config import Config, ConfigIO
from common.grid_tools import Vec2

from ..graphics import Event_loop, Renderer, Textures, Window


class Options:
    def __init__(self, config: Config):
        self.cfg = config
        self.opt_rend = Options_render()

        print(self.cfg)
        for field in self.cfg:
            print("}}}}}}}", field)  #
            # print(self.cfg[field])

            # field = self.cfg[field.model_field]

            name = field["name"]
            annotation = field["type"]
            value = field["value"]

            print(name, annotation, value)
            min = None
            max = None
            for meta in self.cfg.__pydantic_fields__[name].metadata:
                if isinstance(meta, Ge):
                    min = meta.ge
                if isinstance(meta, Le):
                    max = meta.le
            if min is not None and max is not None:
                self.opt_rend.add_cursor(name, "", (min, value, max + 1))
            if annotation is int and min is None:
                self.opt_rend.add_input(name, value, int)
            elif annotation is str:
                self.opt_rend.add_input(name, value, str)
            elif annotation is bool:
                self.opt_rend.add_dropdown(
                    name, value, get_args(Literal[True, False])
                )
            elif annotation is tuple:
                self.opt_rend.add_input(name + " X", value.x, int)
                self.opt_rend.add_input(name + " Y", value.y, int)
            elif get_origin(annotation) is Literal:
                self.opt_rend.add_dropdown(name, value, get_args(annotation))
            self.is_active = False

    def put_to_config(self, fields: list):
        """vars: 0 width, 1 height"""
        print("ptc", self.cfg, fields)
        for value in self.cfg:
            try:
                key = value["name"]
                val = fields[key]["VAL"]
                setattr(self.cfg, key, val)
                print("field is ", key, value, val)  #
                # print(key, " successfully changed to", val)
            except KeyError:
                print(key, "is not handeld yet")
        ConfigIO.to_file(self.cfg, self.cfg.filename)

    def render(self) -> None:
        self.opt_rend.render_options()
        Event_loop.add_hook(Event_loop.close, 33, None)
        Event_loop.add_mous_hook(self.mouse_event, None)
        self.is_active = True

    def save(self) -> None:
        Event_loop.close(None)
        print(
            sys.executable, [sys.executable] + sys.argv + [self.cfg.filename]
        )
        os.execv(
            sys.executable,
            [sys.executable] + sys.argv[:1] + [self.cfg.filename],
        )
        print("Options saved, restarting the program...")
        self.is_active = False
        self.render()

    def mouse_event(self, button: int, x: int, y: int, baa: None) -> None:
        if self.is_active:
            if button == 4:
                self.opt_rend.scroll -= 10
                self.opt_rend.render_options()
            if button == 5:
                self.opt_rend.scroll += 10
                self.opt_rend.render_options()
            if button == 1:
                self.opt_rend.check_click(Vec2(x, y), self)


class Options_render:
    def __init__(self):
        self.width = Window.get_siz().x
        self.height = Window.get_siz().y
        self.sids_padding = self.width * 0.15
        self.top_padding = self.height * 0.03
        self.bar_width = self.width - self.sids_padding * 2
        self.bar_height = self.top_padding / 2
        self.text_siz = self.top_padding

        self.fields = {}

        path = os.path.dirname(os.path.abspath(__file__)) + "/includes/"

        self.imgs = {}
        self.imgs["Bar"] = Textures.load(
            path, "bar.png", Vec2(self.bar_width * 1.05, self.bar_height), (0,)
        )[0]
        self.imgs["Box"] = Textures.load(
            path,
            "box_input.png",
            Vec2(self.bar_width * 1.05, self.bar_height + self.top_padding),
            (0,),
        )[0]
        self.imgs["Arrows"] = Textures.load(
            path,
            "arrow.png",
            Vec2(self.bar_height, self.bar_height),
            (180, 270),
        )
        self.imgs["Drop_back"] = Textures.load(
            path,
            "dropdown_back.png",
            Vec2(self.bar_width * 0.5, self.bar_height * 1.75),
            (0,),
        )[0]
        self.imgs["Cursor"] = Textures.load(
            path,
            "cursor.png",
            Vec2(self.bar_width / 100, self.bar_height),
            (0,),
        )[0]
        self.imgs["Save"] = Textures.load(
            path,
            "save_button.png",
            Vec2(self.width * 0.4, self.height * 0.1),
            (0,),
        )[0]
        self.scroll = 0

    def render_options(self):
        Window.clear_window()
        Renderer.render_text(
            "OPTIONS", Vec2(self.sids_padding * 2, self.scroll)
        )
        Renderer.render_image(
            self.imgs["Save"],
            Vec2(
                self.width * 0.3,
                (self.height * 0.02)
                + (
                    (self.text_siz + self.bar_height + self.top_padding)
                    * len(self.fields)
                )
                + self.text_siz
                + self.scroll,
            ),
        )
        for field in self.fields:
            if self.fields[field]["TYPE"] == "cursor":
                self.render_cursor(field)
            if self.fields[field]["TYPE"] == "input":
                self.render_input(field)
            if self.fields[field]["TYPE"] == "dropdown":
                self.render_dropdown(field)

    def add_cursor(self, name: str, unit: str, vals: tuple):
        """ "vals 0 min, 1 default, 2 max"""
        self.fields[name] = {
            "NAME": name,
            "UNIT": unit,
            "MIN": vals[0],
            "MAX": vals[2],
            "VAL": vals[1],
            "PERCENT": (vals[1] - vals[0]) / (vals[2] - vals[0]),
            "INDEX": len(self.fields),
            "TYPE": "cursor",
        }

    def add_input(self, name: str, val, type):
        """ "vals 0 min, 1 default, 2 max"""
        self.fields[name] = {
            "NAME": name,
            "VAL": val,
            "INPUT": None,
            "INDEX": len(self.fields),
            "DATA_TYPE": type,
            "TYPE": "input",
        }

    def add_dropdown(self, name: str, val, posibles: list):
        """ "vals 0 min, 1 default, 2 max"""
        self.fields[name] = {
            "NAME": name,
            "VAL": val,
            "POSSIBLE": posibles,
            "INDEX": len(self.fields),
            "TYPE": "dropdown",
            "OPEN": False,
        }

    def render_dropdown(self, name: str):
        if name not in self.fields:
            print("Field not found !")
        indicator = f"{name}: {self.fields[name]['VAL']}"
        # print("indicators len is :", len(indicator))
        Renderer.render_text(
            indicator,
            Vec2(
                self.sids_padding * 1.5,
                self.height * 0.02
                + (
                    (self.text_siz + self.bar_height + self.top_padding)
                    * self.fields[name]["INDEX"]
                )
                + self.scroll,
            ),
        )
        if self.fields[name]["OPEN"]:
            Renderer.render_image(
                self.imgs["Arrows"][1],
                Vec2(
                    self.sids_padding * 1.6 + len(indicator) * 10,
                    self.height * 0.02
                    + (
                        (self.text_siz + self.bar_height + self.top_padding)
                        * self.fields[name]["INDEX"]
                    )
                    + self.scroll,
                ),
            )
            i = 1
            for value in self.fields[name]["POSSIBLE"]:
                Renderer.render_image(
                    self.imgs["Drop_back"],
                    Vec2(
                        int(self.sids_padding * 2),
                        int(
                            self.height * 0.02
                            + (
                                (
                                    self.text_siz
                                    + self.bar_height
                                    + self.top_padding
                                )
                                * self.fields[name]["INDEX"]
                            )
                            + self.text_siz * i
                            + self.scroll
                        ),
                    ),
                )

                Renderer.render_text(
                    str(value),
                    Vec2(
                        int(self.sids_padding * 2),
                        int(
                            self.height * 0.02
                            + (
                                (
                                    self.text_siz
                                    + self.bar_height
                                    + self.top_padding
                                )
                                * self.fields[name]["INDEX"]
                            )
                            + self.text_siz * i
                            + self.scroll
                        ),
                    ),
                    0,
                )
                i += 1

        else:
            Renderer.render_image(
                self.imgs["Arrows"][0],
                Vec2(
                    int(self.sids_padding * 1.6 + len(indicator) * 10),
                    self.height * 0.025
                    + (
                        (self.text_siz + self.bar_height + self.top_padding)
                        * self.fields[name]["INDEX"]
                    )
                    + self.scroll,
                ),
            )

    def render_input(self, name: str):
        if name not in self.fields:
            print("Field not found !")
        Renderer.render_text(
            f"{name}: {self.fields[name]['VAL']}",
            Vec2(
                self.sids_padding * 1.5,
                self.height * 0.02
                + (
                    (self.text_siz + self.bar_height + self.top_padding)
                    * self.fields[name]["INDEX"]
                )
                + self.scroll,
            ),
        )
        Renderer.render_image(
            self.imgs["Box"],
            Vec2(
                int(self.sids_padding * 0.95),
                int(
                    self.height * 0.02
                    + (
                        (self.text_siz + self.bar_height + self.top_padding)
                        * self.fields[name]["INDEX"]
                    )
                    + self.text_siz
                    + self.scroll
                ),
            ),
        )
        if self.fields[name]["INPUT"] is None:
            Renderer.render_text(
                "Click to change",
                Vec2(
                    int(self.sids_padding),
                    int(
                        self.height * 0.025
                        + (
                            (
                                self.text_siz
                                + self.bar_height
                                + self.top_padding
                            )
                            * self.fields[name]["INDEX"]
                        )
                        + self.text_siz
                        + self.scroll
                    ),
                ),
            )
        else:
            Renderer.render_text(
                str(self.fields[name]["INPUT"]),
                Vec2(
                    int(self.sids_padding),
                    int(
                        self.height * 0.025
                        + (
                            (
                                self.text_siz
                                + self.bar_height
                                + self.top_padding
                            )
                            * self.fields[name]["INDEX"]
                        )
                        + self.text_siz
                        + self.scroll
                    ),
                ),
            )

    def change_cursor(self, name: str, new_val: tuple):
        """ " new value: 0 value, 1 percent (from 0 to 1)
        (if one is not given the other is gesed)
        """
        if name not in self.fields:
            print("Field not found !")
        if new_val[0]:
            self.fields[name]["VAL"] = new_val[0]
        else:
            self.fields[name]["VAL"] = self.fields[name]["MIN"] + new_val[
                1
            ] * (self.fields[name]["MAX"] - self.fields[name]["MIN"])

        if new_val[1]:
            self.fields[name]["PERCENT"] = new_val[1]
        else:
            self.fields[name]["PERCENT"] = (
                new_val[0] - self.fields[name]["MIN"]
            ) / (self.fields[name]["MAX"] - self.fields[name]["MIN"])
        self.render_options()

    def render_cursor(self, name: str):
        if name not in self.fields:
            print("Field not found !")
        val = int(self.fields[name]["VAL"])
        unit = self.fields[name]["UNIT"]

        indicator = f"{name}: {val}{unit}"
        Renderer.render_text(
            indicator,
            Vec2(
                self.sids_padding * 1.5,
                self.height * 0.02
                + (
                    (self.text_siz + self.bar_height + self.top_padding)
                    * self.fields[name]["INDEX"]
                )
                + self.scroll,
            ),
        )
        Renderer.render_image(
            self.imgs["Bar"],
            Vec2(
                int(self.sids_padding * 0.95),
                int(
                    self.height * 0.02
                    + (
                        (self.text_siz + self.bar_height + self.top_padding)
                        * self.fields[name]["INDEX"]
                    )
                    + self.text_siz
                    + self.scroll
                ),
            ),
        )
        Renderer.render_image(
            self.imgs["Cursor"],
            Vec2(
                int(
                    self.sids_padding
                    + (self.bar_width * self.fields[name]["PERCENT"])
                ),
                (self.height * 0.02)
                + (
                    (self.text_siz + self.bar_height + self.top_padding)
                    * self.fields[name]["INDEX"]
                )
                + self.text_siz
                + self.scroll,
            ),
        )

    def set_field(self, field, opt: Options):
        Window.clear_window()
        try:
            if field["NAME"].endswith("X"):
                x = field["DATA_TYPE"](field["INPUT"])
                second_field = field["NAME"][:-1] + "Y"
                y = self.fields[second_field]["DATA_TYPE"](
                    self.fields[second_field]["VAL"]
                )
                val = Vec2(x, y)
                setattr(opt.cfg, field["NAME"][:-2], val)
                field["VAL"] = val.x
            elif field["NAME"].endswith("Y"):
                y = field["DATA_TYPE"](field["INPUT"])
                second_field = field["NAME"][:-1] + "X"
                x = self.fields[second_field]["DATA_TYPE"](
                    self.fields[second_field]["VAL"]
                )
                val = Vec2(x, y)
                setattr(opt.cfg, field["NAME"][:-2], val)
                field["VAL"] = val.y
            else:
                val = field["DATA_TYPE"](field["INPUT"])
                setattr(opt.cfg, field["NAME"], val)
                field["VAL"] = val
        except Exception as e:
            field["INPUT"] = "This Value is impossible"
            print("This Value is impossible:", e)
        else:
            field["INPUT"] = None
        self.render_options()

    def check_click(self, pos: Vec2, opt: Options) -> None:
        for field_name, field_value in self.fields.items():
            # corsor
            if field_value["TYPE"] == "cursor":
                fpos = Vec2(
                    self.sids_padding,
                    (self.height * 0.02)
                    + (
                        (self.text_siz + self.bar_height + self.top_padding)
                        * self.fields[field_name]["INDEX"]
                    )
                    + self.text_siz
                    + self.scroll,
                )
                siz = Vec2(self.bar_width, self.bar_height)
                if fpos.y < pos.y and fpos.y + siz.y > pos.y:
                    if fpos.x < pos.x and fpos.x + siz.x > pos.x:
                        self.change_cursor(
                            field_name, (None, (pos.x - fpos.x) / siz.x)
                        )
            # inputs
            if field_value["TYPE"] == "input" and (
                field_value["INPUT"] is None
                or field_value["INPUT"] == "This Value is impossible"
            ):
                fpos = Vec2(
                    self.sids_padding,
                    (self.height * 0.02)
                    + (
                        (self.text_siz + self.bar_height + self.top_padding)
                        * self.fields[field_name]["INDEX"]
                    )
                    + self.text_siz
                    + self.scroll,
                )
                siz = Vec2(self.bar_width, self.bar_height + self.top_padding)
                if fpos.y < pos.y and fpos.y + siz.y > pos.y:
                    if fpos.x < pos.x and fpos.x + siz.x > pos.x:
                        field_value["INPUT"] = ""
                        self.render_options()
                        Event_loop.input_to_str(
                            field_value,
                            "INPUT",
                            self.render_options,
                            None,
                            self.set_field,
                            (field_value, opt),
                        )
            # dropdown
            if field_value["TYPE"] == "dropdown":
                fpos = Vec2(
                    self.sids_padding,
                    (
                        (self.text_siz + self.bar_height + self.top_padding)
                        * self.fields[field_name]["INDEX"]
                    )
                    + self.scroll,
                )
                siz = Vec2(
                    self.bar_width / 2, self.bar_height + self.top_padding
                )
                if fpos.y < pos.y and fpos.y + siz.y > pos.y:
                    if fpos.x < pos.x and fpos.x + siz.x > pos.x:
                        if not field_value["OPEN"]:
                            field_value["OPEN"] = True
                        else:
                            field_value["OPEN"] = False
                        self.render_options()
                elif field_value["OPEN"]:
                    i = 1
                    box_height = self.text_siz - 1
                    for value in field_value["POSSIBLE"]:
                        if (
                            fpos.y + (box_height * (i - 1)) + siz.y < pos.y
                            and fpos.y + siz.y + (box_height * i) > pos.y
                        ):
                            if fpos.x < pos.x and fpos.x + siz.x > pos.x:
                                field_value["VAL"] = value
                                self.render_options()
                                return
                        i += 1
                    field_value["OPEN"] = False
                    self.render_options()
        # SAVE button
        save_pos = Vec2(
            self.width * 0.3,
            (self.height * 0.02)
            + (
                (self.text_siz + self.bar_height + self.top_padding)
                * len(self.fields)
            )
            + self.text_siz
            + self.scroll,
        )
        save_siz = Vec2(self.width * 0.4, self.height * 0.1)
        if save_pos.y < pos.y and save_pos.y + save_siz.y > pos.y:
            if save_pos.x < pos.x and save_pos.x + save_siz.x > pos.x:
                vars = []
                for field_name, field_value in self.fields.items():
                    if (
                        field_value["TYPE"] == "input"
                        and field_value["INPUT"] is not None
                    ):
                        field_value["INPUT"] = field_value["INPUT"][:-1]
                        self.set_field(field_value, opt)
                    vars.append(field_value["VAL"])
                opt.put_to_config(self.fields)
                opt.save()
