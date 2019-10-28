import pygame
import pygame.gfxdraw
from .editor_mode import EditorMode
from .grid_functions import draw_grid, draw_selection_square
from .dialogs.entity_picker_dialog import EntityPickerDialog
from entities.characters.level_entity import LevelEntity
from util import pixel_coords_to_tile_coords, tile_coords_to_pixel_coords, make_vector
import config


class EntityMode(EditorMode):
    """Editor is in tile-placement mode"""
    def __init__(self, entity_dialog, level):
        super().__init__()

        self.entity_dialog = entity_dialog  # type: EntityPickerDialog
        self.level = level
        self.level_map = level.tile_map

    def on_map_mousedown(self, evt, screen_mouse_pos):
        if self.entity_dialog.selected_entity is not None:
            location = self._get_preview_world_pos(screen_mouse_pos)

            entity = LevelEntity.build(self.level, entity_values=None, kind=self.entity_dialog.selected_entity.name)
            entity.position = location

            self.level.entity_manager.register(entity)

    def on_map_motion(self, evt, screen_mouse_pos):
        pass  # single click per entity

    def on_map_mouseup(self, evt, screen_mouse_pos):
        pass

    def draw(self, screen):
        # todo: check for option
        # for now, assume grid lines wanted

        draw_grid(screen, config.editor_grid_color,
                  self.level_map.tileset.tile_size, self.level.view_rect)

        sel = self.entity_dialog.selected_entity

        if sel is not None:
            preview_location = self._get_preview_world_pos(pygame.mouse.get_pos())

            screen.blit(sel.preview_surface, preview_location - self.level.position)

    def _get_preview_world_pos(self, screen_mouse_pos):
        sel = self.entity_dialog.selected_entity
        r = sel.preview_surface.get_rect()

        tile_coords = pixel_coords_to_tile_coords(make_vector(*screen_mouse_pos) + self.level.position,
                                                  self.level_map.tileset)

        # center by default (world coordinates)
        r.center = make_vector(*screen_mouse_pos) + self.level.position

        align_bottom = True  # temp: will be controlled by editor soon
        align_left = True

        if align_bottom:
            # snap to grid bottom of grid mouse is currently in
            r.bottom = (tile_coords[1] + 1) * self.level_map.tileset.tile_height

        if align_left:
            r.left = tile_coords[0] * self.level_map.tileset.tile_width

        return make_vector(*r.topleft)  # world coordinates
