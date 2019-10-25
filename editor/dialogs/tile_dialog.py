import pygame
from entities.gui import Text, Texture, Window, Dialog, Button, Option, OptionGroup, Anchor, \
    ScrollableContents, ScrollbarType, Scrollbar
import config
from util import make_vector




class TileDialog(Dialog):
    SIZE = (256, 256)

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
            (TileDialog.SIZE[0] - 30, TileDialog.SIZE[1] - self.get_title_bar_bottom() - self.up.rect.height - 20),
            temp_surf
        )

        self.layout()  # ensure scrollable is positioned

        def down_click():
            self.scrollable.set_scroll(self.scrollable.get_scroll() + make_vector(1, 1))

        self.down.on_click = down_click

        # create scrollbars
        self.vertical_scroll = Scrollbar(make_vector(self.scrollable.rect.right, self.scrollable.rect.top),
                                         ScrollbarType.VERTICAL, self.scrollable.rect.height,
                                         assets.gui_atlas.load_sliced("control_small_block2"),
                                         assets.gui_atlas.load_sliced("sb_thumb_v"), 100,
                                         sb_button_mouseover=assets.gui_atlas.load_sliced("sb_thumb_v_hl"))

        self.horizontal_scroll = Scrollbar(make_vector(self.scrollable.rect.left, self.scrollable.rect.bottom),
                                           ScrollbarType.HORIZONTAL, self.scrollable.rect.width,
                                           assets.gui_atlas.load_sliced("control_small_block2"),
                                           assets.gui_atlas.load_sliced("sb_thumb_h"), 100,
                                           sb_button_mouseover=assets.gui_atlas.load_sliced("sb_thumb_h_hl"))

        self.add_child(self.down)
        self.add_child(self.up)
        self.add_child(self.scrollable)
        self.add_child(self.vertical_scroll)
        self.add_child(self.horizontal_scroll)

        self.layout()
