import pygame
import pygame.gfxdraw
import config
from util import pixel_coords_to_tile_coords, tile_coords_to_pixel_coords, make_vector


def draw_grid(screen, line_color, grid_size, view_rect):
    w, h = grid_size
    ox, oy = (view_rect.left % grid_size[0], view_rect.top % grid_size[1]) if view_rect is not None else (0, 0)

    # horizontal lines
    for y_coord in range(h - oy, config.screen_rect.height, h):
        pygame.gfxdraw.line(screen, 0, y_coord, config.screen_rect.width, y_coord, line_color)

    # vertical lines
    for x_coord in range(w - ox, config.screen_rect.width, w):
        pygame.gfxdraw.line(screen, x_coord, 0, x_coord, config.screen_rect.height, line_color)


def draw_selection_square(screen, level_map, color, view_rect):
    tile_coords = pixel_coords_to_tile_coords(pygame.mouse.get_pos() + make_vector(view_rect.x, view_rect.y), level_map.tileset)

    if level_map.is_in_bounds(tile_coords):
        r = pygame.Rect(
            *tile_coords_to_pixel_coords(tile_coords, level_map.tileset),
            level_map.tileset.tile_width, level_map.tileset.tile_height)

        r.topleft -= make_vector(*view_rect.topleft)

        pygame.gfxdraw.rectangle(screen, r, color)
