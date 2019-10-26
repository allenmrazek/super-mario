import os
import random
import pygame
from animation import Animation
import config


class TileMap:
    class MapSquare:
        __slots__ = ['passable', 'idx']

        def __init__(self, idx=None, passable=True):
            assert isinstance(idx, int) or idx is None

            self.idx = idx
            self.passable = passable

    def __init__(self, map_size, tileset):
        self.tile_map = []
        self.tileset = tileset
        self.width, self.height = map_size

        for _ in range(self.width):
            self.tile_map.append([TileMap.MapSquare() for _ in range(self.height)])

        # make bottom row of blocks
        for x in range(0, self.width):
            self.set_tile((x, self.height - 1), 0)
            self.set_passable((x, self.height - 1), False)

        # temp: set blocks randomly
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.set_tile((x, y), random.randint(0, self.tileset.tile_count - 1))

        # set bounds of rect to all the same block, to make distinct
        for x in range(0, self.width):
            self.set_tile((x, 0), 0)
            self.set_passable((x, 0), False)
            self.set_tile((x, self.height - 1), 0)
            self.set_passable((x, self.height - 1), False)

        for y in range(0, self.height):
            self.set_tile((0, y), 0)
            self.set_passable((0, y), False)
            self.set_tile((self.width - 1, y), 0)
            self.set_passable((self.width - 1, y), False)

    def view_region_to_tile_region(self, view_region):
        # converts a viewing rectangle into visible tile coordinates
        tw, th = config.base_tile_dimensions[0] * config.rescale_factor, \
                 config.base_tile_dimensions[1] * config.rescale_factor

        x_min = int(view_region.left) // tw
        x_max = min(int(view_region.right) // tw + 1, self.width)
        y_min = int(view_region.top) // th
        y_max = min(int(view_region.bottom) // th + 1, self.height)

        return x_min, y_min, x_max, y_max

    def draw(self, screen, view_region):
        # avoid drawing entire map by determining the subset of tiles visible in the given region
        tw, th = self.tileset.tile_size
        x_min, y_min, x_max, y_max = self.view_region_to_tile_region(view_region)

        x_offset = -view_region.x
        y_offset = -view_region.y

        for y in range(y_min, y_max):
            for x in range(x_min, x_max):

                tile = self.tile_map[x][y]

                if tile.idx is not None:
                    self.tileset.blit(screen, (x * tw + x_offset, y * th + y_offset), tile.idx)

    def update(self, dt):
        pass  # todo: update tileset tiles

    def set_tile(self, tile_position, idx):
        assert 0 <= tile_position[0] <= self.width
        assert 0 <= tile_position[1] <= self.height

        self.tile_map[tile_position[0]][tile_position[1]].idx = idx

    def set_passable(self, tile_position, passable):
        assert 0 <= tile_position[0] <= self.width
        assert 0 <= tile_position[1] <= self.height

        self.tile_map[tile_position[0]][tile_position[1]].passable = passable

    def get_passable(self, tile_position):
        assert 0 <= tile_position[0] <= self.width
        assert 0 <= tile_position[1] <= self.height

        return self.tile_map[tile_position[0]][tile_position[1]].passable

    def clip_to_bounds(self, tile_coords):
        tx = min(max(tile_coords[0], 0), self.width - 1)
        ty = min(max(tile_coords[1], 0), self.height - 1)

        return tx, ty

    def is_in_bounds(self, tile_coords):
        return 0 <= tile_coords[0] < self.width and 0 <= tile_coords[1] < self.height

    @property
    def tile_width(self):
        return self.tileset.tile_width

    @property
    def tile_height(self):
        return self.tileset.tile_height
