from .editor_mode import EditorMode
from .grid_functions import *
from util import pixel_coords_to_tile_coords, tile_coords_to_pixel_coords


class PassableMode(EditorMode):
    def __init__(self, level):
        super().__init__()

        self.level = level
        self.tile_map = level.tile_map
        self._motion_set = False  # tiles will be set to this passability on mouse drags

    def draw(self, screen):
        tile_size = self.tile_map.tileset.tile_size
        view_region = self.level.view_rect
        view_position = self.level.position

        # draw grid bits
        draw_grid(screen, config.editor_grid_color, tile_size, view_region)

        # draw impassable tiles
        r = pygame.Rect(0, 0, *tile_size)

        alt_down = pygame.key.get_mods() & pygame.KMOD_ALT

        x_min, y_min, x_max, y_max = self.tile_map.view_region_to_tile_region(view_region)

        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                passable = self.tile_map.get_passable((x, y))

                if not passable:
                    r.topleft = tile_coords_to_pixel_coords((x, y), self.tile_map.tileset)
                    r.x -= view_position[0]
                    r.y -= view_position[1]

                    # draw a nice big X through this tile
                    pygame.gfxdraw.line(screen, r.topleft[0], r.topleft[1], r.bottomright[0], r.bottomright[1],
                                        config.editor_grid_overlay_color)

                    # draw a reddish box if alt is pressed to make it easier to see which tiles aren't passable
                    if alt_down:
                        pygame.gfxdraw.box(screen, r, (255, 0, 100))

        draw_selection_square(screen, self.tile_map, config.editor_grid_overlay_color, self.level.view_rect)

    def on_map_mousedown(self, evt, screen_mouse_pos):
        coords = pixel_coords_to_tile_coords(make_vector(*screen_mouse_pos) + self.level.position,
                                             self.tile_map.tileset)

        if self.tile_map.is_in_bounds(coords):
            # as a super rough test thing, let's try and change a tile with this
            toggle = not self.tile_map.get_passable(coords)
            self._set_tile_passability(coords, toggle)

    def on_map_motion(self, evt, screen_mouse_pos):
        coords = pixel_coords_to_tile_coords(make_vector(*screen_mouse_pos) + self.level.position,
                                             self.tile_map.tileset)
        self._set_tile_passability(coords, self._motion_set)

    def on_map_mouseup(self, evt, screen_mouse_pos):
        pass

    def _set_tile_passability(self, coords, tf):
        self.tile_map.set_passable(coords, tf)
        self._motion_set = tf