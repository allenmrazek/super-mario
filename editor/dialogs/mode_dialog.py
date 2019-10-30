from util import make_vector, bind_callback_parameters
from assets.gui_helper import *


class ModeDialog(Dialog):
    SIZE = 200, 170

    def __init__(self, gui_atlas, on_tile_mode_callback, on_passable_mode_callback, on_config_mode_callback,
                 on_entity_mode_callback):
        font = pygame.font.SysFont("", 24)

        r = config.screen_rect.copy()
        title = "Editor Mode"

        width, height = ModeDialog.SIZE

        pos = make_vector(0, r.bottom - height - 100)

        super().__init__(pos, (width, height), gui_atlas.load_sliced("window_bkg_large"),
                         font=font, title=title, additional_height=8, text_start_offset=(12, 5),
                         tb_bkg=gui_atlas.load_sliced("tb_frame"))

        # create an entry for each mode
        frame_width = 25
        delta_y = 6

        button_size = (width - 2 * frame_width, 24)
        button_text_color = pygame.Color('white')

        opt_mouseover = bind_callback_parameters(gui_atlas.load_sliced, "option_button_hl")
        bkg = bind_callback_parameters(gui_atlas.load_sliced, "option_button")

        # create tile mode
        tile_mode_button = create_button(gui_atlas, make_vector(frame_width, self.get_title_bar_bottom() + delta_y),
                                         button_size,
                                         "Tile", bind_callback_parameters(on_tile_mode_callback), font,
                                         text_color=button_text_color)

        self.add_child(tile_mode_button)

        # passable mode
        passable_mode_button = create_button(gui_atlas,
                                             make_vector(frame_width,
                                                         tile_mode_button.relative_position.y +
                                                         tile_mode_button.height + delta_y), button_size,
                                             "Passability", bind_callback_parameters(on_passable_mode_callback), font,
                                             text_color=button_text_color)

        self.add_child(passable_mode_button)

        # entity mode
        entity_mode_button = create_button(gui_atlas,
                                           make_vector(frame_width,
                                                       passable_mode_button.relative_position.y +
                                                       passable_mode_button.height + delta_y), button_size,
                                           "Entities", bind_callback_parameters(on_entity_mode_callback), font,
                                           text_color=button_text_color)

        self.add_child(entity_mode_button)

        # config mode
        config_mode_button = create_button(gui_atlas,
                                           make_vector(frame_width,
                                                       entity_mode_button.relative_position.y +
                                                       entity_mode_button.height + delta_y), button_size,
                                           "Configuration", bind_callback_parameters(on_config_mode_callback), font,
                                           text_color=button_text_color)

        self.add_child(config_mode_button)
