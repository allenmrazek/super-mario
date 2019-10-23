import pygame
from entities.gui import Text, Texture, Window, Dialog, Option, ElementStyle
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

        super().__init__(pos, (width, height), atlas.load_sliced("rounded_corners"),
                         font=font, title=title)

        # create an entry for each layer
        y_pos = font.get_height()

        option_style = ElementStyle(
            text_color=pygame.Color('black'),
            selected=atlas.load_static("option_button_checked_light"),
            not_selected=atlas.load_static("option_button"),
            font=font,
            background=None
        )

        button_style = ElementStyle(
            background=atlas.load_sliced("very_rounded_corners"),
            font=font,
            text_color=option_style.text_color
        )

        for layer in Layer:
            option = Option(make_vector(0, y_pos), (width - 10, font.get_height()),
                            text=layer.name, option_style=option_style, button_style=button_style)

            self.add_child(option)
            option.layout()
            y_pos += option.height
