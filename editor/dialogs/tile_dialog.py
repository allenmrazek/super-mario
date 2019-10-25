import pygame
from entities.gui import Text, Texture, Window, Dialog, Button, Option, OptionGroup, Anchor
import config
from util import make_vector


class TileDialog(Dialog):
    SIZE = (128, 256)

    def __init__(self, atlas, tileset):
        font = pygame.font.SysFont(None, 24)
        small_font = pygame.font.SysFont(None, 16)

        super().__init__(config.screen_rect.center,
                         TileDialog.SIZE, atlas.load_sliced("bkg_rounded"),
                         font=font, title="Tiles")

        self.tileset = tileset

        # create down/up buttons
        button_size = 64, 20

        self.down = Button(
            make_vector(0, self.get_title_bar_bottom()), button_size, atlas.load_sliced("control_small"),
            font=small_font,
            text="down",
            text_color=pygame.Color('black')
        )

        self.up = Button(
            make_vector(TileDialog.SIZE[0] - button_size[0], self.get_title_bar_bottom()),
            button_size, atlas.load_sliced("control_small"),
            font=small_font,
            text="up",
            text_color=pygame.Color('black'),
            anchor=Anchor.TOP_RIGHT
        )

        self.add_child(self.down)
        self.add_child(self.up)
