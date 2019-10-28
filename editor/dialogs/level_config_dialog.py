import os
import json
from util import make_vector, clamp
from assets.gui_helper import *
from entities.gui.modal import ModalTextInput


class LevelConfigDialog(Dialog):
    SIZE = 256, 256

    def __init__(self, level, gui_atlas):
        font = pygame.font.SysFont("", 24)

        self.gui_atlas = gui_atlas

        r = config.screen_rect.copy()
        title = "Level Configuration"

        width, height = LevelConfigDialog.SIZE

        pos = make_vector(*r.center)
        frame_width = 20

        super().__init__(pos, (width, height), gui_atlas.load_sliced("window_bkg_large"),
                         font=font, title=title, tb_bkg=gui_atlas.load_sliced("tb_frame"), additional_height=8, text_start_offset=(12, 5))

        self.level = level
        black = pygame.Color('black')

        # Background color text
        bkg_color_text = Text(make_vector(frame_width, self.get_title_bar_bottom()), text="Background Color",
                              font=font, text_color=black)

        self.add_child(bkg_color_text)

        slider_width = LevelConfigDialog.SIZE[0] - 80
        slider_left = frame_width + 30

        # slider for r
        r_text = Text(make_vector(frame_width, bkg_color_text.relative_position.y + bkg_color_text.height),
                      text="R:", font=font, text_color=black)

        self.add_child(r_text)

        self.bkg_color_r_slider = create_slider(gui_atlas, make_vector(slider_left, bkg_color_text.relative_position.y + bkg_color_text.height),
                                                slider_width, 0, 255, self._on_slider_changed)

        # slider for g
        g_text = Text(make_vector(frame_width, self.bkg_color_r_slider.relative_position.y + self.bkg_color_r_slider.height),
                      text="G:", font=font, text_color=black)

        self.add_child(g_text)

        self.bkg_color_g_slider = create_slider(gui_atlas, make_vector(slider_left, r_text.relative_position.y + g_text.height),
                                                slider_width, 0, 255, self._on_slider_changed)

        # slider for b
        b_text = Text(make_vector(frame_width, self.bkg_color_g_slider.relative_position.y + self.bkg_color_g_slider.height),
                      text="B:", font=font, text_color=black)

        self.add_child(b_text)

        self.bkg_color_b_slider = create_slider(gui_atlas, make_vector(slider_left, g_text.relative_position.y + b_text.height),
                                                slider_width, 0, 255, self._on_slider_changed)

        self.add_child(self.bkg_color_r_slider)
        self.add_child(self.bkg_color_g_slider)
        self.add_child(self.bkg_color_b_slider)

        # buttons
        pos = make_vector(3 * frame_width // 2, self.bkg_color_b_slider.height + self.bkg_color_b_slider.relative_position.y + 6)
        button_y_offset = 4

        button_size = (self.width - 3 * frame_width, self.bkg_color_b_slider.height * 1.5)

        self.save_button = create_button(gui_atlas, pos, button_size, "Save", font=font, on_click_callback=self._on_save_map)
        self.add_child(self.save_button)

        pos.y += self.save_button.height + button_y_offset

        self.load_button = create_button(gui_atlas, pos, button_size, "Load", font=font, on_click_callback=self._on_load_map)
        self.add_child(self.load_button)

        pos.y += self.save_button.height + button_y_offset

        self.width_button = create_button(gui_atlas, pos, button_size, "Set Width", font=font, on_click_callback=self._on_change_width)
        self.add_child(self.width_button)

        pos.y += self.save_button.height + button_y_offset

        self.height_button = create_button(gui_atlas, pos, button_size, "Set Height", font=font, on_click_callback=self._on_change_height)
        self.add_child(self.height_button)

    def _on_slider_changed(self, new_value):
        r = clamp(int(self.bkg_color_r_slider.value), 0, 255)
        g = clamp(int(self.bkg_color_g_slider.value), 0, 255)
        b = clamp(int(self.bkg_color_b_slider.value), 0, 255)

        self.level.background_color = pygame.Color(r, g, b)  # tuple = invalid, create a make_color at some point

    def _on_save_map(self):
        def _save_map(filename):
            path = os.path.join("levels", filename + ".level")

            if len(filename) == 0:
                print("failed to save map -- no filename")
                return

            with open(path, 'w') as f:
                f.write(json.dumps(self.level.serialize()))
                print(f"Saved map '{path}'")

        def _cancel():
            pass

        ModalTextInput.spawn(self.gui_atlas, "Enter Filename:", _save_map, _cancel)

    def _on_load_map(self):
        def _load_map(filename):
            if len(filename) == 0:
                print("cannot open map -- no filename provided")
                return

            path = os.path.join("levels", filename + ".level")

            if not os.path.exists(path):
                print(f"cannot open '{path}' -- file not found")
                return
            elif not os.path.isfile(path):
                print(f"cannot open '{path}' -- not a file")
                return

            with open(path, 'r') as f:
                self.level.deserialize(json.loads(f.read()))

            print(f"Successfully read '{path}'")

            clr = pygame.Color(*self.level.background_color)

            self.bkg_color_r_slider.value = clr[0]
            self.bkg_color_g_slider.value = clr[1]
            self.bkg_color_b_slider.value = clr[2]

        def _cancel():
            pass

        ModalTextInput.spawn(self.gui_atlas, "Load map filename:", _load_map, _cancel)

    def _on_change_width(self):
        def _set_width(width_str):
            print("change map width here")

        def _cancel():
            pass

        ModalTextInput.spawn(self.gui_atlas, "Map Width:", _set_width, _cancel)

    def _on_change_height(self):
        def _set_height(height_str):
            print("change map height here")

        def _cancel():
            pass

        ModalTextInput.spawn(self.gui_atlas, "Map Height:", _set_height, _cancel)
