import pygame
from entities.gui import Text, Texture, Window, Dialog, Option, OptionGroup
from entities.entity import Layer
from entities.gui import Anchor
import config
from util import make_vector


class LayerDialog(Dialog):

    def __init__(self, atlas):
        font = pygame.font.SysFont("", 24)

        r = config.screen_rect.copy()
        title = "Active Layer"

        # calculate position and dimensions of this dialog to fit all layer names
        width = max(font.size(title)[0] + 20, max([font.size(x.name)[0] for x in Layer]))
        height = font.get_height() * (len(Layer) + 1) + 10

        width, height = 256, 256

        pos = make_vector(r.right - width, r.bottom - height)

        super().__init__(pos, (width, height), atlas.load_sliced("bkg_rounded"),
                         font=font, title=title)

        # create an entry for each layer
        y_pos = font.get_height()

        self.option_group = OptionGroup(tf_require_selected=True)

        for layer in Layer:
            option = Option(make_vector(0, y_pos),
                            (width, font.get_height() * 2),
                            text=layer.name,
                            selected_image=atlas.load_static("option_button_checked_light"),
                            unselected_image=atlas.load_static("option_button"),
                            text_color=pygame.Color('black'),
                            background=atlas.load_sliced("control_small_block2"),
                            mouseover_image=atlas.load_sliced("control_small_block2_dk"),
                            font=font)
            option.selected = False

            self.add_child(option)
            option.layout()
            y_pos += option.height

            self.option_group.add(option)
