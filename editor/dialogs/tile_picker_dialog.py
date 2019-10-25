import pygame
from entities.gui import Dialog, ScrollableContents, ScrollbarType, Scrollbar
import config
from util import make_vector


class TilePickerDialog(Dialog):
    SIZE = (256, 256)

    def __init__(self, assets):
        font = pygame.font.SysFont(None, 24)

        super().__init__(config.screen_rect.center,
                         TilePickerDialog.SIZE, assets.gui_atlas.load_sliced("bkg_rounded"),
                         font=font, title="Tiles")

        self.tileset = assets.tileset

        # contents window
        self.scrollable = ScrollableContents(
            make_vector(6, self.get_title_bar_bottom()),
            (TilePickerDialog.SIZE[0] - 25, TilePickerDialog.SIZE[1] - self.get_title_bar_bottom() - 22),
            assets.tileset.surface
        )

        self.layout()  # ensure scrollable is positioned

        # create scrollbars
        self.vertical_scroll = Scrollbar(make_vector(self.scrollable.rect.right, self.scrollable.rect.top + 5),
                                         ScrollbarType.VERTICAL, self.scrollable.rect.height,
                                         assets.gui_atlas.load_sliced("control_small_block2"),
                                         assets.gui_atlas.load_sliced("sb_thumb_v"),
                                         max(0, self.tileset.surface.get_height() - self.scrollable.height),
                                         sb_button_mouseover=assets.gui_atlas.load_sliced("sb_thumb_v_hl"),
                                         on_value_changed_callback=self._on_scroll_changed)

        self.horizontal_scroll = Scrollbar(make_vector(self.scrollable.rect.left + 5, self.scrollable.rect.bottom),
                                           ScrollbarType.HORIZONTAL, self.scrollable.rect.width - 5,
                                           assets.gui_atlas.load_sliced("control_small_block2"),
                                           assets.gui_atlas.load_sliced("sb_thumb_h"),
                                           max(0, self.tileset.surface.get_width() - self.scrollable.width),
                                           sb_button_mouseover=assets.gui_atlas.load_sliced("sb_thumb_h_hl"),
                                           on_value_changed_callback=self._on_scroll_changed)

        self.add_child(self.scrollable)
        self.add_child(self.vertical_scroll)
        self.add_child(self.horizontal_scroll)

        self.layout()

    def _on_scroll_changed(self, new_val):
        self.scrollable.set_scroll(make_vector(self.horizontal_scroll.value, self.vertical_scroll.value))

