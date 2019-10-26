import pygame
import pygame.gfxdraw
from .editor_mode import EditorMode
from .dialogs.tile_picker_dialog import TilePickerDialog
from util import pixel_coords_to_tile_coords, tile_coords_to_pixel_coords
import config


class PlaceMode(EditorMode):
    """Editor is in tile-placement mode"""
    def __init__(self, tile_dialog, level_map):
        super().__init__()

        self.picker_dialog = tile_dialog  # type: TilePickerDialog
        self.level_map = level_map

    def on_map_click(self, screen_mouse_pos):
        tile_coords = pixel_coords_to_tile_coords(screen_mouse_pos, self.level_map.tileset)

        if self.level_map.is_in_bounds(tile_coords):
            self.level_map.set_tile(self.picker_dialog.selected_tile_idx)

    def draw(self, screen):
        # todo: check for option
        # for now, assume grid lines wanted

        line_color = (255, 0, 0, 128)
        overlay_color = (255, 0, 0, 255)

        # horizontal lines
        for y_coord in range(0, config.screen_rect.height, self.level_map.tileset.tile_height):
            pygame.gfxdraw.line(screen, 0, y_coord, config.screen_rect.width, y_coord, line_color)

        # vertical lines
        for x_coord in range(0, config.screen_rect.width, self.level_map.tileset.tile_width):
            pygame.gfxdraw.line(screen, x_coord, 0, x_coord, config.screen_rect.height, line_color)

        # also draw a square around current selected point, if within map bounds
        tile_coords = pixel_coords_to_tile_coords(pygame.mouse.get_pos(), self.level_map.tileset)

        if self.level_map.is_in_bounds(tile_coords):
            r = pygame.Rect(
                *tile_coords_to_pixel_coords(tile_coords, self.level_map.tileset),
                self.level_map.tileset.tile_width, self.level_map.tileset.tile_height)

            pygame.gfxdraw.rectangle(screen, r, overlay_color)
