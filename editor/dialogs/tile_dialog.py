import pygame
from entities.gui import Text, Texture, Window, Dialog, Button, Option, OptionGroup, Anchor, ScrollableContents
import config
from util import make_vector




class TileDialog(Dialog):
    SIZE = (128, 256)

    def __init__(self, assets):
        font = pygame.font.SysFont(None, 24)
        small_font = pygame.font.SysFont(None, 16)

        super().__init__(config.screen_rect.center,
                         TileDialog.SIZE, assets.gui_atlas.load_sliced("bkg_rounded"),
                         font=font, title="Tiles")

        self.tileset = assets.tileset

        # contents window
        temp_surf = pygame.image.load("images/tiles.png")
        temp_surf = pygame.transform.scale(temp_surf, (temp_surf.get_width() * 4, temp_surf.get_height() * 4))



        # create down/up buttons
        button_size = 32, 20

        self.down = Button(
            make_vector(0, self.get_title_bar_bottom()), button_size, assets.gui_atlas.load_sliced("control_small"),
            font=small_font,
            text="down",
            text_color=pygame.Color('black')
        )

        self.up = Button(
            make_vector(TileDialog.SIZE[0] - button_size[0] - 10, self.get_title_bar_bottom()),
            button_size, assets.gui_atlas.load_sliced("control_small"),
            font=small_font,
            text="up",
            text_color=pygame.Color('black'),
            anchor=Anchor.TOP_LEFT
        )

        self.scrollable = ScrollableContents(
            make_vector(10, self.up.rect.height + self.get_title_bar_bottom()),
            (TileDialog.SIZE[0] - 20, TileDialog.SIZE[1] - self.get_title_bar_bottom() - self.up.rect.height - 10),
            temp_surf
        )

        def down_click():
            self.scrollable.set_scroll(self.scrollable.get_scroll() + make_vector(1, 1))

        self.down.on_click = down_click

        self.add_child(self.down)
        self.add_child(self.up)
        self.add_child(self.scrollable)

        self.layout()
