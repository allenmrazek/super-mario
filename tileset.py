import os
import pygame
from typing import NamedTuple
import config


class _Tile(NamedTuple):
    surface: pygame.Surface
    rect: pygame.Rect


class TileSet:
    def __init__(self, image_path, tile_dimensions, color_key=None):
        path = os.fsencode(os.path.join("images", os.path.join("tilesets", image_path)))

        if not os.path.exists(path) or not os.path.isfile(path):
            raise FileNotFoundError

        # load image
        try:
            self.map = pygame.image.load(image_path)
        except pygame.error:
            print("Error reading %s: %s" % (os.fsdecode(image_path), pygame.get_error()))
            raise

        # Scale image, if needed
        w, h = self.map.get_width() * config.rescale_factor, self.map.get_height() * config.rescale_factor

        self.map = pygame.transform.scale(self.map, (w, h)).convert()  # avoids per-pixel alpha, if any

        if color_key is not None:
            self.map.set_colorkey(color_key)

        assert w % tile_dimensions == 0 and h % tile_dimensions == 0

        # split into tiles
        self.tiles = []
        x_tiles, y_tiles = w // tile_dimensions, h // tile_dimensions

        for y in range(y_tiles):
            for x in range(x_tiles):
                rect = pygame.Rect(x * tile_dimensions, y * tile_dimensions, tile_dimensions, tile_dimensions)
                tile = self.map.subsurface(rect)

                self.tiles.append(_Tile(tile, rect))

        self._draw_rect = pygame.Rect(0, 0, tile_dimensions, tile_dimensions)
        self.dimensions = (tile_dimensions, tile_dimensions)

    def draw(self, screen, tile_idx, tile_position):
        self._draw_rect.x, self._draw_rect.y = int(tile_position[0], tile_position[1])

        screen.blit(self.tiles[tile_idx], self._draw_rect)

    @property
    def num_tiles(self):
        return (self.map.get_width() // self.dimensions[0]) * (self.map.get_height() // self.dimensions[1])
