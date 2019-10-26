from .editor_mode import EditorMode
from .grid_functions import *
from util import pixel_coords_to_tile_coords, tile_coords_to_pixel_coords


class PassableMode(EditorMode):
    def __init__(self, level_map):
        super().__init__()

        self.level_map = level_map

    def draw(self, screen):
        tile_size = (self.level_map.tileset.tile_width, self.level_map.tileset.tile_height)

        # draw grid bits
        draw_grid(screen, config.editor_grid_color, tile_size)

        # draw impassable tiles
        r = pygame.Rect(0, 0, *tile_size)

        alt_down = pygame.key.get_mods() & pygame.KMOD_ALT

        for x in range(0, self.level_map.width):
            for y in range(0, self.level_map.height):
                passable = self.level_map.get_passable((x, y))

                if not passable:
                    r.topleft = tile_coords_to_pixel_coords((x, y), self.level_map.tileset)

                    # draw a nice big X through this tile
                    pygame.gfxdraw.line(screen, r.topleft[0], r.topleft[1], r.bottomright[0], r.bottomright[1],
                                        config.editor_grid_overlay_color)

                    # draw a reddish box if alt is pressed to make it easier to see which tiles aren't passable
                    if alt_down:
                        pygame.gfxdraw.box(screen, r, (255, 0, 100))

        draw_selection_square(screen, self.level_map, config.editor_grid_overlay_color)

    def on_map_click(self, evt, screen_mouse_pos):
        coords = pixel_coords_to_tile_coords(screen_mouse_pos, self.level_map.tileset)

        if self.level_map.is_in_bounds(coords):
            # as a super rough test thing, let's try and change a tile with this
            self.level_map.set_passable(coords, not self.level_map.get_passable(coords))

    def on_map_mousedown(self, evt, screen_mouse_pos):
        pass

