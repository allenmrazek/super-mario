import math
import pygame

block_size = 16  # 16 pixels on a side


def mario_str_to_pixel_value(str_mario_value):
    """Given a classic mario velocity string, convert into a magnitude suitable for the game"""

    if str_mario_value[0:2].lower() == "0x":
        str_mario_value = str_mario_value[2:]

    block_value = int(str_mario_value[:1], 16)
    pixel_value = int(str_mario_value[1:2], 16)
    subpixel_value = int(str_mario_value[2:3], 16)
    subsubpixel_value = int(str_mario_value[3:4], 16)
    subsubsubpixel_value = int(str_mario_value[4:5], 16)

    return block_value * block_size + pixel_value + subpixel_value / 16. + subsubpixel_value / (16. ** 2) + \
        subsubsubpixel_value / (16. ** 3)


def distance_squared(p1, p2):
    deltax = p2[0] - p1[0]
    deltay = p2[1] - p1[1]

    return deltax * deltax + deltay * deltay


def distance(p1, p2):
    return math.sqrt(distance_squared(p1, p2))


def copy_vector(v):
    new_v = pygame.Vector2()
    new_v.x, new_v.y = v[0], v[1]

    return new_v


def make_vector(x, y):
    new_v = pygame.Vector2()

    new_v.x, new_v.y = x, y

    return new_v


def can_collide(mask1, mask2):
    return (mask1 & mask2) != 0


def pixel_coords_to_tile_coords(pixel_coords, tileset):
    x_coord = int(pixel_coords[0] / tileset.tile_width)
    y_coord = int(pixel_coords[1] / tileset.tile_height)

    return x_coord, y_coord


def tile_coords_to_pixel_coords(tile_coords, tileset):
    return tile_coords[0] * tileset.tile_width, tile_coords[1] * tileset.tile_height


def tile_index_to_coords(idx, tileset):
    tile_x = (idx % tileset.num_tiles_per_row)
    tile_y = (idx // tileset.num_tiles_per_col)

    return tile_x, tile_y


def tile_coords_to_index(tile_coords, tileset):
    raise NotImplementedError


def bind_callback_parameters(to_call, *args):
    def _callback(*more_args):
        to_call(*args, *more_args)

    return _callback


def clamp(val, min_val, max_val):
    return max(min(val, max_val), min_val)
