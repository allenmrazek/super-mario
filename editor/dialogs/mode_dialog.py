import pygame
from entities.gui import Text, Texture, Window, Dialog, Option, OptionGroup, Button
from entities.entity import Layer
from entities.gui import Anchor
import config
from util import make_vector, bind_callback_parameters


class ModeDialog(Dialog):
    SIZE = 200, 200

    def __init__(self, gui_atlas, on_tile_mode_callback, on_passable_mode_callback, on_config_mode_callback, on_entity_mode_callback):
        font = pygame.font.SysFont("", 24)

        r = config.screen_rect.copy()
        title = "Editor Mode"

        width, height = ModeDialog.SIZE

        pos = make_vector(0, r.bottom - height - 100)

        super().__init__(pos, (width, height), gui_atlas.load_sliced("bkg_rounded"),
                         font=font, title=title)

        # create an entry for each mode
        y_pos = font.get_height()

        button_size = (width - 20, 20)
        button_text_color = pygame.Color('black')

        opt_mouseover = bind_callback_parameters(gui_atlas.load_sliced, "option_button_hl")
        bkg = bind_callback_parameters(gui_atlas.load_sliced, "option_button")

        # create tile mode
        tile_mode_button = Button(make_vector(10, self.get_title_bar_bottom() + 3),
                                  size=button_size,
                                  background=gui_atlas.load_sliced("option_button"),
                                  font=font,
                                  text="Edit Tiles",
                                  on_click_callback=bind_callback_parameters(on_tile_mode_callback),
                                  text_color=button_text_color,
                                  mouseover_image=gui_atlas.load_sliced("option_button_hl"))

        self.add_child(tile_mode_button)

        # passable mode
        passable_mode_button = Button(make_vector(10, tile_mode_button.relative_position.y + tile_mode_button.height),
                                      size=button_size,
                                      background=gui_atlas.load_sliced("option_button"),
                                      font=font,
                                      text="Edit Passability",
                                      on_click_callback=bind_callback_parameters(on_passable_mode_callback),
                                      text_color=button_text_color,
                                      mouseover_image=gui_atlas.load_sliced("option_button_hl"))

        self.add_child(passable_mode_button)

        # config mode
        config_mode_button = Button(make_vector(10, passable_mode_button.relative_position.y + passable_mode_button.height),
                                      size=button_size,
                                      background=gui_atlas.load_sliced("option_button"),
                                      font=font,
                                      text="Edit Settings",
                                      on_click_callback=bind_callback_parameters(on_config_mode_callback),
                                      text_color=button_text_color,
                                      mouseover_image=gui_atlas.load_sliced("option_button_hl"))
        self.add_child(config_mode_button)

        # entity mode
        entity_mode_button = Button(make_vector(10, config_mode_button.relative_position.y + config_mode_button.height),
                                      size=button_size,
                                      background=bkg(),
                                      font=font,
                                      text="Entities",
                                      on_click_callback=bind_callback_parameters(on_entity_mode_callback),
                                      text_color=button_text_color,
                                      mouseover_image=opt_mouseover())

        self.add_child(entity_mode_button)
