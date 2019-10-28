import pygame
from entities.gui import Dialog, ScrollableContents, ScrollbarType, Scrollbar
import config
from util import make_vector
from util import tile_coords_to_pixel_coords
from util import pixel_coords_to_tile_coords
from util import tile_index_to_coords


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
            self._create_tileset_surface()
        )

        self.layout()  # ensure scrollable is positioned

        # create scrollbars
        self.vertical_scroll = Scrollbar(make_vector(self.scrollable.rect.right, self.scrollable.rect.top + 5),
                                         ScrollbarType.VERTICAL, self.scrollable.rect.height,
                                         assets.gui_atlas.load_sliced("control_small_block2"),
                                         assets.gui_atlas.load_sliced("sb_thumb_v"),
                                         max(0, self.tileset.surface.get_height() - self.scrollable.height),
                                         sb_button_mouseover=assets.gui_atlas.load_sliced("sb_thumb_v_dk"),
                                         on_value_changed_callback=self._on_scroll_changed)

        self.horizontal_scroll = Scrollbar(make_vector(self.scrollable.rect.left + 5, self.scrollable.rect.bottom),
                                           ScrollbarType.HORIZONTAL, self.scrollable.rect.width - 5,
                                           assets.gui_atlas.load_sliced("control_small_block2"),
                                           assets.gui_atlas.load_sliced("sb_thumb_h"),
                                           max(0, self.tileset.surface.get_width() - self.scrollable.width),
                                           sb_button_mouseover=assets.gui_atlas.load_sliced("sb_thumb_h_dk"),
                                           on_value_changed_callback=self._on_scroll_changed)

        self.add_child(self.scrollable)
        self.add_child(self.vertical_scroll)
        self.add_child(self.horizontal_scroll)

        self.layout()

        self.selected_tile_idx = 0

    def _on_scroll_changed(self, new_val):
        self.scrollable.set_scroll(make_vector(self.horizontal_scroll.value, self.vertical_scroll.value))

    def handle_event(self, evt, game_events):
        # can't just call super to handle this for us, because Window is a parent class and will eat any
        # mousedown events which we need to select tiles
        self.handle_event_children(evt, game_events)

        if not evt.consumed:
            if evt.type == pygame.MOUSEBUTTONDOWN:
                inside_content_window = self.scrollable.get_absolute_rect().collidepoint(evt.pos)

                if inside_content_window:
                    self.consume(evt)
                    self._set_selected(evt.pos)

        # this will re-dispatch the event, including to parent classes
        super().handle_event(evt, game_events)

    def draw(self, screen: pygame.Surface, view_rect):
        super().draw(screen, view_rect)

        # calc position of selected tile, ignoring scroll position for the moment
        coords = tile_index_to_coords(self.selected_tile_idx, self.tileset)

        tile_x = coords[0] * self.tileset.tile_width
        tile_y = coords[1] * self.tileset.tile_height

        # account for scrolling
        top_left = self.scrollable.get_absolute_position() + make_vector(tile_x - self.scrollable.get_scroll().x,
                                                                         tile_y - self.scrollable.get_scroll().y)
        r = pygame.Rect(*top_left, self.tileset.tile_width, self.tileset.tile_height)
        r.inflate_ip(2, 2)

        existing_clip = screen.get_clip()
        screen.set_clip(self.rect)

        pygame.draw.rect(screen, (255, 0, 0), r, 3)

        screen.set_clip(existing_clip)

    def _set_selected(self, mouse_pos):
        # get mouse pos relative to scrollable window
        relative_pos = mouse_pos - self.scrollable.get_absolute_position()

        # account for scroll amount
        relative_pos += self.scrollable.get_scroll()

        # calculate a tile x and y (in terms of tiles, not pixels) on the tile sheet
        tile_x, tile_y = pixel_coords_to_tile_coords(relative_pos, self.tileset)

        # convert to index
        self.selected_tile_idx = tile_y * self.tileset.num_tiles_per_row + tile_x

    def _create_tileset_surface(self):
        # the raw tileset surface isn't suitable since it has gaps -> convert to a surface that does not have such gaps
        s = pygame.Surface((self.tileset.tile_width * self.tileset.num_tiles_per_row,
                            self.tileset.tile_height * self.tileset.num_tiles_per_col))

        for idx in range(self.tileset.tile_count):
            coords = tile_index_to_coords(idx, self.tileset)
            pos = (coords[0] * self.tileset.tile_width, coords[1] * self.tileset.tile_height)
            self.tileset.blit(s, pos, idx)

        s = s.convert()
        s.set_colorkey(self.tileset.surface.get_colorkey())

        return s
