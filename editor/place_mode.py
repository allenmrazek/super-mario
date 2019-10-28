import pygame
import pygame.gfxdraw
from .editor_mode import EditorMode
from .grid_functions import draw_grid, draw_selection_square
from .dialogs.tile_picker_dialog import TilePickerDialog
from util import pixel_coords_to_tile_coords, tile_coords_to_pixel_coords, make_vector
import config


class PlaceMode(EditorMode):
    """Editor is in tile-placement mode"""
    def __init__(self, tile_dialog, level):
        super().__init__()

        self.picker_dialog = tile_dialog  # type: TilePickerDialog
        self.level = level
        self.level_map = level.tile_map

    def on_map_mousedown(self, evt, screen_mouse_pos):
        self.on_map_motion(evt, screen_mouse_pos)

    def on_map_motion(self, evt, screen_mouse_pos):
        tile_coords = pixel_coords_to_tile_coords(make_vector(*screen_mouse_pos) + self.level.position, self.level_map.tileset)

        if self.level_map.is_in_bounds(tile_coords):
            self.level_map.set_tile(tile_coords, self.picker_dialog.selected_tile_idx)

    def on_map_mouseup(self, evt, screen_mouse_pos):
        pass

    def draw(self, screen):
        # todo: check for option
        # for now, assume grid lines wanted

        draw_grid(screen, config.editor_grid_color,
                  self.level_map.tileset.tile_size, self.level.view_rect)

        # also draw a square around current selected point, if within map bounds
        draw_selection_square(screen, self.level_map, config.editor_grid_overlay_color, self.level.view_rect)
