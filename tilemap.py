import os
import pygame
from tileset import TileSet


class TileMap:
    def __init__(self, tile_set: TileSet, size, filename=None):
        self.tile_set = tile_set
        self.map = []
        self.width, self.height = int(size[0]), int(size[1])

    def set_width(self, num_tiles, preserve=True):
        new_map = []

        for row in range(self.height):
            new_map[row] = [[] for _ in range(num_tiles)]

            if preserve:
                for i in range(0, min(num_tiles, self.width)):
                    new_map[row][i] = (self.map[row][i])

        self.map = new_map

    def set_height(self, num_tiles, preserve=True):
        new_map = []

        for row in range(num_tiles):
            if preserve:
                new_map[row] = self.map[row][:num_tiles]
            else:
                new_map[row] = [[] for _ in range(self.width)]

        self.map = new_map

    def set_size(self, size, preserve=True):
        self.set_width(size[0], preserve)
        self.set_height(size[1], preserve)

    @staticmethod
    def load_from_file(filename):
        fn = os.fsencode(filename)

        if not os.path.exists(fn) or not os.path.isfile(fn):
            raise FileNotFoundError

        raise NotImplementedError  # todo: file format

    def save_to_file(self, filename):
        raise NotImplementedError

    def draw(self, screen, view_region):
        # avoid drawing entire map by determining the subset of tiles visible in the given region
        x_min = int(view_region.left) // self.tile_set.dimensions[0]
        x_max = int(view_region.right) // self.tile_set.dimensions[0] + 1
        y_min = int(view_region.top) // self.tile_set.dimensions[1]
        y_max = int(view_region.bottom) // self.tile_set.dimensions[1] + 1

        tile_w, tile_h = self.tile_set.dimensions

        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                tile_idx = self.map[x][y]

                self.tile_set.draw(screen, tile_idx, x * tile_w, y * tile_h)


