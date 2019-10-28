import pygame
import pygame.gfxdraw
from .editor_mode import EditorMode
from .grid_functions import draw_grid, draw_selection_square
from .dialogs.entity_picker_dialog import EntityPickerDialog
from util import pixel_coords_to_tile_coords, tile_coords_to_pixel_coords, make_vector
import config


class EntityMode(EditorMode):
    """Editor is in tile-placement mode"""
    def __init__(self, entity_dialog, level):
        super().__init__()

        self.entity_dialog = entity_dialog  # type: EntityPickerDialog
        self.level = level
        self.level_map = level.tile_map

    def on_map_click(self, evt, screen_mouse_pos):
        if self.entity_dialog.selected_entity is not None:
            print(f"would place {self.entity_dialog.selected_entity.name} here")

    def on_map_mousedown(self, evt, screen_mouse_pos):
        pass  # single click per entity

    def draw(self, screen):
        # todo: check for option
        # for now, assume grid lines wanted

        draw_grid(screen, config.editor_grid_color,
                  self.level_map.tileset.tile_size, self.level.view_rect)

        # also draw a square around current selected point, if within map bounds
        # draw_selection_square(screen, self.level_map, config.editor_grid_overlay_color, self.level.view_rect)

        sel = self.entity_dialog.selected_entity

        if sel is not None:
            r = sel.preview_surface.get_rect()
            mouse_pos = pygame.mouse.get_pos()

            r.topleft = make_vector(*mouse_pos) - make_vector(r.width // 2, r.height // 2)
            tile_coords = pixel_coords_to_tile_coords(make_vector(*mouse_pos) + self.level.position,
                                                      self.level_map.tileset)

            align_bottom = True  # temp: will be controlled by editor soon
            align_left = True

            if align_bottom:
                # snap to grid bottom of grid mouse is currently in
                r.bottom = (tile_coords[1] + 1) * self.level_map.tileset.tile_height

            if align_left:
                r.left = tile_coords[0] * self.level_map.tileset.tile_width

            screen.blit(sel.preview_surface, r)
