import pygame
from entities.gui import Text, Texture, Window, Dialog
from entities.entity import Layer
from entities.gui import Anchor
import config
from util import make_vector


class LayerDialog(Dialog):

    def __init__(self, atlas):
        font=pygame.font.SysFont("", 24)

        r = config.screen_rect.copy()

        # calculate position and dimensions of this dialog to fit all layer names
        width = max([font.size(x.name)[0] for x in Layer])
        height = font.get_height() * (len(Layer) + 1) + 10

        pos = make_vector(r.right - width, r.bottom - height)

        super().__init__(pos, (width, height), atlas.load_sliced("rounded_corners"),
                         font=font, title="Active Layer")

        # create an entry for each layer
        y_pos = font.get_height()

        for layer in Layer:
            text = Text(make_vector(0, y_pos), layer.name, anchor=Anchor.TOP_LEFT, color=pygame.Color('green'))

            y_pos += font.get_height()

            self.add_child(text)
